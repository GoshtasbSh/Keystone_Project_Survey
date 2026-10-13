"""Scores are documented and hand-checked with round-half-up; Python's round()
is half-to-even (22.5 -> 22). 18 IAQ and 18 risk scores were 1 low (21
respondents in all); no risk tier changes."""
from __future__ import annotations

import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'api'))

from _processing import _compute_iaq_score, _round_half_up  # noqa: E402


@pytest.mark.parametrize('x,nd,out', [
    (22.5, 0, 23), (37.5, 0, 38), (7.5, 0, 8), (2.5, 0, 3), (22.4, 0, 22),
    (18.35, 1, 18.4), (18.349, 1, 18.3),
    (0.35 * 10 + 0.35 * 30 + 0.30 * 25, 0, 22),     # float noise 21.999...
])
def test_round_half_up(x, nd, out):
    assert _round_half_up(x, nd) == out


def test_non_finite_passes_through():
    import math
    assert math.isnan(_round_half_up(float('nan'), 1))


def test_three_water_problems_round_up():
    r = {'Mold': '', 'Leakage 2_1': 'less than one week', 'Leakage 2_2': 'none',
         'Leakage 2_3': 'more than one week', 'Leakage 2_4': 'not fixed',
         'Cooling System _1': '', 'Cooling System _2': '',
         'Cooling System _3': '', 'Cooling System _4': '', 'Cooking': ''}
    assert _compute_iaq_score(r) == 23          # 22.5


@pytest.mark.parametrize('h,i,s,risk', [
    (0, 0, 35, 11),      # 10.5 -> 11 (was 10)
    (18, 2, 25, 15),     # 14.5 -> 15 (was 14)
    (94, 17, 25, 46),
])
def test_risk_is_exact_half_up(h, i, s, risk):
    assert (35 * h + 35 * i + 30 * s + 50) // 100 == risk
