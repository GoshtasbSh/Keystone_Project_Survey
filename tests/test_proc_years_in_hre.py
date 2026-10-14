"""A typed answer in a text-entry column is not a choice code.

QID12_TEXT ('How long have you lived in HRE') was run through QID12's choice
map, so a typed '1' became 'Year(s)' for 9 respondents and fell out of the
years statistics. Answers in months were not parsed at all."""
from __future__ import annotations

import pathlib
import sys

import pandas as pd
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'api'))

from _processing import (  # noqa: E402
    _apply_qsf_display_labels, _parse_years_numeric,
)

TYPED_ONE = ['R_71LqP7xFx71BPsl', 'R_1LOVKbX2iH6Xh3j', 'R_6xzTr24XxYm8KC4',
             'R_kVLcdKScFHPgWVR', 'R_2jh8CoISTKs6UKv', 'R_m7ABYoFMDa7R15C',
             'R_l2K5bwgfJ6nwQIN', 'R_eubE9bDo3QIohbh', 'R_iUaZoRCDNkHIsjm']


def _all_props(geo):
    """Drawn plus superseded features (GAP-10), so a respondent whose answer
    becomes an earlier same-household response is still found."""
    return {f['properties']['response_id']: f['properties']
            for f in geo['features'] + geo.get('superseded_features', [])}


def test_text_entry_column_is_not_relabelled():
    df = pd.DataFrame({'How long they there': ['1', '12', '5 months'],
                       'QID47': ['1', '2', '4']})
    qmap = {'QID12_TEXT': 0, 'QID12': 0, 'QID47': 1}
    _apply_qsf_display_labels(df, qmap)
    assert df['How long they there'].tolist() == ['1', '12', '5 months']
    assert df['QID47'].tolist() == ['less than 1 year', '1-5 years', 'Indefinitely']


@pytest.mark.parametrize('typed,years', [
    ('1', 1.0), ('10', 10.0), ('10 years', 10.0), ('15 yrs', 15.0),
    ('1yr', 1.0), ('40yrs', 40.0), ('7 y', 7.0), ('30 yeads ', 30.0),
    ('2.5 years', 2.5), ('.5', 0.5), ('10+', 10.0),
    ('12 yrs, family home for 20', 12.0),
    ('5 months', round(5 / 12, 4)), ('5months', round(5 / 12, 4)),
    ('2mo', round(2 / 12, 4)), ('3 mo', 0.25), ('9 months', 0.75),
    ('6/25', None), ('Last montj', None), ('No answer', None),
    ('Piedmont', None), ('Year(s)', None), ('', None), (None, None),
])
def test_years_parser(typed, years):
    assert _parse_years_numeric(typed) == years


@pytest.fixture(scope='module')
def october(october_iaq_copy):
    geo, analysis, *_ = october_iaq_copy
    return _all_props(geo), analysis


def test_october_typed_one_is_one_year(october):
    props, _ = october
    assert [props[r]['years_in_hre'] for r in TYPED_ONE] == ['1'] * 9
    assert not any(p['years_in_hre'] == 'Year(s)' for p in props.values())


def test_october_years_stats(october):
    # GAP-10 RE-BASELINE: analysis-level numbers over the 106 households
    # (latest response each, MATCH-3). Before the dedup (114 placed
    # responses) they read (110, 11.2, 7.5); the '<1 yr' (8) and '1–4' (27)
    # bins did not move.
    _, analysis = october
    y = analysis['residency']['years_in_hre']
    assert (y['n_valid'], y['mean'], y['median']) == (102, 10.9, 7.0)
    # Every bin, read from the run and matched by the independent recompute
    # (VER-2 semantics, latest per household); the bins sum to n_valid.
    assert y['distribution'] == {'<1 yr': 8, '1–4': 27, '5–9': 24,
                                 '10–19': 23, '20–29': 11, '30+': 9}
    assert sum(y['distribution'].values()) == y['n_valid']


def test_calendar_years_and_fractions_are_not_guessed():
    # A bare calendar year is a "since" year, not 1990 years; one such answer
    # would add ~19 years to the published mean. A trailing fraction would
    # silently drop to its whole part. Neither is guessed.
    for typed in ('1990', '2005', '2005 years', '150', '1990 yrs'):
        assert _parse_years_numeric(typed) is None, typed
    for typed in ('2 1/2 years', '5 1/2', '1/2 year', '3 1/2yrs'):
        assert _parse_years_numeric(typed) is None, typed
    assert _parse_years_numeric('100') == 100
    assert _parse_years_numeric('120 months') == 10
    assert _parse_years_numeric('2.5 years') == 2.5
