"""QID42's fourth scale point is literally 'none' ("the problem never
happened"). Treating it as a blank cell erased it from 323 popup cells
(105 of 114 respondents). Scores were never affected."""
from __future__ import annotations

import pathlib
import sys

import pandas as pd
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'api'))

from _processing import (  # noqa: E402
    _cell, _is_blank_answer, _isna, _val_at_orig_idx,
)

LEAK = ('leakage_roof', 'leakage_walls', 'leakage_windows', 'leakage_floor')


def _all_props(geo):
    """Drawn plus superseded features (GAP-10): R_5LnXMcaezhqW28F becomes a
    superseded earlier answer once the household dedup lands, and the 323
    count is over every placed response, drawn or not."""
    return {f['properties']['response_id']: f['properties']
            for f in geo['features'] + geo.get('superseded_features', [])}


@pytest.mark.parametrize('v,blank', [
    (None, True), (float('nan'), True), ('', True), ('  ', True), ('nan', True),
    ('none', False), ('None', False), ('No', False), (0, False),
])
def test_blank_answer_predicate(v, blank):
    assert _is_blank_answer(v) is blank


def test_cell_keeps_the_scale_point_none():
    assert _cell({'Leakage 2_1': 'none'}, 'Leakage 2_1') == 'none'
    assert _cell({'Leakage 2_1': float('nan')}, 'Leakage 2_1') == ''


def test_val_at_orig_idx_keeps_none():
    assert _val_at_orig_idx(pd.Series(['none', 'x']), 0) == 'none'


def test_isna_is_unchanged_for_addresses_and_notes():
    assert _isna('none') is True


@pytest.fixture(scope='module')
def october(october_iaq_copy):
    geo, *_ = october_iaq_copy
    return _all_props(geo)


def test_october_water_matrix_none_survives(october):
    assert [october['R_5LnXMcaezhqW28F'][k] for k in LEAK] == ['none'] * 4
    assert sum(1 for p in october.values() for k in LEAK if p[k] == 'none') == 323
