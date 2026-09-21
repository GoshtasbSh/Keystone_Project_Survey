"""The IAQ composite must score what the questionnaire actually asked.

Two of its inputs are matrix questions whose cells hold a SCALE POINT, not a
tick, and one is a check-all with no "none of these" option. Reading any
non-empty cell as a positive finding got all three wrong:

  QID149  mold, "check all that apply", choices are SPACES only. There is no
          "no mold" option, so respondents with no mold wrote it in the free-text
          "Other:" box. 30+ of them said "None" / "No" / "No mold" and were
          scored as having mold — +30, a third of the whole composite.

  QID42   water problems, scale = how long it persisted, whose last point is
          literally 'none'. (Already handled; pinned here so it stays that way.)

  QID205  cooling, scale = the system's AGE, last point "Don't know/Not
          applicable". 35 households took the +4 no-A/C penalty and 29 of them
          had reported a real age for central or window A/C.

These tests state the intended reading per respondent, so a regression shows up
as a specific wrong household rather than a drifting average.
"""
from __future__ import annotations

import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'api'))

from _processing import (  # noqa: E402
    _compute_iaq_score, _has_mold_evidence,
)


def row(**kw):
    """A normalised row with every column the IAQ scorer reads, blank default."""
    base = {'Mold': '', 'Mold_10_TEXT': '',
            'Leakage 2_1': '', 'Leakage 2_2': '', 'Leakage 2_3': '', 'Leakage 2_4': '',
            'Cooling System _1': '', 'Cooling System _2': '',
            'Cooling System _3': '', 'Cooling System _4': '', 'Cooking': ''}
    base.update(kw)
    return base


# ── mold ──────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize('cell,text,expected', [
    ('', '', False),                                  # no answer
    ('Bathroom', '', True),                           # a named space
    ('Kitchen,Bathroom', '', True),
    ('Other:', 'None', False),                        # 21 respondents said this
    ('Other:', 'No', False),                          # 7 said this
    ('Other:', 'No mold', False),                     # 3 said this
    ('Other:', "I don't think so", False),
    ('Other:', "I don't know", False),                # not knowing is not evidence
    ('Other:', '', False),                            # ticked, typed nothing
    ('Other:', 'closet', True),                       # a real place
    ('Other:', 'I can smell mold but have not found it', True),
    ('Bedroom,Other:', 'None', True),                 # a named space still counts
])
def test_mold_evidence_reads_the_respondents_actual_answer(cell, text, expected):
    assert _has_mold_evidence(row(Mold=cell, Mold_10_TEXT=text)) is expected


def test_denying_mold_in_the_other_box_costs_no_iaq_points():
    said_none = _compute_iaq_score(row(Mold='Other:', Mold_10_TEXT='None'))
    named = _compute_iaq_score(row(Mold='Bathroom'))
    assert said_none == 0, 'a household that said "None" was charged for mold'
    assert named == 30


# ── water problems (QID42) ────────────────────────────────────────────────────

def test_none_is_not_a_water_problem():
    assert _compute_iaq_score(row(**{f'Leakage 2_{i}': 'none'
                                     for i in (1, 2, 3, 4)})) == 0


def test_each_real_water_problem_scores_seven_and_a_half():
    assert _compute_iaq_score(row(**{
        'Leakage 2_1': 'less than one week', 'Leakage 2_2': 'none',
        'Leakage 2_3': 'more than one week', 'Leakage 2_4': 'not fixed'})) == 22


# ── cooling (QID205) ──────────────────────────────────────────────────────────

def test_central_ac_with_a_real_age_is_not_scored_as_having_no_ac():
    """The 29-household case: an A/C age reported AND the no-A/C row answered."""
    r = row(**{'Cooling System _1': 'less than 10 years',
               'Cooling System _2': 'less than 10 years',
               'Cooling System _3': 'less than 10 years',
               'Cooling System _4': "Don't know/Not applicable"})
    assert _compute_iaq_score(r) == 0


def test_genuinely_no_ac_still_takes_the_penalty():
    r = row(**{'Cooling System _4': 'less than 10 years'})
    assert _compute_iaq_score(r) == 4
    # "Don't know/Not applicable" on the no-A/C row, and no A/C reported
    # anywhere, is still a household reporting no air conditioning.
    r2 = row(**{'Cooling System _4': "Don't know/Not applicable"})
    assert _compute_iaq_score(r2) == 4


def test_window_or_fan_only_is_the_moderate_case():
    assert _compute_iaq_score(row(**{'Cooling System _2': '10 to 15 years'})) == 2
    assert _compute_iaq_score(row(**{'Cooling System _3': 'More than 15 years'})) == 2
    # central A/C present → baseline, no cooling penalty
    assert _compute_iaq_score(row(**{'Cooling System _1': 'More than 15 years',
                                     'Cooling System _3': 'More than 15 years'})) == 0


def test_dont_know_alone_is_not_a_cooling_system():
    """"Don't know/Not applicable" on a system row says nothing either way, so
    it must not be read as owning that system."""
    r = row(**{'Cooling System _1': "Don't know/Not applicable",
               'Cooling System _2': 'less than 10 years'})
    assert _compute_iaq_score(r) == 2, 'DK on central should not suppress the +2'


# ── stove (QID148) ────────────────────────────────────────────────────────────

@pytest.mark.parametrize('stove,expected', [
    ('electric cooktops', 0),
    ('gas cooktops', 10),
    ("don't know", 0),
    ('gas cooktops,Other:', 10),
])
def test_only_a_combustion_stove_scores(stove, expected):
    assert _compute_iaq_score(row(Cooking=stove)) == expected


# ── the composite, on a real household ────────────────────────────────────────

def test_worked_example_matches_the_documented_model():
    """R_3m2YTbXOWKc8exo from the May export, hand-calculated:
    mold named in inner+outer walls (+30), one water problem 'more than one
    week' (+7.5), central A/C < 10 years (no cooling penalty), electric stove.
    """
    r = row(Mold='Inner walls/Windows,Outer walls/Windows',
            **{'Leakage 2_1': 'none', 'Leakage 2_2': 'none',
               'Leakage 2_3': 'more than one week', 'Leakage 2_4': 'none',
               'Cooling System _1': 'less than 10 years',
               'Cooling System _2': 'less than 10 years',
               'Cooling System _3': "Don't know/Not applicable",
               'Cooling System _4': "Don't know/Not applicable",
               'Cooking': 'electric cooktops'})
    assert _compute_iaq_score(r) == 38
