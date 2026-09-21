"""The two export formats must yield the same answers after normalisation.

April is a TEXT export (cells hold the question's VariableNaming override) and
May is a NUMERIC one (cells hold recode codes). They are the same survey, and
for the responses present in both they are the same respondents — so once the
pipeline has resolved labels against the QSF, every shared response must carry
identical answers. Any disagreement means one of the two formats is being read
wrongly.

This is the regression guard for the label corruption found on 2026-09-20:
stale VariableNaming overrides made the text export show placeholder strings,
a reversed house-age scale, and other questions' labels.
"""
from __future__ import annotations

import pathlib
import sys
from collections import Counter

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'api'))
sys.path.insert(0, str(ROOT / 'scripts' / 'audit'))

from _processing import (  # noqa: E402
    _apply_qsf_display_labels, _apply_qsf_recode_labels, _read_qualtric_csv,
)
from survey_logic import qsf_labels, resolve_answer_label  # noqa: E402

APRIL = ROOT / 'data' / 'Keystone Heights Survey - V1_April 15, 2026_13.25.csv'
MAY = pathlib.Path('/Users/goshtasbshahriari/UF Dropbox/Goshtasb Shahriari Mehr/'
                   'DTSC_Lab/Keystone_Data/Keystone Heights Survey - V1_May 4, 2026_16.57.csv')

PLACEHOLDER = 'click to write'


def _load(path):
    raw, qmap = _read_qualtric_csv(path.read_bytes())
    mask = raw['Finished'].astype(str).str.strip().str.lower().isin(['true', '1'])
    df = raw[mask].reset_index(drop=True)
    _apply_qsf_display_labels(df, qmap)
    _apply_qsf_recode_labels(df, qmap)
    return df


@pytest.fixture(scope='module')
def april():
    if not APRIL.exists():
        pytest.skip('April export not present')
    return _load(APRIL)


@pytest.fixture(scope='module')
def may():
    if not MAY.exists():
        pytest.skip('May export not present')
    return _load(MAY)


def test_qsf_label_map_is_present_and_loaded():
    labels = qsf_labels()
    assert labels, 'api/qsf_labels.py missing — run scripts/build_qsf_label_map.py'
    assert 'QID141' in labels and 'QID192' in labels


@pytest.mark.parametrize('qid,exported,expected', [
    # The house-age scale is reversed by VariableNaming: the override text
    # 'Before 1960' is attached to choice 1, whose real label is '2000-now'.
    ('QID192', 'Before 1960', '2000-now'),
    ('QID192', 'Built 2000 or later', 'Before 1960'),
    # The safety scale exports as durations belonging to another question.
    ('QID21', 'Less than 6 months', 'Always feel safe'),
    ('QID194', 'Less than 6 months', 'Always feel safe'),
    # Placeholders resolve to the real choice.
    ('QID141', 'Click to write Choice 5',
     'Critical- Uninhabitable without repairs.'),
    ('QID181', 'Click to write Scale Point 3', 'Important'),
    # Numeric codes resolve too.
    ('QID192', '5', "I don't know"),
    ('QID21', '1', 'Always feel safe'),
])
def test_known_corruptions_resolve_to_the_real_answer(qid, exported, expected):
    assert resolve_answer_label(qid, exported) == expected


@pytest.mark.parametrize('qid,code,expected', [
    # QID141's RecodeValues send choice 5 to code 1, which choice 1 also uses.
    ('QID141', '1', 'Critical- Uninhabitable without repairs.'),
    # QID17 sends choices 3,4,5 to codes 1,2,3; choices 1,2 keep 1,2.
    ('QID17', '1', 'Moderately Urgent'),
    ('QID17', '2', 'Slightly Urgent'),
    ('QID17', '3', 'Not Urgent'),
    # QID100 sends choices 3,4 to codes 1,2.
    ('QID100', '1', 'Somewhat'),
    ('QID100', '2', 'Not Applicable'),
])
def test_colliding_codes_resolve_to_the_explicitly_recoded_choice(qid, code, expected):
    """A code claimed by two choices belongs to the one RecodeValues names.

    An explicit RecodeValues entry is a deliberate act by the survey author; a
    choice landing on a code only because unlisted choices recode to their own
    key is just Qualtrics' default. So the explicit claim wins.

    This is not a guess: for the 75 respondents in both the April (text) and May
    (numeric) exports the pairing is 1:1 with no counterexample — code 1 on
    QID141 is always "Click to write Choice 5" in the text export (11 rows),
    QID17 code 1 is always choice 3 (36 rows) and code 2 always choice 4 (25),
    QID100 code 1 always choice 3 (47) and code 2 always choice 4 (24).
    """
    assert resolve_answer_label(qid, code) == expected


def test_no_colliding_codes_remain_unresolved():
    """Every question's codes must now map to exactly one choice.

    If a new questionnaire edit introduces a collision this rule cannot settle,
    this fails rather than letting raw codes reach the dashboard.
    """
    stuck = {q: e['ambiguous_code'] for q, e in qsf_labels().items()
             if e.get('ambiguous_code')}
    assert not stuck, f'unresolvable recode collisions: {stuck}'


def test_unknown_values_are_still_refused_not_guessed():
    """The resolver only ever returns a real answer, never a nearest guess."""
    assert resolve_answer_label('QID141', 'no such answer') is None
    assert resolve_answer_label('QID141', '97') is None
    assert resolve_answer_label('QID_does_not_exist', '1') is None


def test_no_placeholder_text_survives_in_either_export(april, may):
    leaks = []
    for label, df in (('april', april), ('may', may)):
        for col in df.columns:
            vals = df[col].astype(str)
            n = int(vals.str.lower().str.contains(PLACEHOLDER, regex=False).sum())
            if n:
                leaks.append((label, str(col), n))
    assert not leaks, f'Qualtrics placeholder text still reaching users: {leaks}'


def test_condition_scale_is_not_inverted(april, may):
    """The worst answer must not be reported as the best one."""
    for label, df in (('april', april), ('may', may)):
        counts = Counter(df['QID141'].astype(str))
        critical = counts.get('Critical- Uninhabitable without repairs.', 0)
        excellent = counts.get('Excellent- No repairs needed.', 0)
        assert critical > 0, f'[{label}] no Critical responses — scale likely inverted'
        assert excellent == 0, (
            f'[{label}] {excellent} responses labelled Excellent; this survey has '
            f'none, and code 1 is Critical (see QID141_RECODE_LABELS)')


def test_shared_responses_agree_across_both_export_formats(april, may):
    a = {str(r): i for i, r in enumerate(april['ResponseId'].astype(str))}
    m = {str(r): i for i, r in enumerate(may['ResponseId'].astype(str))}
    shared = sorted(set(a) & set(m))
    assert len(shared) >= 50, f'only {len(shared)} shared responses'

    cols = [c for c in ('QID141', 'QID192', 'QID128', 'Ownership',
                        'Hospital Respiratory') if c in april.columns and c in may.columns]
    assert cols, 'none of the checked columns are present'

    diffs = []
    for rid in shared:
        ra, rm = april.iloc[a[rid]], may.iloc[m[rid]]
        for c in cols:
            va, vm = str(ra[c]).strip(), str(rm[c]).strip()
            if va.lower() in ('nan', '') and vm.lower() in ('nan', ''):
                continue
            if va != vm:
                diffs.append((rid, c, va, vm))

    detail = '\n'.join(f'  {r} {c}: april={a!r} may={b!r}' for r, c, a, b in diffs[:20])
    assert not diffs, (
        f'{len(diffs)} value(s) differ between the text and numeric exports for the '
        f'same respondent:\n{detail}')
