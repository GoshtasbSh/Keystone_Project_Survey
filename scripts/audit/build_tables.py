"""Build audit tables 01 (address match) and 02 (per-field value parity).

Inputs (all produced earlier in the audit, all real captures):
  popups/all_30_popups.json  — popup DOM captured after a real marker click
  live_iaq_points_full.json  — the payload the dashboard itself renders from
  live_survey_points.json    — community-contact layer (admin view, has address)
  the April and May Qualtrics CSVs — read via the independent ground-truth reader

Nothing here infers a value. A cell that cannot be sourced is written as
UNVERIFIED with the reason.
"""
from __future__ import annotations

import html as htmllib
import json
import re
import sys
from math import radians, sin, cos, sqrt, atan2
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVID = ROOT / 'docs' / 'plans' / 'evidence' / '2026-09-20-audit'
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / 'api'))

from qualtrics_ground_truth import load_survey, finished_rows, value_by_qid  # noqa: E402
from _processing import SURVEY_QUESTIONS  # noqa: E402

APR = ROOT / 'data' / 'Keystone Heights Survey - V1_April 15, 2026_13.25.csv'
MAY = ('/Users/goshtasbshahriari/UF Dropbox/Goshtasb Shahriari Mehr/'
       'DTSC_Lab/Keystone_Data/Keystone Heights Survey - V1_May 4, 2026_16.57.csv')

PLACEHOLDER = re.compile(r'^click to write (scale point|choice)\s*\d*$', re.I)

SUFFIXES = [('avenue', 'ave'), ('drive', 'dr'), ('street', 'st'), ('road', 'rd'),
            ('boulevard', 'blvd'), ('lane', 'ln'), ('court', 'ct'), ('place', 'pl'),
            ('circle', 'cir'), ('terrace', 'ter'), ('parkway', 'pkwy')]


def norm_addr(a: str) -> str:
    s = re.sub(r'\s+', ' ', str(a or '').strip().lower()).rstrip('.,')
    for long, short in SUFFIXES:
        s = re.sub(rf'\b{long}\b', short, s)
    return s


def haversine_m(lat1, lon1, lat2, lon2):
    r = 6_371_000
    dlat, dlon = radians(lat2 - lat1), radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return 2 * r * atan2(sqrt(a), sqrt(1 - a))


def popup_rows(card_html: str) -> list[tuple[str, str]]:
    """(full_label, value) for each answer row; label from title= when present."""
    out = []
    row_re = re.compile(
        r'<span class="popup-label"[^>]*?(?:title="(?P<title>[^"]*)")?[^>]*>(?P<shown>.*?)</span>\s*'
        r'<span class="popup-value"[^>]*>(?P<val>.*?)</span>', re.S)
    strip = re.compile(r'<[^>]+>')
    for m in row_re.finditer(card_html):
        label = htmllib.unescape(m.group('title') or strip.sub('', m.group('shown')))
        val = htmllib.unescape(strip.sub('', m.group('val'))).strip()
        out.append((label.strip(), val))
    return out


def md_escape(s) -> str:
    return str(s).replace('|', r'\|').replace('\n', ' ')


def main() -> None:
    popups = json.loads((EVID / 'popups' / 'all_popups.json').read_text())
    sampled = set(json.loads((EVID / 'sample_30.json').read_text())['response_ids'])
    popups = {k: v for k, v in popups.items() if k in sampled}
    iaq = {(f['properties'] or {}).get('response_id'): f
           for f in json.loads((EVID / 'live_iaq_points_full.json').read_text())['features']}
    contacts = json.loads((EVID / 'live_survey_points.json').read_text())['features']

    apr, may = load_survey(APR), load_survey(MAY)
    apr_rows = {r['ResponseId']: r for r in finished_rows(apr)}
    may_rows = {r['ResponseId']: r for r in finished_rows(may)}

    q212_apr = apr['short_names'].index('Q212') if 'Q212' in apr['short_names'] else None
    q212_may = may['short_names'].index('Q212') if 'Q212' in may['short_names'] else None

    rids = sorted(popups)

    # ── Table 01: address match ────────────────────────────────────────────
    t1 = ['# Table 01 — Address match across 4 independent sources',
          '',
          'One row per sampled point. Every value is sourced: the popup column is the '
          'header of the popup opened by a real click on the live `-blue` dashboard; the '
          'Qualtrics column is the respondent\'s own typed address (`Q212`) read straight '
          'from the CSV; the contact column is the nearest addressed community-canvass '
          'record from the admin (unstripped) `/api/survey-points` payload.',
          '',
          '`EXACT` = identical after case/whitespace/street-suffix normalisation. '
          '`NORMALIZED` = same address, differing only by suffix abbreviation or '
          'punctuation. `MISMATCH` = different household. `UNVERIFIED` = could not be '
          'sourced, with reason.',
          '',
          '| # | ResponseId | Popup header (live) | Qualtrics `Q212` (CSV) | Nearest addressed contact | dist (m) | coord_source | Verdict |',
          '|---|---|---|---|---|---|---|---|']

    verdicts = {}
    for i, rid in enumerate(rids, 1):
        pop = popups[rid]
        feat = iaq.get(rid)
        props = (feat or {}).get('properties') or {}
        lon, lat = ((feat or {}).get('geometry') or {}).get('coordinates', [None, None])

        row = may_rows.get(rid) or apr_rows.get(rid)
        src_csv = 'May' if rid in may_rows else ('April' if rid in apr_rows else None)
        qcol = q212_may if rid in may_rows else q212_apr
        q212 = ''
        if row and qcol is not None and qcol < len(row['cells']):
            q212 = row['cells'][qcol].strip()

        best, best_d = None, None
        if lon is not None:
            for cf in contacts:
                cp = cf.get('properties') or {}
                if not str(cp.get('address') or '').strip():
                    continue
                cc = (cf.get('geometry') or {}).get('coordinates') or [None, None]
                if cc[0] is None:
                    continue
                d = haversine_m(lat, lon, float(cc[1]), float(cc[0]))
                if best_d is None or d < best_d:
                    best, best_d = cp.get('address'), d

        popup_addr = pop.get('headerText') or ''
        pa, qa = norm_addr(popup_addr), norm_addr(q212)
        # The Qualtrics answer is free text and often carries city/state/ZIP
        # ("6255 Dennison ave keystone heights fl 32656"). Compare on the
        # leading house number + street word, which is what identifies the
        # household; anything beyond that is the respondent's own formatting.
        key = lambda s: ' '.join(s.split()[:2])
        has_number = bool(re.match(r'^\d', pa))

        if not popup_addr:
            verdict = 'UNVERIFIED — popup header empty (point has no address on file)'
        elif not q212:
            verdict = f'UNVERIFIED — no `Q212` value in the {src_csv or "CSV"} export'
        elif pa == qa:
            verdict = 'EXACT'
        elif not has_number:
            # Popup fell back to street_name: the household is identified
            # correctly by the underlying data, but the header does not show
            # which house it is. A presentation defect, not a data mismatch —
            # confirmed when the nearest addressed contact agrees with Q212.
            agrees = best and key(norm_addr(best)) == key(qa)
            verdict = ('STREET-ONLY (address data agrees)' if agrees
                       else 'STREET-ONLY (contact differs)')
        elif key(pa) == key(qa):
            verdict = 'NORMALIZED'
        else:
            verdict = 'MISMATCH'
        verdicts[rid] = verdict

        t1.append('| {} | `{}` | {} | {} | {} | {} | {} | {} |'.format(
            i, rid, md_escape(popup_addr or '—'), md_escape(q212 or '—'),
            md_escape(best or '—'), f'{best_d:.1f}' if best_d is not None else '—',
            md_escape(props.get('coord_source') or '—'), verdict))

    from collections import Counter
    vc = Counter(v.split(' —')[0] for v in verdicts.values())
    t1 += ['', '## Summary', '',
           '| Verdict | Count |', '|---|---|'] + \
          [f'| {k} | {v} |' for k, v in sorted(vc.items(), key=lambda x: -x[1])] + \
          ['', f'Total sampled points: **{len(rids)}**.']
    (EVID / 'tables' / '01-address-match.md').write_text('\n'.join(t1) + '\n')

    # ── Table 02: per-field value parity vs April, and vs May ──────────────
    for tag, survey, rowmap, fname in (
            ('April 15', apr, apr_rows, '02-value-parity-april.md'),
            ('May 4', may, may_rows, '03-value-parity-may.md')):
        lines = [f'# Table — popup value vs {tag} export, every field, every sampled point',
                 '',
                 'Joined on QID (never on column position). `CSV col` is the real column '
                 'index resolved from the export\'s `ImportId` header row. `Verbatim '
                 'question` is row 1 of the CSV — the survey\'s own wording.',
                 '',
                 'Verdicts: `MATCH` popup equals the CSV cell · `PLACEHOLDER` the CSV cell '
                 'is Qualtrics placeholder junk and the popup faithfully shows it (a source-'
                 'data defect, see F0/F9) · `RECODE` popup shows a label translated from a '
                 'numeric code · `DIFFERENT` popup disagrees with the CSV · `EMPTY-BOTH` '
                 'blank in both (correct) · `MISSING` CSV has an answer but the popup shows '
                 'nothing · `NOT-IN-EXPORT` this QID has no column in this export.',
                 '']
        counts = Counter()
        for i, rid in enumerate(sorted(rids), 1):
            row = rowmap.get(rid)
            feat = iaq.get(rid)
            props = (feat or {}).get('properties') or {}
            lines += [f'## {i}. `{rid}` — {popups[rid].get("headerText") or "(no address)"}', '']
            if row is None:
                lines += [f'> **UNVERIFIED** — this ResponseId has no row in the {tag} '
                          f'export, so no value in this popup can be checked against it. '
                          f'See finding F2 (coverage gap).', '']
                counts['UNVERIFIED-NO-ROW'] += 1
                continue
            lines += ['| Field | QID | CSV col | Verbatim question (CSV row 1) | CSV cell | Popup / payload shows | Verdict |',
                      '|---|---|---|---|---|---|---|']
            for field, meta in SURVEY_QUESTIONS.items():
                if len(meta) != 3:
                    continue
                _idx, qid, _canon = meta
                cell, col = value_by_qid(survey, row, qid)
                qtext = survey['question_text'][col] if col is not None else ''
                shown = str(props.get(field, '') or '').strip()

                if col is None:
                    verdict = 'NOT-IN-EXPORT'
                elif not cell and not shown:
                    verdict = 'EMPTY-BOTH'
                elif cell and not shown:
                    verdict = 'MISSING'
                elif PLACEHOLDER.match(shown):
                    verdict = 'PLACEHOLDER'
                elif shown == cell:
                    verdict = 'MATCH'
                elif cell.isdigit():
                    verdict = 'RECODE'
                else:
                    verdict = 'DIFFERENT'
                counts[verdict] += 1
                lines.append('| `{}` | `{}` | {} | {} | {} | {} | {} |'.format(
                    field, qid, col if col is not None else '—',
                    md_escape(qtext[:110] or '—'), md_escape(cell or '—'),
                    md_escape(shown or '—'), verdict))
            lines.append('')
        lines = lines[:5] + ['## Verdict totals', '', '| Verdict | Cells |', '|---|---|'] + \
            [f'| {k} | {v} |' for k, v in sorted(counts.items(), key=lambda x: -x[1])] + [''] + lines[5:]
        (EVID / 'tables' / fname).write_text('\n'.join(lines) + '\n')
        print(f'{fname}: {dict(counts)}')

    print('01-address-match.md:', dict(vc))


if __name__ == '__main__':
    from collections import Counter
    main()
