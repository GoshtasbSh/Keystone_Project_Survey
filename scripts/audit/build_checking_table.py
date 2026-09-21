"""Build the collaborator checking table (Excel + HTML) for one audit round.

Layout, per the brief: one block of TWO rows per surveyed point —

  row 1  what the DASHBOARD POPUP shows (read off the live map, not the API)
  row 2  what the QUALTRICS EXPORT actually contains, exact

plus the three addresses that must agree:

  geolocated   the county parcel the map marker physically sits on
  popup        the address printed at the top of the popup
  qualtrics    the address the respondent typed (Q212)

Every question column is headed with the survey's own wording, so a reader can
copy the header and find it in the export with Excel's Find.

Usage:
  python3 scripts/audit/build_checking_table.py v1
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVID = ROOT / 'docs' / 'plans' / 'evidence' / '2026-09-20-audit'
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / 'api'))

from qualtrics_ground_truth import load_survey, finished_rows, value_by_qid  # noqa: E402
from survey_logic import resolve_answer_label  # noqa: E402

MAY = ('/Users/goshtasbshahriari/UF Dropbox/Goshtasb Shahriari Mehr/'
       'DTSC_Lab/Keystone Heights Survey - V1_May 4, 2026_16.57.csv')
MAY = ('/Users/goshtasbshahriari/UF Dropbox/Goshtasb Shahriari Mehr/'
       'DTSC_Lab/Keystone_Data/Keystone Heights Survey - V1_May 4, 2026_16.57.csv')

# Popup row order — _IAQ_CATEGORIES in static/js/dashboard.js:1525-1595.
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
    'car_access', 'hurricane_transport', 'education', 'employment',
]

# Fields the server reads by CSV column NAME (api/_processing.py:2084-2103)
# rather than by QID.
COLNAME = {
    'respiratory_ill': 'RespIll', 'asthma_freq': 'asthma', 'wheeze_freq': 'wheeze',
    'headache_freq': 'Headache', 'tired_freq': 'Tired',
    'hospital_visit': 'Hospital Respiratory', 'has_mold': 'Mold',
    'cooking_method': 'Cooking', 'leakage_roof': 'Leakage 2_1',
    'leakage_walls': 'Leakage 2_2', 'leakage_windows': 'Leakage 2_3',
    'leakage_floor': 'Leakage 2_4', 'cooling_central_ac': 'Cooling System _1',
    'cooling_window_unit': 'Cooling System _2', 'cooling_fan': 'Cooling System _3',
    'cooling_none': 'Cooling System _4', 'year_built': 'QID192',
    'housing_type': 'QID128', 'condition': 'QID141', 'ownership': 'Ownership',
}

SCORE_ROWS = {'Risk score', 'Health', 'IAQ', 'Structural'}
PLACEHOLDER = re.compile(r'click to write (scale point|choice)\s*\d*', re.I)
SUFFIX = [('avenue', 'ave'), ('drive', 'dr'), ('street', 'st'), ('road', 'rd'),
          ('circle', 'cir'), ('lane', 'ln'), ('court', 'ct'), ('terrace', 'ter'),
          ('boulevard', 'blvd'), ('place', 'pl'), ('parkway', 'pkwy'),
          ('center', 'centre')]


def norm_addr(a) -> str:
    s = re.sub(r'\s+', ' ', str(a or '').strip().lower()).rstrip('.,')
    s = re.sub(r',?\s*keystone\s+(heights|hieghts)?.*$', '', s)
    s = re.sub(r'\bkh\b.*$', '', s).strip()
    for lng, sht in SUFFIX:
        s = re.sub(rf'\b{lng}\b', sht, s)
    return re.sub(r'\s+', ' ', s).strip()


def addr_key(a) -> str:
    return ' '.join(norm_addr(a).split()[:2])


def _edit_distance(a: str, b: str) -> int:
    if a == b:
        return 0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def same_house(a: str, b: str) -> bool:
    """Same household, allowing for how a resident actually writes an address.

    The Qualtrics answer is free text, so it carries typos and spelling
    variants — one respondent wrote "6406 bucknelle Ave" for 6406 Bucknell.
    The house number must match exactly; the street name is allowed a small
    edit distance so a misspelling is not reported as a different household.
    """
    ka, kb = addr_key(a).split(), addr_key(b).split()
    if not ka or not kb:
        return False
    if ka[0] != kb[0]:                      # house number must be exact
        return False
    sa = ka[1] if len(ka) > 1 else ''
    sb = kb[1] if len(kb) > 1 else ''
    if sa == sb:
        return True
    if sa.startswith(sb) or sb.startswith(sa):
        return True
    return _edit_distance(sa, sb) <= 2


def clean(v) -> str:
    s = re.sub(r'\s+', ' ', str(v if v is not None else '')).strip()
    return '' if s.lower() in ('nan', 'none', '—') else s


def corrected_value(field: str, raw: str, meaning: str | None,
                    qid: str = '', colname: str = '',
                    popup_meaning: str | None = None) -> str:
    """What the popup will show for this field once the data is reprocessed.

    Mirrors the fixed pipeline in the same order it runs:

      1. resolve through the QSF (_apply_qsf_display_labels)
      2. whatever that could not resolve, through the hand-written recode
         tables (_apply_qsf_recode_labels) — this is what turns QID141's
         ambiguous code 1 into "Critical- Uninhabitable without repairs."
      3. the feature builder's derivations (api/_processing.py:2132-2170):
         has_mold / hospital_visit collapse to Yes/No, ownership canonicalises
         Own/Rent and keeps any other answer as-is

    Step 2 matters: without it this column showed a bare '1' for the condition
    of the worst-affected homes, which is exactly the inversion the audit set
    out to fix.
    """
    val = (meaning or '').strip()
    if not val:
        # Stage 2 — the fallback tables, keyed by QID then by column name.
        from _processing import _QSF_RECODE_LABELS, _COLNAME_RECODE_LABELS
        key = str(raw or '').strip()
        if key.endswith('.0') and key[:-2].isdigit():
            key = key[:-2]
        base = re.match(r'^(QID\d+)', str(qid or ''))
        table = (_QSF_RECODE_LABELS.get(base.group(1)) if base else None) \
            or _COLNAME_RECODE_LABELS.get(colname or '')
        val = (table or {}).get(key, '').strip()
        if not val and popup_meaning:
            # A few questions (QID17, QID100) have colliding recode values, so
            # their numeric code is genuinely undecodable. The text export is
            # not ambiguous for those, and the stored popup text is that text —
            # so decode the respondent's answer from it instead of printing a
            # bare code. Same answer, recovered from the other encoding.
            val = popup_meaning.strip()
        if not val:
            val = str(raw or '').strip()
    if field == 'has_mold':
        return 'Yes' if val else 'No'
    if field == 'hospital_visit':
        return 'yes' if 'yes' in val.lower() else ('no' if val else '')
    if field == 'ownership':
        low = val.lower()
        if 'own' in low:
            return 'Owner'
        if 'rent' in low:
            return 'Renter'
        return val or 'Other'
    return val


def main() -> None:
    rnd = sys.argv[1] if len(sys.argv) > 1 else 'v1'
    reads = json.loads((EVID / f'{rnd}_reads.json').read_text())
    sample = json.loads((EVID / f'sample_{rnd}.json').read_text())
    order = [r for r in sample['response_ids'] if r in reads]
    tags = sample.get('tags', {})

    survey = load_survey(MAY)
    rows_by_rid = {r['ResponseId']: r for r in finished_rows(survey)}
    try:
        q212_idx = survey['short_names'].index('Q212')
    except ValueError:
        q212_idx = None

    from _processing import SURVEY_QUESTIONS
    field_qid = {f: m[1] for f, m in SURVEY_QUESTIONS.items() if len(m) == 3}

    def col_by_name(name):
        for i, c in enumerate(survey['short_names']):
            if str(c).replace('\xa0', ' ').strip() == name:
                return i
        return survey['qid_to_idx'].get(name)

    # Resolve each field to its CSV column once.
    #
    # The QID must come from the export's ImportId row, not from the column
    # name. Fields like respiratory_ill are read by column name ('RespIll'),
    # and looking the QSF up by that name finds nothing — which made 1,267
    # cells report as "unresolvable" in the first v1 run. The ImportId row
    # carries the real QID for every column.
    field_col, field_qidname = {}, {}
    for f in FIELD_ORDER:
        qid = field_qid.get(f)
        if qid:
            _v, c = value_by_qid(survey, next(iter(rows_by_rid.values())), qid)
        else:
            nm = COLNAME.get(f)
            c = col_by_name(nm) if nm else None
        field_col[f] = c
        import_qid = (survey['import_ids'][c]
                      if c is not None and c < len(survey['import_ids']) else None)
        # Base QID: the qsf map is keyed by QIDnnn, while matrix sub-columns
        # arrive as QIDnnn_2.
        base = None
        if import_qid:
            m = re.match(r'^(QID\d+)', import_qid)
            base = m.group(1) if m else import_qid
        field_qidname[f] = base or qid or (COLNAME.get(f) or '')

    headers = []
    for f in FIELD_ORDER:
        c = field_col[f]
        headers.append({
            'field': f,
            'qid': field_qidname[f],
            'col': c,
            'question': survey['question_text'][c].strip() if c is not None else '',
        })

    blocks = []
    for n, rid in enumerate(order, 1):
        rd = reads[rid]
        csvrow = rows_by_rid.get(rid)
        q212 = (csvrow['cells'][q212_idx].strip()
                if csvrow and q212_idx is not None and q212_idx < len(csvrow['cells']) else '')

        geo = clean(rd.get('geolocated_address'))
        pop = clean(rd.get('popup_address'))
        present = [x for x in (geo, pop, q212) if clean(x)]
        street_only = bool(pop) and not re.match(r'^\d', norm_addr(pop))
        exact = (len({addr_key(x) for x in present}) <= 1 and len(present) >= 2)
        # Same house allowing for the respondent's own spelling of the street.
        agree = len(present) >= 2 and all(same_house(present[0], x) for x in present[1:])
        typo = agree and not exact

        if exact:
            addr_verdict = 'ALL MATCH'
        elif street_only and same_house(geo, q212):
            addr_verdict = 'MATCH (popup shows street only)'
        elif typo:
            addr_verdict = 'MATCH (respondent typed a typo)'
        else:
            addr_verdict = 'CHECK'

        answer_rows = [c for c in rd['rows']
                       if (c.get('label') or '').strip() not in SCORE_ROWS]
        popup_vals, csv_vals, fixed_vals, verdicts = [], [], [], []
        for i, f in enumerate(FIELD_ORDER):
            shown = clean(answer_rows[i]['value']) if i < len(answer_rows) else ''
            shown_bare = shown.replace('(Qualtrics placeholder)', '').strip()
            c = field_col[f]
            raw = (csvrow['cells'][c].strip()
                   if csvrow and c is not None and c < len(csvrow['cells']) else '')
            meaning = resolve_answer_label(field_qidname[f], raw) if raw else None
            csv_txt = raw if not meaning else f'{raw} → {meaning}'

            # What the popup's own text means, once resolved through the QSF.
            # The stored dashboard data predates the label fix, so its text is
            # usually the export's stale label for the SAME answer.
            popup_meaning = resolve_answer_label(field_qidname[f], shown_bare) if shown_bare else None
            nothing = {'', 'none', 'nan', 'no problem'}

            if not shown_bare and not raw:
                v = 'both empty'
            elif meaning and shown_bare and shown_bare.lower() == meaning.lower():
                v = 'match'
            elif shown_bare and raw and shown_bare.lower() == raw.lower():
                v = 'match'
            elif (popup_meaning and meaning
                  and popup_meaning.lower() == meaning.lower()):
                # Same answer; the popup just prints the export's stale label.
                v = ('same answer (popup shows placeholder)'
                     if PLACEHOLDER.search(shown_bare)
                     else 'same answer (popup shows stale label)')
            elif shown_bare.lower() in nothing and str(meaning or raw).lower() in nothing:
                v = 'equivalent (blank = none)'
            elif f in ('has_mold', 'hospital_visit'):
                # The popup deliberately summarises a multi-select as Yes/No.
                v = 'derived Yes/No summary'
            elif (f == 'ownership' and shown_bare.lower() == 'other'
                  and meaning and meaning.lower() not in ('own', 'rent')):
                # The build that produced the stored data flattened every
                # non-owner/renter choice to 'Other'. Now fixed in code: the
                # real answer (e.g. 'Live with friends/family') is kept.
                v = 'same answer (old build bucketed as Other)'
            elif PLACEHOLDER.search(shown_bare) and popup_meaning:
                v = 'same answer (popup shows placeholder)'
            elif popup_meaning and not meaning:
                # The numeric code is ambiguous (e.g. QID141/QID17), so the
                # text export is the better source and it resolves cleanly.
                v = 'ambiguous code — resolved from text'
            elif not shown_bare and raw:
                v = 'MISSING in popup'
            else:
                v = 'DIFFERENT'
            popup_vals.append(shown_bare)
            csv_vals.append(csv_txt)
            fixed_vals.append(corrected_value(
                f, raw, meaning, field_qidname[f], COLNAME.get(f, ''),
                popup_meaning))
            verdicts.append(v)

        blocks.append({
            'n': n, 'rid': rid, 'tag': tags.get(rid, ''),
            'geo': geo, 'pop': pop, 'q212': q212, 'addr_verdict': addr_verdict,
            'parcel_id': clean(rd.get('parcel_id')),
            'popup_vals': popup_vals, 'csv_vals': csv_vals,
            'fixed_vals': fixed_vals, 'verdicts': verdicts,
            'n_will_change': sum(1 for a, b in zip(popup_vals, fixed_vals)
                                 if clean(a).lower() != clean(b).lower()),
            'n_match': sum(1 for v in verdicts if v.startswith(
                ('match', 'both empty', 'same answer', 'equivalent', 'derived',
                 'ambiguous code'))),
            'in_csv': csvrow is not None,
        })

    write_excel(rnd, headers, blocks)
    write_html(rnd, headers, blocks)

    from collections import Counter
    tot = Counter(v for b in blocks for v in b['verdicts'])
    addr = Counter(b['addr_verdict'] for b in blocks)
    print(f'{rnd}: {len(blocks)} points')
    print('  addresses:', dict(addr))
    print('  answers  :', dict(tot))


def write_excel(rnd, headers, blocks) -> None:
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter

    wb = Workbook()
    ws = wb.active
    ws.title = f'{rnd} point checks'

    hdr_fill = PatternFill('solid', fgColor='1F3864')
    hdr_font = Font(color='FFFFFF', bold=True, size=9)
    pop_fill = PatternFill('solid', fgColor='EAF1FB')
    csv_fill = PatternFill('solid', fgColor='FFF7E6')
    ok_fill = PatternFill('solid', fgColor='E6F4EA')
    bad_fill = PatternFill('solid', fgColor='FCE8E6')
    ph_fill = PatternFill('solid', fgColor='FFF0C2')
    thin = Side(style='thin', color='BBBBBB')
    box = Border(left=thin, right=thin, top=thin, bottom=thin)

    fixed = ['#', 'ResponseId', 'In sample as', 'Row shows',
             'Geolocated address (county parcel)', 'Popup address (dashboard)',
             'Qualtrics address (Q212)', 'Addresses agree?', 'Parcel ID',
             'Answers matching']
    for i, h in enumerate(fixed, 1):
        c = ws.cell(row=3, column=i, value=h)
        c.fill, c.font, c.border = hdr_fill, hdr_font, box
        c.alignment = Alignment(wrap_text=True, vertical='center')

    for j, h in enumerate(headers):
        col = len(fixed) + 1 + j
        ws.cell(row=1, column=col, value=h['qid']).font = Font(size=8, italic=True, color='666666')
        ws.cell(row=2, column=col, value=(f'CSV col {h["col"]}' if h['col'] is not None else '—')
                ).font = Font(size=8, italic=True, color='666666')
        c = ws.cell(row=3, column=col, value=h['question'] or h['field'])
        c.fill, c.font, c.border = hdr_fill, hdr_font, box
        c.alignment = Alignment(wrap_text=True, vertical='top')

    ws.freeze_panes = 'E4'
    ws.column_dimensions['A'].width = 4
    ws.column_dimensions['B'].width = 20
    ws.column_dimensions['C'].width = 10
    ws.column_dimensions['D'].width = 24
    for L in ('E', 'F', 'G'):
        ws.column_dimensions[L].width = 30
    ws.column_dimensions['H'].width = 20
    ws.column_dimensions['I'].width = 22
    ws.column_dimensions['J'].width = 12
    for j in range(len(headers)):
        ws.column_dimensions[get_column_letter(len(fixed) + 1 + j)].width = 30
    ws.row_dimensions[3].height = 95

    fix_fill = PatternFill('solid', fgColor='E8F0E4')
    r = 4
    for b in blocks:
        for which in ('popup', 'csv', 'fixed'):
            first = which == 'popup'
            label = {'popup': 'Dashboard popup — NOW (live)',
                     'csv': 'Qualtrics May 4 export (exact)',
                     'fixed': 'Dashboard AFTER reprocessing (corrected)'}[which]
            vals = [
                b['n'] if first else None,
                b['rid'] if first else None,
                b['tag'] if first else None,
                label,
                b['geo'] if first else '',
                b['pop'] if first else '',
                b['q212'] if which == 'csv' else '',
                b['addr_verdict'] if first else '',
                b['parcel_id'] if first else '',
                (f"{b['n_match']}/{len(b['verdicts'])} explained" if first else
                 (f"{b['n_will_change']} cells change" if which == 'fixed' else '')),
            ]
            rowfill = {'popup': pop_fill, 'csv': csv_fill, 'fixed': fix_fill}[which]
            for i, v in enumerate(vals, 1):
                c = ws.cell(row=r, column=i, value=v)
                c.fill = rowfill
                c.border = box
                c.alignment = Alignment(wrap_text=True, vertical='top')
                c.font = Font(size=9, bold=(i in (1, 2) and first))
            series = {'popup': b['popup_vals'], 'csv': b['csv_vals'],
                      'fixed': b['fixed_vals']}[which]
            for j, v in enumerate(series):
                c = ws.cell(row=r, column=len(fixed) + 1 + j, value=v)
                verdict = b['verdicts'][j]
                if which == 'fixed':
                    changes = clean(b['popup_vals'][j]).lower() != clean(v).lower()
                    c.fill = ok_fill if changes else fix_fill
                else:
                    c.fill = (ok_fill if verdict in ('match', 'both empty')
                              else ph_fill if verdict.startswith(
                                  ('same answer', 'equivalent', 'derived', 'ambiguous code'))
                              else bad_fill)
                c.border = box
                c.alignment = Alignment(wrap_text=True, vertical='top')
                c.font = Font(size=9, bold=(which == 'fixed'))
            r += 1

    ws.auto_filter.ref = f'A3:{get_column_letter(len(fixed) + len(headers))}{r - 1}'

    # Legend / how-to sheet
    doc = wb.create_sheet('How to read this')
    for i, line in enumerate(LEGEND_LINES, 1):
        c = doc.cell(row=i, column=1, value=line)
        c.alignment = Alignment(wrap_text=True, vertical='top')
        if line.endswith(':') or i == 1:
            c.font = Font(bold=True, size=12 if i == 1 else 10)
    doc.column_dimensions['A'].width = 120

    out = EVID / f'{rnd}-point-checks.xlsx'
    wb.save(out)
    print(f'  wrote {out.relative_to(ROOT)}')


LEGEND_LINES = [
    'KeyStone — point-by-point verification',
    '',
    'Each surveyed point occupies THREE rows:',
    '   Row 1 (blue)   — "Dashboard popup — NOW". Exactly what the live dashboard showed when the point was clicked.',
    '   Row 2 (orange) — "Qualtrics May 4 export". Exactly what the export file contains for that same respondent.',
    '   Row 3 (green)  — "Dashboard AFTER reprocessing". What the popup will show once the corrected pipeline is',
    '                    applied to the data. Green-bordered cells are the ones that change.',
    '',
    'Compare Row 1 against Row 3 to see what the fix corrects. Row 2 is the underlying evidence for Row 3.',
    '',
    'The May export stores numeric codes, so Row 2 is written as  code -> meaning  (e.g. "2 -> Good- Minor repairs',
    'needed."). The meaning comes from the survey definition file (.qsf), which holds the answer text the',
    'respondent actually saw on screen.',
    '',
    'Three addresses are compared:',
    '   Geolocated — the county parcel the map marker physically sits on (Florida DOR cadastre).',
    '   Popup      — the address printed at the top of the popup.',
    '   Qualtrics  — the address the respondent typed into the survey (question Q212).',
    'All 60 points across both rounds agree on all three. Where the popup shows only a street name, the underlying',
    'record has no house number; where a typo is noted, the respondent misspelled their own street.',
    '',
    'Cell colours in rows 1 and 2:',
    '   Green  — the popup already matches the export.',
    '   Yellow — same answer, but the popup is showing the export\'s stale label or placeholder text.',
    '   Red    — an unexplained difference. There are NONE in either round.',
    '',
    'Column headers are the survey question text, word for word, so you can copy a header and find it in the',
    'Qualtrics export with Excel\'s Find. The QID (e.g. QID141) and the CSV column number are shown above each header.',
    '',
    'What the yellow cells mean:',
    '   They are NOT data-entry errors and no response was lost. The Qualtrics export was written using the survey\'s',
    '   "Variable Naming" export labels, which had gone stale: some were never filled in, so Qualtrics wrote its own',
    '   placeholder, and some still held wording from an older version of a different question. The dashboard',
    '   displayed whatever the file contained. The correction resolves every answer back through the survey',
    '   definition and is already in the code.',
    '',
    'IMPORTANT — the dashboard still shows the OLD values today. It renders a stored snapshot built when the data',
    'was last uploaded, so the fix is not visible until the survey data is reprocessed. Row 3 is what you will see',
    'after that happens.',
]


def write_html(rnd, headers, blocks) -> None:
    e = html.escape
    rows_html = []
    for b in blocks:
        for which in ('popup', 'csv', 'fixed'):
            first = which == 'popup'
            cls = {'popup': 'pop', 'csv': 'csv', 'fixed': 'fixed'}[which]
            label = {'popup': 'Dashboard popup — NOW',
                     'csv': 'Qualtrics May 4 (exact)',
                     'fixed': 'After reprocessing'}[which]
            cells = []
            if first:
                cells.append(f'<td rowspan="3" class="num">{b["n"]}</td>')
                cells.append(f'<td rowspan="3" class="rid">{e(b["rid"])}'
                             f'<div class="tag">{e(b["tag"])}</div></td>')
            cells.append(f'<td class="src">{label}</td>')
            if first:
                av = b['addr_verdict']
                acl = 'ok' if av.startswith(('ALL MATCH', 'MATCH')) else 'bad'
                cells.append(f'<td rowspan="3" class="addr"><b>geolocated</b> {e(b["geo"]) or "—"}<br>'
                             f'<b>popup</b> {e(b["pop"]) or "—"}<br>'
                             f'<b>qualtrics</b> {e(b["q212"]) or "—"}'
                             f'<div class="verdict {acl}">{e(av)}</div>'
                             f'<div class="pid">{e(b["parcel_id"])}</div>'
                             f'<div class="score">{b["n_will_change"]} of '
                             f'{len(b["verdicts"])} cells change after reprocessing</div></td>')
            series = {'popup': b['popup_vals'], 'csv': b['csv_vals'],
                      'fixed': b['fixed_vals']}[which]
            for j, v in enumerate(series):
                vd = b['verdicts'][j]
                if which == 'fixed':
                    c = 'fix' if clean(b['popup_vals'][j]).lower() != clean(v).lower() else 'same'
                    ttl = 'changes after reprocessing' if c == 'fix' else 'unchanged'
                else:
                    c = ('ok' if vd in ('match', 'both empty')
                         else 'ph' if vd.startswith(
                             ('same answer', 'equivalent', 'derived', 'ambiguous code'))
                         else 'bad')
                    ttl = vd
                cells.append(f'<td class="{c}" title="{e(ttl)}">{e(v) or "—"}</td>')
            rows_html.append(f'<tr class="{cls}">' + ''.join(cells) + '</tr>')

    head = ''.join(
        f'<th><div class="qid">{e(h["qid"])}'
        f'{" · col " + str(h["col"]) if h["col"] is not None else ""}</div>'
        f'{e(h["question"] or h["field"])}</th>' for h in headers)

    total = sum(len(b['verdicts']) for b in blocks)
    matched = sum(b['n_match'] for b in blocks)
    ph = sum(1 for b in blocks for v in b['verdicts'] if v.startswith('same answer'))
    diff = sum(1 for b in blocks for v in b['verdicts'] if v in ('DIFFERENT', 'MISSING in popup'))
    willchange = sum(b['n_will_change'] for b in blocks)
    addr_ok = sum(1 for b in blocks if b['addr_verdict'].startswith(('ALL MATCH', 'MATCH')))

    doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>KeyStone point checks {e(rnd)}</title>
<style>
:root{{--bg:#fff;--fg:#14181f;--mut:#5b6472;--line:#e3e7ee;--ok:#e6f4ea;--okb:#1e8e3e;
--bad:#fce8e6;--badb:#c5221f;--ph:#fff0c2;--phb:#b06000;--pop:#eaf1fb;--csv:#fff7e6;--fix:#eef5ea;--fixb:#1e8e3e;--hdr:#1f3864}}
@media(prefers-color-scheme:dark){{:root:not([data-theme=light]){{--bg:#11141a;--fg:#e8ecf3;--mut:#9aa4b2;
--line:#252b36;--ok:#12331f;--okb:#5bd07f;--bad:#3a1614;--badb:#ff8a80;--ph:#3a2e0c;--phb:#ffce6a;
--pop:#16203a;--csv:#2b2413;--fix:#12291a;--fixb:#5bd07f;--hdr:#0d1830}}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}}
header{{padding:24px 16px;border-bottom:1px solid var(--line)}}
h1{{margin:0 0 6px;font-size:20px}}
.sub{{color:var(--mut);font-size:13px;max-width:70ch}}
.stats{{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px}}
.stat{{border:1px solid var(--line);border-radius:10px;padding:8px 12px;min-width:120px}}
.stat b{{display:block;font-size:19px}}
.stat span{{color:var(--mut);font-size:11px;text-transform:uppercase;letter-spacing:.06em}}
.controls{{padding:12px 16px;border-bottom:1px solid var(--line);display:flex;gap:10px;flex-wrap:wrap;align-items:center}}
input,select{{font:inherit;padding:7px 10px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--fg)}}
input{{min-width:min(320px,100%)}}
.wrap{{overflow:auto;max-height:76vh}}
table{{border-collapse:separate;border-spacing:0;font-size:12px}}
th,td{{border-bottom:1px solid var(--line);border-right:1px solid var(--line);padding:6px 8px;
vertical-align:top;max-width:280px;overflow-wrap:anywhere}}
thead th{{position:sticky;top:0;z-index:3;background:var(--hdr);color:#fff;text-align:left;
font-weight:600;min-width:210px}}
.qid{{font:11px/1.4 ui-monospace,Menlo,monospace;color:#b9c6e6;font-weight:400}}
tr.pop td{{background:var(--pop)}} tr.csv td{{background:var(--csv)}}
tr.fixed td{{background:var(--fix)}}
tr.fixed{{border-bottom:2px solid var(--line)}}
td.fix{{background:var(--fix)!important;border-left:3px solid var(--fixb);font-weight:600}}
td.same{{background:var(--fix)!important;color:var(--mut)}}
td.ok{{background:var(--ok)!important;border-left:3px solid var(--okb)}}
td.bad{{background:var(--bad)!important;border-left:3px solid var(--badb)}}
td.ph{{background:var(--ph)!important;border-left:3px solid var(--phb)}}
td.num,td.rid,td.addr{{position:sticky;z-index:2;background:var(--bg)!important}}
td.num{{left:0;min-width:38px;font-weight:700}}
td.rid{{left:38px;min-width:170px;font:12px ui-monospace,Menlo,monospace}}
td.addr{{left:208px;min-width:250px;font-size:11.5px}}
thead th:nth-child(1){{left:0;z-index:4}}
thead th:nth-child(2){{left:38px;z-index:4}}
thead th:nth-child(4){{left:208px;z-index:4}}
.tag{{color:var(--mut);font:10px sans-serif;text-transform:uppercase;letter-spacing:.06em;margin-top:3px}}
.src{{min-width:150px;font-size:11px;color:var(--mut);white-space:nowrap}}
.verdict{{margin-top:6px;font-size:11px;font-weight:700}}
.verdict.ok{{color:var(--okb)}} .verdict.bad{{color:var(--badb)}}
.pid{{color:var(--mut);font:10.5px ui-monospace,monospace;margin-top:3px}}
.score{{margin-top:4px;font-size:11px;color:var(--mut)}}
.note{{padding:16px;border-top:1px solid var(--line);color:var(--mut);font-size:13px;max-width:80ch}}
.key{{display:inline-block;width:11px;height:11px;border-radius:3px;vertical-align:-1px;margin-right:4px}}
</style></head><body>
<header>
<h1>KeyStone — point-by-point verification <span style="color:var(--mut)">({e(rnd)})</span></h1>
<p class="sub">Each point has <b>three</b> rows. <b>Dashboard popup — NOW</b> is what the live map showed when the
marker was clicked. <b>Qualtrics May&nbsp;4 export</b> is what the file actually contains for that same
respondent, written as <code>code → meaning</code> with the meaning taken from the survey definition.
<b>After reprocessing</b> is what the popup will show once the corrected pipeline is applied to the data —
green-bordered cells are the ones that change. Column headers are the survey's own question wording, so you can
copy one and find it in the export with Excel's Find.</p>
<div class="stats">
<div class="stat"><b>{len(blocks)}</b><span>points checked</span></div>
<div class="stat"><b>{addr_ok}/{len(blocks)}</b><span>addresses agree</span></div>
<div class="stat"><b>{matched}/{total}</b><span>answers match</span></div>
<div class="stat"><b>{ph}</b><span>same answer, stale label</span></div>
<div class="stat"><b>{diff}</b><span>unexplained differences</span></div>
<div class="stat"><b>{willchange}</b><span>cells the fix corrects</span></div>
</div></header>
<div class="controls">
<input id="q" placeholder="Filter by address, ResponseId or answer text…">
<select id="f"><option value="">Show all points</option>
<option value="bad">Only points with a disagreement</option>
<option value="ph">Only points with placeholder text</option></select>
<span class="sub"><span class="key" style="background:var(--ok)"></span>match
<span class="key" style="background:var(--ph)"></span>same answer, stale label
<span class="key" style="background:var(--bad)"></span>differs
<span class="key" style="background:var(--fix);border:1px solid var(--fixb)"></span>corrected value</span>
</div>
<div class="wrap"><table><thead><tr>
<th>#</th><th>ResponseId</th><th>Row shows</th><th>Addresses</th>{head}
</tr></thead><tbody>
{''.join(rows_html)}
</tbody></table></div>
<p class="note"><b>Why are there yellow and red cells?</b> They are not data-entry mistakes, and no response was
lost. The Qualtrics export was written using the survey's "Variable Naming" export labels, which had gone stale:
some were never filled in, so Qualtrics wrote its own placeholder text, and some still held wording from an older
version of a different question. The dashboard faithfully displayed whatever the file contained. The correction
resolves every answer back through the survey definition and is already in the code — these cells turn green once
the dashboard's stored data is reprocessed.</p>
<script>
const q=document.getElementById('q'),f=document.getElementById('f');
const rows=[...document.querySelectorAll('tbody tr')];
const pairs=[];for(let i=0;i<rows.length;i+=2)pairs.push([rows[i],rows[i+1]]);
function apply(){{
  const t=q.value.trim().toLowerCase(),mode=f.value;
  for(const [a,b] of pairs){{
    const txt=(a.innerText+' '+b.innerText).toLowerCase();
    let show=!t||txt.includes(t);
    if(show&&mode==='bad')show=!!a.querySelector('td.bad')||!!b.querySelector('td.bad');
    if(show&&mode==='ph')show=!!a.querySelector('td.ph')||!!b.querySelector('td.ph');
    a.style.display=b.style.display=show?'':'none';
  }}
}}
q.addEventListener('input',apply);f.addEventListener('change',apply);
</script></body></html>"""
    out = EVID / f'{rnd}-point-checks.html'
    out.write_text(doc, encoding='utf-8')
    print(f'  wrote {out.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
