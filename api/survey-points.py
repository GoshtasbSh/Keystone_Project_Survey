"""GET /api/survey-points — community-contact GeoJSON.

Two access levels (mirrors the iaq-points pattern):
  - No auth / guest: features returned with notes, status_detail, and
    second_attempt stripped. Coordinates, address, status, and match
    metadata are still included so the map and analysis work normally.
  - Team member (Bearer JWT): full properties including canvassing notes
    and status details.

?bust=<n>  cache-buster (ignored, for client-side forcing only)
"""
from http.server import BaseHTTPRequestHandler

import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parent))
from _lib import load_cached, json_response, empty_geojson, _bearer_jwt, require_team_member


# Fields that contain canvassing PII — omitted from the public response.
# Single source of truth: both the top-level strip and the nested
# `coincident_contacts` strip (see _strip_pii below) key off this set.
_PII_FIELDS = {
    'notes', 'status_detail', 'second_attempt',
    'address', 'matched_address', 'street_name',
}


def _strip_contact_entry(entry):
    """Strip `_PII_FIELDS` keys from one `coincident_contacts` entry.

    Defensive about shape: dedup_contacts_at_parcel (api/_processing.py)
    always stamps dicts here, but this endpoint must never 500, so any
    non-dict junk is passed through unchanged rather than raising.
    """
    if not isinstance(entry, dict):
        return entry
    return {k: v for k, v in entry.items() if k not in _PII_FIELDS}


def _strip_pii(geojson: dict) -> dict:
    """Return a copy of the GeoJSON with PII fields removed from properties.

    Recurses into `properties.coincident_contacts` — dedup_contacts_at_parcel
    stamps collapsed households' address/matched_address/street_name/notes
    onto each entry there, and those keys are PII exactly like their
    top-level counterparts. `coincident_contacts` may be absent, null, an
    empty list, or (defensively) contain non-dict junk; all pass through
    without raising.
    """
    features = []
    for f in geojson.get('features', []):
        props = {k: v for k, v in (f.get('properties') or {}).items()
                 if k not in _PII_FIELDS}
        coincident = props.get('coincident_contacts')
        if isinstance(coincident, list):
            props['coincident_contacts'] = [_strip_contact_entry(e) for e in coincident]
        features.append({**f, 'properties': props})
    return {**geojson, 'features': features}


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        data = load_cached('community_contact') or empty_geojson()

        # Determine if caller is an authenticated team member. We reuse
        # _bearer_jwt — if the token is present and valid it means the
        # dashboard is calling with the user's Supabase session token.
        jwt = _bearer_jwt(self)
        is_member = False
        if jwt:
            from _lib import supabase_anon, supabase_admin
            sb_anon = supabase_anon()
            sb_adm  = supabase_admin()
            if sb_anon and sb_adm:
                try:
                    resp = sb_anon.auth.get_user(jwt)
                    user = getattr(resp, 'user', None)
                    uid = getattr(user, 'id', None) if user else None
                    if uid:
                        r = sb_adm.table('team_members').select('role').eq('id', uid).limit(1).execute()
                        is_member = bool(r.data)
                except Exception:
                    pass

        if not is_member:
            data = _strip_pii(data)

        json_response(self, 200, data, cache='no-store')
