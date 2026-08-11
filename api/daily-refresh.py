"""GET or POST /api/daily-refresh — scheduled merge of field_survey_points into
the cached community-contact GeoJSON blob.

Invoked by Vercel Cron (see vercel.json). Lightweight — no geopandas/fiona.
Heavy spatial analysis (parcel matching, STRtree) is performed once by the
local admin via scripts/ingest.py when new parcel or contact data arrives.

Protected by CRON_SECRET header when called from Vercel's scheduler.
"""
from __future__ import annotations

from http.server import BaseHTTPRequestHandler
from datetime import datetime, timezone
from urllib.parse import urlparse, parse_qs
import json as _json
import os
import urllib.request as _urlreq
from zoneinfo import ZoneInfo

import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parent))
from _lib import (
    supabase_admin, load_cached, json_response, empty_geojson, haversine_m,
    _bearer_jwt, supabase_anon, merge_preserve_analysis,
)
import hmac as _hmac

# Status colours — mirrors _processing.STATUS so the analysis blob is consistent
# with what IAQ and survey uploads produce. Kept inline to avoid pulling pandas.
_STATUS_COLORS = {
    "Completed":      "#10b981",
    "No Answer":      "#f97316",
    "Inaccessible":   "#ef4444",
    "Not Interested": "#8b5cf6",
    "Left Info":      "#3b82f6",
    "Vacant":         "#6b7280",
    "Follow Up":      "#06b6d4",
    "Other":          "#ec4899",
    "Unknown":        "#9ca3af",
}
LOCAL_TZ = ZoneInfo("America/New_York")

# I7 fix (2026-08-10): tolerate migration 27 (the optional `address` column
# on field_survey_points) not being applied yet, same pattern as
# api/upload.py's _FIELD_COLS_BASE / _FIELD_COLS_ENRICHED. Try the enriched
# select first; the caller falls back to the base columns on ANY exception.
_FIELD_COLS_BASE     = "id, lat, lon, status, notes, collector_id, collector_name, collected_at"
_FIELD_COLS_ENRICHED = _FIELD_COLS_BASE + ", address"


def _compute_analysis(features: list) -> dict:
    """Minimal contact-level analysis — same output shape as compute_contact_analysis()
    in _processing.py, but uses only stdlib so daily-refresh stays lightweight."""
    sc: dict = {}
    st_count: dict = {}
    st_status: dict = {}
    for f in features:
        s  = f["properties"].get("status", "Unknown")
        sn = f["properties"].get("street_name", "Unknown")
        sc[s] = sc.get(s, 0) + 1
        st_count[sn] = st_count.get(sn, 0) + 1
        if sn not in st_status:
            st_status[sn] = {}
        st_status[sn][s] = st_status[sn].get(s, 0) + 1
    total = len(features)
    comp  = sc.get("Completed", 0)
    return {
        "total_points":    total,
        "completion_rate": round(comp / total * 100, 1) if total else 0,
        "status_counts":   sc,
        "status_colors":   _STATUS_COLORS,
        "streets": [
            {"name": n, "count": c, "statuses": st_status.get(n, {})}
            for n, c in sorted(st_count.items(), key=lambda x: -x[1])
        ],
        "parcel_stats": {},
    }


def _refresh_iaq_match_status(iaq_features: list) -> None:
    """Re-derive `match_status` on every IAQ feature from `iaq_matched`,
    mirroring api/_processing.py's upload-time tagging
    (`'matched' if iaq_matched else 'iaq_only'`). Mutates in place.

    Task 15: the field-point match pass above can flip `iaq_matched`
    true on an IAQ feature that was uploaded (and tagged) before any
    field pin existed for its parcel. Its stored `match_status` then
    goes stale at 'iaq_only' even though `iaq_matched` is now true —
    only the browser's client-side backfill (_backfillIaqMatchStatus in
    static/js/dashboard.js) ever corrected this, so the raw stored blob
    (and anything reading it directly, e.g. a CSV export) kept reading
    the wrong value. Re-deriving here keeps the server's stored value
    in sync with the field it's derived from.
    """
    for f in iaq_features or []:
        props = (f or {}).get("properties")
        if props is None:
            continue
        props["match_status"] = "matched" if props.get("iaq_matched") else "iaq_only"


# ── Task 16: daily integrity metrics ────────────────────────────────────
def _compute_integrity_metrics(iaq_feats: list, features: list,
                                contacts_table_rows: int) -> dict:
    """Pure computation — no I/O. Reuses `orphan_iaq_features` from
    api/survey_logic.py (the same source of truth as /api/iaq-points?unmatched=1
    and the mobile 'Already Responded' list) so the orphan count here can
    never drift from what surveyors actually see.
    """
    from survey_logic import orphan_iaq_features
    return {
        "computed_at": datetime.now(timezone.utc).isoformat(),
        "n_iaq": len(iaq_feats),
        "n_orphans": len(orphan_iaq_features(iaq_feats, features)),
        "n_contacts": sum(1 for f in features
                          if (f.get("properties") or {}).get("source") != "field"),
        "n_field_points": sum(1 for f in features
                              if (f.get("properties") or {}).get("source") == "field"),
        "contacts_table_rows": contacts_table_rows,
    }


def _table_row_count(sb, table: str) -> int:
    """Exact row count via PostgREST's `count=exact` header. Never raises
    — a monitoring query must never break the refresh it's monitoring."""
    try:
        r = sb.table(table).select("id", count="exact").execute()
        return int(getattr(r, "count", 0) or 0)
    except Exception as e:
        print(f"[daily-refresh] {table} row count failed: {e}")
        return 0


def _previous_integrity_metrics(sb) -> dict | None:
    """Read the integrity_metrics row as it stood BEFORE this tick's
    upsert overwrites it — i.e. what the last refresh computed. Used
    only for the response-count-drop check below. Never raises; missing
    history (first-ever run) just means no drop check happens."""
    try:
        r = (sb.table("keystone_dashboard_data")
               .select("payload")
               .eq("data_type", "integrity_metrics")
               .limit(1).execute())
        rows = getattr(r, "data", None) or []
        return (rows[0].get("payload") or {}) if rows else None
    except Exception as e:
        print(f"[daily-refresh] previous integrity metrics read failed: {e}")
        return None


def _persist_integrity_metrics(sb, iaq_feats: list, features: list) -> dict | None:
    """Compute + upsert daily integrity metrics to a NEW, dedicated
    `data_type='integrity_metrics'` row in keystone_dashboard_data.

    Deliberately its own row — never touches the existing
    community_contact / iaq_survey / analysis / parcel_address_index
    blobs. Runs on every refresh tick (not just ticks that change
    something) so the metric is a genuine daily heartbeat rather than
    something that goes stale on quiet days. Never raises; a metrics
    failure must not fail the refresh it's reporting on.

    Also logs (server-side only — see Task 16 report for why this isn't
    wired into either daily-email path) a
    "Response count dropped from X to Y" warning when n_iaq decreases
    versus the metrics row this same upsert is about to replace.
    """
    try:
        contacts_table_rows = _table_row_count(sb, "community_contacts")
        metrics = _compute_integrity_metrics(iaq_feats, features, contacts_table_rows)

        prev = _previous_integrity_metrics(sb)
        prev_n_iaq = prev.get("n_iaq") if prev else None
        if isinstance(prev_n_iaq, int) and metrics["n_iaq"] < prev_n_iaq:
            print(f"[daily-refresh] ⚠️ Response count dropped from "
                  f"{prev_n_iaq} to {metrics['n_iaq']}")

        sb.table("keystone_dashboard_data").upsert({
            "data_type": "integrity_metrics",
            "payload": metrics,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }, on_conflict="data_type").execute()
        return metrics
    except Exception as e:
        print(f"[daily-refresh] integrity metrics persist failed: {e}")
        return None


def _field_row_to_feature(row: dict) -> dict | None:
    # NB (updated 2026-08-10, I7 fix): field_survey_points now carries an
    # OPTIONAL `address` column (migration 27) that a surveyor may fill in
    # at pin-placement time. This comment used to claim we "deliberately do
    # not surface any address-like field here" — that was true before
    # migration 27 existed, but is now false and contradicted api/upload.py:
    # _field_row_to_feature, which already surfaces `address`. Without this,
    # a surveyor's typed address only ever reached the map via a manual
    # community-contact upload (api/upload.py), never via the 4x/day cron
    # this function backs. `row.get("address")` is safe even against the
    # base (pre-migration-27) select in _run_refresh, which never includes
    # the key at all — it simply returns None.
    lon = row.get("lon")
    lat = row.get("lat")
    if lon is None or lat is None:
        return None  # skip rows with no valid coordinates
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lon, lat]},
        "properties": {
            "source": "field",
            "field_point_id": row.get("id"),
            "status": row.get("status") or "Unknown",
            "street_name": "Field Survey",  # mirrors app.py _field_pts_to_geojson_features
            "notes": row.get("notes") or "",
            "collector": row.get("collector_name"),
            "collector_id": row.get("collector_id"),
            "collected_at": row.get("collected_at"),
            "address": row.get("address") or None,
        },
    }


def _run_refresh() -> dict:
    sb = supabase_admin()
    if not sb:
        return {"refreshed": False, "reason": "Supabase service role key not configured"}

    # Last snapshot timestamp
    try:
        versions = (
            sb.table("keystone_analysis_versions")
            .select("created_at")
            .eq("data_type", "community_contact")
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
        last_at = versions.data[0]["created_at"] if versions.data else "2000-01-01T00:00:00Z"
    except Exception as e:
        return {"refreshed": False, "reason": f"Could not read versions: {e}"}

    # New field points since then — paginate to avoid silent 1000-row PostgREST cap.
    cap_reached = False
    try:
        new_rows: list = []
        PAGE = 1000
        HARD_CAP = 100_000
        offset = 0
        # I7 fix: try the enriched (+address) select first; tolerate
        # migration 27 not being applied yet by falling back to the base
        # columns on ANY exception, once, at the first page — mirrors
        # api/upload.py's _load_all_field_features fallback pattern.
        cols = _FIELD_COLS_ENRICHED
        while offset < HARD_CAP:
            try:
                page = (
                    sb.table("field_survey_points")
                    .select(cols)
                    .gt("collected_at", last_at)
                    .range(offset, offset + PAGE - 1)
                    .execute()
                ).data or []
            except Exception as e:
                if cols is _FIELD_COLS_ENRICHED:
                    print(f"[daily-refresh] field_survey_points select with address "
                          f"failed ({type(e).__name__}: {e}) — retrying without it "
                          f"(migration 27 not applied?)")
                    cols = _FIELD_COLS_BASE
                    continue
                raise
            if not page:
                break
            new_rows.extend(page)
            if len(page) < PAGE:
                break
            offset += PAGE
        cap_reached = offset >= HARD_CAP and len(new_rows) >= HARD_CAP
        if cap_reached:
            print(f"[daily-refresh] WARNING: field_survey_points capped at {HARD_CAP} rows — "
                  "points beyond this limit were NOT merged. Investigate if table is large.")
    except Exception as e:
        return {"refreshed": False, "reason": f"Could not read field points: {e}"}

    # NOTE: even when no new field rows have arrived since the last
    # snapshot we still fall through and re-run the IAQ matcher against
    # the cached blob. Reason: the v3 matcher used to skip Completed
    # field pins, so any Completed pins added historically may still be
    # missing has_iaq_survey + iaq_matched. This idempotent re-pass
    # backfills them. We only persist + version-snapshot when something
    # actually changed (n_iaq_upgraded > 0 OR new_rows > 0 OR iaq blob
    # flipped) so unchanged invocations remain a no-op.

    # Load existing cached community-contact blob and append.
    # NB: must use 'community_contact' — the data_type every read endpoint queries.
    # (Earlier versions used 'survey_points', which was a dead key.)
    existing = load_cached("community_contact") or empty_geojson()
    features = list(existing.get("features") or [])
    new_features = [f for f in (_field_row_to_feature(r) for r in new_rows) if f is not None]

    # Upgrade new field points that have a Qualtric IAQ survey for the
    # SAME parcel. v3 (2026-05-05): use _processing.load_parcel_index +
    # _apply_iaq_to_field_features so daily-refresh and upload share the
    # exact same parcel-aware logic. Falls back to a tight 30 m haversine
    # if the parcel index can't be built (e.g. cached blob missing).
    iaq_stored = load_cached("iaq_survey") or {}
    iaq_feats = (iaq_stored.get("geojson") or {}).get("features") or []
    n_iaq_upgraded = 0
    # Snapshot iaq_matched per IAQ feature so we can detect downstream
    # flips and persist the iaq_survey blob only when something changed.
    iaq_matched_before = [bool((f.get("properties") or {}).get("iaq_matched"))
                          for f in iaq_feats]
    # Append new rows BEFORE running the matcher — we want the matcher
    # to also re-evaluate pre-existing field points (e.g. yesterday's
    # Completed pins that the buggy v3 matcher skipped) so they finally
    # pick up has_iaq_survey + iaq_matched. The matcher is idempotent.
    features.extend(new_features)
    field_features_for_match = [
        f for f in features
        if (f.get("properties") or {}).get("source") == "field"
    ]
    if iaq_feats and field_features_for_match:
        try:
            # Late import: keeps the daily-refresh function bundle slim
            # when the IAQ blob is empty (no upgrade work to do).
            from _processing import load_parcel_index, _apply_iaq_to_field_features
            parcel_idx = load_parcel_index()
            n_iaq_upgraded = _apply_iaq_to_field_features(
                field_features_for_match, iaq_feats, parcel_idx=parcel_idx)
        except Exception as e:
            print(f"[daily-refresh] parcel-aware match unavailable ({e}); "
                  f"falling back to 30 m distance.")
            for ff in field_features_for_match:
                if ff["properties"].get("has_iaq_survey"):
                    continue
                f_lon, f_lat = ff["geometry"]["coordinates"]
                for iaq_f in iaq_feats:
                    i_lon, i_lat = iaq_f["geometry"]["coordinates"]
                    if haversine_m(f_lat, f_lon, i_lat, i_lon) <= 30:
                        ff["properties"]["status"] = "Completed"
                        ff["properties"]["has_iaq_survey"] = True
                        iaq_f["properties"]["iaq_matched"] = True
                        n_iaq_upgraded += 1
                        break

    merged = {"type": "FeatureCollection", "features": features}

    # Tag every Completed contact / field-as-feature with match_status
    # (G1 = matched, G2 = contact_only) so the desktop map's stroke
    # encoding stays correct after the daily-refresh append. Then dedup
    # at the parcel rep-point so a freshly-appended field point at the
    # same parcel as an existing CSV contact collapses to a single dot.
    try:
        from _processing import tag_contact_match_status, dedup_contacts_at_parcel
        tag_contact_match_status(features)
        features = dedup_contacts_at_parcel(features)
        merged = {"type": "FeatureCollection", "features": features}
    except Exception as e:
        print(f"[daily-refresh] tag/dedup failed: {e}")

    local_day = datetime.now(LOCAL_TZ).date().isoformat()
    label = f"Daily Update {local_day} — {len(new_rows)} new field visits ({len(features)} total)"

    # Persist iaq_survey blob if any iaq_matched flag flipped during the
    # field-point match pass. Without this, the IAQ-only dot keeps its
    # G3 yellow rim on the map even though a field pin now ground-truths
    # the parcel as 'matched' (G1, white rim).
    iaq_matched_after = [bool((f.get("properties") or {}).get("iaq_matched"))
                         for f in iaq_feats]
    iaq_blob_changed = (iaq_matched_before != iaq_matched_after)
    if iaq_blob_changed and iaq_stored:
        try:
            # Task 15: keep the stored match_status in sync with
            # iaq_matched before writing — this blob is about to be
            # persisted anyway (iaq_blob_changed), so this adds no new
            # write, it just corrects what the existing write contains.
            _refresh_iaq_match_status(iaq_feats)
            iaq_payload = dict(iaq_stored)
            geo = dict(iaq_payload.get("geojson") or {})
            geo["features"] = iaq_feats
            iaq_payload["geojson"] = geo
            sb.table("keystone_dashboard_data").upsert({
                "data_type": "iaq_survey",
                "payload": iaq_payload,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }, on_conflict="data_type").execute()
        except Exception as e:
            print(f"[daily-refresh] iaq_survey blob persist failed: {e}")

    # Task 16: daily integrity metrics — a NEW data_type='integrity_metrics'
    # row, computed on every tick regardless of whether anything else
    # changed. Never touches community_contact / iaq_survey / analysis /
    # parcel_address_index.
    _persist_integrity_metrics(sb, iaq_feats, features)

    # Persist merged blob + version snapshot — but only when something
    # actually changed. Empty refresh ticks (no new rows AND no IAQ
    # backfill) skip the write so we don't churn the version table.
    something_changed = bool(new_rows) or n_iaq_upgraded > 0 or iaq_blob_changed
    if not something_changed:
        return {"refreshed": False, "reason": "No new field data and no IAQ backfill needed",
                "last_analysis": last_at}
    try:
        sb.table("keystone_dashboard_data").upsert({
            "data_type": "community_contact",
            "payload": merged,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }, on_conflict="data_type").execute()
        sb.table("keystone_analysis_versions").insert({
            "data_type": "community_contact",
            "payload": merged,
            "label": label,
            "n_points": len(features),
        }).execute()
    except Exception as e:
        return {"refreshed": False, "reason": f"Write failed: {e}"}

    # Recompute and persist analysis stats so the dashboard's Analysis tab
    # reflects today's field-point additions rather than the last upload.
    # NB: scripts/ingest.py is the only thing that computes parcel_stats
    # (needs geopandas/shapely — too heavy for a Vercel function). We must
    # PRESERVE the previous analysis blob's parcel_stats and any other
    # server-only fields so the Parcels tab stays populated. Without this
    # merge, every daily-refresh tick wipes the parcel analysis.
    try:
        # Single shared helper now lives in _lib so the upload, restore,
        # and daily-refresh paths all preserve parcel_stats identically.
        recomputed = merge_preserve_analysis(_compute_analysis(features))
        sb.table("keystone_dashboard_data").upsert({
            "data_type": "analysis",
            "payload": recomputed,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }, on_conflict="data_type").execute()
    except Exception as e:
        print(f"[daily-refresh] analysis recompute failed: {e}")

    return {"refreshed": True, "new_field_points": len(new_rows),
            "total_points": len(features), "label": label,
            "cap_reached": cap_reached}


def _cron_authorized(handler_obj) -> bool:
    """Bearer CRON_SECRET check. Constant-time. Fails closed if CRON_SECRET
    is unset — no environment-variable backdoors."""
    secret = os.environ.get("CRON_SECRET", "")
    if not secret:
        return False
    got = handler_obj.headers.get("authorization", "") or handler_obj.headers.get("Authorization", "")
    expected = f"Bearer {secret}"
    return _hmac.compare_digest(got or "", expected)


def _admin_authorized(handler_obj) -> bool:
    """Admin user-JWT check — used by the dashboard's "Run Daily Refresh
    Now" button. Validates the JWT and checks team_members.role='admin'."""
    jwt = _bearer_jwt(handler_obj)
    if jwt is None:
        return False
    sb_anon = supabase_anon()
    sb_adm  = supabase_admin()
    if sb_anon is None or sb_adm is None:
        return False
    try:
        resp = sb_anon.auth.get_user(jwt)
        user = getattr(resp, "user", None)
        uid = getattr(user, "id", None) if user else None
    except Exception:
        return False
    if not uid:
        return False
    try:
        r = sb_adm.table("team_members").select("role").eq("id", uid).limit(1).execute()
        rows = r.data or []
    except Exception:
        rows = []
    return bool(rows) and (rows[0].get("role") == "admin")


def _authorized(handler_obj) -> bool:
    return _cron_authorized(handler_obj) or _admin_authorized(handler_obj)


def _maybe_dispatch_email_action(handler_obj) -> bool:
    """If the request carries ?action=invite|my-report|daily-report,
    delegate to the email-logic module (kept underscore-prefixed so it
    is NOT counted against the Hobby 12-function cap). Returns True if
    handled (a response has been written)."""
    qs = parse_qs(urlparse(handler_obj.path).query)
    action = (qs.get("action", [""])[0] or "").lower()
    if not action:
        return False
    # Read body (POST). For GET we just pass an empty dict.
    body: dict = {}
    try:
        length = int(handler_obj.headers.get("Content-Length") or "0")
        if length > 0:
            raw = handler_obj.rfile.read(length)
            try:
                parsed = _json.loads(raw.decode("utf-8") or "{}")
                if isinstance(parsed, dict):
                    body = parsed
            except Exception:
                body = {}
    except Exception:
        body = {}
    try:
        from _email_logic import dispatch as _email_dispatch  # type: ignore
    except Exception:
        return False
    return bool(_email_dispatch(handler_obj, action, body))


class handler(BaseHTTPRequestHandler):
    def _handle(self):
        # ── Email-logic actions (invite / my-report / daily-report) ──
        # These come in BEFORE the refresh authorisation gate because
        # each handler does its own auth (admin JWT, user JWT, guest
        # session id, or cron bearer).
        qs = parse_qs(urlparse(self.path).query)
        action = (qs.get("action", [""])[0] or "").lower()
        mode = (qs.get("mode", [""])[0] or "").lower()
        if action in ("invite", "my-report", "daily-report"):
            if _maybe_dispatch_email_action(self):
                return
            json_response(self, 500, {"error": "email dispatch failed"})
            return
        if mode == "report":
            # Vercel cron triggers at 00:00 UTC (EDT) and 01:00 UTC (EST);
            # the local-time gate below picks exactly one per DST window.
            cron_ok = _cron_authorized(self)
            admin_ok = _admin_authorized(self)
            if not (cron_ok or admin_ok):
                json_response(self, 401, {"error": "unauthorized"})
                return
            if cron_ok and not admin_ok:
                now_local = datetime.now(LOCAL_TZ)
                if now_local.hour != 20:
                    json_response(self, 200, {
                        "report": False,
                        "reason": "outside Florida 20:00 local window",
                        "local_time": now_local.isoformat(),
                    })
                    return
            # Synthesize an action=daily-report request and delegate.
            try:
                from _email_logic import dispatch as _email_dispatch  # type: ignore
                _email_dispatch(self, "daily-report", {})
            except Exception as e:
                json_response(self, 500, {"error": f"{type(e).__name__}"})
            return
        cron_ok = _cron_authorized(self)
        admin_ok = _admin_authorized(self)
        if not (cron_ok or admin_ok):
            json_response(self, 401, {"error": "unauthorized"})
            return
        # Default: data refresh. Cron is scheduled at both 04:00 and 05:00
        # UTC so DST shifts still hit local midnight in Florida. Only the
        # invocation that is actually 00:00 local performs work.
        if cron_ok and not admin_ok:
            now_local = datetime.now(LOCAL_TZ)
            if now_local.hour != 0:
                json_response(self, 200, {
                    "refreshed": False,
                    "reason": "outside Florida local-midnight window",
                    "local_time": now_local.isoformat(),
                })
                return
        try:
            result = _run_refresh()
            json_response(self, 200, result)
        except Exception as e:
            json_response(self, 500, {"error": str(e)})

    def do_GET(self):  # Vercel Cron issues GET
        self._handle()

    def do_POST(self):  # Manual trigger during testing
        self._handle()
