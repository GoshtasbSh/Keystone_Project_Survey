"""R_dGTyY060JYUPQkh ticked only 'Other:' and wrote 'Propane camp stove'; the
documented +10 gas/propane rule never read the text."""
from __future__ import annotations

import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'api'))

from _processing import _compute_iaq_score, load_parcel_index, process_iaq_bytes  # noqa: E402

OCTOBER = pathlib.Path('/Users/goshtasbshahriari/UF Dropbox/Goshtasb Shahriari Mehr/'
                       'DTSC_Lab/Keystone_Data/'
                       'Keystone Heights Survey - V1_October 7, 2026_00.47.csv')


def row(**kw):
    base = {'Mold': '', 'Mold_10_TEXT': '',
            'Leakage 2_1': '', 'Leakage 2_2': '', 'Leakage 2_3': '', 'Leakage 2_4': '',
            'Cooling System _1': '', 'Cooling System _2': '',
            'Cooling System _3': '', 'Cooling System _4': '',
            'Cooking': '', 'Cooking _9_TEXT': ''}
    base.update(kw)
    return base


def _all_props(geo):
    """Drawn plus superseded features (GAP-10), for per-respondent lookups."""
    return {f['properties']['response_id']: f['properties']
            for f in geo['features'] + geo.get('superseded_features', [])}


@pytest.mark.parametrize('stove,text,expected', [
    ('Other:', 'Propane camp stove ', 10),
    ('Other:', 'No stove', 0),
    ('Other:', "Don't have", 0),
    ('Other:', 'Eye portable ', 0),
    ('gas cooktops,Other:', 'Gas cooktop doesn’t work', 10),   # no double count
    ('electric cooktops', 'propane', 0),     # text ignored unless Other ticked
])
def test_other_stove_text_is_scored(stove, text, expected):
    assert _compute_iaq_score(row(Cooking=stove, **{'Cooking _9_TEXT': text})) == expected


def test_october_respondent():
    if not OCTOBER.exists():
        pytest.skip('October export not present')
    geo, *_ = process_iaq_bytes(OCTOBER.read_bytes(), [], load_parcel_index())
    p = _all_props(geo)
    assert p['R_dGTyY060JYUPQkh']['iaq_score'] == 12      # was 2
    assert p['R_dGTyY060JYUPQkh']['overall_risk'] == 15   # was 11
