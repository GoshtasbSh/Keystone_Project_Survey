"""Generate api/qsf_labels.json — the authoritative answer labels, from the QSF.

Why this exists
---------------
A Qualtrics question carries two label sets:

  Choices[k].Display / Answers[k].Display  — what the respondent saw. The truth.
  VariableNaming[k]                        — an export-label override.

The TEXT-format CSV writes VariableNaming. In the KeyStone survey those
overrides were never updated as the questionnaire was edited, so they hold
placeholder strings ("Click to write Choice 5") and, worse, labels left over
from other questions (QID192's age bands are reversed; QID21's safety scale
exports as durations). The dashboard therefore displayed answers that were not
the respondent's answer.

This map lets the pipeline translate whatever the export wrote back to what the
respondent actually chose:

  text export    cell == VariableNaming[k]  -> k -> Display[k]
  numeric export cell == recode code        -> k -> Display[k]

Matrix questions resolve against Answers (the scale points); multiple-choice
questions resolve against Choices. Qualtrics writes "Scale Point N" placeholders
for the former and "Choice N" for the latter, which is a useful cross-check.

Any text that maps to more than one choice is recorded as ambiguous and is left
untranslated at runtime rather than guessed — QID141 is the real case: its
RecodeValues collapse choice 5 onto code 1, which choice 1 already uses.

Run:  python3 scripts/build_qsf_label_map.py [path/to/survey.qsf]
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_QSF = ('/Users/goshtasbshahriari/UF Dropbox/Goshtasb Shahriari Mehr/'
               'DTSC_Lab/Keystone_Data/Keystone_Heights_Survey_-_V1 (1).qsf')
OUT = ROOT / 'api' / 'qsf_labels.json'


def norm(s) -> str:
    return ' '.join(str(s or '').replace('\xa0', ' ').split()).strip()


def build(qsf_path: str) -> dict:
    qsf = json.loads(Path(qsf_path).read_text(encoding='utf-8'))
    out: dict = {}

    for el in qsf.get('SurveyElements', []):
        if el.get('Element') != 'SQ':
            continue
        p = el.get('Payload') or {}
        qid = p.get('QuestionID')
        if not qid:
            continue

        # Qualtrics stores these as a dict keyed by choice id, but for some
        # question types as a plain list — in which case the ids are 1-based
        # positions.
        def as_map(v):
            if isinstance(v, list):
                return {str(i): item for i, item in enumerate(v, 1)}
            return v or {}

        answers = as_map(p.get('Answers'))
        choices = as_map(p.get('Choices'))
        # A matrix question's cell holds the chosen SCALE POINT, which lives in
        # Answers. Everything else resolves against Choices.
        is_matrix = bool(answers)
        target = answers if is_matrix else choices
        if not target:
            continue

        display = {str(k): norm((v or {}).get('Display'))
                   for k, v in target.items() if (v or {}).get('Display') is not None}
        if not display:
            continue

        var_naming = {str(k): norm(v) for k, v in (p.get('VariableNaming') or {}).items()}
        recodes = {str(k): str(v) for k, v in (p.get('RecodeValues') or {}).items()}
        if is_matrix:
            recodes = {str(k): str(v) for k, v in
                       (p.get('AnswerRecodeValues') or recodes or {}).items()}

        # text -> choice key. VariableNaming wins where present, because that is
        # what the export actually wrote; the raw Display is included for keys
        # the override does not cover (the export falls back to it).
        text_to_key: dict = defaultdict(set)
        for k, disp in display.items():
            src = var_naming.get(k, disp)
            if src:
                text_to_key[src.lower()].add(k)
            # Claim the plain Display for this key only when no override
            # redirects that text elsewhere; otherwise the override wins.
            if disp and k not in var_naming:
                text_to_key[disp.lower()].add(k)

        # recode code -> choice key (unlisted keys recode to themselves)
        code_to_key: dict = defaultdict(set)
        for k in display:
            code_to_key[recodes.get(k, k)].add(k)

        out[qid] = {
            'matrix': is_matrix,
            'display': display,
            'text_to_key': {t: sorted(ks) for t, ks in text_to_key.items() if t and ks},
            'code_to_key': {c: sorted(ks) for c, ks in code_to_key.items()},
            'ambiguous_text': sorted(t for t, ks in text_to_key.items() if len(ks) > 1),
            'ambiguous_code': sorted(c for c, ks in code_to_key.items() if len(ks) > 1),
        }

    return out


def main() -> None:
    qsf_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_QSF
    data = build(qsf_path)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1, sort_keys=True))

    amb_t = {q: v['ambiguous_text'] for q, v in data.items() if v['ambiguous_text']}
    amb_c = {q: v['ambiguous_code'] for q, v in data.items() if v['ambiguous_code']}
    print(f'wrote {OUT.relative_to(ROOT)}  ({len(data)} questions, '
          f'{OUT.stat().st_size / 1024:.1f} KB)')
    print(f'questions with ambiguous TEXT (left untranslated): {amb_t or "none"}')
    print(f'questions with ambiguous CODE (left untranslated): {amb_c or "none"}')


if __name__ == '__main__':
    main()
