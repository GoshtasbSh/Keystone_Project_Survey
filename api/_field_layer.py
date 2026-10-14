"""Field-pin half of the community_contact blob — single source of truth.

The community_contact blob holds two kinds of features: CSV contacts
(written by the contacts upload) and one copy of every field pin from
`field_survey_points` (source='field'). Until 2026-10 the cron and the
IAQ upload only ever APPENDED pins to that blob, so a pin deleted in the
field app lived on forever (audit 2026-10-13: 28 deleted test pins still
drawn, counted and, in one case, linked to a real respondent).

Every write path now calls `rebuild_field_layer`, which keeps the CSV
contacts exactly as they are and replaces the field half with one fresh
feature per CURRENT `field_survey_points` row. Stdlib only — imported by
daily-refresh, upload, versions and scripts/.
"""
from __future__ import annotations

import copy
import json

FIELD_COLS_BASE = "id, lat, lon, status, notes, collector_id, collector_name, collected_at"
FIELD_COLS_ENRICHED = FIELD_COLS_BASE + ", address"

# Mirrors _processing.STATUS (kept inline so this module stays stdlib-only).
STATUS_COLORS = {
    "Completed": "#10b981", "No Answer": "#f97316", "Inaccessible": "#ef4444",
    "Not Interested": "#8b5cf6", "Left Info": "#3b82f6", "Vacant": "#6b7280",
    "Follow Up": "#06b6d4", "Other": "#ec4899", "Unknown": "#9ca3af",
}

# Keys _processing._apply_iaq_to_field_features writes onto a field pin.
IAQ_LINK_KEYS = (
    "has_iaq_survey", "iaq_overall_risk", "iaq_risk_tier", "iaq_health_score",
    "iaq_iaq_score", "iaq_struct_score", "iaq_response_id",
    "iaq_match_lon", "iaq_match_lat",
)

_RESTORE_KEYS = ("status", "street_name", "notes", "address", "matched_address",
                 "collected_at")


def is_field_feature(f) -> bool:
    p = (f or {}).get("properties") or {}
    return p.get("source") == "field" or p.get("field_point_id") is not None


def field_row_to_feature(row: dict):
    lon = row.get("lon")
    lat = row.get("lat")
    if lon is None or lat is None:
        return None
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lon, lat]},
        "properties": {
            "source": "field",
            "field_point_id": row.get("id"),
            "status": row.get("status") or "Unknown",
            "street_name": "Field Survey",
            "notes": row.get("notes") or "",
            "collector": row.get("collector_name"),
            "collector_id": row.get("collector_id"),
            "collected_at": row.get("collected_at"),
            # Migration 27 (optional pin address); absent on the base select.
            "address": row.get("address") or None,
        },
    }


def load_all_field_rows(sb, log_prefix: str = "[field-layer]") -> list:
    """Every field_survey_points row, paginated past PostgREST's 1000-row
    cap. Tries the migration-27 `address` column first and falls back to
    the base column set once, at the first page, on ANY exception. A
    failure on a later page (or on the base select) raises: callers must
    never mistake "could not read" for "the table is empty"."""
    rows: list = []
    page = 1000
    hard_cap = 100_000
    offset = 0
    cols = FIELD_COLS_ENRICHED
    while offset < hard_cap:
        try:
            batch = (
                sb.table("field_survey_points")
                .select(cols)
                .range(offset, offset + page - 1)
                .execute()
                .data
            ) or []
        except Exception as e:
            if cols is FIELD_COLS_ENRICHED and offset == 0:
                print(f"{log_prefix} field_survey_points select with address failed "
                      f"({type(e).__name__}: {e}) — retrying without it "
                      f"(migration 27 not applied?)")
                cols = FIELD_COLS_BASE
                continue
            raise
        if not batch:
            break
        rows.extend(batch)
        if len(batch) < page:
            break
        offset += page
    if offset >= hard_cap and len(rows) >= hard_cap:
        print(f"{log_prefix} WARNING: field_survey_points capped at {hard_cap} rows")
    # Deterministic order so an unchanged table produces a byte-identical
    # blob (lets callers skip no-op writes).
    rows.sort(key=lambda r: str(r.get("id")))
    return rows


def cell_key(coords, cell_deg: float = 1e-5):
    """Same 1e-5° (~1.1 m) grid as _processing.dedup_contacts_at_parcel."""
    return (round(coords[1] / cell_deg), round(coords[0] / cell_deg))


def _restore_swallowed_contact(entry: dict, host: dict, restore_lookup) -> dict:
    """Turn a CSV contact that a field pin swallowed back into a feature.

    Before 2026-10 the cron ran dedup_contacts_at_parcel over contacts AND
    field pins together, so a pin could win a parcel and fold a real CSV
    contact into its `coincident_contacts` (6386 Baylor inside test pin
    b989a847; 6393 Cascade inside pin b0310717). Rebuilding the pin must
    not lose that contact. `restore_lookup` (cell_key -> full feature from
    version history, built by scripts/prod_runbook.py) gives a
    full-fidelity copy; without it we rebuild a minimal feature from the
    entry so nothing is ever dropped.
    """
    coords = list((host.get("geometry") or {}).get("coordinates") or [None, None])[:2]
    hit = (restore_lookup or {}).get(cell_key(coords)) if coords[0] is not None else None
    if hit is not None:
        feat = copy.deepcopy(hit)
        props = feat.setdefault("properties", {})
    else:
        props = {k: entry.get(k) for k in _RESTORE_KEYS if entry.get(k) is not None}
        props.setdefault("address", "")
        props.setdefault("status", "Unknown")
        props["color"] = STATUS_COLORS.get(props["status"], "#9ca3af")
        feat = {"type": "Feature",
                "geometry": {"type": "Point", "coordinates": coords},
                "properties": props}
    # The IAQ link is re-derived by the next IAQ match, never carried over.
    for k in IAQ_LINK_KEYS + ("match_status",):
        props.pop(k, None)
    props["restored_from_field_pin"] = (host.get("properties") or {}).get("field_point_id")
    return feat


def rebuild_field_layer(blob_features: list, field_rows: list,
                        restore_lookup: dict | None = None,
                        carry_iaq_link_from: list | None = None) -> tuple:
    """Return (features, report).

    features = every non-field feature of `blob_features` (order and
    content untouched) + any CSV contact a field pin had swallowed
    + exactly one fresh feature per `field_rows` row (table order).

    A blob field feature whose id is no longer in the table is dropped.
    `carry_iaq_link_from` (field features, e.g. the CURRENT blob's) lets a
    pin keep the survey link of its copy there — used by version restore,
    which does not re-run the parcel matcher; every other caller re-runs
    _apply_iaq_to_field_features on the result instead.

    report = {"added": [ids], "removed": [ids], "restored_contacts": n,
              "removed_details": [{id, collector, status, collected_at}]}
    """
    contacts: list = []
    old_field: dict = {}
    restored: list = []
    for f in blob_features or []:
        if not is_field_feature(f):
            contacts.append(f)
            continue
        props = f.get("properties") or {}
        old_field[str(props.get("field_point_id"))] = f
        for entry in props.get("coincident_contacts") or []:
            if isinstance(entry, dict) and entry.get("source") != "field":
                restored.append(_restore_swallowed_contact(entry, f, restore_lookup))

    link_src = {str((f.get("properties") or {}).get("field_point_id")): f
                for f in carry_iaq_link_from or []}
    fresh: list = []
    for row in field_rows or []:
        feat = field_row_to_feature(row)
        if feat is None:
            continue
        if carry_iaq_link_from is not None:
            old = link_src.get(str(row.get("id")))
            old_p = (old or {}).get("properties") or {}
            if old_p.get("has_iaq_survey"):
                for k in IAQ_LINK_KEYS:
                    if k in old_p:
                        feat["properties"][k] = old_p[k]
                # Same rule as _processing._apply_iaq_to_field_features: the
                # surveyor's status is kept; only a pin without one reads
                # as Completed.
                if feat["properties"].get("status") in (None, "", "Unknown"):
                    feat["properties"]["status"] = "Completed"
                    feat["properties"]["color"] = STATUS_COLORS["Completed"]
        fresh.append(feat)

    table_ids = {str(r.get("id")) for r in field_rows or [] if r.get("id") is not None}
    removed = sorted(set(old_field) - table_ids)
    report = {
        "added": sorted(table_ids - set(old_field)),
        "removed": removed,
        "restored_contacts": len(restored),
        "removed_details": [
            {
                "field_point_id": fid,
                "collector": (old_field[fid].get("properties") or {}).get("collector"),
                "status": (old_field[fid].get("properties") or {}).get("status"),
                "collected_at": (old_field[fid].get("properties") or {}).get("collected_at"),
            }
            for fid in removed
        ],
    }
    return contacts + restored + fresh, report


def features_signature(features: list) -> str:
    """Canonical JSON used to skip writes that would change nothing."""
    return json.dumps(features, sort_keys=True, separators=(",", ":"), default=str)
