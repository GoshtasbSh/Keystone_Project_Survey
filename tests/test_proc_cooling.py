"""R_oGMYPwP8cLkeLsx: window unit 'less than 10 years' AND "Don't know" in one
multi-answer cell was read as no A/C (+4 instead of +2): IAQ 19, should be 17."""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'api'))

from _processing import _compute_iaq_score  # noqa: E402

DK = "Don't know/Not applicable"


def row(**kw):
    base = {'Mold': '', 'Mold_10_TEXT': '',
            'Leakage 2_1': '', 'Leakage 2_2': '', 'Leakage 2_3': '', 'Leakage 2_4': '',
            'Cooling System _1': '', 'Cooling System _2': '',
            'Cooling System _3': '', 'Cooling System _4': '', 'Cooking': ''}
    base.update(kw)
    return base


def test_window_ac_with_age_and_dont_know_is_still_window_ac():
    r = row(**{'Cooling System _1': DK,
               'Cooling System _2': f'less than 10 years,{DK}',
               'Cooling System _3': DK, 'Cooling System _4': DK})
    assert _compute_iaq_score(r) == 2


def test_central_with_age_and_dont_know_is_baseline():
    r = row(**{'Cooling System _1': f'{DK},10 to 15 years', 'Cooling System _4': DK})
    assert _compute_iaq_score(r) == 0


def test_dont_know_alone_still_does_not_count():
    assert _compute_iaq_score(row(**{'Cooling System _1': DK,
                                     'Cooling System _2': 'less than 10 years'})) == 2


def test_october_respondent(october_iaq_copy):
    geo, *_ = october_iaq_copy
    # Drawn plus superseded (GAP-10): found whether or not this response is
    # later marked as an earlier same-household answer.
    p = {f['properties']['response_id']: f['properties']
         for f in geo['features'] + geo.get('superseded_features', [])}
    assert p['R_oGMYPwP8cLkeLsx']['iaq_score'] == 17
    assert p['R_oGMYPwP8cLkeLsx']['overall_risk'] == 46
