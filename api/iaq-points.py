"""GET /api/iaq-points — IAQ survey GeoJSON.

Default (anonymous): per-respondent SURVEY_ANSWER_FIELDS are stripped from
each feature so individual residents' answers never leak via the public
endpoint. Cached aggressively at the CDN.

?full=1  (auth-gated, team-member required): returns the full payload with
SURVEY_ANSWER_FIELDS preserved so the dashboard's Survey Answers popup tab
can render. Response is `Cache-Control: private` — never let a shared CDN
serve a signed-in user's PII to an anonymous one.

?unmatched=1  (public, read-only): households that answered Qualtrics but
have no canvass record — the "do not knock — they already responded" list.
Folded into this handler rather than a standalone api/unmatched-iaq.py
because this project sits at Vercel's 12-function Hobby-plan ceiling; see
api/upload.py, api/versions.py and api/daily-refresh.py for the same
`?type=`/`?mode=` multiplexing pattern.

Each unmatched feature carries a `parcel_address` derived from the county
cadastre (public property data), NOT the resident's typed address, which
is never emitted. Only an explicit WHITELIST of fields is returned per
feature (see UNMATCHED_WHITELIST below) — never the raw per-respondent
survey/health answers (has_mold, respiratory_ill, health_score, etc.),
which would otherwise leak publicly now stamped with a street address.

The unmatched path degrades gracefully if the `parcel_address_index` blob
has not been published yet (data_type='parcel_address_index' row missing,
or an empty payload): orphan features are still returned, each carrying
the fallback `parcel_address` below. This path must never 500 and must
never raise because that blob is absent.

The point-in-polygon ray-cast used to resolve `parcel_address` lives in
api/survey_logic.py (`lookup_parcel`) — the single source of truth shared
with scripts/build_parcel_address_index.py, so a geometry fix (e.g.
honouring interior-ring holes) only has to be made once.
"""
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parent))
from _lib import (
    load_cached, json_response, empty_geojson, strip_survey_answers,
    require_team_member,
)
from survey_logic import orphan_iaq_features, lookup_parcel

FALLBACK_ADDRESS = 'Address not on file'

# Explicit WHITELIST for ?unmatched=1 — NOT a blacklist. strip_survey_answers
# only removes SURVEY_ANSWER_FIELDS (per-respondent survey answers); it does
# NOT remove health fields like has_mold/respiratory_ill/asthma_freq/
# wheeze_freq/headache_freq/hospital_visit/health_score, which live on the
# same raw IAQ feature. Those must never ship on this public, unauthenticated
# path — especially now that each feature is stamped with a street address.
# Kept to exactly what the two consumers (keystone_field_web/index.html,
# static/js/dashboard.js) read off an orphan feature.
UNMATCHED_WHITELIST = (
    'response_id', 'parcel_address', 'parcel_id', 'orphan',
    'street_name', 'overall_risk', 'risk_tier',
)


def build_unmatched_iaq(iaq_features: list, contact_features: list, index: dict) -> dict:
    """Pure builder: orphan IAQ features with `parcel_address` attached,
    properties trimmed to UNMATCHED_WHITELIST.

    Never raises on a missing/empty ``index`` — every feature falls back to
    FALLBACK_ADDRESS. Kept separate from do_GET so it is unit-testable
    without an HTTP handler or a live Supabase connection.
    """
    orphans = orphan_iaq_features(iaq_features, contact_features)

    out = []
    for f in orphans:
        coords = ((f.get('geometry') or {}).get('coordinates') or [None, None])
        lon, lat = coords[0], coords[1]
        addr, pid = (None, None)
        if lon is not None and lat is not None:
            addr, pid = lookup_parcel(index, float(lon), float(lat))
        props = f.get('properties') or {}
        new_props = {k: props[k] for k in UNMATCHED_WHITELIST if k in props}
        new_props['parcel_address'] = addr or FALLBACK_ADDRESS
        new_props['parcel_id'] = pid
        new_props['orphan'] = True
        out.append({**f, 'properties': new_props})

    return {'type': 'FeatureCollection', 'features': out} if out else empty_geojson()


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        qs = parse_qs(urlparse(self.path).query)
        want_unmatched = (qs.get("unmatched", ["0"])[0] or "").lower() in ("1", "true", "yes")

        if want_unmatched:
            iaq_blob = load_cached('iaq_survey') or {}
            iaq_feats = (iaq_blob.get('geojson') or {}).get('features') or []
            contacts = (load_cached('community_contact') or {}).get('features') or []
            index = load_cached('parcel_address_index') or {}
            data = build_unmatched_iaq(iaq_feats, contacts, index)
            json_response(self, 200, data, cache='no-store')
            return

        want_full = (qs.get("full", ["0"])[0] or "").lower() in ("1", "true", "yes")

        payload = load_cached("iaq_survey") or {}
        data = payload.get("geojson") if isinstance(payload, dict) else None

        if want_full:
            # Auth-gate: any team member (admin or member) may see full answers.
            if require_team_member(self) is None:
                return  # 401/403 already written
            # no-store: blob updates on every IAQ upload; browser cache
            # of stale data caused "uploaded N but panel shows M" reports.
            json_response(self, 200, data or empty_geojson(), cache="no-store")
            return

        # Anonymous public path: strip SURVEY_ANSWER_FIELDS.
        data = strip_survey_answers(data) if data else empty_geojson()
        json_response(self, 200, data, cache="no-store")
