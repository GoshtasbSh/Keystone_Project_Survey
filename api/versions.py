"""GET  /api/versions                — list historical analysis snapshots.
POST /api/versions?id=<version_id> — restore a snapshot (admin-only).

Consolidated from the previous api/versions.py (GET) + api/versions/restore.py (POST)
to fit the Hobby plan's 12-function ceiling.
"""
from __future__ import annotations

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parent))
from _lib import (
    supabase_admin, supabase_anon, json_response, require_admin,
    require_team_member, merge_preserve_analysis,
)
from _processing import compute_contact_analysis
from _field_layer import load_all_field_rows, rebuild_field_layer, is_field_feature
from _dashboard_writes import commit_dashboard_writes, load_blob_with_stamp


def build_contact_restore(version_payload: dict, current_blob: dict | None,
                          field_rows: list) -> tuple:
    """Contacts come from the chosen version; field pins come from the
    CURRENT field_survey_points table, never from the snapshot, so a
    restore cannot bring back a pin that was deleted since (audit
    2026-10-13 F4: 28 deleted test pins). Each pin keeps the survey link
    it has in the current blob (the parcel matcher is not re-run here;
    the nightly refresh re-derives it). Returns (payload, report)."""
    feats, report = rebuild_field_layer(
        version_payload.get("features") or [], field_rows,
        carry_iaq_link_from=[f for f in (current_blob or {}).get("features") or []
                             if is_field_feature(f)])
    return {**version_payload, "features": feats}, report


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if require_team_member(self) is None:
            return
        sb = supabase_admin() or supabase_anon()
        if not sb:
            json_response(self, 200, [])
            return
        try:
            r = (sb.table("keystone_analysis_versions")
                   .select("id, data_type, label, n_points, created_at")
                   .order("created_at", desc=True)
                   .limit(100)
                   .execute())
            rows = r.data or []
            grouped = {
                "community_contact": [x for x in rows if x["data_type"] == "community_contact"],
                "iaq_survey":        [x for x in rows if x["data_type"] == "iaq_survey"],
            }
            json_response(self, 200, grouped)
        except Exception as e:
            json_response(self, 500, {"error": str(e)})

    def do_POST(self):
        # POST = restore a version. Admin only.
        if require_admin(self) is None:
            return
        qs  = parse_qs(urlparse(self.path).query)
        raw = qs.get("id", [""])[0]
        if not raw or not raw.isdigit():
            json_response(self, 400, {"error": "Missing or invalid ?id= parameter."})
            return
        version_id = int(raw)

        sb = supabase_admin()
        if not sb:
            json_response(self, 500, {"error": "Supabase service key not configured."})
            return

        r = (sb.table("keystone_analysis_versions")
               .select("id, label, data_type, payload, created_at")
               .eq("id", version_id)
               .execute())
        if not r.data:
            json_response(self, 404, {"error": "Version not found."})
            return

        v       = r.data[0]
        payload = v["payload"]

        if "features" in payload:          # community_contact blob
            try:
                current, _ = load_blob_with_stamp(sb, "community_contact")
                field_rows = load_all_field_rows(sb, "[versions]")
            except Exception as e:
                print(f"[versions] restore read failed: {e}")
                json_response(self, 500, {"error": "Could not read current field points; nothing was restored."})
                return
            restored, report = build_contact_restore(payload, current, field_rows)
            blobs = [{"data_type": "community_contact", "payload": restored}]
            try:
                # Preserve parcel_stats etc. — Vercel can't recompute them.
                blobs.append({"data_type": "analysis", "payload": merge_preserve_analysis(
                    compute_contact_analysis(restored["features"]))})
            except Exception as _e:
                print(f"[versions] analysis recompute on restore failed: {_e}")
            try:
                commit_dashboard_writes(sb, blobs, [])
            except Exception as e:
                print(f"[versions] restore write failed: {type(e).__name__}: {e}")
                json_response(self, 500, {"error": "Saving the restore failed. With migration 29 "
                                                   "applied nothing was changed; check Vercel logs."})
                return
            print(f"[versions] restored id={version_id} points={len(restored['features'])} "
                  f"field_removed={len(report['removed'])} "
                  f"restored_contacts={report['restored_contacts']}")
            json_response(self, 200, {
                "restored": True,
                "type":     "community_contact",
                "label":    v["label"],
                "points":   len(restored["features"]),
                "field_points_removed": len(report["removed"]),
            })
            return

        if "geojson" in payload:           # iaq_survey blob
            try:
                commit_dashboard_writes(sb, [{"data_type": "iaq_survey", "payload": payload}], [])
            except Exception as e:
                print(f"[versions] restore write failed: {type(e).__name__}: {e}")
                json_response(self, 500, {"error": "Saving the restore failed; check Vercel logs."})
                return
            json_response(self, 200, {
                "restored": True,
                "type":     "iaq_survey",
                "label":    v["label"],
                "points":   len(payload.get("geojson", {}).get("features", [])),
            })
            return

        json_response(self, 400, {"error": "Unknown payload format."})
