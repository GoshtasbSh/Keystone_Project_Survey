"""Run the real analysis pipeline on both exports and diff every number.

The two files are the same survey: April is a TEXT export, May a NUMERIC one,
and 72 respondents appear in both. Restricted to those shared respondents, every
statistic the Analysis panel shows must come out identical. Any difference is a
format-handling defect, not a data difference.

Run:  python3 scripts/audit/run_analysis_both_formats.py
"""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'api'))

from _processing import (  # noqa: E402
    _compute_iaq_analysis, _compute_street_stats, _validate_iaq_columns,
    process_iaq_bytes, load_parcel_index,
)

APRIL = ROOT / 'data' / 'Keystone Heights Survey - V1_April 15, 2026_13.25.csv'
MAY = pathlib.Path('/Users/goshtasbshahriari/UF Dropbox/Goshtasb Shahriari Mehr/'
                   'DTSC_Lab/Keystone_Data/Keystone Heights Survey - V1_May 4, 2026_16.57.csv')

OUT = ROOT / 'docs' / 'plans' / 'evidence' / '2026-09-21-analysis-audit'


def run(path: pathlib.Path, parcels):
    geo, analysis, streets, n_up, failed = process_iaq_bytes(
        path.read_bytes(), [], parcels)
    return geo['features'], analysis, streets, failed


def flatten(d, prefix=''):
    """Flatten a nested analysis dict to {dotted.path: scalar}."""
    out = {}
    for k, v in (d or {}).items():
        if str(k).startswith('_') or k in ('survey_questions', 'chart_sources',
                                           'validation', 'input_format',
                                           'recode_translation_applied'):
            continue
        key = f'{prefix}{k}'
        if isinstance(v, dict):
            out.update(flatten(v, key + '.'))
        elif isinstance(v, list):
            out[key] = json.dumps(v, sort_keys=True)
        else:
            out[key] = v
    return out


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    parcels = load_parcel_index()

    results = {}
    for label, path in (('april_text', APRIL), ('may_numeric', MAY)):
        if not path.exists():
            print(f'!! {label}: file missing {path}')
            return 2
        feats, analysis, streets, failed = run(path, parcels)
        results[label] = {'features': feats, 'analysis': analysis}
        print(f'\n=== {label}: {len(feats)} geocoded features, '
              f'{len(failed)} geocode failures, '
              f"input_format={analysis.get('input_format')}, "
              f"qid_fallbacks={analysis.get('_qid_fallback_qids')}")
        missing = _validate_iaq_columns(
            [c for c in []]) if False else None  # noqa
        (OUT / f'analysis-{label}.json').write_text(
            json.dumps(analysis, indent=2, sort_keys=True, default=str))

    # Restrict to respondents present in BOTH exports, then recompute the
    # analysis from that identical respondent set for each format.
    by_id = {}
    for label in results:
        by_id[label] = {p['properties']['response_id']: p
                        for p in results[label]['features']
                        if p['properties'].get('response_id')}
    shared = sorted(set(by_id['april_text']) & set(by_id['may_numeric']))
    print(f'\nshared respondents (geocoded in both): {len(shared)}')

    recomputed = {}
    for label in results:
        subset = [by_id[label][r] for r in shared]
        recomputed[label] = _compute_iaq_analysis(subset)
        (OUT / f'analysis-shared-{label}.json').write_text(
            json.dumps(recomputed[label], indent=2, sort_keys=True, default=str))

    fa = flatten(recomputed['april_text'])
    fm = flatten(recomputed['may_numeric'])
    keys = sorted(set(fa) | set(fm))
    diffs = [(k, fa.get(k, '<absent>'), fm.get(k, '<absent>'))
             for k in keys if fa.get(k, '<absent>') != fm.get(k, '<absent>')]

    print(f'\n{len(keys)} statistics compared on the same {len(shared)} '
          f'respondents; {len(diffs)} differ\n')
    for k, a, m in diffs:
        print(f'  {k}\n      april(text)   = {a!r}\n      may(numeric)  = {m!r}')

    (OUT / 'format-diff.json').write_text(json.dumps(
        {'shared_respondents': len(shared), 'statistics_compared': len(keys),
         'differences': [{'stat': k, 'april_text': a, 'may_numeric': m}
                         for k, a, m in diffs]},
        indent=2, default=str))
    return 0 if not diffs else 1


if __name__ == '__main__':
    sys.exit(main())
