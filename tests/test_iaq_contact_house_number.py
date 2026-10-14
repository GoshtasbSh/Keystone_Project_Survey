"""Tier-3 (same parcel point) IAQ<->contact links must have the same house
number, and an upload must be able to remove a link an older upload made.

6306 Amherst Ave showed R_36hwtQ5ZQOhBucE, who typed 6318 Amherst; 6376
Antioch showed R_mT2CaA2cdWYOmij, who typed 6378 Antioch. Both were linked
only because the response landed on the contact's parcel point.
"""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'api'))

from _processing import _house_number, _match_iaq_to_contacts  # noqa: E402

PT = [-82.014265, 29.790102]


def _contact(addr, coords=PT, **props):
    return {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': list(coords)},
            'properties': {'address': addr, 'status': props.pop('status', 'No Answer'),
                           **props}}


def _iaq(rid, raw, coords=PT):
    return {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': list(coords)},
            'properties': {'response_id': rid, 'raw_address': raw, 'iaq_matched': False,
                           'overall_risk': 46, 'risk_tier': 'Medium',
                           'health_score': 1, 'iaq_score': 2, 'struct_score': 3}}


def test_house_number_is_normalised():
    assert _house_number('06318 Amherst Ave') == '6318'
    assert _house_number('6386 Baylor') == '6386'
    assert _house_number('First house right bowdoin') == ''
    assert _house_number('') == ''


def test_same_point_different_house_number_is_not_linked():
    contacts = [_contact('6306 Amherst Ave')]
    iaq = [_iaq('R_36hwtQ5ZQOhBucE', '6318 Amherst Ave Keystone Heights, Fl. 32656')]
    assert _match_iaq_to_contacts(iaq, contacts) == {}
    p = iaq[0]['properties']
    assert p['match_review'] == 'house_number_mismatch'
    assert '6318' in p['match_review_note'] and '6306' in p['match_review_note']


def test_same_point_same_house_number_still_links_by_tier_3():
    """Street text too different for tier 2, same house number: tier 3 links."""
    contacts = [_contact('6390 Old County Road')]
    iaq = [_iaq('R_1', '6390 Zzyzx')]
    assert _match_iaq_to_contacts(iaq, contacts) == {0: 0}
    assert 'match_review' not in iaq[0]['properties']


def test_contact_without_a_house_number_is_not_linked_by_coordinates():
    contacts = [_contact('Lot behind the church')]
    iaq = [_iaq('R_1', '6390 Bucknell Ave')]
    assert _match_iaq_to_contacts(iaq, contacts) == {}
    assert iaq[0]['properties']['match_review'] == 'house_number_mismatch'


from _processing import (  # noqa: E402
    STATUS, _reset_contact_iaq_links, _upgrade_contacts_from_iaq,
)


def test_reset_restores_the_canvass_status_and_drops_the_old_link():
    c = _contact('6376 Antioch', status='Completed',
                 status_detail='Come back after 4:00 pm; works nights ',
                 color=STATUS['Completed'], has_iaq_survey=True,
                 iaq_response_id='R_mT2CaA2cdWYOmij', iaq_overall_risk=37,
                 iaq_risk_tier='Medium', iaq_health_score=0, iaq_iaq_score=64,
                 iaq_struct_score=50, iaq_match_lon=-82.016571, iaq_match_lat=29.789677)
    untouched = _contact('6300 Amherst Ave', status='Left Info', status_detail='left flier')
    field = {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': PT},
             'properties': {'source': 'field', 'field_point_id': 'x', 'status': 'Completed',
                            'has_iaq_survey': True, 'iaq_response_id': 'R_9'}}
    n = _reset_contact_iaq_links([c, untouched, field])
    assert n == 1
    p = c['properties']
    assert p['status'] == 'Follow Up' and p['color'] == STATUS['Follow Up']
    for k in ('has_iaq_survey', 'iaq_response_id', 'iaq_overall_risk', 'iaq_match_lon'):
        assert k not in p
    assert untouched['properties']['status'] == 'Left Info'
    assert field['properties']['iaq_response_id'] == 'R_9'   # field pins untouched


def test_reset_then_rematch_gives_the_same_completed_contact():
    c = _contact('6390 Bucknell Ave', status='Completed', status_detail='Completed survey',
                 has_iaq_survey=True, iaq_response_id='R_old')
    iaq = [_iaq('R_new', '6390 Bucknell Ave')]
    _reset_contact_iaq_links([c])
    m = _match_iaq_to_contacts(iaq, [c])
    assert _upgrade_contacts_from_iaq([c], iaq, m) == 1
    assert c['properties']['status'] == 'Completed'
    assert c['properties']['iaq_response_id'] == 'R_new'
    assert iaq[0]['properties']['iaq_matched'] is True
