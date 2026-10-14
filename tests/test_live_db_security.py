"""Live security probes against production Supabase and the deployed site.

READ-ONLY: every request is a GET, including the RPC probes (PostgREST
serves STABLE functions over GET), so nothing is inserted, updated or
deleted and no POST ever reaches production.
Skipped unless KEYSTONE_LIVE_PROBE=1, so the normal suite never touches the
network. Run it with .env sourced:

  set -a; . ./.env; set +a; KEYSTONE_LIVE_PROBE=1 .venv/bin/python -m pytest tests/test_live_db_security.py -q
"""
import json
import os
import urllib.error
import urllib.request

import pytest

pytestmark = pytest.mark.skipif(os.environ.get('KEYSTONE_LIVE_PROBE') != '1',
                                reason='set KEYSTONE_LIVE_PROBE=1 and source .env to run live probes')

URL = os.environ.get('SUPABASE_URL', '').rstrip('/')
ANON = os.environ.get('SUPABASE_ANON_KEY', '')
SERVICE = os.environ.get('SUPABASE_SERVICE_ROLE_KEY', '')
SITE = os.environ.get('KEYSTONE_SITE', 'https://keystone-project-survey-blue.vercel.app').rstrip('/')


def _req(url, key=None, timeout=120):
    """GET only, by construction: this suite must never write to production."""
    headers = {'Accept': 'application/json'}
    if key:
        headers.update({'apikey': key, 'Authorization': f'Bearer {key}'})
    req = urllib.request.Request(url, headers=headers, method='GET')
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
            return r.status, (json.loads(raw) if raw else None)
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            return e.code, json.loads(raw)
        except ValueError:
            return e.code, raw.decode('utf-8', 'replace')


def _assert_denied(status, body, what):
    assert status in (401, 403), f'anon can access {what}: HTTP {status}, body={str(body)[:200]}'
    assert isinstance(body, dict) and body.get('code') == '42501', f'{what}: unexpected error {body!r}'


@pytest.mark.parametrize('table', ['keystone_dashboard_data', 'keystone_analysis_versions'])
def test_anon_cannot_read_table(table):
    status, body = _req(f'{URL}/rest/v1/{table}?select=data_type&limit=1', ANON)
    _assert_denied(status, body, table)


@pytest.mark.parametrize('fn', ['active_guests', 'active_member_ids', 'list_roster'])
def test_anon_cannot_call_team_only_rpc(fn):
    # GET, not POST: all three are STABLE, and a GET keeps the suite read-only.
    status, body = _req(f'{URL}/rest/v1/rpc/{fn}', ANON)
    _assert_denied(status, body, f'rpc/{fn}')


def test_active_guests_no_longer_returns_session_id():
    # Migration 25: RETURNS TABLE(name) only. select=id must be a 42703.
    status, body = _req(f'{URL}/rest/v1/rpc/active_guests?select=id', SERVICE)
    assert status == 400 and isinstance(body, dict) and body.get('code') == '42703', \
        f'active_guests still exposes id: HTTP {status} {str(body)[:200]}'


def test_migration_26_audit_columns_exist():
    cols = ('uploaded_by_user_id,uploaded_by_email,source_filename,source_row_count,'
            'geocoded_count,failed_geocodes,dropped_response_ids,forced')
    status, body = _req(f'{URL}/rest/v1/keystone_analysis_versions?select={cols}&limit=1', SERVICE)
    assert status == 200, f'migration 26 not applied: HTTP {status} {str(body)[:200]}'


def test_migration_27_field_address_column_exists():
    status, body = _req(f'{URL}/rest/v1/field_survey_points?select=address&limit=1', SERVICE)
    assert status == 200, f'migration 27 not applied: HTTP {status} {str(body)[:200]}'


def test_service_role_still_reads_dashboard_data():
    status, body = _req(f'{URL}/rest/v1/keystone_dashboard_data?select=data_type', SERVICE)
    assert status == 200
    assert {'iaq_survey', 'community_contact', 'analysis'} <= {r['data_type'] for r in body}


@pytest.mark.parametrize('path,key', [
    ('api/iaq-points', 'features'),
    ('api/field-points', 'features'),
    ('api/community-contacts', 'features'),
    ('api/survey-points', 'features'),
    ('api/parcels', 'features'),
])
def test_public_endpoints_still_serve(path, key):
    status, body = _req(f'{SITE}/{path}')
    assert status == 200, f'{path}: HTTP {status}'
    assert isinstance(body, dict) and len(body.get(key) or []) > 0, f'{path}: empty {key}'


def test_config_serves_the_same_anon_key_we_probe_with():
    status, body = _req(f'{SITE}/api/config')
    assert status == 200 and body.get('supabase_anon_key') == ANON, \
        'the /api/config anon key differs from .env; re-run probes with the served key'
