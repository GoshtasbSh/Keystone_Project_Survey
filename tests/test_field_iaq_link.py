"""Field pin <-> Qualtrics response linking (_apply_iaq_to_field_features).

- nearest response within 30 m, not the first one in the list;
- distances compared at 0.1 m, so pin 187e3184 (30.009 m) links;
- a house number written in the pin's notes links up to 60 m
  (df4a4686: '6280 survey completed previously on qualtrics', 34.3 m);
- every pass copies the response's CURRENT scores (7 pins were stale);
- a pin whose response is gone and that matches nothing loses the link.
"""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'api'))

from _processing import (  # noqa: E402
    _apply_iaq_to_field_features, _haversine_m, _note_house_numbers,
    field_iaq_signature,
)

LON0, LAT0 = -82.0088710455206, 29.7791820935855   # pin df4a4686
M_PER_DEG_LAT = 6_371_000 * 3.141592653589793 / 180


def _north(m):
    return [LON0, LAT0 + m / M_PER_DEG_LAT]


def _pin(notes='', **props):
    return {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [LON0, LAT0]},
            'properties': {'source': 'field', 'field_point_id': 'pin', 'status': 'Completed',
                           'notes': notes, **props}}


def _iaq(rid, coords, house='', street='Dennison Ave', risk=31):
    return {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': coords},
            'properties': {'response_id': rid, 'house_number': house, 'street_name': street,
                           'overall_risk': risk, 'risk_tier': 'Low', 'health_score': 1,
                           'iaq_score': 2, 'struct_score': 3, 'iaq_matched': False}}


def test_distance_helper_matches_the_setup():
    assert abs(_haversine_m(LAT0, LON0, _north(34.3)[1], LON0) - 34.3) < 0.01


def test_nearest_response_wins_not_the_first_listed():
    far, near = _iaq('R_far', _north(25)), _iaq('R_near', _north(10))
    pin = _pin()
    assert _apply_iaq_to_field_features([pin], [far, near]) == 1
    assert pin['properties']['iaq_response_id'] == 'R_near'
    assert near['properties']['iaq_matched'] is True
    assert far['properties']['iaq_matched'] is False


def test_thirty_metres_is_compared_at_decimetre_precision():
    pin_in, pin_out = _pin(), _pin()
    assert _apply_iaq_to_field_features([pin_in], [_iaq('R_1', _north(30.04))]) == 1
    assert _apply_iaq_to_field_features([pin_out], [_iaq('R_2', _north(30.06))]) == 0
    assert 'iaq_response_id' not in pin_out['properties']


def test_house_number_in_notes_links_up_to_60_m_and_beats_a_nearer_house():
    target = _iaq('R_5BmauNbh58cXIzf', _north(34.3), house='6280')
    neighbour = _iaq('R_6276', _north(12), house='6276')
    pin = _pin('6280 survey completed previously on qualtrics ')
    _apply_iaq_to_field_features([pin], [neighbour, target])
    assert pin['properties']['iaq_response_id'] == 'R_5BmauNbh58cXIzf'


def test_house_number_in_notes_is_not_linked_beyond_60_m():
    pin = _pin('6409 Beloit said she completed about a week ago')
    _apply_iaq_to_field_features([pin], [_iaq('R_bt9', _north(103.5), house='6409',
                                                street='Beloit Ave')])
    assert 'iaq_response_id' not in pin['properties']


def test_note_naming_another_known_street_is_not_linked_by_number():
    on_baylor = _iaq('R_baylor', _north(40), house='6414', street='Baylor Ave')
    on_vassar = _iaq('R_vassar', _north(45), house='6414', street='Vassar Dr')
    pin = _pin('Previously done in qualtrics 6414 Baylor')
    _apply_iaq_to_field_features([pin], [on_vassar, on_baylor])
    assert pin['properties']['iaq_response_id'] == 'R_baylor'


def test_phone_numbers_are_not_house_numbers():
    assert _note_house_numbers('call 352-555-1234 after 4') == []
    assert _note_house_numbers('6255 Dennison completed') == [('6255', 'dennison')]
    assert _note_house_numbers('House ID 7314') == [('7314', '')]


def test_scores_are_refreshed_on_an_already_linked_pin():
    pin = _pin('6308 completed previously on qualtrics ', has_iaq_survey=True,
               iaq_response_id='R_6SGNzs6svx7pBbb', iaq_overall_risk=37,
               iaq_risk_tier='Medium')
    resp = _iaq('R_6SGNzs6svx7pBbb', _north(5), house='6308', risk=23)
    before = field_iaq_signature(pin)
    assert _apply_iaq_to_field_features([pin], [resp]) == 0   # not newly enriched
    assert pin['properties']['iaq_overall_risk'] == 23
    assert field_iaq_signature(pin) != before


def test_link_to_a_response_that_no_longer_exists_is_cleared():
    pin = _pin('', has_iaq_survey=True, iaq_response_id='R_gone', iaq_overall_risk=13)
    _apply_iaq_to_field_features([pin], [_iaq('R_far', _north(200))])
    p = pin['properties']
    assert 'has_iaq_survey' not in p and 'iaq_response_id' not in p
    assert p['status'] == 'Completed'          # surveyor's status is kept


def test_linking_keeps_the_surveyors_status():
    # The binding rule: an upload or refresh never alters a real field
    # point's observation. The link is carried by has_iaq_survey / iaq_*.
    pin = _pin(status='Not Interested', color='#123456')
    assert _apply_iaq_to_field_features([pin], [_iaq('R_1', _north(5))]) == 1
    p = pin['properties']
    assert p['has_iaq_survey'] is True and p['iaq_response_id'] == 'R_1'
    assert p['status'] == 'Not Interested'
    assert p['color'] == '#123456'


def test_linking_a_pin_with_no_status_marks_it_completed():
    for status in ('', None, 'Unknown'):
        pin = _pin(status=status)
        assert _apply_iaq_to_field_features([pin], [_iaq('R_1', _north(5))]) == 1
        assert pin['properties']['status'] == 'Completed', status
        assert pin['properties']['has_iaq_survey'] is True
