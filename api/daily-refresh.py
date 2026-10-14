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
    supabase_admin, load_cached, json_response, empty_geojson,
    _bearer_jwt, supabase_anon, merge_preserve_analysis,
)
from _field_layer import (
    FIELD_COLS_BASE as _FIELD_COLS_BASE,
    FIELD_COLS_ENRICHED as _FIELD_COLS_ENRICHED,
    field_row_to_feature, load_all_field_rows, rebuild_field_layer,
    is_field_feature, features_signature,
)
from _dashboard_writes import (
    commit_dashboard_writes, load_blob_with_stamp, StaleWriteError,
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


def _refresh_iaq_validation_counts(iaq_payload: dict, iaq_feats: list,
                                   contact_feats: list) -> None:
    """Recompute the matched / unmatched counts stored with the IAQ blob
    after the field pass flipped iaq_matched, in both places the blob keeps
    them (payload.validation and payload.analysis.validation). Other keys
    (completed_in_csv, responses_mapped, ...) are kept. Mutates in place."""
    from survey_logic import build_validation_summary
    counts = build_validation_summary(iaq_feats, contact_feats)
    analysis = dict(iaq_payload.get("analysis") or {})
    analysis["validation"] = {**(analysis.get("validation") or {}), **counts}
    iaq_payload["analysis"] = analysis
    iaq_payload["validation"] = {**(iaq_payload.get("validation") or {}), **counts}


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
    # Single definition lives in _field_layer (shared with upload.py and
    # versions.py); kept under this name for tests/importers.
    return field_row_to_feature(row)


def _match_field_to_iaq(field_feats: list, iaq_feats: list, parcel_loader=None) -> int:
    """Link pins with the ONE shared matcher (_processing._apply_iaq_to_field_features:
    note house number <= 60 m, then same parcel, then NEAREST within 30 m).
    Without a parcel index it still runs, skipping only the parcel tier —
    never a separate first-survey-within-30-m loop (audit P21)."""
    if not (iaq_feats and field_feats):
        return 0
    from _processing import load_parcel_index, _apply_iaq_to_field_features
    try:
        parcel_idx = (parcel_loader or load_parcel_index)()
    except Exception as e:
        print(f"[daily-refresh] parcel index unavailable ({e}); matching without parcel snap.")
        parcel_idx = None
    return _apply_iaq_to_field_features(field_feats, iaq_feats, parcel_idx=parcel_idx)


def _run_refresh() -> dict:
    """Rebuild the field half of the community_contact blob from the
    CURRENT field_survey_points table (audit 2026-10-13 F4/DEP-6/DEP-7).

    The old version appended rows newer than a timestamp watermark and
    never removed anything, so deleted pins lived on forever. Now:
      * every table row becomes exactly one fresh field feature;
      * a blob field feature whose row is gone is dropped;
      * CSV contacts are left exactly as stored (tag + parcel dedup run
        over contacts only — never over field pins, which used to let a
        pin swallow a real contact);
      * all writes go through one transaction with a compare-and-set on
        the blobs read here, so an upload that lands mid-refresh is never
        overwritten (StaleWriteError -> the handler retries once).
    """
    sb = supabase_admin()
    if not sb:
        return {"refreshed": False, "reason": "Supabase service role key not configured"}

    try:
        field_rows = load_all_field_rows(sb, "[daily-refresh]")
    except Exception as e:
        return {"refreshed": False, "reason": f"Could not read field points: {e}"}

    try:
        existing, cc_stamp = load_blob_with_stamp(sb, "community_contact")
        iaq_stored, iaq_stamp = load_blob_with_stamp(sb, "iaq_survey")
    except Exception as e:
        # Never treat "could not read" as "empty": that would rewrite the
        # blob with field pins only and wipe every CSV contact.
        return {"refreshed": False, "reason": f"Could not read cached blobs: {e}"}

    existing = existing or empty_geojson()
    old_features = list(existing.get("features") or [])
    # Taken before the tagger mutates the contact dicts in place.
    old_sig = features_signature(old_features)
    features, report = rebuild_field_layer(old_features, field_rows)
    contacts = [f for f in features if not is_field_feature(f)]
    field_feats = [f for f in features if is_field_feature(f)]

    iaq_stored = iaq_stored or {}
    iaq_feats = (iaq_stored.get("geojson") or {}).get("features") or []
    iaq_matched_before = [bool((f.get("properties") or {}).get("iaq_matched"))
                          for f in iaq_feats]
    try:
        _match_field_to_iaq(field_feats, iaq_feats)
    except Exception as e:
        # Every pin above was rebuilt without its survey link; writing now
        # would strip every link from the map. Skip this tick instead.
        return {"refreshed": False, "reason": f"Field-survey matching failed: {e}"}

    try:
        from _processing import tag_contact_match_status, dedup_contacts_at_parcel
        tag_contact_match_status(contacts)
        contacts = dedup_contacts_at_parcel(contacts)
    except Exception as e:
        print(f"[daily-refresh] tag/dedup failed: {e}")
    features = contacts + field_feats
    merged = {**existing, "type": "FeatureCollection", "features": features}

    iaq_matched_after = [bool((f.get("properties") or {}).get("iaq_matched"))
                         for f in iaq_feats]
    iaq_blob_changed = bool(iaq_stored) and iaq_matched_before != iaq_matched_after

    # Task 16: daily heartbeat row, written every tick (its own data_type).
    _persist_integrity_metrics(sb, iaq_feats, features)

    contact_changed = old_sig != features_signature(features)
    if not (contact_changed or iaq_blob_changed):
        return {"refreshed": False,
                "reason": "No field-point changes and no IAQ backfill needed"}

    local_day = datetime.now(LOCAL_TZ).date().isoformat()
    n_new, n_removed = len(report["added"]), len(report["removed"])
    label = (f"Daily Update {local_day} — {n_new} new field visits"
             + (f", {n_removed} deleted pins removed" if n_removed else "")
             + f" ({len(features)} total)")
    if n_removed:
        print(f"[daily-refresh] removed {n_removed} field features whose "
              f"field_survey_points row no longer exists: {report['removed_details']}")

    blobs = [{"data_type": "community_contact", "payload": merged}]
    if iaq_blob_changed:
        # Task 15: keep stored match_status in sync with iaq_matched.
        _refresh_iaq_match_status(iaq_feats)
        iaq_payload = dict(iaq_stored)
        geo = dict(iaq_payload.get("geojson") or {})
        geo["features"] = iaq_feats
        iaq_payload["geojson"] = geo
        _refresh_iaq_validation_counts(iaq_payload, iaq_feats, contacts)
        blobs.append({"data_type": "iaq_survey", "payload": iaq_payload})
    try:
        # parcel_stats etc. are preserved from the cached analysis (Vercel
        # cannot recompute them) — same helper as upload and restore.
        blobs.append({"data_type": "analysis",
                      "payload": merge_preserve_analysis(_compute_analysis(features))})
    except Exception as e:
        print(f"[daily-refresh] analysis recompute failed: {e}")

    try:
        commit_dashboard_writes(
            sb, blobs,
            versions=[{"data_type": "community_contact", "payload": merged,
                       "label": label, "n_points": len(features)}],
            expected={"community_contact": cc_stamp, "iaq_survey": iaq_stamp},
        )
    except StaleWriteError:
        raise
    except Exception as e:
        return {"refreshed": False, "reason": f"Write failed: {e}"}

    return {"refreshed": True, "new_field_points": n_new,
            "removed_field_points": n_removed,
            "restored_contacts": report["restored_contacts"],
            "total_points": len(features), "label": label,
            "cap_reached": len(field_rows) >= 100_000}


def _run_refresh_with_retry() -> dict:
    """An upload (or a field-pin delete) that commits between our read and
    our write makes the compare-and-set refuse the write; re-read and try
    once more, then give up until the next tick."""
    for attempt in (1, 2):
        try:
            return _run_refresh()
        except StaleWriteError as e:
            print(f"[daily-refresh] attempt {attempt}: {e}")
    return {"refreshed": False,
            "reason": "Dashboard data changed during the refresh (concurrent upload); "
                      "skipped — the next run will pick everything up."}


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
            result = _run_refresh_with_retry()
            json_response(self, 200, result)
        except Exception as e:
            json_response(self, 500, {"error": str(e)})

    def do_GET(self):  # Vercel Cron issues GET
        self._handle()

    def do_POST(self):  # Manual trigger during testing
        self._handle()
