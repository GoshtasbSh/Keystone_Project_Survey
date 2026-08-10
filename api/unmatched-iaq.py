"""GET /api/unmatched-iaq — households that answered Qualtrics but have no
canvass record.

This is the "do not knock — they already responded" list. Each feature
carries a `parcel_address` derived from the county cadastre (public
property data), NOT the resident's typed address, which stays stripped.

Read-only. Never writes. Per-respondent survey answers are always removed.

Degrades gracefully if the `parcel_address_index` blob has not been
published yet (data_type='parcel_address_index' row missing, or an empty
payload): orphan features are still returned, each carrying the fallback
`parcel_address` below. This endpoint must never 500 and must never raise
because that blob is absent.

The point-in-polygon ray-cast used to resolve `parcel_address` lives in
api/survey_logic.py (`lookup_parcel`) — the single source of truth shared
with scripts/build_parcel_address_index.py, so a geometry fix (e.g.
honouring interior-ring holes) only has to be made once.
"""
from http.server import BaseHTTPRequestHandler

import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parent))
from _lib import load_cached, json_response, empty_geojson, strip_survey_answers
from survey_logic import orphan_iaq_features, lookup_parcel

FALLBACK_ADDRESS = 'Address not on file'


def build_unmatched_iaq(iaq_features: list, contact_features: list, index: dict) -> dict:
    """Pure builder: orphan IAQ features with `parcel_address` attached.

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
        props = dict(f.get('properties') or {})
        props['parcel_address'] = addr or FALLBACK_ADDRESS
        props['parcel_id'] = pid
        props['orphan'] = True
        out.append({**f, 'properties': props})

    return strip_survey_answers(
        {'type': 'FeatureCollection', 'features': out}) if out else empty_geojson()


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        iaq_blob = load_cached('iaq_survey') or {}
        iaq_feats = (iaq_blob.get('geojson') or {}).get('features') or []
        contacts = (load_cached('community_contact') or {}).get('features') or []
        index = load_cached('parcel_address_index') or {}

        data = build_unmatched_iaq(iaq_feats, contacts, index)
        json_response(self, 200, data, cache='no-store')
