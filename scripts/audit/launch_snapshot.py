"""Read-only snapshot of production state for the launch gate.

GET only (service-role key from .env, never printed). Writes into --out:
  dd_<data_type>.json         every keystone_dashboard_data row
  field_survey_points.json    every field_survey_points row
  versions.json               keystone_analysis_versions (no payloads)
  field_points.sha256         per-row and total hash of the IMMUTABLE columns

  --compare <baseline dir>    exit 1 unless every baseline field point is
                              still present with the same immutable hash,
                              no row was added by a test account, and the
                              only column that may differ is iaq_matched
                              going False -> True.

Usage:
  .venv/bin/python scripts/audit/launch_snapshot.py --out "$GATE/before"
  .venv/bin/python scripts/audit/launch_snapshot.py --out "$GATE/after" \
      --compare "$GATE/before"

The --out folder holds survey answers and addresses: keep it OUTSIDE the repo.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Columns a launch fix must never change on a real field point.
FIELD_IMMUTABLE = ('id', 'lat', 'lon', 'status', 'notes', 'collector_id', 'collector_name',
                   'collected_at', 'is_offline', 'guest_session_id', 'synced_at')
TEST_COLLECTOR = re.compile(r'\b(test\w*|qa(\s+tester)?)\b', re.I)


def row_hash(row: dict) -> str:
    core = {k: row.get(k) for k in FIELD_IMMUTABLE}
    return hashlib.sha256(json.dumps(core, sort_keys=True, default=str).encode()).hexdigest()


def total_hash(rows: list[dict]) -> str:
    return hashlib.sha256(''.join(sorted(row_hash(r) for r in rows)).encode()).hexdigest()


def compare_field_points(before: list[dict], after: list[dict]) -> list[str]:
    fails = []
    b = {str(r['id']): r for r in before}
    a = {str(r['id']): r for r in after}
    for fid, row in b.items():
        if fid not in a:
            fails.append(f'field point {fid} DELETED')
            continue
        if row_hash(row) != row_hash(a[fid]):
            changed = [k for k in FIELD_IMMUTABLE if row.get(k) != a[fid].get(k)]
            fails.append(f'field point {fid} changed: {changed}')
        if bool(row.get('iaq_matched')) and not bool(a[fid].get('iaq_matched')):
            fails.append(f'field point {fid} iaq_matched went True -> False')
    for fid in sorted(set(a) - set(b)):
        if TEST_COLLECTOR.search(str(a[fid].get('collector_name') or '')):
            fails.append(f"test-account field point {fid} ({a[fid].get('collector_name')}) present")
    return fails


def _env() -> dict:
    env = {}
    with open(ROOT / '.env') as fh:
        for line in fh:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def _get(url: str, key: str, path: str):
    """One PostgREST GET. Never sends a body, so it cannot write."""
    req = urllib.request.Request(f'{url}/rest/v1/{path}', method='GET',
                                 headers={'apikey': key, 'Authorization': f'Bearer {key}'})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def _dump(obj, path: Path, **kw) -> None:
    with open(path, 'w') as fh:
        json.dump(obj, fh, **kw)


def snapshot(out: Path) -> None:
    env = _env()
    url, key = env['SUPABASE_URL'].rstrip('/'), env['SUPABASE_SERVICE_ROLE_KEY']
    out.mkdir(parents=True, exist_ok=True)
    for row in _get(url, key, 'keystone_dashboard_data?select=data_type,updated_at,payload'):
        _dump(row, out / f"dd_{row['data_type']}.json")
    fields = _get(url, key, 'field_survey_points?select=*&order=id')
    _dump(fields, out / 'field_survey_points.json', indent=1, default=str)
    vers = _get(url, key, 'keystone_analysis_versions?select=id,data_type,label,n_points,created_at'
                          '&order=created_at.desc&limit=200')
    _dump(vers, out / 'versions.json', indent=1)
    lines = [f'{row_hash(r)}  {r["id"]}' for r in sorted(fields, key=lambda r: str(r['id']))]
    lines.append(f'{total_hash(fields)}  TOTAL ({len(fields)} rows)')
    (out / 'field_points.sha256').write_text('\n'.join(lines) + '\n')
    print(f'snapshot -> {out}: {len(fields)} field rows, total {total_hash(fields)[:16]}')


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--compare', default=None)
    a = ap.parse_args(argv)
    out = Path(a.out)
    snapshot(out)
    if not a.compare:
        return 0
    with open(Path(a.compare) / 'field_survey_points.json') as fh:
        before = json.load(fh)
    with open(out / 'field_survey_points.json') as fh:
        after = json.load(fh)
    fails = compare_field_points(before, after)
    for f in fails:
        print('FAIL', f)
    print(f'field points: before {len(before)} rows {total_hash(before)[:16]}, '
          f'after {len(after)} rows {total_hash(after)[:16]}; {len(fails)} failure(s)')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
