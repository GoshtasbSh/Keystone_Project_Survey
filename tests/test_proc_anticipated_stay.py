"""QID47 is multi-answer: R_7dct1jzsaXwNyyR's '1-5 years,6-10 years' was
charted as a third, combined bar instead of once in each option's bar."""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'api'))

from _processing import _compute_iaq_analysis  # noqa: E402


def _feat(**props):
    base = {'overall_risk': 0, 'health_score': 0, 'iaq_score': 0, 'struct_score': 0}
    base.update(props)
    return {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [0, 0]},
            'properties': base}


def test_anticipated_stay_counts_each_option():
    a = _compute_iaq_analysis([_feat(anticipated_stay='1-5 years,6-10 years'),
                               _feat(anticipated_stay='Indefinitely'),
                               _feat(anticipated_stay='1-5 years')])
    assert a['residency']['anticipated_stay'] == {
        '1-5 years': 2, '6-10 years': 1, 'Indefinitely': 1}


def test_october_stay_bars(october_iaq_copy):
    _g, a, *_ = october_iaq_copy
    # GAP-10 RE-BASELINE: analysis-level (drawn features only), one latest
    # response per household (MATCH-3): 106 households. Before the dedup
    # (114 placed responses) it read 64 / 27 / 8 / 6 / 10.
    assert a['residency']['anticipated_stay'] == {
        'Indefinitely': 59, '1-5 years': 26, 'less than 1 year': 8,
        '6-10 years': 5, "Don't know": 9}
