"""reconcile_responses: every ResponseId has one disposition; links obey the launch rules."""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts' / 'audit'))

import recompute_independent as RI  # noqa: E402
import reconcile_responses as RR    # noqa: E402


def test_house_no():
    assert RR.house_no('6306 Amherst Ave') == '6306'
    assert RR.house_no('  6318 amherst') == '6318'
    assert RR.house_no('First house right bowdoin') is None


def test_dispositions_are_exclusive_and_ordered():
    R = {'U': {'finished': '0', 'status': '0'}, 'P': {'finished': '1', 'status': '1'},
         'N': {'finished': '1', 'status': '16'}, 'S': {'finished': '1', 'status': '0'},
         'K': {'finished': '1', 'status': '16'}}
    d = RR.dispositions(R, placed={'S', 'K'}, superseded={'S': 'K'})
    assert d == {'U': 'unfinished', 'P': 'preview', 'N': 'unplaced', 'S': 'superseded', 'K': 'analysed'}


def test_status_16_offline_rows_are_not_previews():
    assert '16' not in RR.PREVIEW_STATUSES and '0' not in RR.PREVIEW_STATUSES
    assert RR.PREVIEW_STATUSES == RI.PREVIEW_STATUSES


def test_expected_sets_are_consistent():
    assert len(RR.EXPECTED_UNFINISHED) == 8 and len(RR.EXPECTED_PREVIEW) == 3
    assert len(RR.EXPECTED_UNPLACED) == 12 and len(RR.EXPECTED_SUPERSEDED) == 8
    assert RR.EXPECTED_NOW_MATCHED <= set(RR.EXPECTED_SUPERSEDED.values())
    assert len(RR.TEST_PIN_IDS) == 28
    assert 137 - 8 - 3 - 12 - 8 == RR.EXPECTED_ANALYSED
    assert RR.EXPECTED_MATCHED_CONTACTS >= 84


def test_test_pin_ids_equal_the_runbook_cleanup_set():
    sys.path.insert(0, str(ROOT / 'scripts'))
    sys.path.insert(0, str(ROOT / 'api'))
    import prod_runbook
    assert RR.TEST_PIN_IDS == set(prod_runbook.EXPECTED_TEST_PIN_IDS)


def _feature(rid, coords, **props):
    return {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': coords},
            'properties': {'response_id': rid, **props}}


def test_check_flags_cross_house_link_stale_pin_and_test_pin():
    R = {'R_x': {'finished': '1', 'status': '0', 'QID225_TEXT': '6318 Amherst Ave'}}
    iaq = {'geojson': {'features': [_feature('R_x', [-82.0, 29.7], overall_risk=40, match_status='matched')]},
           'analysis': {}}
    contacts = {'features': [
        {'properties': {'id': 53, 'address': '6306 Amherst Ave', 'match_status': 'matched',
                        'iaq_response_id': 'R_x'}},
        {'properties': {'source': 'field', 'field_point_id': 'b989a847-2d01-4121-ad7c-9eedff36fd38',
                        'iaq_response_id': 'R_x', 'iaq_overall_risk': 33}},
    ]}
    fails, _ = RR.check(R, iaq, contacts, field_rows=[])
    joined = '\n'.join(fails)
    assert 'linked to R_x typed 6318' in joined
    assert 'stale risk 33 != 40' in joined
    assert 'test pins still in blob' in joined


def _sup_fixture(kept_for_baylor):
    """All 8 earlier answers held in geojson.superseded_features (MATCH-3)."""
    sup = [_feature(e, [-82.0, 29.7], superseded=True, superseded_by=k)
           for e, k in RR.EXPECTED_SUPERSEDED.items()]
    sup[0]['properties']['superseded_by'] = kept_for_baylor
    return {'geojson': {'features': [], 'superseded_features': sup}, 'analysis': {}}


def test_superseded_features_are_read_and_their_kept_answer_checked():
    good = RR.check({}, _sup_fixture('R_j1xG6QD0Gw1G3uU'), {'features': []}, field_rows=[])[0]
    assert not [f for f in good if f.startswith('superseded flags')]
    bad = RR.check({}, _sup_fixture('R_somethingElse'), {'features': []}, field_rows=[])[0]
    assert [f for f in bad if f.startswith('superseded flags')]


def test_a_superseded_answer_drawn_on_the_map_fails():
    iaq = {'geojson': {'features': [_feature('R_5LnXMcaezhqW28F', [-82.0, 29.7])]}, 'analysis': {}}
    R = {'R_5LnXMcaezhqW28F': {'finished': '1', 'status': '0'}}
    fails = RR.check(R, iaq, {'features': []}, field_rows=[])[0]
    assert any(f.startswith('drawn ids') for f in fails)


def _canvass(cid, address, status='Completed', lon=-82.0, **props):
    base = {'id': cid, 'address': address, 'status': status, 'status_detail': 'done',
            'notes': '', 'date': '2026-01-10', 'second_attempt': ''}
    return {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [lon, 29.78]},
            'properties': {**base, **props}}


def _before_after():
    before = [_canvass(53, '6306 Amherst Ave'), _canvass(100, '6376 Antioch'),
              _canvass(7, '6100 Harvard Ave', lon=-82.1),
              {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [-82.2, 29.7]},
               'properties': {'source': 'field', 'field_point_id': 'p1'}}]
    after = [_canvass(53, '6306 Amherst Ave', status='No Answer'),
             _canvass(100, '6376 Antioch', status='Follow Up'),
             _canvass(7, '6100 Harvard Ave', lon=-82.1, match_status='matched', has_iaq_survey=True),
             _canvass(191, '6386 Baylor', restored_from_field_pin='b989a847')]
    return before, after


def test_canvass_contacts_survive_with_only_the_documented_changes():
    before, after = _before_after()
    assert RR.compare_canvass_contacts(before, after) == []


def test_lost_duplicated_or_edited_canvass_contact_fails():
    before, after = _before_after()
    # drop one contact and duplicate another: same count, still caught
    dup = [after[0], after[1], after[3], dict(after[3])]
    fails = '\n'.join(RR.compare_canvass_contacts(before, dup))
    assert 'contact 7 (6100 Harvard Ave) missing' in fails
    assert 'duplicate contact id 191' in fails
    for key, val in (('notes', 'edited'), ('status_detail', 'x'), ('date', '2026-02-02'),
                     ('second_attempt', 'y'), ('address', '6101 Harvard Ave')):
        b, a = _before_after()
        a[2]['properties'][key] = val
        assert any(key in f for f in RR.compare_canvass_contacts(b, a)), key
    b, a = _before_after()
    a[2]['geometry']['coordinates'] = [-82.1001, 29.78]
    assert any('geometry' in f for f in RR.compare_canvass_contacts(b, a))


def test_undocumented_status_change_or_new_contact_fails():
    b, a = _before_after()
    a[2]['properties']['status'] = 'Refused'
    assert any('status' in f for f in RR.compare_canvass_contacts(b, a))
    b, a = _before_after()
    a.append(_canvass(500, '1 New St'))
    assert any('unexpected new contact 500' in f for f in RR.compare_canvass_contacts(b, a))
    b, a = _before_after()
    a[3]['properties'].pop('restored_from_field_pin')
    assert any('unexpected new contact 191' in f for f in RR.compare_canvass_contacts(b, a))
