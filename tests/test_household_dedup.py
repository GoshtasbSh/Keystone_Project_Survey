"""One household, one response (user decision 2026-10-13).

Eight households answered the survey twice. Both answers were drawn as
stacked dots and both counted in every percentage. The rule now: keep only
the LATEST response (by RecordedDate) per household -- one parcel point
plus one typed house number -- and keep the earlier one in the stored data
(geojson['superseded_features']) without drawing, matching or counting it.
"""
from __future__ import annotations

import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'api'))

from _processing import (  # noqa: E402
    _supersede_repeat_households,
)


# earlier -> kept, for the 8 households in the October export.
OCT_PAIRS = {
    'R_5LnXMcaezhqW28F': 'R_j1xG6QD0Gw1G3uU',   # 6386 Baylor
    'R_6pRawZol21jqapc': 'R_3915ZWsZpRAwPi9',   # 7168 Wesleyan
    'R_1E4YReRP6XTeX06': 'R_0U4XyfXUNDttX9a',   # 6390 Bucknell
    'R_kZXrW8v3LxbbUTV': 'R_hv0cc021NGKRc5M',   # 6401 Bucknell
    'R_6s0PVusMDUucFQY': 'R_h6cnt2kXgSK5Bbg',   # 6255 Dennison
    'R_iB2E7Yzs7PSGMlr': 'R_ju3Amx8yBiJ45L0',   # 6223 Harvard
    'R_2KqXYjOIYV1zFdH': 'R_5oBDIEcTfYUvj8n',   # 7205 Princeton
    'R_mLTilJCf3lIPEoI': 'R_6Nqhz2mzupemk9v',   # 6324 Dennison (11 s apart)
}


def _f(rid, house, date, lon=-82.0100, lat=29.7800):
    return {'type': 'Feature',
            'geometry': {'type': 'Point', 'coordinates': [lon, lat]},
            'properties': {'response_id': rid, 'house_number': house,
                           'recorded_date': date, 'iaq_matched': False}}


def test_latest_response_per_household_is_kept():
    feats = [_f('R_new', '6386', '2026-03-03 10:00:00'),
             _f('R_old', '6386', '2026-01-17 09:00:26'),
             _f('R_other', '6390', '2026-01-01 00:00:00', lon=-82.0200)]
    kept, superseded = _supersede_repeat_households(feats)
    assert [f['properties']['response_id'] for f in kept] == ['R_new', 'R_other']
    assert [f['properties']['response_id'] for f in superseded] == ['R_old']
    old = superseded[0]['properties']
    assert old['superseded'] is True and old['superseded_by'] == 'R_new'
    assert old['match_status'] == 'superseded' and old['iaq_matched'] is False
    new = kept[0]['properties']
    assert new['household_responses'] == 2
    assert new['superseded_response_ids'] == ['R_old']
    assert 'household_responses' not in kept[1]['properties']


def test_same_timestamp_later_csv_row_wins():
    feats = [_f('R_a', '6324', '2026-07-20 09:01:41'),
             _f('R_b', '6324', '2026-07-20 09:01:41')]
    kept, superseded = _supersede_repeat_households(feats)
    assert [f['properties']['response_id'] for f in kept] == ['R_b']
    assert [f['properties']['response_id'] for f in superseded] == ['R_a']


def test_two_house_numbers_on_one_parcel_point_are_two_households():
    """A double lot: 6306 and 6318 Amherst can share a parcel point."""
    feats = [_f('R_6306', '6306', '2026-01-01 00:00:00'),
             _f('R_6318', '6318', '2026-02-01 00:00:00')]
    kept, superseded = _supersede_repeat_households(feats)
    assert len(kept) == 2 and superseded == []


def test_responses_without_a_house_number_are_never_grouped():
    feats = [_f('R_x', '', '2026-01-01 00:00:00'),
             _f('R_y', '', '2026-02-01 00:00:00')]
    kept, superseded = _supersede_repeat_households(feats)
    assert len(kept) == 2 and superseded == []


@pytest.fixture(scope='module')
def october(october_iaq_copy):
    return october_iaq_copy


def test_october_keeps_one_response_per_household(october):
    geojson, analysis, streets, _n_up, _failed = october
    kept = {f['properties']['response_id'] for f in geojson['features']}
    sup = {f['properties']['response_id']: f['properties']['superseded_by']
           for f in geojson['superseded_features']}
    assert sup == OCT_PAIRS
    assert not (kept & set(OCT_PAIRS))           # earlier ones not drawn
    assert set(OCT_PAIRS.values()) <= kept       # latest ones are
    assert len(geojson['features']) == 106
    for f in geojson['superseded_features']:     # no PII helpers stored
        assert 'raw_address' not in f['properties']
        assert 'years_in_hre_num' not in f['properties']


def test_october_counts_report_responses_and_households(october):
    _geojson, analysis, streets, _n_up, _failed = october
    v = analysis['validation']
    assert analysis['n_responses'] == 106          # every chart's denominator
    assert analysis['n_households'] == 106
    assert analysis['n_responses_mapped'] == 114
    assert v['responses_mapped'] == 114
    assert v['households_mapped'] == 106
    assert v['repeat_responses_excluded'] == 8
    assert v['total_iaq_responses'] == 106
    # Dropped / charted-% are about PLACING responses (114), not households.
    # completed_in_csv is 129 today and 126 once previews are filtered out.
    done = v['completed_in_csv']
    assert done in (129, 126)
    assert v['dropped_no_geocode'] == done - 114       # NOT done - 106
    assert v['charted_pct_of_completed'] == round(114 / done * 100, 1)
    assert sum(d['n'] for d in streets.values()) == 106
