"""Anonymous / member / admin access probes against a deployed KeyStone site.

Read-only: every request is a GET, except one POST /api/versions WITHOUT an
id, which require_admin rejects (member -> 403) or the handler rejects before
any write (admin -> 400 "Missing or invalid ?id=").

Tokens come from the environment and are never printed or stored:
  KS_MEMBER_JWT / KS_ADMIN_JWT                     a Supabase access token, or
  KS_MEMBER_EMAIL + KS_MEMBER_PASSWORD (and KS_ADMIN_*)  to sign in with the anon key.
A role with no credentials is reported SKIPPED (the gate then fails).

Usage:
  .venv/bin/python scripts/audit/access_probe.py --base https://keystone-project-survey-blue.vercel.app
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

# Property keys the PUBLIC endpoints may carry (frozen 2026-10-13 from the
# live site). A launch fix may remove keys; any NEW key on a public endpoint
# (free text, notes, typed address, ...) fails the probe.
ANON_ALLOWED = {
    'api/iaq-points': {'asthma_freq', 'color', 'condition', 'coord_source', 'has_mold', 'headache_freq',
                       'health_score', 'hospital_visit', 'housing_type', 'iaq_matched', 'iaq_score',
                       'match_status', 'overall_risk', 'ownership', 'respiratory_ill', 'response_id',
                       'risk_tier', 'street_name', 'struct_score', 'wheeze_freq', 'year_built',
                       'superseded_by'},
    'api/iaq-points?unmatched=1': {'orphan', 'overall_risk', 'parcel_address', 'parcel_id',
                                   'response_id', 'risk_tier', 'street_name'},
    'api/field-points': {'collected_at', 'collector', 'collector_id', 'guest_session_id', 'id',
                         'is_field', 'notes', 'status'},
    'api/community-contacts': {'coincident_contacts', 'collected_at', 'collector', 'collector_id', 'color',
                               'coord_source', 'date', 'field_point_id', 'has_iaq_survey',
                               'iaq_health_score', 'iaq_iaq_score', 'iaq_match_lat', 'iaq_match_lon',
                               'iaq_overall_risk', 'iaq_response_id', 'iaq_risk_tier', 'iaq_struct_score',
                               'id', 'match_status', 'source', 'status'},
}
ANON_ALLOWED['api/survey-points'] = ANON_ALLOWED['api/community-contacts']
# Fields that must be blank for anon even though the key is present.
ANON_BLANK = {'api/field-points': ('notes', 'collector_id', 'guest_session_id')}
PRIVATE_DATA_TYPES = ('iaq_survey', 'community_contact', 'analysis', 'survey_points', 'integrity_metrics')
INTERNAL_DOCS = ('DEPLOY.md', 'PARITY.md', 'AUDIT_PHASE3.md', 'PHASE1_DEPLOY.md',
                 'PI_PRESENTATION.md', 'REVIEW_STATUS.md')


def http(method, url, headers=None, body=None):
    req = urllib.request.Request(url, method=method, headers=headers or {}, data=body)
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def token_for(role: str, sb_url: str, anon: str) -> str | None:
    tok = os.environ.get(f'KS_{role}_JWT')
    if tok:
        return tok
    email, pw = os.environ.get(f'KS_{role}_EMAIL'), os.environ.get(f'KS_{role}_PASSWORD')
    if not (email and pw):
        return None
    st, body = http('POST', f'{sb_url}/auth/v1/token?grant_type=password',
                    {'apikey': anon, 'Content-Type': 'application/json'},
                    json.dumps({'email': email, 'password': pw}).encode())
    return json.loads(body).get('access_token') if st == 200 else None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default='https://keystone-project-survey-blue.vercel.app')
    ap.add_argument('--service-env', default=None,
                    help='.env with SUPABASE_SERVICE_ROLE_KEY: also probe migrations 25/26/27 (GET only)')
    a = ap.parse_args(argv)
    B = a.base.rstrip('/')
    results = []

    def ok(name, cond, detail=''):
        results.append((name, 'PASS' if cond else 'FAIL', detail))

    st, body = http('GET', f'{B}/api/config')
    cfg = json.loads(body)
    sb_url, anon = cfg['supabase_url'].rstrip('/'), cfg['supabase_anon_key']

    # ── anonymous ──
    for dt in PRIVATE_DATA_TYPES:
        st, body = http('GET', f'{sb_url}/rest/v1/keystone_dashboard_data?select=data_type&data_type=eq.{dt}',
                        {'apikey': anon, 'Authorization': f'Bearer {anon}'})
        ok(f'anon PostgREST keystone_dashboard_data[{dt}]', st in (200, 401, 403) and (st != 200 or json.loads(body) == []),
           f'{st} {body[:80]!r}')
    for tbl in ('keystone_analysis_versions', 'field_survey_points'):
        st, body = http('GET', f'{sb_url}/rest/v1/{tbl}?select=id&limit=1',
                        {'apikey': anon, 'Authorization': f'Bearer {anon}'})
        ok(f'anon PostgREST {tbl}', st != 200 or json.loads(body) == [], f'{st}')
    for path in ('api/analysis', 'api/analysis?meta=1', 'api/versions', 'api/daily-refresh',
                 'api/iaq-points?full=1'):
        st, _ = http('GET', f'{B}/{path}')
        ok(f'anon GET /{path} is 401', st == 401, str(st))
    for path, allowed in ANON_ALLOWED.items():
        st, body = http('GET', f'{B}/{path}')
        feats = json.loads(body).get('features', []) if st == 200 else []
        keys = set().union(*[set(f['properties']) for f in feats]) if feats else set()
        ok(f'anon /{path} keys within allowlist', st == 200 and keys <= allowed, f'extra={sorted(keys - allowed)}')
        for k in ANON_BLANK.get(path, ()):
            leaked = [f['properties'].get('id') for f in feats if f['properties'].get(k)]
            ok(f'anon /{path} {k} blank', not leaked, f'{len(leaked)} leaked')
    for doc in INTERNAL_DOCS:
        st, _ = http('GET', f'{B}/{doc}')
        ok(f'anon /{doc} not served', st == 404, str(st))

    # ── live schema: migrations 25, 26, 27 applied (service key, GET only) ──
    if a.service_env:
        env = dict(l.strip().split('=', 1) for l in open(a.service_env)
                   if '=' in l and not l.lstrip().startswith('#'))
        svc = env['SUPABASE_SERVICE_ROLE_KEY'].strip().strip('"').strip("'")
        S = {'apikey': svc, 'Authorization': f'Bearer {svc}'}
        st, body = http('GET', f'{sb_url}/rest/v1/rpc/active_guests?select=id', S)
        ok('migration 25: active_guests() no longer returns id', st == 400 and b'42703' in body, f'{st}')
        st, _ = http('GET', f'{sb_url}/rest/v1/keystone_analysis_versions?select=uploaded_by_email,dropped_response_ids&limit=1', S)
        ok('migration 26: version audit columns exist', st == 200, str(st))
        st, _ = http('GET', f'{sb_url}/rest/v1/field_survey_points?select=address&limit=1', S)
        ok('migration 27: field_survey_points.address exists', st == 200, str(st))

    # ── member / admin ──
    for role in ('MEMBER', 'ADMIN'):
        tok = token_for(role, sb_url, anon)
        if not tok:
            results.append((f'{role.lower()} probes', 'SKIPPED', 'no credentials in env'))
            continue
        H = {'Authorization': f'Bearer {tok}'}
        st, body = http('GET', f'{B}/api/iaq-points?full=1', H)
        feats = json.loads(body).get('features', []) if st == 200 else []
        ok(f'{role} iaq-points?full=1 200 with answers', st == 200 and feats and 'education' in feats[0]['properties'],
           f'{st} n={len(feats)}')
        st, body = http('GET', f'{B}/api/analysis?meta=1', H)
        meta = json.loads(body) if st == 200 else {}
        ok(f'{role} analysis?meta=1 has iaq version', st == 200 and bool((meta.get('iaq') or {}).get('created_at')),
           json.dumps(meta.get('iaq'))[:120])
        st, body = http('GET', f'{B}/api/versions', H)
        vers = json.loads(body) if st == 200 else {}
        ok(f'{role} versions 200', st == 200 and 'iaq_survey' in vers, str(st))
        newest = (vers.get('iaq_survey') or [{}])[0]
        ok(f'{role} badge reads the newest iaq_survey version (History top row)',
           bool(newest) and (meta.get('iaq') or {}).get('id') == newest.get('id'),
           f"badge={(meta.get('iaq') or {}).get('id')} history={newest.get('id')} {newest.get('label', '')[:60]}")
        st, body = http('GET', f'{B}/api/field-points', H)
        feats = json.loads(body).get('features', []) if st == 200 else []
        ok(f'{role} field-points notes visible', st == 200 and any(f['properties'].get('notes') for f in feats),
           f'n={len(feats)}')
        st, body = http('POST', f'{B}/api/versions', H, b'')
        want = 403 if role == 'MEMBER' else 400
        ok(f'{role} POST /api/versions (no id) -> {want}', st == want, f'{st} {body[:80]!r}')

    width = max(len(r[0]) for r in results)
    for name, verdict, detail in results:
        print(f'{verdict:8} {name:<{width}}  {detail}')
    bad = [r for r in results if r[1] != 'PASS']
    print(f'{len(results) - len(bad)}/{len(results)} passed')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
