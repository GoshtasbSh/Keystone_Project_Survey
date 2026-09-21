"""What an upload puts in front of a user must be the survey's own text.

Simulates the label half of `process_iaq_bytes` end to end, for BOTH export
formats, and asserts that every value the popup can show is a real answer:

  * no Qualtrics placeholder strings ("Click to write Choice 5")
  * no literal 'nan'
  * no bare recode codes ('6', '6.0') where the survey has a label
  * no invented wording — every question label is verbatim survey text
  * the two formats produce the SAME answers for the same respondent

Run before any upload. If this passes for a new export, the popup will show
the respondent's real answers for every question it covers.
"""
from __future__ import annotations

import pathlib
import re
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'api'))
sys.path.insert(0, str(ROOT / 'scripts' / 'audit'))

from _processing import (  # noqa: E402
    IAQ_FEATURE_POPUP_LABELS, SURVEY_QUESTIONS, _apply_qsf_display_labels,
    _apply_qsf_recode_labels, _cell, _extract_survey_extras, _read_qualtric_csv,
)
from qualtrics_ground_truth import load_survey  # noqa: E402

APRIL = ROOT / 'data' / 'Keystone Heights Survey - V1_April 15, 2026_13.25.csv'
MAY = pathlib.Path('/Users/goshtasbshahriari/UF Dropbox/Goshtasb Shahriari Mehr/'
                   'DTSC_Lab/Keystone_Data/Keystone Heights Survey - V1_May 4, 2026_16.57.csv')

PLACEHOLDER = re.compile(r'click to write', re.I)
BARE_CODE = re.compile(r'^\d+(\.0)?$')

# Raw IAQ fields, and the CSV column each is read from
# (api/_processing.py:2179-2200).
RAW_FIELDS = {
    'housing_type': 'QID128', 'year_built': 'QID192', 'condition': 'QID141',
    'respiratory_ill': 'RespIll', 'asthma_freq': 'asthma', 'wheeze_freq': 'wheeze',
    'headache_freq': 'Headache', 'tired_freq': 'Tired',
    'leakage_roof': 'Leakage 2_1', 'leakage_walls': 'Leakage 2_2',
    'leakage_windows': 'Leakage 2_3', 'leakage_floor': 'Leakage 2_4',
    'cooling_central_ac': 'Cooling System _1', 'cooling_window_unit': 'Cooling System _2',
    'cooling_fan': 'Cooling System _3', 'cooling_none': 'Cooling System _4',
    'cooking_method': 'Cooking',
}

# Questions whose recode values collide in this survey. The collision is now
# resolved in favour of the choice RecodeValues explicitly names (see
# tests/test_qsf_label_resolution.py), so NOTHING is exempt any more: a numeric
# export must decode as cleanly as a text one. Kept as an empty set so the
# guard test below still pins the scope and fails if a new one appears.
AMBIGUOUS_IN_NUMERIC: set[str] = set()

# Free-text numeric answers: a number IS the answer.
NUMERIC_ANSWERS = {'years_in_hre', 'years_in_hre_num'}


def _popup_values(path: pathlib.Path) -> list[dict]:
    """Every field the popup can render, for every completed response."""
    raw, qmap = _read_qualtric_csv(path.read_bytes())
    mask = raw['Finished'].astype(str).str.strip().str.lower().isin(['true', '1'])
    df = raw[mask].reset_index(drop=True)

    _apply_qsf_display_labels(df, qmap)      # QSF pass first
    _apply_qsf_recode_labels(df, qmap)       # then the fallback tables

    out = []
    for i in range(len(df)):
        row = df.iloc[i]
        nr = {str(k).replace('\xa0', ' ').strip(): v for k, v in row.items()}
        props = dict(_extract_survey_extras(row, qmap, df_columns=df.columns))
        for field, col in RAW_FIELDS.items():
            props[field] = _cell(nr, col)
        props['response_id'] = _cell(nr, 'ResponseId')
        out.append(props)
    return out


@pytest.fixture(scope='module')
def april():
    if not APRIL.exists():
        pytest.skip('April export not present')
    return _popup_values(APRIL)


@pytest.fixture(scope='module')
def may():
    if not MAY.exists():
        pytest.skip('May export not present')
    return _popup_values(MAY)


@pytest.mark.parametrize('fmt', ['april', 'may'])
def test_no_placeholder_text_reaches_the_popup(fmt, request):
    rows = request.getfixturevalue(fmt)
    bad = [(r.get('response_id'), f, v) for r in rows for f, v in r.items()
           if isinstance(v, str) and PLACEHOLDER.search(v)]
    assert not bad, f'[{fmt}] placeholder text would be shown: {bad[:10]}'


@pytest.mark.parametrize('fmt', ['april', 'may'])
def test_no_literal_nan_reaches_the_popup(fmt, request):
    rows = request.getfixturevalue(fmt)
    bad = [(r.get('response_id'), f) for r in rows for f, v in r.items()
           if isinstance(v, str) and v.strip().lower() == 'nan']
    assert not bad, f'[{fmt}] {len(bad)} cell(s) would read "nan": {bad[:10]}'


@pytest.mark.parametrize('fmt', ['april', 'may'])
def test_no_bare_recode_codes_reach_the_popup(fmt, request):
    rows = request.getfixturevalue(fmt)
    skip = NUMERIC_ANSWERS | (AMBIGUOUS_IN_NUMERIC if fmt == 'may' else set())
    bad = [(r.get('response_id'), f, v) for r in rows for f, v in r.items()
           if f not in skip and isinstance(v, str) and BARE_CODE.match(v.strip())]
    assert not bad, (
        f'[{fmt}] {len(bad)} cell(s) would show a raw code instead of an '
        f'answer: {bad[:10]}')


def test_ambiguous_questions_are_known_and_only_affect_numeric_exports(may, april):
    """No question may fall back to showing a raw recode code, in either format.

    QID17, QID100 and QID141 all have colliding RecodeValues; all three are now
    resolved from the survey definition, so a numeric export shows real answers
    everywhere a text export does. If a questionnaire edit introduces a
    collision that cannot be resolved, this fails.
    """
    numeric_bare = {f for r in may for f, v in r.items()
                    if isinstance(v, str) and BARE_CODE.match(v.strip())
                    and f not in NUMERIC_ANSWERS}
    assert numeric_bare <= AMBIGUOUS_IN_NUMERIC, (
        f'new undecodable question(s) in the numeric export: '
        f'{numeric_bare - AMBIGUOUS_IN_NUMERIC}')
    # The same questions resolve cleanly in the text export.
    text_bare = {f for r in april for f, v in r.items()
                 if isinstance(v, str) and BARE_CODE.match(v.strip())
                 and f not in NUMERIC_ANSWERS}
    assert not (text_bare & AMBIGUOUS_IN_NUMERIC), (
        f'text export should resolve these: {text_bare & AMBIGUOUS_IN_NUMERIC}')


def test_every_popup_label_is_verbatim_survey_text():
    """No invented wording: each label must appear in the export as written."""
    if not APRIL.exists():
        pytest.skip('April export not present')
    survey = load_survey(APRIL)
    haystack = '\u0001'.join(survey['question_text'])
    labels = [m[2] for m in SURVEY_QUESTIONS.values() if len(m) == 3]
    labels += list(IAQ_FEATURE_POPUP_LABELS.values())
    missing = [L for L in labels if L not in haystack]
    assert not missing, (
        f'{len(missing)} of {len(labels)} popup labels are not verbatim survey '
        f'text: {[m[:70] for m in missing]}')


def test_both_formats_show_the_same_answer_for_the_same_respondent(april, may):
    a = {r['response_id']: r for r in april if r.get('response_id')}
    m = {r['response_id']: r for r in may if r.get('response_id')}
    shared = sorted(set(a) & set(m))
    assert len(shared) >= 50, f'only {len(shared)} shared responses'

    diffs = []
    for rid in shared:
        for f in sorted(set(a[rid]) & set(m[rid])):
            if f in NUMERIC_ANSWERS or f in AMBIGUOUS_IN_NUMERIC:
                continue
            va, vm = str(a[rid][f] or '').strip(), str(m[rid][f] or '').strip()
            if va.lower() in ('', 'none') and vm.lower() in ('', 'none'):
                continue
            if va != vm:
                diffs.append((rid, f, va[:40], vm[:40]))
    detail = '\n'.join(f'  {r} {f}: text={x!r} numeric={y!r}' for r, f, x, y in diffs[:15])
    assert not diffs, (
        f'{len(diffs)} field(s) differ between the text and numeric exports for '
        f'the same respondent:\n{detail}')
