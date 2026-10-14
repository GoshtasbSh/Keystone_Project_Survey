"""After every PROC fix, the October export must produce these exact figures.
Re-baseline here (not elsewhere) if a later task (e.g. duplicate households)
intentionally changes them.

Re-baselined (GAP-10) for the two changes that landed after PROC-1..10:

* MATCH-3, latest response per household: ``geo['features']`` holds the
  106 households drawn and analysed. The 8 earlier answers from repeat
  households are in ``geo['superseded_features']``, so 114 responses are
  still placed. Every analysis figure is over the 106 households.
* The PI's shared-code decision of 2026-10-13: QID141 code 1 reads
  "Excellent- No repairs needed." and is no longer "Critical", so it adds
  0 structural points instead of 35. QID17 is unchanged. QID100 and QID221
  read Yes / "No / Not applicable". The status is verified, so the UI shows
  no "label unverified" note.

The figures below were checked against an independent recompute that does
not import api/. That recompute is VER-2's recompute_independent.py with
GAP-9's exact half-up applied, latest per household, and the decided
shared-code reading. It agreed on every score, tier, condition, mold,
hospital, years and stay figure. Its only difference was the deliberate
"No / Not applicable" skirting wording. Under the old "Critical" reading
the same recompute gives GAP-10's numbers (tiers 71/34/1 and Critical 19),
which confirms that only the reading changed.
"""
from __future__ import annotations

import pathlib
import sys
from decimal import ROUND_HALF_UP, Decimal

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'api'))


def _all_props(geo):
    """Drawn plus superseded features (GAP-10), for per-respondent lookups."""
    return {f['properties']['response_id']: f['properties']
            for f in geo['features'] + geo.get('superseded_features', [])}


def _mean1(values):
    """Half-up to 1 decimal, the pipeline's documented rounding rule."""
    return float(Decimal(repr(round(sum(values) / len(values), 9)))
                 .quantize(Decimal('0.1'), rounding=ROUND_HALF_UP))


@pytest.fixture(scope='module')
def october(october_iaq_copy):
    geo, a, streets, *_ = october_iaq_copy
    return geo, a, streets


def test_october_headline_figures(october):
    geo, a, _ = october
    # 114 placed responses = 106 households drawn + 8 earlier answers kept.
    assert len(geo['features']) == 106
    assert len(geo.get('superseded_features', [])) == 8
    assert len(_all_props(geo)) == 114
    assert a['scores'] == {'mean_risk': 25.0, 'mean_health': 23.5,
                           'mean_iaq': 18.6, 'mean_struct': 34.2}
    assert a['risk_tiers'] == {'low': 75, 'medium': 30, 'high': 1}
    assert a['health']['mold_pct'] == 28.3
    assert a['health']['hospital_pct'] == 27.4
    assert a['housing']['conditions'] == {'Fair': 31, 'Good': 37, 'Poor': 19, 'Excellent': 19}
    v = a['validation']
    assert (v['completed_in_csv'], v['dropped_no_geocode'],
            v['charted_pct_of_completed'], v['excluded_test_responses']) == (126, 12, 90.5, 3)
    assert a['shared_code_labels']['verified'] is True


def test_october_figures_are_over_the_drawn_households(october):
    """The means and tiers come from exactly the drawn features. An earlier
    answer from a repeat household is never counted."""
    geo, a, _ = october
    drawn = [f['properties'] for f in geo['features']]
    assert not any(p.get('superseded') for p in drawn)
    assert all(f['properties'].get('superseded') for f in geo['superseded_features'])
    for key, field in (('mean_risk', 'overall_risk'), ('mean_health', 'health_score'),
                       ('mean_iaq', 'iaq_score'), ('mean_struct', 'struct_score')):
        assert a['scores'][key] == _mean1([p[field] for p in drawn]), key
    risk = [p['overall_risk'] for p in drawn]
    assert a['risk_tiers'] == {'low': sum(r < 34 for r in risk),
                               'medium': sum(34 <= r < 67 for r in risk),
                               'high': sum(r >= 67 for r in risk)}
    assert sum(a['housing']['conditions'].values()) == len(drawn)


def test_october_individual_rescored(october):
    geo, *_ = october
    p = _all_props(geo)
    assert (p['R_36hwtQ5ZQOhBucE']['iaq_score'], p['R_36hwtQ5ZQOhBucE']['overall_risk']) == (10, 22)
    assert (p['R_oGMYPwP8cLkeLsx']['iaq_score'], p['R_oGMYPwP8cLkeLsx']['overall_risk']) == (17, 46)
    assert (p['R_dGTyY060JYUPQkh']['iaq_score'], p['R_dGTyY060JYUPQkh']['overall_risk']) == (12, 15)
