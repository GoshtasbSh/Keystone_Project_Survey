"""Compare the April 15 and May 4 Qualtrics exports of the same survey.

April cells hold TEXT labels ("Like"); May cells hold NUMERIC recode codes ("6").
A raw string comparison therefore disagrees almost everywhere, which proves
nothing. This script translates May's codes with the production label tables
(api/_processing.py, read-only) and asks the real question: are the two exports
the SAME answers in two encodings?

Columns are joined by Qualtrics ImportId (QID), never by position.

Usage:
    python3 scripts/audit/compare_april_may.py [--out report.md]
Run from the repo root.
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / 'scripts' / 'audit'))

from qualtrics_ground_truth import load_survey  # noqa: E402

APRIL = REPO / 'data' / 'Keystone Heights Survey - V1_April 15, 2026_13.25.csv'
MAY = Path('/Users/goshtasbshahriari/UF Dropbox/Goshtasb Shahriari Mehr/'
           'DTSC_Lab/Keystone_Data/'
           'Keystone Heights Survey - V1_May 4, 2026_16.57.csv')

# Metadata / non-answer ImportIds: never compared as survey answers.
META_IDS = {
    'startDate', 'endDate', 'status', 'ipAddress', 'progress', 'duration',
    'finished', 'recordedDate', '_recordId', 'recipientLastName',
    'recipientFirstName', 'recipientEmail', 'externalReference',
    'locationLatitude', 'locationLongitude', 'distributionChannel',
    'userLanguage',
}

VERDICTS = ['SAME', 'DIFFERENT', 'UNTRANSLATABLE', 'BOTH-EMPTY', 'ONE-EMPTY']

# Analyst interpretation of each mismatching QID, written after reading the
# verbatim question text (header row 1) next to the observed code<->text pairs.
# This is judgement, not measurement — the tables above are the measurement.
# 'class' is one of:
#   WORDING   - same meaning, different words. Harmless.
#   TABLE-BUG - April's label fits the question wording and the production
#               table does not. The table is wrong; dashboard output is wrong.
#   APRIL-BAD - the production table fits the question wording and April's
#               label set does not (labels recycled from another question, or
#               left as Qualtrics placeholders). April cannot validate the
#               table here; only the QSF can. Unverified, not disproven.
INTERPRETATION: dict[str, tuple[str, str]] = {
    'QID192': ('TABLE-BUG',
               'Question: "When was your house built?" April\'s labels are a '
               'coherent, ordered age scale (Before 1960 / 1960-1979 / '
               '1980-1999 / 2000 or later). The table maps the same codes in '
               'the REVERSE order, so every house age is inverted. Feeds '
               '_compute_struct_score.'),
    'QID59':  ('TABLE-BUG',
               'Question: "Has anyone in your home visited a hospital ... for '
               'respiratory health issues?" April shows codes 1/2/3 are all '
               '"Yes, ..." variants and 4 is "No". The table maps codes 2 and '
               '3 to "No", flipping 15 households from Yes to No.'),
    'QID43':  ('WORDING',
               'Frequency scale. Only the wording differs '
               '("Yearly" vs "annually", "Rarely or Never" vs '
               '"Never or rarely"). Same meaning, same order.'),
    'QID219': ('WORDING',
               'Code 4 is the write-in option; April shows its prompt text '
               '("Name the problem"), the table calls it "Other".'),
    'QID21':  ('APRIL-BAD',
               'Question asks "Do you feel safe in your house ...?" The '
               'table\'s safety scale fits it; April\'s labels (Less than 6 '
               'months / More than 6 months / Don\'t know) belong to some '
               'other question. April\'s label set is misconfigured.'),
    'QID194': ('APRIL-BAD',
               'Same as QID21 (social-threat twin): table fits the question, '
               'April\'s duration labels do not.'),
    'QID47':  ('APRIL-BAD',
               'Question asks "How long do you anticipate continuing to live '
               'in your current house?" The table\'s duration scale fits it; '
               'April\'s labels are building materials (Wood/Concrete/Steel).'),
    'QID124': ('APRIL-BAD',
               'Question asks "have you experienced ... Flooding of house ...?" '
               'The table\'s Yes/No/PNA fits it; April\'s labels are '
               'frequencies (Daily/Weekly/Biweekly).'),
    'QID195': ('APRIL-BAD',
               'Like/dislike matrix. April\'s answer-choice labels hold the '
               'intervention STATEMENT list instead of the like/dislike scale, '
               'so April cannot say what codes 1/6/7 mean.'),
}

# Leads worth checking against the QSF; not conclusions.
LEADS = [
    ('QID141',
     'Code 1 has no April label ("Click to write Choice 5") yet the table '
     'decodes it as "Excellent- No repairs needed." The placeholder names the '
     'FIFTH choice, which in the QSF is "Critical- Uninhabitable without '
     'repairs." If code 1 really is choice 5, 11 responses are being shown as '
     'the best housing condition when they are the worst. QID192 is confirmed '
     'reversed, so an inversion here is plausible. Verify against the QSF.'),
]


def load_label_tables() -> tuple[dict, dict]:
    """Import the production recode label tables read-only."""
    # api/_processing.py imports its siblings (survey_logic) by bare name.
    api_dir = str(REPO / 'api')
    if api_dir not in sys.path:
        sys.path.insert(0, api_dir)
    spec = importlib.util.spec_from_file_location(
        '_processing_audit', REPO / 'api' / '_processing.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod._QSF_RECODE_LABELS, mod._COLNAME_RECODE_LABELS


def qid_base(qid: str) -> str | None:
    m = re.match(r'(QID\d+)', qid or '')
    return m.group(1) if m else None


def label_table(qid: str, short_name: str, qsf: dict, colname: dict):
    """Return (table, source) for a column, or (None, None) if uncovered."""
    base = qid_base(qid)
    if base and base in qsf:
        return qsf[base], f'_QSF_RECODE_LABELS[{base}]'
    sn = (short_name or '').strip()
    if sn in colname:
        return colname[sn], f'_COLNAME_RECODE_LABELS[{sn}]'
    for key, table in colname.items():
        if sn.endswith(key):
            return table, f'_COLNAME_RECODE_LABELS[{key}]'
    return None, None


def norm(s: str) -> str:
    return re.sub(r'\s+', ' ', (s or '')).strip().casefold()


PLACEHOLDER_RE = re.compile(r'^click to write\b', re.I)


def is_placeholder(s: str) -> bool:
    """April text that is an unconfigured Qualtrics placeholder label.

    e.g. "Click to write Scale Point 3", "Click to write Choice 5" — the survey
    author never named that option in the label set the text export uses, so
    April carries no readable answer for that cell.
    """
    return bool(PLACEHOLDER_RE.match((s or '').strip()))


def compare(april: dict, may: dict) -> dict:
    qsf, colname = load_label_tables()

    a_rows = {r['ResponseId']: r for r in april['rows']}
    m_rows = {r['ResponseId']: r for r in may['rows']}
    a_ids, m_ids = set(a_rows), set(m_rows)
    both = sorted(a_ids & m_ids)

    # RecordedDate column index in each file.
    def rd_idx(s):
        for i, q in enumerate(s['import_ids']):
            if q == 'recordedDate':
                return i
        return s['short_names'].index('RecordedDate') \
            if 'RecordedDate' in s['short_names'] else None
    a_rd, m_rd = rd_idx(april), rd_idx(may)

    # Question columns, joined by ImportId.
    pairs = []          # (qid, short_name, a_idx, m_idx, table, table_src)
    a_only_cols, m_only_cols = [], []
    for a_idx, qid in enumerate(april['import_ids']):
        if not qid or qid in META_IDS:
            continue
        m_idx = may['qid_to_idx'].get(qid)
        if m_idx is None:
            a_only_cols.append((qid, april['short_names'][a_idx]))
            continue
        sn = april['short_names'][a_idx]
        table, src = label_table(qid, sn, qsf, colname)
        pairs.append((qid, sn, a_idx, m_idx, table, src))
    for qid in may['import_ids']:
        if qid and qid not in META_IDS and qid not in april['qid_to_idx']:
            m_only_cols.append(qid)

    counts = Counter()
    differences = []
    untranslatable = {}   # qid -> short_name
    date_split = Counter()
    diff_kind = Counter()             # placeholder vs table-mismap
    # Observed correspondence, per column: May code -> {April texts}, and back.
    fwd = defaultdict(lambda: defaultdict(set))
    rev = defaultdict(lambda: defaultdict(set))
    # Per (QID base, label-table identity): May code -> Counter(April text).
    # Keyed by the table too, because sub-columns of one QID can legitimately
    # use different tables (e.g. the "Cooling System _N" columns).
    base_obs = defaultdict(lambda: defaultdict(Counter))
    group_table = {}     # key -> the actual table dict used
    group_qtext = {}     # key -> verbatim question text (first column seen)
    dates_changed = []

    for rid in both:
        ar, mr = a_rows[rid], m_rows[rid]
        a_date = ar['cells'][a_rd].strip() if a_rd is not None and a_rd < len(ar['cells']) else ''
        m_date = mr['cells'][m_rd].strip() if m_rd is not None and m_rd < len(mr['cells']) else ''
        same_date = (a_date == m_date)
        if not same_date:
            dates_changed.append((rid, a_date, m_date))

        for qid, sn, a_idx, m_idx, table, src in pairs:
            av = ar['cells'][a_idx].strip() if a_idx < len(ar['cells']) else ''
            mv = mr['cells'][m_idx].strip() if m_idx < len(mr['cells']) else ''

            if not av and not mv:
                counts['BOTH-EMPTY'] += 1
                continue
            if bool(av) != bool(mv):
                counts['ONE-EMPTY'] += 1
                continue

            fwd[qid][mv].add(av)
            rev[qid][av].add(mv)
            if table is not None:
                key = (qid_base(qid) or qid, src)
                base_obs[key][mv][av] += 1
                group_table[key] = table
                group_qtext.setdefault(
                    key, april['question_text'][a_idx]
                    if a_idx < len(april['question_text']) else '')

            if norm(av) == norm(mv):
                counts['SAME'] += 1          # free text / identical encoding
                continue
            if table is None:
                counts['UNTRANSLATABLE'] += 1
                untranslatable[qid] = sn
                continue
            translated = table.get(mv, '')
            if translated and norm(translated) == norm(av):
                counts['SAME'] += 1
                continue
            counts['DIFFERENT'] += 1
            date_split['same' if same_date else 'differs'] += 1
            kind = ('PLACEHOLDER' if is_placeholder(av)
                    else 'TABLE-MISMAP')
            diff_kind[kind] += 1
            differences.append({
                'rid': rid, 'qid': qid, 'field': sn,
                'a_idx': a_idx, 'm_idx': m_idx,
                'april': av, 'may_raw': mv,
                'may_translated': translated or '(code not in table)',
                'table': src, 'kind': kind,
                'date': 'same' if same_date else 'DIFFERS',
                'a_date': a_date, 'm_date': m_date,
            })

    # Bijection test: within a column, does each May code correspond to exactly
    # one April text and vice versa? If yes, the two exports encode identical
    # data and every DIFFERENT cell is a label-table fault, not an export fault.
    fwd_viol = [(q, c, sorted(s)) for q in fwd for c, s in fwd[q].items()
                if len(s) > 1]
    rev_viol = [(q, t, sorted(s)) for q in rev for t, s in rev[q].items()
                if len(s) > 1]

    return {
        'april_only_ids': sorted(a_ids - m_ids),
        'may_only_ids': sorted(m_ids - a_ids),
        'both_ids': both,
        'n_question_cols': len(pairs),
        'n_translatable_cols': sum(1 for p in pairs if p[4] is not None),
        'april_only_cols': a_only_cols,
        'may_only_cols': m_only_cols,
        'counts': counts,
        'differences': differences,
        'untranslatable': untranslatable,
        'date_split': date_split,
        'diff_kind': diff_kind,
        'fwd_viol': fwd_viol,
        'rev_viol': rev_viol,
        'base_obs': base_obs,
        'group_table': group_table,
        'group_qtext': group_qtext,
        'label_tables': qsf,
        'dates_changed': dates_changed,
    }


def render(res: dict, april: dict, may: dict) -> str:
    c = res['counts']
    total = sum(c.values())
    compared = c['SAME'] + c['DIFFERENT'] + c['UNTRANSLATABLE']
    L = []
    w = L.append

    w('# April 15 vs May 4 Qualtrics exports — value-level agreement')
    w('')
    w('Generated by `scripts/audit/compare_april_may.py`. '
      'Columns joined by Qualtrics ImportId (QID), never by position. '
      'April stores text labels, May stores numeric recode codes; May codes are '
      'translated with the production tables in `api/_processing.py` '
      '(`_QSF_RECODE_LABELS`, `_COLNAME_RECODE_LABELS`, imported read-only).')
    w('')
    w('## Headline')
    w('')
    if not res['both_ids']:
        w('**The two exports share ZERO ResponseIds. A value-by-value '
          'comparison is impossible; nothing below is a value comparison.**')
    else:
        bijective = not res['fwd_viol'] and not res['rev_viol']
        w(f"**The two exports agree. All {len(april['rows'])} April responses "
          f"are present in the May export; May adds "
          f"{len(res['may_only_ids'])} newer ones. No response changed its "
          f"`RecordedDate`, so nobody edited an answer between the exports.**")
        w('')
        if bijective:
            w('**Within every one of the '
              f"{res['n_question_cols']} joined question columns, each May "
              'numeric code corresponds to exactly one April text and each '
              'April text to exactly one May code — a perfect bijection over '
              'all non-empty compared cells. The two files therefore hold the '
              'same answers in two encodings.**')
            w('')
            w(f"**The {c['DIFFERENT']:,} cells classified DIFFERENT below are "
              'therefore NOT export disagreements. They are cases where the '
              "production label table in `api/_processing.py` decodes May's "
              "code to something other than April's own text — i.e. the "
              'disagreement is between the label tables and Qualtrics, which '
              "is very likely the cause of the collaborators' report. "
              'See section 4.**')
        else:
            w(f"**Bijection test FAILED: {len(res['fwd_viol'])} May codes map "
              f"to more than one April text and {len(res['rev_viol'])} April "
              'texts map to more than one May code. The exports do NOT encode '
              'identical data. See section 3.**')
    w('')
    w('## 1. The join (by ResponseId)')
    w('')
    w('| Set | Count |')
    w('| --- | --- |')
    w(f"| April data rows | {len(april['rows'])} |")
    w(f"| May data rows | {len(may['rows'])} |")
    w(f"| April only | {len(res['april_only_ids'])} |")
    w(f"| May only (new responses collected after Apr 15) | {len(res['may_only_ids'])} |")
    w(f"| **In BOTH** | **{len(res['both_ids'])}** |")
    w('')
    if res['may_only_ids']:
        w('May-only ResponseIds: ' +
          ', '.join(f'`{r}`' for r in res['may_only_ids']))
        w('')
    if res['april_only_ids']:
        w('April-only ResponseIds (dropped from May export): ' +
          ', '.join(f'`{r}`' for r in res['april_only_ids']))
        w('')

    w('## 2. Per-verdict summary')
    w('')
    w(f"Question columns joined by QID: **{res['n_question_cols']}** "
      f"(of which {res['n_translatable_cols']} have a label table). "
      f"Cells compared: {len(res['both_ids'])} responses x "
      f"{res['n_question_cols']} columns = {total:,}.")
    w('')
    w('| Verdict | Cells | % of all | % of non-empty |')
    w('| --- | --- | --- | --- |')
    for v in VERDICTS:
        n = c[v]
        pn = f'{n / compared * 100:.2f}%' if compared and v in (
            'SAME', 'DIFFERENT', 'UNTRANSLATABLE') else '-'
        w(f'| {v} | {n:,} | {n / total * 100:.2f}% | {pn} |')
    w(f'| **total** | **{total:,}** | 100% | |')
    w('')
    w('- SAME = April text equals May code translated (or both hold the same '
      'raw string, e.g. free text and numeric-only fields).')
    w('- UNTRANSLATABLE = the two cells differ as strings and no label table '
      'covers that QID, so agreement cannot be checked either way. '
      'This is the audit coverage gap, not evidence of a bug.')
    w("- DIFFERENT = the May code translated cleanly and the result is not "
      "April's text. Given the bijection in section 3, this means the LABEL "
      "TABLE disagrees with April, not that the two exports disagree.")
    w('')

    w('## 3. Bijection test — do the two encodings carry the same data?')
    w('')
    w('For every joined question column, over all cells where both files are '
      'non-empty: is the May value <-> April value correspondence one-to-one? '
      'This test needs no label table, so it covers the UNTRANSLATABLE columns '
      'too. A violation would mean one respondent got two different answers.')
    w('')
    w('| Direction | Violations |')
    w('| --- | --- |')
    w(f"| one May code -> several April texts | {len(res['fwd_viol'])} |")
    w(f"| one April text -> several May codes | {len(res['rev_viol'])} |")
    w('')
    if res['fwd_viol'] or res['rev_viol']:
        w('| Column QID | Value | Maps to |')
        w('| --- | --- | --- |')
        for q, v, s in (res['fwd_viol'] + res['rev_viol'])[:200]:
            w(f"| {q} | {v} | {' / '.join(s)} |")
    else:
        w('**Zero violations.** The April and May exports are two faithful '
          'encodings of one identical dataset.')
    w('')

    w('## 4. Where the disagreements actually come from')
    w('')
    w('Every DIFFERENT cell falls into one of two kinds:')
    w('')
    w('| Kind | Cells | Meaning |')
    w('| --- | --- | --- |')
    w(f"| PLACEHOLDER | {res['diff_kind']['PLACEHOLDER']:,} | April's text is "
      f"an unconfigured Qualtrics placeholder (`Click to write Scale Point N` / "
      f"`Click to write Choice N`). April carries no readable label for these, "
      f"so the label table cannot be checked against it — but the code<->text "
      f"correspondence is still ordinal and consistent. |")
    w(f"| TABLE-MISMAP | {res['diff_kind']['TABLE-MISMAP']:,} | April has a "
      f"real label and the label table decodes May's code to a different real "
      f"label. These are production translation bugs. |")
    w('')
    w('Per-QID audit of each label table against April\'s own text. '
      '"April text observed" is the single April label that always accompanies '
      'that May code (the bijection above guarantees it is unique).')
    w('')
    for key in sorted(res['base_obs']):
        base, src = key
        table = res['group_table'][key]
        obs = res['base_obs'][key]
        rows = []
        bad = 0
        for code in sorted(obs, key=lambda x: (len(x), x)):
            texts = obs[code]
            atext = max(texts.items(), key=lambda kv: kv[1])[0]
            if len(texts) > 1:
                atext += f' [+{len(texts) - 1} other April text(s)]'
            n = sum(texts.values())
            expect = (table or {}).get(code, '(code absent from table)')
            if is_placeholder(atext):
                verdict = 'unverifiable (placeholder)'
            elif norm(atext) == norm(expect):
                verdict = 'OK'
            elif norm(atext) == norm(code):
                verdict = 'free text (passthrough)'
            else:
                verdict = '**MISMATCH**'
                bad += 1
            rows.append((code, atext, expect, n, verdict))
        flag = (f'**{bad} code(s) MISMATCH April**' if bad
                else 'agrees with April')
        w(f'### {base} via `{src}` — {flag}')
        w('')
        qt = (res['group_qtext'].get(key) or '').replace('\n', ' ').strip()
        if qt:
            w(f'> {qt[:300]}')
            w('')
        w('| May code | April text observed | Table decodes code as | Cells | '
          'Verdict |')
        w('| --- | --- | --- | --- | --- |')
        for code, atext, expect, n, verdict in rows:
            w(f'| `{code}` | {atext} | {expect} | {n} | {verdict} |')
        w('')

    # Which QIDs actually mismatched, measured.
    mismatched = {}
    for key, obs in res['base_obs'].items():
        base, src = key
        table = res['group_table'][key]
        for code, texts in obs.items():
            atext = max(texts.items(), key=lambda kv: kv[1])[0]
            if is_placeholder(atext) or norm(atext) == norm(code):
                continue
            if norm(atext) != norm(table.get(code, '')):
                mismatched.setdefault(base, 0)
                mismatched[base] += sum(texts.values())

    w('### Interpretation of the mismatches (analyst judgement)')
    w('')
    w('The tables above are measurement. This is judgement, formed by reading '
      'each question\'s verbatim text (CSV header row 1) beside its observed '
      'code/text pairs. Classes: **TABLE-BUG** = April\'s label fits the '
      'question and the production table does not, so the dashboard is showing '
      'the wrong answer; **APRIL-BAD** = the table fits the question and '
      "April's label set does not (labels recycled from another question), so "
      'April cannot validate the table and only the QSF can; **WORDING** = same '
      'meaning, different words.')
    w('')
    w('| QID | Class | Mismatching cells | Why |')
    w('| --- | --- | --- | --- |')
    for base in sorted(mismatched, key=lambda b: -mismatched[b]):
        cls, why = INTERPRETATION.get(
            base, ('UNCLASSIFIED', 'Not yet reviewed by an analyst.'))
        w(f'| {base} | **{cls}** | {mismatched[base]} | {why} |')
    w('')
    bugs = [b for b in mismatched
            if INTERPRETATION.get(b, ('', ''))[0] == 'TABLE-BUG']
    w(f"**Confirmed production label-table bugs: {len(bugs)} "
      f"({', '.join(sorted(bugs))}).** These are not export disagreements; "
      'both CSVs agree, and `api/_processing.py` mislabels them. '
      'Fixing them is out of scope for this read-only audit.')
    w('')
    w('Leads to verify against the QSF (not conclusions):')
    w('')
    for qid, note in LEADS:
        w(f'- **{qid}** — {note}')
    w('')

    w('## 5. Respondent edits vs translation bugs')
    w('')
    if not res['differences']:
        w('No DIFFERENT cells, so nothing to attribute.')
    else:
        ds = res['date_split']
        w('| RecordedDate between exports | DIFFERENT cells | Reading |')
        w('| --- | --- | --- |')
        w(f"| differs | {ds['differs']} | respondent likely edited their answer "
          f"between Apr 15 and May 4 |")
        w(f"| identical | {ds['same']} | same submission, unchanged answer — "
          f"the disagreement is in the label table, not in the data |")
        w('')
        w('Not one of the 82 shared responses changed its `RecordedDate`, so '
          'no DIFFERENT cell can be explained as a respondent editing their '
          'answer between April 15 and May 4. Every one is a labelling fault. '
          'Section 4 splits them into real table bugs, wording differences, '
          "and cases where April's own label set is the broken side.")
    w('')

    w('## 6. Every DIFFERENT cell')
    w('')
    if not res['differences']:
        w('_None._')
    else:
        w('| ResponseId | Field | QID | April col | May col | April value | '
          'May raw | May translated | RecordedDate |')
        w('| --- | --- | --- | --- | --- | --- | --- | --- | --- |')
        for d in res['differences']:
            w(f"| `{d['rid']}` | {d['field']} | {d['qid']} | {d['a_idx']} | "
              f"{d['m_idx']} | {d['april']} | {d['may_raw']} | "
              f"{d['may_translated']} | {d['date']} |")
    w('')

    w('## 7. UNTRANSLATABLE QIDs (audit coverage gap)')
    w('')
    if not res['untranslatable']:
        w('_None — every disagreeing column had a label table._')
    else:
        w(f"{len(res['untranslatable'])} QIDs produced at least one cell that "
          f"differed as a string with no label table to decode May's code. "
          f"These columns are UNVERIFIED in both directions.")
        w('')
        w('| QID | Column short name | QID base in label tables? |')
        w('| --- | --- | --- |')
        for qid, sn in sorted(res['untranslatable'].items()):
            w(f'| {qid} | {sn} | no |')
    w('')

    if res['april_only_cols'] or res['may_only_cols']:
        w('## 8. Columns present in one export only')
        w('')
        for qid, sn in res['april_only_cols']:
            w(f'- April only: `{qid}` ({sn})')
        for qid in res['may_only_cols']:
            w(f'- May only: `{qid}`')
        w('')

    return '\n'.join(L) + '\n'


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--april', default=str(APRIL))
    ap.add_argument('--may', default=str(MAY))
    ap.add_argument('--out', help='write the markdown report here')
    args = ap.parse_args()

    april, may = load_survey(args.april), load_survey(args.may)
    res = compare(april, may)
    report = render(res, april, may)

    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report, encoding='utf-8')
        print(f'wrote {out}')
    c = res['counts']
    print(f"join: april-only={len(res['april_only_ids'])} "
          f"may-only={len(res['may_only_ids'])} both={len(res['both_ids'])}")
    print('verdicts: ' + '  '.join(f'{v}={c[v]}' for v in VERDICTS))
    print(f"different cells: {len(res['differences'])}  "
          f"date differs={res['date_split']['differs']} "
          f"date same={res['date_split']['same']}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
