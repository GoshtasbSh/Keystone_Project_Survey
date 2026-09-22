"""Fail if any chart label in an analysis blob is not a label the respondent saw.

Every categorical distribution the dashboard renders is checked, key by key,
against Choices/Answers Display in api/qsf_labels.py (built from the QSF).
A key that matches a stale VariableNaming override instead of the real choice
text is an error: that is the defect that put 'Click to write Choice 4' and
'Less than 6 months' on the Survey Results tab.

Usage:  python3 scripts/audit/verify_chart_labels.py <analysis.json>
Exit 0 = every label is respondent-visible text. Exit 1 = at least one is not.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'api'))
from qsf_labels import QSF_LABELS  # noqa: E402

# RAW: every key must be text from the question's Choices/Answers Display.
# Second element marks a multi-select, whose answers arrive comma-joined.
RAW = {
    'housing_safety.env':          ('QID21',  False),
    'housing_safety.social':       ('QID194', False),
    'residency.anticipated_stay':  ('QID47',  True),
    'residency.mh_skirting':       ('QID100', False),
    'affordability.urgency':       ('QID17',  False),
    'affordability.strategy':      ('QID19',  True),
    'demographics_ext.employment': ('QID176', False),
}

# DERIVED: the pipeline re-buckets these, so the keys are its own vocabulary,
# not QSF text. Checked for (a) an unexpected bucket and (b) coverage — a
# derived distribution that loses respondents is dropping answers on the floor.
DERIVED = {
    'housing.types':                ('QID128', {'Single Wide', 'Double Wide', 'Site Built',
                                                'Non-traditional', 'Other'}),
    'housing.conditions':           ('QID141', {'Excellent', 'Good', 'Fair', 'Poor', 'Critical',
                                                'Unknown'}),
    'housing.year_built':           ('QID192', {'2000+', '1980–1999', '1960–1979',
                                                'Before 1960', 'Unknown'}),
    'mobility.car_access':          ('QID211', {'yes', 'no', 'na', 'other', 'not_sure'}),
    'mobility.hurricane_transport': ('QID219', {'yes', 'no', 'na', 'other', 'not_sure'}),
    'demographics_ext.education':   ('QID178', {'less than high school',
                                                'High school diploma or equivalent',
                                                'Some college, no degree', "Bachelor's Degree",
                                                'Graduate Degree',
                                                'Vocational/Technical Licensing or Certification'}),
}

# Labels that are legitimately not QSF choices.
ALLOWED = {'', 'No answer', 'Unknown', 'Other', 'Not Applicable', 'nan'}


def dig(blob, path):
    cur = blob
    for part in path.split('.'):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def stale_terms(qid):
    """VariableNaming text that is NOT the display text for the same key."""
    e = QSF_LABELS.get(qid) or {}
    disp = e.get('display') or {}
    out = {}
    for text, keys in (e.get('text_to_key') or {}).items():
        for k in keys:
            real = disp.get(k)
            if real and text.strip().lower() != real.strip().lower():
                out[text.strip().lower()] = real
    return out


def fragments(dist, qid):
    """Detect a single-select answer that was comma-split into fragments."""
    e = QSF_LABELS.get(qid) or {}
    out = []
    for full in (e.get('display') or {}).values():
        if ',' not in full:
            continue
        present = [p.strip() for p in full.split(',') if p.strip() in dist]
        if len(present) > 1:
            counts = {p: dist[p] for p in present}
            out.append(f'{full!r} was comma-split into {counts} '
                       f'— one answer counted as {len(present)}')
    return out


def main(path):
    blob = json.load(open(path))
    n = blob.get('n_responses') or 0
    errors, warns, checked = [], [], 0

    for apath, (qid, multi) in RAW.items():
        dist = dig(blob, apath)
        entry = QSF_LABELS.get(qid)
        if dist is None or not entry:
            warns.append(f'SKIP {apath}')
            continue
        valid = {v.strip().lower() for v in entry['display'].values()}
        stale = stale_terms(qid)
        bad = {}
        for label in dist:
            checked += 1
            parts = [p.strip() for p in label.split(',')] if multi else [label.strip()]
            for p in parts:
                if p in ALLOWED or p.lower() in valid:
                    continue
                real = stale.get(p.lower())
                bad[p] = (f'STALE export label — respondent saw {real!r}' if real
                          else f'not a {qid} choice')
        for p, why in sorted(bad.items()):
            errors.append(f'{apath}: {p!r} {why}')

    for apath, (qid, vocab) in DERIVED.items():
        dist = dig(blob, apath)
        if dist is None:
            warns.append(f'SKIP {apath}')
            continue
        checked += len(dist)
        for label in sorted(dist):
            if label not in vocab:
                errors.append(f'{apath}: {label!r} is not a declared bucket for {qid}')
        for f in fragments(dist, qid):
            errors.append(f'{apath}: {f}')
        total = sum(v for v in dist.values() if isinstance(v, int))
        if n and total < n * 0.9:
            warns.append(f'{apath}: buckets cover {total}/{n} responses '
                         f'({total / n:.0%}) — answers may be dropped')

    print(f'checked {checked} label(s) across '
          f'{len(RAW) + len(DERIVED)} distribution(s), n_responses={n}')
    for w in warns:
        print(f'  ! {w}')
    if errors:
        print(f'\nFAIL — {len(errors)} problem(s):')
        for e in errors:
            print(f'  x {e}')
        return 1
    print('\nPASS — every label is text the respondent actually saw.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else 'verify/before-iaq.json'))
