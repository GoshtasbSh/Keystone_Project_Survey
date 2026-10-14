"""IAQ upload: safety guard counts superseded responses as still stored, and
the public path never ships them."""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'api'))

from api.upload import _all_iaq_features, evaluate_iaq_upload_safety  # noqa: E402
from _lib import strip_survey_answers  # noqa: E402

PT = [-82.0190051597457, 29.7838438366905]


def _iaq(rid, coords=PT, matched=False, risk=17):
    return {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': list(coords)},
            'properties': {'response_id': rid, 'iaq_matched': matched,
                           'match_status': 'matched' if matched else 'iaq_only',
                           'overall_risk': risk, 'risk_tier': 'Low', 'health_score': 1,
                           'iaq_score': 2, 'struct_score': 3, 'street_name': 'Beloit Ave',
                           'house_number': '6409'}}


def test_superseded_responses_count_as_stored_for_the_safety_guard():
    stored = {'features': [_iaq('R_old'), _iaq('R_new')]}
    incoming = {'features': [_iaq('R_new')], 'superseded_features': [_iaq('R_old')]}
    res = evaluate_iaq_upload_safety(_all_iaq_features(stored),
                                     _all_iaq_features(incoming), {}, 'oct.csv', False)
    assert res['allowed'] is True and res['diff']['dropped'] == []


def test_public_strip_drops_superseded_responses_and_house_numbers():
    gj = {'type': 'FeatureCollection', 'features': [_iaq('R_new')],
          'superseded_features': [_iaq('R_old')]}
    out = strip_survey_answers(gj)
    assert 'superseded_features' not in out
    assert 'house_number' not in out['features'][0]['properties']
    assert 'superseded_features' in gj                 # input not mutated
