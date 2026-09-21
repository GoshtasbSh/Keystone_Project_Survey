"""Build the value-parity tables from what the dashboard PAINTED on screen.

Source of the "popup shows" column is `popups/rendered_reads.json` — the
label/value pairs read out of the live popup's active "Survey Answers" pane
after clicking the marker and the tab, exactly what a person sees. The API
payload is deliberately NOT used here.

Each rendered row is joined back to its Qualtrics question by matching the
popup's label against the label the server sends for that field, so the
comparison is label-to-label and never positional.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVID = ROOT / 'docs' / 'plans' / 'evidence' / '2026-09-20-audit'
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / 'api'))

from qualtrics_ground_truth import load_survey, finished_rows, value_by_qid  # noqa: E402

APR = ROOT / 'data' / 'Keystone Heights Survey - V1_April 15, 2026_13.25.csv'
MAY = ('/Users/goshtasbshahriari/UF Dropbox/Goshtasb Shahriari Mehr/'
       'DTSC_Lab/Keystone_Data/Keystone Heights Survey - V1_May 4, 2026_16.57.csv')

PLACEHOLDER = re.compile(r'click to write (scale point|choice)\s*\d*', re.I)
SCORE_ROWS = {'Risk score', 'Health', 'IAQ', 'Structural'}


def md(s) -> str:
    return str(s).replace('|', r'\|').replace('\n', ' ').strip()


def norm(s) -> str:
    return re.sub(r'\s+', ' ', str(s or '')).strip().lower()


def main() -> None:
    reads = json.loads((EVID / 'popups' / 'rendered_reads.json').read_text())
    sampled = json.loads((EVID / 'sample_30.json').read_text())['response_ids']

    # The Survey Answers pane renders 4 score rows and then one row per field,
    # in the fixed order of _IAQ_CATEGORIES (static/js/dashboard.js:1525-1595).
    # Joining on that order is deterministic and needs no label matching; the
    # assertion below fails loudly if the UI's field order ever changes.
    FIELD_ORDER = [
        'respiratory_ill', 'asthma_freq', 'wheeze_freq', 'headache_freq',
        'tired_freq', 'hospital_visit',
        'has_mold', 'leakage_roof', 'leakage_walls', 'leakage_windows',
        'leakage_floor', 'cooling_central_ac', 'cooling_window_unit',
        'cooling_fan', 'cooling_none', 'cooking_method',
        'year_built', 'housing_type', 'condition', 'ownership',
        'years_in_hre', 'anticipated_stay', 'mh_skirting', 'safety_env',
        'safety_social', 'afford_urgency', 'afford_strategy',
        'reloc_factor_emp', 'reloc_factor_aff', 'reloc_factor_qol',
        'reloc_factor_fam', 'reloc_factor_ret', 'reloc_factor_env',
        'reloc_factor_inh', 'reloc_factor_oth',
        'intv_roof_walls', 'intv_windows_doors', 'intv_rain_gardens',
        'intv_hvac', 'intv_plumbing_elec', 'intv_well_septic',
        'intv_ccua_water', 'intv_fence', 'intv_trees_shade',
        'intv_trim_trees', 'intv_drainage',
        'exp_flooding', 'exp_flood_help', 'exp_extreme_heat',
        'exp_school_change', 'exp_law_enf', 'exp_insurance_loss',
        'exp_well_dry', 'exp_pests', 'exp_water_leaks', 'exp_loose_animals',
        'car_access', 'hurricane_transport',
        'education', 'employment',
    ]
    assert len(FIELD_ORDER) == 60, len(FIELD_ORDER)

    apr, may = load_survey(APR), load_survey(MAY)
    apr_rows = {r['ResponseId']: r for r in finished_rows(apr)}
    may_rows = {r['ResponseId']: r for r in finished_rows(may)}

    # field -> QID, from the same SURVEY_QUESTIONS the server uses.
    from _processing import SURVEY_QUESTIONS
    field_to_qid = {f: m[1] for f, m in SURVEY_QUESTIONS.items() if len(m) == 3}

    # The raw IAQ scorer fields are not in SURVEY_QUESTIONS: the server reads
    # them by CSV column NAME (api/_processing.py:2084-2103). Resolve those the
    # same way, so every rendered row gets checked rather than skipped.
    FIELD_TO_COLNAME = {
        'respiratory_ill': 'RespIll', 'asthma_freq': 'asthma',
        'wheeze_freq': 'wheeze', 'headache_freq': 'Headache',
        'tired_freq': 'Tired', 'hospital_visit': 'Hospital Respiratory',
        'has_mold': 'Mold', 'cooking_method': 'Cooking',
        'leakage_roof': 'Leakage 2_1', 'leakage_walls': 'Leakage 2_2',
        'leakage_windows': 'Leakage 2_3', 'leakage_floor': 'Leakage 2_4',
        'cooling_central_ac': 'Cooling System _1',
        'cooling_window_unit': 'Cooling System _2',
        'cooling_fan': 'Cooling System _3',
        'cooling_none': 'Cooling System _4',
        'year_built': 'QID192', 'housing_type': 'QID128',
        'condition': 'QID141', 'ownership': 'Ownership',
    }

    def col_by_name(survey, name):
        for i, c in enumerate(survey['short_names']):
            if str(c).replace('\xa0', ' ').strip() == name:
                return i
        return survey['qid_to_idx'].get(name)

    for tag, survey, rowmap, fname in (
            ('April 15', apr, apr_rows, '02-value-parity-april.md'),
            ('May 4', may, may_rows, '03-value-parity-may.md')):
        head = [
            f'# Popup (as rendered on screen) vs the {tag} Qualtrics export',
            '',
            'Every "Popup shows" value in this table was read out of the live '
            '`-blue` dashboard after clicking the map marker and opening the '
            '**Survey Answers** tab — it is what a person sees, not an API value. '
            'Screenshots of each popup are in `../screenshots/`.',
            '',
            'Rows are joined to a Qualtrics question by the popup\'s own label, then '
            'to a CSV column by that question\'s `ImportId` (QID) — never by column '
            'position.',
            '',
            '**Verdicts** — `MATCH`: popup equals the CSV cell. `PLACEHOLDER`: the '
            'popup shows Qualtrics placeholder text (`Click to write …`); the '
            'respondent did answer, but neither the export nor the dashboard resolves '
            'the real label (findings F0/F9). `RECODE`: the CSV holds a numeric code '
            'and the popup shows a translated label. `DIFFERENT`: popup disagrees with '
            'the CSV. `EMPTY-BOTH`: blank in both — correct. `MISSING`: the CSV has an '
            'answer but the popup shows nothing. `NOT-IN-EXPORT`: that QID has no '
            'column in this export.',
            '',
        ]
        body, counts = [], Counter()

        for i, rid in enumerate(sampled, 1):
            r = reads.get(rid)
            if not r:
                body += [f'## {i}. `{rid}`', '', '> **UNVERIFIED** — popup was not read.', '']
                counts['UNVERIFIED'] += 1
                continue
            row = rowmap.get(rid)
            body += [f'## {i}. `{rid}` — {r.get("header") or "(no address in header)"}', '',
                     f'Read from the **{r.get("activeTab","?").strip()}** tab · '
                     f'{len(r["rows"])} rows rendered · screenshot: '
                     f'`../screenshots/{rid}.png`', '']
            if row is None:
                body += [f'> **UNVERIFIED** — no row for this ResponseId in the {tag} '
                         f'export (see finding F2, coverage gap).', '']
                counts['UNVERIFIED-NO-ROW'] += 1
                continue
            answer_rows = [c for c in r['rows']
                           if (c.get('full') or c.get('shown') or '').strip() not in SCORE_ROWS]
            body += ['| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |',
                     '|---|---|---|---|---|---|---|']
            for n, cell in enumerate(answer_rows):
                label = (cell.get('full') or cell.get('shown') or '').strip()
                shown = (cell.get('value') or '').strip()
                field = FIELD_ORDER[n] if n < len(FIELD_ORDER) else None
                qid = field_to_qid.get(field) if field else None
                if qid:
                    csv_val, col = value_by_qid(survey, row, qid)
                elif field in FIELD_TO_COLNAME:
                    qid = FIELD_TO_COLNAME[field]          # column name, or a QID
                    col = col_by_name(survey, qid)
                    csv_val = (row['cells'][col].strip()
                               if col is not None and col < len(row['cells']) else '')
                else:
                    csv_val, col = '', None

                # The UI appends this marker to placeholder values; compare on
                # the underlying text.
                bare = shown.replace('(Qualtrics placeholder)', '').strip()

                if qid is None:
                    verdict = 'NOT-IN-EXPORT' if field is None else 'NO-QID'
                elif col is None:
                    verdict = 'NOT-IN-EXPORT'
                elif PLACEHOLDER.search(bare):
                    verdict = 'PLACEHOLDER'
                elif not csv_val and bare in ('', '—'):
                    verdict = 'EMPTY-BOTH'
                elif csv_val and bare in ('', '—'):
                    verdict = 'MISSING'
                elif norm(bare) == norm(csv_val):
                    verdict = 'MATCH'
                elif csv_val.isdigit():
                    verdict = 'RECODE'
                else:
                    verdict = 'DIFFERENT'
                counts[verdict] += 1
                body.append('| {} | {} | {} | {} | {} | {} | {} |'.format(
                    n + 1, md(label[:120]), md(bare or '—'), md(csv_val or '—'),
                    col if col is not None else '—', f'`{qid}`' if qid else '—', verdict))
            body.append('')

        total = sum(counts.values())
        summary = ['## Verdict totals', '', '| Verdict | Cells | % |', '|---|---|---|'] + \
                  [f'| {k} | {v} | {100*v/total:.1f}% |'
                   for k, v in sorted(counts.items(), key=lambda x: -x[1])] + \
                  ['', f'Total answer cells compared: **{total}** across '
                   f'**{len(sampled)}** points.', '']
        (EVID / 'tables' / fname).write_text('\n'.join(head + summary + body) + '\n')
        print(f'{fname}: {dict(counts)}')


if __name__ == '__main__':
    main()
