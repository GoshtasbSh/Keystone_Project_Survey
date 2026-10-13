"""Typed "Other" answers and named mold rooms reach members, never the public.

Every text-entry column used to be dropped: R_dGTyY060JYUPQkh's stove showed
'Other:' without 'Propane camp stove', and R_378SeCJx2uslNli's mold showed only
'Yes' without their four rooms.
"""
from __future__ import annotations

import pathlib
import sys

import pandas as pd
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'api'))

from _lib import SURVEY_ANSWER_FIELDS, strip_survey_answers  # noqa: E402
from _processing import (  # noqa: E402
    IAQ_FEATURE_POPUP_LABELS, OTHER_TEXT_FIELDS, _extract_other_texts,
    _mold_locations, _redact_free_text, load_parcel_index, process_iaq_bytes,
)

OCTOBER = pathlib.Path('/Users/goshtasbshahriari/UF Dropbox/Goshtasb Shahriari Mehr/'
                       'DTSC_Lab/Keystone_Data/'
                       'Keystone Heights Survey - V1_October 7, 2026_00.47.csv')
NEW_FIELDS = set(OTHER_TEXT_FIELDS) | {'mold_locations'}


def _all_props(geo):
    """Drawn plus superseded features (GAP-10), for per-respondent lookups."""
    return {f['properties']['response_id']: f['properties']
            for f in geo['features'] + geo.get('superseded_features', [])}


def test_every_new_field_is_members_only():
    assert NEW_FIELDS <= set(SURVEY_ANSWER_FIELDS)
    fc = {'type': 'FeatureCollection', 'features': [
        {'type': 'Feature', 'geometry': None,
         'properties': {**{k: 'x' for k in NEW_FIELDS}, 'overall_risk': 3}}]}
    assert strip_survey_answers(fc)['features'][0]['properties'] == {'overall_risk': 3}


def test_every_new_field_has_a_popup_label():
    assert NEW_FIELDS <= set(IAQ_FEATURE_POPUP_LABELS)


@pytest.mark.parametrize('raw,clean', [
    ('Propane camp stove ', 'Propane camp stove'),
    ('call me 352-555-0101 please', 'call me [phone removed] please'),
    ('mail jane.doe@ufl.edu', 'mail [email removed]'),
    ('', ''),
    ('x' * 400, 'x' * 300),
])
def test_redaction(raw, clean):
    assert _redact_free_text(raw) == clean


def test_mold_locations_drop_the_bare_other():
    assert _mold_locations('Kitchen,Bathroom,Other:') == 'Kitchen, Bathroom'
    assert _mold_locations('Other:') == ''
    assert _mold_locations('') == ''


def test_other_text_read_by_exact_import_id_only():
    row = pd.Series(['Other:', 'Propane camp stove', 'gas cooktops'])
    out = _extract_other_texts(row, {'QID148': 0, 'QID148_4_TEXT': 1})
    assert out['cooking_other'] == 'Propane camp stove'
    assert out['mold_other'] == ''            # no column -> blank, never a guess


@pytest.fixture(scope='module')
def october():
    if not OCTOBER.exists():
        pytest.skip('October export not present')
    geo, *_ = process_iaq_bytes(OCTOBER.read_bytes(), [], load_parcel_index())
    return _all_props(geo)


def test_october_free_text_examples(october):
    assert october['R_dGTyY060JYUPQkh']['cooking_other'] == 'Propane camp stove'
    assert october['R_378SeCJx2uslNli']['mold_locations'] == \
        'Kitchen, Bathroom, Inner walls/Windows, Ceiling'
    assert october['R_iUaZoRCDNkHIsjm']['housing_type_other'] == 'Triple wide mobile home'
    assert october['R_iB2E7Yzs7PSGMlr']['ownership_other'] == 'Rent to own'
    assert october['R_36hwtQ5ZQOhBucE']['mold_other'] == 'no evidence to my knowledge'
