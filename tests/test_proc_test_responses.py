"""Qualtrics previews, tests and spam are not respondents.

Before 2026-10-13 the only filter was Finished, so the 3 Status=1 previews in
the October export counted as "completed" (129 instead of 126) and were
dropped only because their typed address was blank or 'ttt'. A preview with a
real-looking address would have been mapped and scored. Status 16 (the field
tablets' offline app) is real and must be kept.
"""
from __future__ import annotations

import pathlib
import sys

import pandas as pd
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'api'))

from _processing import _is_test_response, load_parcel_index, process_iaq_bytes  # noqa: E402

OCTOBER = pathlib.Path('/Users/goshtasbshahriari/UF Dropbox/Goshtasb Shahriari Mehr/'
                       'DTSC_Lab/Keystone_Data/'
                       'Keystone Heights Survey - V1_October 7, 2026_00.47.csv')
PREVIEWS = {'R_78IEP3v2S0sfWk9', 'R_7dXknXZ9AtNEPvF', 'R_7duCmfU1iGEFEXI'}


def _all_props(geo):
    """Drawn features plus any superseded (earlier same-household) answers.

    Superseded-aware from the start (GAP-10): once the household dedup lands,
    geo['features'] holds one response per household and the earlier answers
    move to geo['superseded_features']; together they are still every placed
    response.
    """
    return {f['properties']['response_id']: f['properties']
            for f in geo['features'] + geo.get('superseded_features', [])}


@pytest.mark.parametrize('status,channel,is_test', [
    ('0', 'qr', False),            # IP Address — real
    ('16', '', False),             # Offline app — real (92 October rows)
    ('4', '', False),              # Imported — real
    ('1', 'preview', True),        # Survey Preview
    ('2', '', True),               # Survey Test
    ('8', '', True),               # Spam
    ('9', '', True),               # Preview Spam
    ('17', '', True),              # Offline Survey Preview
    (1.0, '', True),               # pandas float code
    ('Survey Preview', 'preview', True),   # text export (April)
    ('Offline', '', False),                # text export (April)
    ('IP Address', 'qr', False),
    ('0', 'preview', True),        # channel alone marks a preview
])
def test_status_codes_and_labels(status, channel, is_test):
    raw = pd.DataFrame({'Status': [status], 'DistributionChannel': [channel]})
    assert bool(_is_test_response(raw).iloc[0]) is is_test


def test_no_status_column_excludes_nothing():
    raw = pd.DataFrame({'Finished': ['1', '1']})
    assert not _is_test_response(raw).any()


@pytest.fixture(scope='module')
def october():
    if not OCTOBER.exists():
        pytest.skip('October export not present')
    return process_iaq_bytes(OCTOBER.read_bytes(), [], load_parcel_index())


def test_october_counts_exclude_the_three_previews(october):
    geo, analysis, _streets, _n, failed = october
    v = analysis['validation']
    assert v['excluded_test_responses'] == 3
    assert set(v['excluded_test_ids']) == PREVIEWS
    assert v['completed_in_csv'] == 126
    assert v['dropped_no_geocode'] == 12
    assert v['charted_pct_of_completed'] == 90.5
    # Every placed response, drawn or superseded (GAP-10: stays 114 after the
    # household dedup splits them 106 + 8).
    assert len(geo['features']) + len(geo.get('superseded_features', [])) == 114
    ids = set(_all_props(geo))
    assert not ids & PREVIEWS
