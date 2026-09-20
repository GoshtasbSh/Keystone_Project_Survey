"""Draw the audit's reproducible 30-point sample of MATCHED survey points.

A "matched point" is an IAQ/Qualtrics response feature whose
properties.iaq_matched is True — the Qualtrics respondent was paired to a
community-canvass contact on the same parcel (api/_processing.py:1348, :1436).

The candidate list is sorted by response_id BEFORE sampling so the draw is
reproducible regardless of the order the server returned features in.

SAMPLING FRAME — measured 2026-09-20, and the reason it is restricted:
production serves 110 IAQ responses, but only 75 appear in the May 4 CSV and
66 in the April 15 CSV. 35 live responses (32%) are in NEITHER file, i.e.
production was loaded from a Qualtrics export newer than anything in the
project's data folders. A point with no CSV row cannot be value-checked
against the survey at all, so the audit frame is
``iaq_matched AND response_id present in the May 4 export`` (May is a strict
superset of April: all 75 April ids appear in May). The 35-response coverage
gap is reported as a finding in its own right rather than hidden by the
restriction.
"""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

SEED = 20260920
TARGET_N = 30
ROOT = Path(__file__).resolve().parents[2]
EVID = ROOT / 'docs' / 'plans' / 'evidence' / '2026-09-20-audit'
MAY_CSV = ('/Users/goshtasbshahriari/UF Dropbox/Goshtasb Shahriari Mehr/'
           'DTSC_Lab/Keystone_Data/Keystone Heights Survey - V1_May 4, 2026_16.57.csv')
APR_CSV = ROOT / 'data' / 'Keystone Heights Survey - V1_April 15, 2026_13.25.csv'

sys.path.insert(0, str(Path(__file__).resolve().parent))
from qualtrics_ground_truth import load_survey, finished_rows  # noqa: E402


def main() -> None:
    src = EVID / 'live_iaq_points_full.json'
    feats = json.loads(src.read_text())['features']

    may_ids = {r['ResponseId'] for r in finished_rows(load_survey(MAY_CSV))}
    apr_ids = {r['ResponseId'] for r in finished_rows(load_survey(APR_CSV))}

    matched = [f for f in feats if (f.get('properties') or {}).get('iaq_matched')]
    rid = lambda f: str((f.get('properties') or {}).get('response_id') or '')

    verifiable = sorted([f for f in matched if rid(f) in may_ids], key=rid)
    unverifiable = sorted([rid(f) for f in matched if rid(f) not in may_ids])

    if len(verifiable) <= TARGET_N:
        sample = verifiable
        note = (f'Only {len(verifiable)} matched+verifiable points exist; auditing ALL '
                f'of them. The sample was NOT padded to reach {TARGET_N}.')
    else:
        sample = random.Random(SEED).sample(verifiable, TARGET_N)
        sample.sort(key=rid)
        note = (f'Randomly sampled {TARGET_N} of {len(verifiable)} matched points that '
                f'are present in the May 4 export and therefore value-checkable.')

    out = {
        'seed': SEED,
        'total_iaq_features': len(feats),
        'total_matched': len(matched),
        'matched_and_in_may_csv': len(verifiable),
        'matched_but_in_no_csv': len(unverifiable),
        'matched_but_in_no_csv_ids': unverifiable,
        'coverage_gap_note': (
            f'{len(unverifiable)} matched live responses have no row in the May 4 export '
            f'and cannot be value-checked against any CSV in the project. Production '
            f'appears to have been loaded from a newer Qualtrics export.'
        ),
        'sampled': len(sample),
        'sampled_in_april_csv': sum(1 for f in sample if rid(f) in apr_ids),
        'note': note,
        'response_ids': [rid(f) for f in sample],
        'features': sample,
    }
    (EVID / 'sample_30.json').write_text(json.dumps(out, indent=2))
    print(f"total_iaq={len(feats)} matched={len(matched)} "
          f"verifiable={len(verifiable)} sampled={len(sample)} seed={SEED}")
    print(f"sampled also in April export: {out['sampled_in_april_csv']}/{len(sample)}")
    print(f"COVERAGE GAP: {len(unverifiable)} matched responses in no CSV")
    print(note)


if __name__ == '__main__':
    main()
