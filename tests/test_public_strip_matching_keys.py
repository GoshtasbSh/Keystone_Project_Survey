"""Keys added by MATCH-1/3 must not reach anonymous /api/iaq-points
(strip_survey_answers is a blacklist)."""
from api._lib import SURVEY_ANSWER_FIELDS, strip_survey_answers

KEYS = ('house_number', 'recorded_date', 'match_review', 'match_review_note',
        'household_responses', 'superseded_response_ids')


def test_matching_internals_are_members_only():
    missing = [k for k in KEYS if k not in SURVEY_ANSWER_FIELDS]
    assert missing == []


def test_public_feature_keeps_only_map_keys():
    fc = {'type': 'FeatureCollection', 'features': [{'type': 'Feature', 'geometry': None,
          'properties': {**{k: 'x' for k in KEYS}, 'overall_risk': 3, 'response_id': 'R_a'}}]}
    assert strip_survey_answers(fc)['features'][0]['properties'] == {'overall_risk': 3, 'response_id': 'R_a'}
