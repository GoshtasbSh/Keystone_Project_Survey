"""One per-question switch decides what a shared numeric code means.

QID141, QID17, QID100 and QID221 have RecodeValues that put two choices on
the same exported code. survey_logic.SHARED_CODE_RESOLUTION holds, per
question, which of the two the code (and the recoded choice's own text-export
answer) is shown as. Changing that dict must be the ONLY change needed to
relabel every affected answer.

It ships with the PI's decision of 2026-10-13 (ledger "USER DECISION"):
  QID141 condition       code 1 -> "Excellent- No repairs needed." (never Critical)
  QID100 / QID221        code 1 -> "Yes", code 2 -> "No / Not applicable"
  QID17  afford_urgency  unchanged: 1 Moderately, 2 Slightly, 3 Not Urgent
"""
from __future__ import annotations

import pathlib
import sys

import pandas as pd
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'api'))

import survey_logic  # noqa: E402
from _processing import (  # noqa: E402
    _apply_qsf_display_labels, _compute_iaq_analysis,
)
from survey_logic import (  # noqa: E402
    SHARED_CODES, compute_struct_score, resolve_answer_label,
    shared_code_choice_key, shared_code_status,
)


DECIDED_RESOLUTION = {'QID141': 'original_choice', 'QID17': 'recoded_choice',
                      'QID100': 'original_choice', 'QID221': 'original_choice'}

DECIDED = {
    ('QID141', '1'): 'Excellent- No repairs needed.',
    ('QID17', '1'): 'Moderately Urgent', ('QID17', '2'): 'Slightly Urgent',
    ('QID100', '1'): 'Yes', ('QID100', '2'): 'No / Not applicable',
    ('QID221', '1'): 'Yes', ('QID221', '2'): 'No / Not applicable',
}
# Every question on 'recoded_choice' — the labels shown before 2026-10-13.
RECODED = {
    ('QID141', '1'): 'Critical- Uninhabitable without repairs.',
    ('QID17', '1'): 'Moderately Urgent', ('QID17', '2'): 'Slightly Urgent',
    ('QID100', '1'): 'Somewhat', ('QID100', '2'): 'Not Applicable',
    ('QID221', '1'): 'Somewhat', ('QID221', '2'): 'Not Applicable',
}
# Every question on 'original_choice'.
ORIGINAL = {
    ('QID141', '1'): 'Excellent- No repairs needed.',
    ('QID17', '1'): 'Very Urgent', ('QID17', '2'): 'Urgent',
    ('QID100', '1'): 'Yes', ('QID100', '2'): 'No / Not applicable',
    ('QID221', '1'): 'Yes', ('QID221', '2'): 'No / Not applicable',
}


def _all_modes(monkeypatch, mode):
    monkeypatch.setattr(survey_logic, 'SHARED_CODE_RESOLUTION',
                        {q: mode for q in SHARED_CODES})


def _all_props(geo):
    """Drawn plus superseded features (GAP-10), for per-respondent lookups."""
    return {f['properties']['response_id']: f['properties']
            for f in geo['features'] + geo.get('superseded_features', [])}


def test_ships_with_the_decided_labels():
    assert survey_logic.SHARED_CODE_RESOLUTION == DECIDED_RESOLUTION
    for (qid, code), label in DECIDED.items():
        assert resolve_answer_label(qid, code) == label, (qid, code)
        assert resolve_answer_label(qid, float(code)) == label   # '1.0' too


@pytest.mark.parametrize('mode,expected', [('recoded_choice', RECODED),
                                           ('original_choice', ORIGINAL)])
def test_the_switch_relabels_every_shared_code(monkeypatch, mode, expected):
    _all_modes(monkeypatch, mode)
    for (qid, code), label in expected.items():
        assert resolve_answer_label(qid, code) == label, (qid, code)


def test_the_switch_is_per_question(monkeypatch):
    monkeypatch.setattr(survey_logic, 'SHARED_CODE_RESOLUTION',
                        {**DECIDED_RESOLUTION, 'QID17': 'original_choice'})
    assert resolve_answer_label('QID17', '1') == 'Very Urgent'
    assert resolve_answer_label('QID141', '1') == 'Excellent- No repairs needed.'
    assert resolve_answer_label('QID100', '1') == 'Yes'


def test_an_unknown_mode_is_refused(monkeypatch):
    monkeypatch.setattr(survey_logic, 'SHARED_CODE_RESOLUTION',
                        {**DECIDED_RESOLUTION, 'QID141': 'guess'})
    with pytest.raises(ValueError):
        resolve_answer_label('QID141', '1')


@pytest.mark.parametrize('mode', ['recoded_choice', 'original_choice'])
def test_unshared_codes_and_unshared_text_answers_do_not_move(monkeypatch, mode):
    _all_modes(monkeypatch, mode)
    assert resolve_answer_label('QID17', '3') == 'Not Urgent'
    assert resolve_answer_label('QID141', '4') == 'Poor- Major repairs needed.'
    assert resolve_answer_label('QID141', 'Excellent- No repairs needed.') == \
        'Excellent- No repairs needed.'
    assert resolve_answer_label('QID100', 'Yes') == 'Yes'
    assert resolve_answer_label('QID17', 'Very Urgent') == 'Very Urgent'
    assert shared_code_choice_key('QID192', '1') is None


def test_text_export_answers_follow_the_same_switch(monkeypatch):
    """The text export names the recoded choice ('Click to write Choice 5');
    it must read the same as the numeric code, or the two export formats
    disagree for the same respondent."""
    assert resolve_answer_label('QID141', 'Click to write Choice 5') == \
        'Excellent- No repairs needed.'
    assert resolve_answer_label('QID100', 'Click to write Choice 3') == 'Yes'
    assert resolve_answer_label('QID221', 'Click to write Choice 4') == 'No / Not applicable'
    assert resolve_answer_label('QID17', 'Click to write Choice 3') == 'Moderately Urgent'
    _all_modes(monkeypatch, 'recoded_choice')
    assert resolve_answer_label('QID141', 'Click to write Choice 5') == \
        'Critical- Uninhabitable without repairs.'
    assert resolve_answer_label('QID100', 'Click to write Choice 3') == 'Somewhat'


def test_shared_code_table_matches_the_generated_label_map():
    labels = survey_logic.qsf_labels()
    for qid, codes in SHARED_CODES.items():
        for code, (recoded, original) in codes.items():
            assert labels[qid]['code_to_key'][code] == [recoded]
            assert original in labels[qid]['display']


def test_the_switch_reaches_the_dataframe_and_the_scores():
    df = pd.DataFrame({'QID141': ['1', '4'], 'QID17': ['1', '3'], 'QID100': ['1', '2']})
    _apply_qsf_display_labels(df, {'QID141': 0, 'QID17': 1, 'QID100': 2})
    assert df['QID141'].tolist() == ['Excellent- No repairs needed.',
                                     'Poor- Major repairs needed.']
    assert df['QID17'].tolist() == ['Moderately Urgent', 'Not Urgent']
    assert df['QID100'].tolist() == ['Yes', 'No / Not applicable']
    assert compute_struct_score({'QID141': df['QID141'][0]}) == 0
    feats = [{'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [0, 0]},
              'properties': {'overall_risk': 0, 'health_score': 0, 'iaq_score': 0,
                             'struct_score': 0, 'condition': c}}
             for c in df['QID141']]
    assert _compute_iaq_analysis(feats)['housing']['conditions'] == {'Excellent': 1, 'Poor': 1}


def test_status_reports_every_question_resolved():
    assert shared_code_status() == {
        'resolution': DECIDED_RESOLUTION,
        'questions': ['QID100', 'QID141', 'QID17', 'QID221'],
        'fields': ['condition', 'afford_urgency', 'mh_skirting'],
        'verified': True}


@pytest.fixture(scope='module')
def october(october_iaq_copy):
    geo, a, *_ = october_iaq_copy
    return _all_props(geo), a


def test_october_code_1_condition_is_rescored_as_excellent(october):
    props, _a = october
    p = props['R_5241irqeSjBwQi1']                  # QID141 exported as code 1
    assert p['condition'] == 'Excellent- No repairs needed.'
    assert p['struct_score'] == 45                  # was 80 (+35 for "Critical")
    assert p['overall_risk'] == 25                  # was 35
    assert p['risk_tier'] == 'Low'                  # was Medium
    assert not any('critical' in str(q.get('condition', '')).lower()
                   for q in props.values())


def test_october_analysis_reports_the_labels_resolved(october):
    props, a = october
    assert a['shared_code_labels'] == shared_code_status()
    assert a['shared_code_labels']['verified'] is True
    assert 'Critical' not in a['housing']['conditions']
    assert a['housing']['conditions']['Excellent'] > 0
    assert set(a['residency']['mh_skirting']) <= {'Yes', 'No / Not applicable'}
