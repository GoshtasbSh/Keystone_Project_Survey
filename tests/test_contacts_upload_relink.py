"""A contacts upload re-links the new contacts to the stored (kept) IAQ
responses, the same way process_iaq_bytes does, so matched contacts and the
matched/contact_only counts survive until the next IAQ upload (ledger U9a).
The stored responses have no raw_address (PII is stripped before saving), so
the link uses their stored house_number and parcel point."""
from __future__ import annotations

import copy
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'api'))

from _processing import relink_contacts_to_stored_iaq, tag_contact_match_status  # noqa: E402

PT = [-82.017276, 29.783271]


def _contact(addr, coords=PT, status='Completed', detail='Completed survey'):
    return {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': list(coords)},
            'properties': {'address': addr, 'status': status, 'status_detail': detail}}


def _stored(rid, house, coords=PT):
    return {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': list(coords)},
            'properties': {'response_id': rid, 'house_number': house, 'overall_risk': 40,
                           'risk_tier': 'Medium', 'health_score': 1, 'iaq_score': 2,
                           'struct_score': 3, 'iaq_matched': True, 'match_status': 'matched'}}


def test_stored_response_relinks_the_fresh_contact():
    contacts = [_contact('6386 Baylor Ave'), _contact('6390 Bucknell Ave', [-82.02, 29.78])]
    stored = [_stored('R_j1xG', '6386')]
    before = copy.deepcopy(stored)
    assert relink_contacts_to_stored_iaq(contacts, stored) == 1
    p = contacts[0]['properties']
    assert p['has_iaq_survey'] is True and p['iaq_response_id'] == 'R_j1xG'
    assert (p['iaq_match_lon'], p['iaq_match_lat']) == tuple(PT)
    assert 'has_iaq_survey' not in contacts[1]['properties']
    assert stored == before, 'the stored IAQ blob must not be mutated'
    assert tag_contact_match_status(contacts) == {'matched': 1, 'contact_only': 1}


def test_different_house_number_on_the_same_point_is_not_linked():
    contacts = [_contact('6376 Antioch Ave')]
    assert relink_contacts_to_stored_iaq(contacts, [_stored('R_6378', '6378')]) == 0
    assert 'has_iaq_survey' not in contacts[0]['properties']


def test_nothing_stored_is_a_no_op():
    contacts = [_contact('6386 Baylor Ave')]
    assert relink_contacts_to_stored_iaq(contacts, []) == 0
    assert relink_contacts_to_stored_iaq([], [_stored('R', '6386')]) == 0
