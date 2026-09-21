"""The production extractor must agree, cell for cell, with an independent read.

`scripts/audit/qualtrics_ground_truth.py` parses the Qualtrics CSV without
importing any of the code under test, so agreement between the two is real
evidence that values come from the columns they are supposed to come from.

Compared raw-to-raw: recode translation happens downstream of extraction, so a
numeric export's '6' is the correct extracted value here and 'Like' would be
wrong.
"""
from __future__ import annotations

import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'api'))
sys.path.insert(0, str(ROOT / 'scripts' / 'audit'))

from _processing import (  # noqa: E402
    SURVEY_QUESTIONS, _extract_survey_extras, _read_qualtric_csv,
)
from qualtrics_ground_truth import load_survey, value_by_qid  # noqa: E402

APRIL = ROOT / 'data' / 'Keystone Heights Survey - V1_April 15, 2026_13.25.csv'
MAY = pathlib.Path('/Users/goshtasbshahriari/UF Dropbox/Goshtasb Shahriari Mehr/'
                   'DTSC_Lab/Keystone_Data/Keystone Heights Survey - V1_May 4, 2026_16.57.csv')
N_POINTS = 10


def _finished(raw):
    mask = raw['Finished'].astype(str).str.strip().str.lower().isin(['true', '1'])
    return raw[mask].reset_index(drop=True)


def _same_value(got: str, expected: str) -> bool:
    """Equal as a value, ignoring pandas' float rendering of integer codes.

    This test's job is to prove the extractor reads the RIGHT COLUMN. A numeric
    export's code 6 arriving as '6.0' is the same answer from the same cell —
    that representation issue is asserted separately below, so it is not
    conflated with a wrong-column read here.
    """
    if got == expected:
        return True
    try:
        return float(got) == float(expected)
    except (TypeError, ValueError):
        return False


@pytest.mark.parametrize('csv_path,label', [(APRIL, 'april'), (MAY, 'may')])
def test_extractor_matches_independent_reader(csv_path, label):
    if not csv_path.exists():
        pytest.skip(f'export not present: {csv_path}')

    truth = load_survey(csv_path)
    raw, qmap = _read_qualtric_csv(csv_path.read_bytes())
    finished = _finished(raw)
    assert len(finished) >= N_POINTS, f'only {len(finished)} completed responses'

    truth_by_rid = {r['ResponseId']: r for r in truth['rows']}
    diffs = []
    checked = 0

    for i in range(N_POINTS):
        row = finished.iloc[i]
        rid = str(row['ResponseId']).strip()
        t_row = truth_by_rid.get(rid)
        assert t_row is not None, f'{rid} missing from the independent reader'

        extracted = _extract_survey_extras(row, qmap, df_columns=finished.columns)
        for field, meta in SURVEY_QUESTIONS.items():
            if len(meta) != 3:
                continue
            _idx, qid, _text = meta
            expected, col = value_by_qid(truth, t_row, qid)
            if col is None:
                continue  # QID absent from this export — covered by the label test
            got = str(extracted.get(field, '') or '').strip()
            checked += 1
            if not _same_value(got, expected.strip()):
                diffs.append((rid, field, qid, col, expected, got))

    detail = '\n'.join(
        f'  {r} {f} ({q}) csv_col={c}: csv={e!r} extracted={g!r}'
        for r, f, q, c, e, g in diffs)
    assert not diffs, (
        f'[{label}] {len(diffs)} of {checked} extracted values disagree with the '
        f'independent reader:\n{detail}')


@pytest.mark.parametrize('csv_path,label', [(APRIL, 'april'), (MAY, 'may')])
def test_no_field_falls_back_to_a_hardcoded_column_index(csv_path, label):
    """Every field must resolve by QID, not by the positional fallback.

    `_extract_survey_extras` falls back to a hardcoded column index when a QID
    cannot be resolved (api/_processing.py:882-886). That fallback is only
    correct while the export keeps its historical column order, so any field
    relying on it is a silent wrong-column read waiting to happen.
    """
    if not csv_path.exists():
        pytest.skip(f'export not present: {csv_path}')
    raw, qmap = _read_qualtric_csv(csv_path.read_bytes())
    finished = _finished(raw)
    miss: list = []
    _extract_survey_extras(finished.iloc[0], qmap,
                           df_columns=finished.columns, miss_log=miss)
    assert not miss, (
        f'[{label}] these QIDs did not resolve and fell back to a hardcoded '
        f'column index: {sorted(set(miss))}')


@pytest.mark.parametrize('csv_path,label', [(APRIL, 'april'), (MAY, 'may')])
def test_numeric_codes_are_not_extracted_as_floats(csv_path, label):
    """A recode code must not reach the feature as '6.0'.

    pandas reads a numeric-recode column as float64, so `str(v)` in
    `_val_at_orig_idx` (api/_processing.py:798) yields '6.0'. Recode lookup
    tolerates that (`_normalize_qualtrics_recode_key`), but any question with no
    label table keeps the raw string and the dashboard then shows '6.0' as the
    respondent's answer.
    """
    if not csv_path.exists():
        pytest.skip(f'export not present: {csv_path}')
    raw, qmap = _read_qualtric_csv(csv_path.read_bytes())
    finished = _finished(raw)
    floaty = []
    for i in range(N_POINTS):
        extracted = _extract_survey_extras(finished.iloc[i], qmap,
                                           df_columns=finished.columns)
        for field, value in extracted.items():
            # years_in_hre_num is a derived float for histogram binning, not a
            # displayed answer — a float is correct there.
            if field == 'years_in_hre_num':
                continue
            s = str(value or '').strip()
            if s.endswith('.0') and s[:-2].isdigit():
                floaty.append((field, s))
    assert not floaty, (
        f'[{label}] {len(floaty)} value(s) extracted as a float string instead of '
        f'an integer code, e.g. {sorted(set(floaty))[:8]}')
