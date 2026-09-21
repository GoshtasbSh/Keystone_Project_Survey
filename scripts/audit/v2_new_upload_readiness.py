"""v2 — will the analysis still be right for the export uploaded tomorrow?

The format-parity check proved the two exports we HAVE agree. This checks the
things that can differ in an export we have not seen yet:

  1. Column layout. Qualtrics reorders columns between exports, and adds and
     removes them as the questionnaire is edited. Every analysis input is looked
     up by the question's Qualtrics ID, so a permuted export must give byte-
     identical results. Proven by actually permuting it.
  2. New columns appearing. An unrelated new question must not shift anything.
  3. A column disappearing. Must be REFUSED by the upload guard, not silently
     scored as 0.
  4. Extra responses. More rows must not change existing households' numbers.
  5. Payload integrity. The blob written to Supabase must be JSON-serialisable
     with no NaN, and must carry every key the dashboard reads.
  6. The upload guard's verdict against the live stored response set.

Run:  python3 scripts/audit/v2_new_upload_readiness.py
"""
from __future__ import annotations

import csv
import io
import json
import math
import pathlib
import random
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'api'))

from _processing import (  # noqa: E402
    load_parcel_index, process_iaq_bytes, _validate_iaq_columns, _read_qualtric_csv,
)
from upload import evaluate_iaq_upload_safety  # noqa: E402

APRIL = ROOT / 'data' / 'Keystone Heights Survey - V1_April 15, 2026_13.25.csv'
MAY = pathlib.Path('/Users/goshtasbshahriari/UF Dropbox/Goshtasb Shahriari Mehr/'
                   'DTSC_Lab/Keystone_Data/Keystone Heights Survey - V1_May 4, 2026_16.57.csv')
EVID = ROOT / 'docs' / 'plans' / 'evidence' / '2026-09-21-analysis-audit'

# Keys the dashboard reads out of analysis (static/js/dashboard.js).
REQUIRED_ANALYSIS_KEYS = [
    'n_responses', 'scores', 'risk_tiers', 'health', 'housing', 'ownership',
    'residency', 'housing_safety', 'affordability', 'interventions',
    'experiences', 'mobility', 'demographics_ext', 'survey_questions',
    'chart_sources', 'validation',
]
REQUIRED_HEALTH_KEYS = ['respiratory_pct', 'asthma_pct', 'wheeze_pct',
                        'mold_pct', 'hospital_pct']

PARCELS = load_parcel_index()
FAILS: list[str] = []


def check(ok: bool, label: str, detail: str = '') -> bool:
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}"
          + (f'  — {detail}' if detail and not ok else ''))
    if not ok:
        FAILS.append(f'{label}: {detail}')
    return ok


def rows_of(path: pathlib.Path) -> list[list[str]]:
    return list(csv.reader(path.open(encoding='utf-8-sig')))


def to_bytes(rows: list[list[str]]) -> bytes:
    buf = io.StringIO()
    csv.writer(buf, lineterminator='\n').writerows(rows)
    return buf.getvalue().encode('utf-8')


def run(b: bytes):
    return process_iaq_bytes(b, [], PARCELS)


def comparable(analysis: dict) -> str:
    """Analysis reduced to a stable string, ignoring diagnostics."""
    d = {k: v for k, v in analysis.items()
         if not k.startswith('_') and k not in ('validation',)}
    return json.dumps(d, sort_keys=True, default=str)


def per_household(features: list) -> dict:
    return {f['properties']['response_id']:
            {k: f['properties'].get(k) for k in
             ('health_score', 'iaq_score', 'struct_score', 'overall_risk',
              'risk_tier', 'has_mold', 'ownership', 'condition', 'year_built')}
            for f in features if f['properties'].get('response_id')}


def find_nan(obj, path='') -> list[str]:
    bad = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            bad += find_nan(v, f'{path}.{k}')
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            bad += find_nan(v, f'{path}[{i}]')
    elif isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
        bad.append(path)
    elif isinstance(obj, str) and obj.strip().lower() == 'nan':
        bad.append(path + ' (literal "nan")')
    return bad


def main() -> int:
    baseline_rows = rows_of(MAY)
    base_geo, base_an, base_streets, _n, _f = run(to_bytes(baseline_rows))
    base_sig = comparable(base_an)
    base_hh = per_household(base_geo['features'])
    print(f'baseline: {len(base_geo["features"])} households, '
          f'{len(baseline_rows[0])} columns\n')

    # ── 1. column layout must not matter ─────────────────────────────────────
    print('1. Column order independence (6 random permutations)')
    ncol = len(baseline_rows[0])
    for seed in (1, 2, 3, 4, 5, 6):
        order = list(range(ncol))
        random.Random(seed).shuffle(order)
        permuted = [[r[i] if i < len(r) else '' for i in order]
                    for r in baseline_rows]
        geo, an, _s, _n2, _f2 = run(to_bytes(permuted))
        same_an = comparable(an) == base_sig
        same_hh = per_household(geo['features']) == base_hh
        check(same_an and same_hh, f'seed {seed}: identical analysis and per-household scores',
              f'analysis_same={same_an} households_same={same_hh}')
        check(an.get('_qid_fallback_qids') == [],
              f'seed {seed}: every question still found by its Qualtrics ID',
              f"fell back for {an.get('_qid_fallback_qids')}")

    # ── 2. an unrelated new column must change nothing ───────────────────────
    print('\n2. A new, unrelated question appears in the export')
    added = [r[:] for r in baseline_rows]
    added[0].append('BrandNewQuestion')
    added[1].append('Some question we have never seen before')
    added[2].append('{"ImportId":"QID9999"}')
    for r in added[3:]:
        r.append('42')
    geo, an, _s, _n3, _f3 = run(to_bytes(added))
    check(comparable(an) == base_sig and per_household(geo['features']) == base_hh,
          'analysis unchanged by an extra column')

    # ── 3. a missing question column must be refused, not scored as 0 ────────
    print('\n3. A required question is missing from the export')
    drop_name = 'RespIll'
    di = [i for i, c in enumerate(baseline_rows[0])
          if str(c).replace('\xa0', ' ').strip() == drop_name][0]
    stripped = [[v for i, v in enumerate(r) if i != di] for r in baseline_rows]
    raw, _q = _read_qualtric_csv(to_bytes(stripped))
    missing = _validate_iaq_columns(raw.columns)
    check(bool(missing), f'{drop_name} missing is detected', str(missing))
    _g4, an4, _s4, _n4, _f4 = run(to_bytes(stripped))
    warn = (an4.get('validation_warnings') or {}).get('missing_columns')
    check(bool(warn), 'the analysis carries the missing-column warning', str(warn))
    verdict = evaluate_iaq_upload_safety([], _g4['features'], an4, 'broken.csv', False)
    check(not verdict['allowed'] and verdict['reason'] == 'degraded_export',
          'the upload guard REFUSES the degraded export', str(verdict['reason']))

    # ── 4. extra responses must not disturb existing households ─────────────
    print('\n4. The new export has more responses')
    # Synthesise 12 genuinely new households by cloning existing completed rows
    # under fresh ResponseIds. (April contains no completed response that May
    # lacks, so it cannot supply them.) Cloning keeps every answer valid, which
    # is what this check needs: the question is whether ADDING rows disturbs the
    # rows already there.
    m_names = [str(c).replace('\xa0', ' ').strip() for c in baseline_rows[0]]
    rid_i = m_names.index('ResponseId')
    fin_i = m_names.index('Finished')
    completed = [r for r in baseline_rows[3:]
                 if r[fin_i].strip().lower() in ('true', '1')]
    extra = []
    for k, src in enumerate(completed[:12]):
        clone = src[:]
        clone[rid_i] = f'R_SYNTHETIC{k:04d}'
        extra.append(clone)
    grown = [r[:] for r in baseline_rows] + extra
    geo5, an5, _s5, _n5, _f5 = run(to_bytes(grown))
    hh5 = per_household(geo5['features'])
    unchanged = {k: v for k, v in base_hh.items() if k in hh5 and hh5[k] == v}
    check(len(unchanged) == len(base_hh),
          f'all {len(base_hh)} existing households keep identical scores '
          f'after {len(extra)} responses are added',
          f'{len(base_hh) - len(unchanged)} changed')
    check(an5['n_responses'] >= base_an['n_responses'],
          'response count grew', f"{base_an['n_responses']} -> {an5['n_responses']}")
    g5 = evaluate_iaq_upload_safety(base_geo['features'], geo5['features'],
                                    an5, 'grown.csv', False)
    check(g5['allowed'], 'the upload guard ALLOWS a strict superset',
          str(g5['reason']))

    # ── 5. payload integrity ─────────────────────────────────────────────────
    print('\n5. The blob written to the database')
    payload = {'geojson': base_geo, 'analysis': base_an,
               'street_stats': base_streets,
               'validation': base_an.get('validation', {}),
               'source_filename': MAY.name}
    try:
        blob = json.dumps(payload, allow_nan=False)
        check(True, f'payload is strict JSON ({len(blob) / 1024:.0f} KB)')
    except ValueError as e:
        check(False, 'payload is strict JSON', str(e))
        blob = ''
    nans = find_nan(payload)
    check(not nans, 'no NaN and no literal "nan" anywhere in the payload',
          f'{len(nans)}: {nans[:6]}')
    missing_keys = [k for k in REQUIRED_ANALYSIS_KEYS if k not in base_an]
    check(not missing_keys, 'every key the dashboard reads is present',
          str(missing_keys))
    mh = [k for k in REQUIRED_HEALTH_KEYS if k not in base_an.get('health', {})]
    check(not mh, 'every health statistic is present', str(mh))
    sq = base_an.get('survey_questions', {})
    check(len(sq) >= 60, f'popup carries {len(sq)} question labels')
    # every intervention/experience field must have a percentage
    iv = base_an['interventions']['pct_want']
    ex = base_an['experiences']['pct_yes']
    check(len(iv) == 11 and len(ex) == 10,
          f'all 11 interventions and 10 experiences aggregated ({len(iv)}, {len(ex)})')
    check(all(isinstance(v, (int, float)) and 0 <= v <= 100 for v in
              list(iv.values()) + list(ex.values())),
          'every percentage is a number in 0-100')

    # ── 6. guard verdict against the CURRENT live stored responses ───────────
    print('\n6. Against the live stored response set')
    live = EVID / 'live-dashboard-readings.json'
    n_live = json.loads(live.read_text())['data_untouched']['iaq_responses']
    fake_stored = [{'properties': {'response_id': f'LIVE_{i}'}} for i in range(n_live)]
    v6 = evaluate_iaq_upload_safety(fake_stored, base_geo['features'],
                                    base_an, 'may.csv', False)
    check(not v6['allowed'] and v6['reason'] == 'response_regression',
          f'an export with fewer than the stored {n_live} responses is REFUSED',
          str(v6['reason']))

    print('\n' + '=' * 68)
    if FAILS:
        print(f'{len(FAILS)} CHECK(S) FAILED')
        for f in FAILS:
            print('  !', f)
        return 1
    print('ALL CHECKS PASSED — a new export is read correctly regardless of its')
    print('column layout, extra columns, or extra responses; a degraded or')
    print('shrinking export is refused rather than silently mis-scored.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
