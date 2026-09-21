"""Every popup question label must be the survey's own wording, verbatim.

The point of showing the question in the popup is that a collaborator can
copy it and find it in the Qualtrics CSV/Excel with Find. A paraphrase or a
truncated string never matches, so "close enough" is a failure here.

Row 1 of the Qualtrics export is the question-text row. Unlike the answer
cells (which the export fills from the survey's VariableNaming overrides and
which are therefore unreliable — see audit finding F9), row 1 is the real
question wording, so it is the correct source for these labels.
"""
from __future__ import annotations

import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'api'))
sys.path.insert(0, str(ROOT / 'scripts' / 'audit'))

from _processing import SURVEY_QUESTIONS  # noqa: E402
from qualtrics_ground_truth import load_survey  # noqa: E402

CSV = ROOT / 'data' / 'Keystone Heights Survey - V1_April 15, 2026_13.25.csv'


@pytest.fixture(scope='module')
def survey():
    if not CSV.exists():
        pytest.skip(f'survey export not present: {CSV}')
    return load_survey(CSV)


def _column_for(survey, qid):
    idx = survey['qid_to_idx'].get(qid)
    if idx is None:
        base = qid[:-5] if qid.endswith('_TEXT') else qid
        idx = survey['qid_to_idx'].get(base)
    return idx


def test_every_survey_question_label_is_verbatim_csv_text(survey):
    mismatches = []
    absent = []
    for field, meta in SURVEY_QUESTIONS.items():
        if len(meta) != 3:
            continue
        _idx, qid, canonical = meta
        col = _column_for(survey, qid)
        if col is None:
            absent.append((field, qid))
            continue
        actual = survey['question_text'][col].strip()
        if canonical.strip() != actual:
            mismatches.append((field, qid, canonical.strip(), actual))

    detail = '\n'.join(
        f'  {f} ({q})\n    code: {c!r}\n    csv:  {a!r}' for f, q, c, a in mismatches)
    assert not mismatches, (
        f'{len(mismatches)} label(s) are not verbatim survey text '
        f'(so they cannot be found with Excel Find):\n{detail}')
    # Reported separately: a QID genuinely absent from this export is a data
    # question, not a label bug, and must not be silently folded into the above.
    assert not absent, f'QIDs not present in this export: {absent}'
