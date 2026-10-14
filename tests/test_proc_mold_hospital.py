"""R_36hwtQ5ZQOhBucE wrote 'no evidence to my knowledge' and was scored as
having mold (+30 IAQ). R_5TtaBRz99nWhzm1 and R_mT2CaA2cdWYOmij left the
hospital question blank and were shown "No"; every "yes" lost which choice."""
from __future__ import annotations

import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'api'))

from _lib import SURVEY_ANSWER_FIELDS  # noqa: E402
from _processing import (  # noqa: E402
    IAQ_FEATURE_POPUP_LABELS, _compute_iaq_score, _has_mold_evidence,
    _hospital_flag, _mold_text_denies, load_parcel_index, process_iaq_bytes,
)

OCTOBER = pathlib.Path('/Users/goshtasbshahriari/UF Dropbox/Goshtasb Shahriari Mehr/'
                       'DTSC_Lab/Keystone_Data/'
                       'Keystone Heights Survey - V1_October 7, 2026_00.47.csv')


def row(**kw):
    base = {'Mold': '', 'Mold_10_TEXT': '',
            'Leakage 2_1': '', 'Leakage 2_2': '', 'Leakage 2_3': '', 'Leakage 2_4': '',
            'Cooling System _1': '', 'Cooling System _2': '',
            'Cooling System _3': '', 'Cooling System _4': '', 'Cooking': ''}
    base.update(kw)
    return base


def _drawn_props(geo):
    """Features drawn on the map — the analysis denominator (households once
    the MATCH-3 dedup lands)."""
    return {f['properties']['response_id']: f['properties'] for f in geo['features']}


def _all_props(geo):
    """Drawn plus superseded features (GAP-10), for per-respondent lookups."""
    return {f['properties']['response_id']: f['properties']
            for f in geo['features'] + geo.get('superseded_features', [])}


@pytest.mark.parametrize('text,denies', [
    ('no evidence to my knowledge', True),
    ('No evidence', True),
    ('no evidence of mold', True),
    ('No visible evidence', True),
    ('not to my knowledge', True),
    ('None', True), ('N0o', True), ('No where visable', True),   # unchanged
    ('closet', False),
    ('Outside trim', False),
    ('evidence in the closet', False),
    ('no evidence but I smell it in the closet', False),
])
def test_mold_denial_phrases(text, denies):
    assert _mold_text_denies(text) is denies


def test_no_evidence_costs_no_mold_points():
    r = row(Mold='Other:', Mold_10_TEXT='no evidence to my knowledge')
    assert _has_mold_evidence(r) is False
    assert _compute_iaq_score(r) == 0


@pytest.mark.parametrize('cell,flag', [
    ('', ''), ('No', 'no'),
    ('Yes, Doctor visits for allergy.', 'yes'),
    ('Yes, hospitalization/visiting the emergency room for asthma attack.', 'yes'),
    ('Yes, Others.', 'yes'),
])
def test_hospital_flag_has_a_blank_state(cell, flag):
    assert _hospital_flag(cell) == flag


def test_hospital_detail_is_members_only_and_labelled():
    assert 'hospital_visit_detail' in SURVEY_ANSWER_FIELDS
    assert 'hospital_visit_detail' in IAQ_FEATURE_POPUP_LABELS


@pytest.fixture(scope='module')
def october():
    if not OCTOBER.exists():
        pytest.skip('October export not present')
    geo, analysis, *_ = process_iaq_bytes(OCTOBER.read_bytes(), [], load_parcel_index())
    return geo, analysis


def test_october_no_evidence_respondent(october):
    geo, _ = october
    props = _all_props(geo)
    assert props['R_36hwtQ5ZQOhBucE']['has_mold'] is False
    assert props['R_36hwtQ5ZQOhBucE']['iaq_score'] == 10


def test_october_mold_pct(october):
    # GAP-10 RE-BASELINE: over the 106 households (latest response each,
    # MATCH-3). It read 28.1 (32 / 114 placed responses) before the dedup,
    # and 28.9 before the mold fix.
    _, analysis = october
    assert analysis['health']['mold_pct'] == 28.3


def test_october_hospital_blank_and_detail(october):
    geo, analysis = october
    every = _all_props(geo)
    for rid in ('R_5TtaBRz99nWhzm1', 'R_mT2CaA2cdWYOmij'):
        assert every[rid]['hospital_visit'] == ''
        assert every[rid]['hospital_visit_detail'] == ''
    yes_any = [p for p in every.values() if p['hospital_visit'] == 'yes']
    assert yes_any and all(p['hospital_visit_detail'].startswith('Yes') for p in yes_any)
    # hospital_pct is over the drawn features (households after MATCH-3).
    drawn = _drawn_props(geo)
    yes = [p for p in drawn.values() if p['hospital_visit'] == 'yes']
    assert analysis['health']['hospital_pct'] == round(len(yes) / len(drawn) * 100, 1)
