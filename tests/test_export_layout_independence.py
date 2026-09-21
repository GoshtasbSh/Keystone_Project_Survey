"""The analysis must not depend on where Qualtrics puts the columns.

Qualtrics reorders columns between exports, and adds and removes them as the
questionnaire is edited. Every analysis input is located by the question's
Qualtrics ImportId, so a permuted export must produce byte-identical results.

This is the regression guard for the 2026-09-21 finding: a matrix's "Other"
free-text column (ImportId ``QID181_8_TEXT``) also claimed the bare
``QID181_8``, and both claims were registered with ``setdefault`` in one pass —
so the winner was whichever column came FIRST in the file. In the real exports
the matrix column happens to precede the text column, so the correct one won by
luck of ordering. Permuting the columns made the relocation-factors "Other"
chart report free text ("Kids school") instead of the importance rating.
"""
from __future__ import annotations

import csv
import io
import json
import pathlib
import random
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'api'))

from _processing import (  # noqa: E402
    _build_colname_qid_map, _read_qualtric_csv, load_parcel_index,
    process_iaq_bytes,
)

MAY = pathlib.Path('/Users/goshtasbshahriari/UF Dropbox/Goshtasb Shahriari Mehr/'
                   'DTSC_Lab/Keystone_Data/Keystone Heights Survey - V1_May 4, 2026_16.57.csv')


def _rows():
    if not MAY.exists():
        pytest.skip('May export not present')
    return list(csv.reader(MAY.open(encoding='utf-8-sig')))


def _to_bytes(rows):
    buf = io.StringIO()
    csv.writer(buf, lineterminator='\n').writerows(rows)
    return buf.getvalue().encode('utf-8')


def _signature(analysis: dict) -> str:
    return json.dumps({k: v for k, v in analysis.items()
                       if not k.startswith('_') and k != 'validation'},
                      sort_keys=True, default=str)


# ── the precedence rule itself, without touching a file ──────────────────────

def test_an_exact_qid_beats_a_text_stripped_alias_either_order():
    """The column literally named QID181_8 wins, whichever order they appear in."""
    forward = _build_colname_qid_map(['QID181_8', 'QID181_8_TEXT'])
    reverse = _build_colname_qid_map(['QID181_8_TEXT', 'QID181_8'])
    assert forward['QID181_8'] == 0
    assert reverse['QID181_8'] == 1, (
        'the _TEXT column shadowed the real QID181_8 column when it came first')
    # the _TEXT column keeps its own exact key in both orders
    assert forward['QID181_8_TEXT'] == 1
    assert reverse['QID181_8_TEXT'] == 0


def test_a_text_alias_still_resolves_when_no_exact_column_exists():
    """QID12 is declared as QID12_TEXT; an export carrying only one of the two
    forms must still resolve. The alias exists for exactly this case."""
    m = _build_colname_qid_map(['QID12_TEXT'])
    assert m['QID12_TEXT'] == 0
    assert m['QID12'] == 0


def test_import_id_map_gives_the_matrix_column_not_its_other_text_box():
    raw, qmap = _read_qualtric_csv(_to_bytes(_rows()))
    assert qmap['QID181_8'] != qmap['QID181_8_TEXT'], (
        'the matrix answer and its free-text box resolved to the same column')


# ── end to end ────────────────────────────────────────────────────────────────

@pytest.mark.parametrize('seed', [1, 2, 3, 4])
def test_permuting_the_columns_changes_nothing(seed):
    rows = _rows()
    parcels = load_parcel_index()
    _g0, a0, _s0, _n0, _f0 = process_iaq_bytes(_to_bytes(rows), [], parcels)

    order = list(range(len(rows[0])))
    random.Random(seed).shuffle(order)
    permuted = [[r[i] if i < len(r) else '' for i in order] for r in rows]
    _g1, a1, _s1, _n1, _f1 = process_iaq_bytes(_to_bytes(permuted), [], parcels)

    assert a1['_qid_fallback_qids'] == [], (
        f"questions no longer found by ImportId: {a1['_qid_fallback_qids']}")
    assert _signature(a1) == _signature(a0), 'the analysis depends on column order'


def test_reloc_other_reports_importance_not_free_text():
    """The bug's visible symptom: this chart must hold scale points."""
    rows = _rows()
    _g, a, _s, _n, _f = process_iaq_bytes(_to_bytes(rows), [], load_parcel_index())
    bins = a['residency']['reloc_factors']['reloc_factor_oth']
    scale = {'Not important', 'Slightly important', 'Important',
             'Very Important', 'One of my key concerns'}
    assert bins, 'no answers at all for the Other relocation factor'
    assert set(bins) <= scale, (
        f'free-text answers leaked into the importance chart: {set(bins) - scale}')


def test_an_unrelated_new_question_does_not_shift_anything():
    rows = [r[:] for r in _rows()]
    parcels = load_parcel_index()
    _g0, a0, _s0, _n0, _f0 = process_iaq_bytes(_to_bytes(rows), [], parcels)
    rows[0].append('BrandNewQuestion')
    rows[1].append('A question added after this code was written')
    rows[2].append('{"ImportId":"QID9999"}')
    for r in rows[3:]:
        r.append('42')
    _g1, a1, _s1, _n1, _f1 = process_iaq_bytes(_to_bytes(rows), [], parcels)
    assert _signature(a1) == _signature(a0)
