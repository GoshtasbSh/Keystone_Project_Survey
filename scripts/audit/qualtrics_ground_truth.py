"""Independent Qualtrics CSV reader — the audit's ground truth.

Deliberately does NOT import api/_processing.py. If this module and the
production extractor agree, that agreement is evidence. If this module
imported the code under audit, agreement would be circular and worthless.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

csv.field_size_limit(10_000_000)


def load_survey(path: str | Path) -> dict:
    """Parse a 3-header-row Qualtrics CSV.

    Returns:
        {
          'n_cols': int,
          'short_names':   [str, ...],   # header row 0
          'question_text': [str, ...],   # header row 1 — VERBATIM survey text
          'import_ids':    [str|None],   # header row 2, QID per column
          'qid_to_idx':    {qid: idx},
          'rows': [ {'ResponseId': str, 'cells': [str, ...]}, ... ],
        }
    """
    path = Path(path)
    with path.open(newline='', encoding='utf-8-sig') as f:
        raw = list(csv.reader(f))
    if len(raw) < 3:
        raise ValueError(f"{path.name}: fewer than 3 header rows")

    short_names, question_text, meta_row = raw[0], raw[1], raw[2]
    if 'ImportId' not in ' '.join(meta_row):
        raise ValueError(f"{path.name}: row 3 is not ImportId metadata")

    import_ids: list[str | None] = []
    qid_to_idx: dict[str, int] = {}
    for idx, cell in enumerate(meta_row):
        m = re.search(r'"ImportId"\s*:\s*"([^"]+)"', cell or '')
        qid = m.group(1) if m else None
        import_ids.append(qid)
        if qid:
            qid_to_idx.setdefault(qid, idx)
            base = qid[:-5] if qid.endswith('_TEXT') else qid
            qid_to_idx.setdefault(base, idx)

    rid_idx = short_names.index('ResponseId')
    rows = [
        {'ResponseId': r[rid_idx], 'cells': r}
        for r in raw[3:]
        if len(r) > rid_idx and r[rid_idx].strip()
    ]
    return {
        'n_cols': len(short_names),
        'short_names': short_names,
        'question_text': question_text,
        'import_ids': import_ids,
        'qid_to_idx': qid_to_idx,
        'rows': rows,
    }


def value_by_qid(survey: dict, row: dict, qid: str) -> tuple[str, int | None]:
    """Return (cell_value, column_index) for a QID, ('', None) if absent."""
    idx = survey['qid_to_idx'].get(qid)
    if idx is None:
        base = qid[:-5] if qid.endswith('_TEXT') else qid
        idx = survey['qid_to_idx'].get(base)
    if idx is None or idx >= len(row['cells']):
        return '', None
    return row['cells'][idx].strip(), idx


def finished_rows(survey: dict) -> list[dict]:
    """Rows where Finished is True/1 — the only rows production processes."""
    try:
        fi = survey['short_names'].index('Finished')
    except ValueError:
        return survey['rows']
    out = []
    for r in survey['rows']:
        if fi < len(r['cells']) and r['cells'][fi].strip().lower() in ('true', '1'):
            out.append(r)
    return out


if __name__ == '__main__':
    s = load_survey(sys.argv[1])
    print(f"n_cols: {s['n_cols']}")
    print(f"qids discovered: {len(s['qid_to_idx'])}")
    print(f"data rows: {len(s['rows'])}")
    print(f"finished rows: {len(finished_rows(s))}")
    print("first 12 ImportIds:",
          json.dumps([q for q in s['import_ids'] if q][:12]))
