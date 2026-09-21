"""Hand-calculate every score for 10 respondents and compare with the pipeline.

Deliberately independent of api/_processing.py: this module reads the CSV with
the stdlib `csv` module, decodes each cell against the .qsf itself, and
implements the scoring arithmetic from the written model. It shares no code with
the thing it is checking, so an error in the pipeline cannot hide here by being
made twice.

The model, as documented in api/_processing.py and api/survey_logic.py:

  freq(v)      weekly=4, monthly=3, seasonal=2, yearly/annual=1, else 0
  health       min((H*.5 + R*1 + A*1 + W*.8 + T*.3) / 14.4 * 80, 80)
               + 20 (capped at 100) if the hospital answer contains "yes"
  iaq          +30 any mold cell non-empty
               +7.5 per non-empty water-problem cell (4 of them)
               +4 if "No Air-conditioning" ticked, else
               +2 if a window unit or fan is ticked and central A/C is not
               +10 if the stove answer mentions gas or propane      capped 100
  struct       year built: Before 1960 +30, 1960-1979 +20, 1980-1999 +10
               type: single wide +25, double wide +15, non-traditional +20
               condition: critical +35, poor +25, fair +15             capped 100
  overall      round(.35*health + .35*iaq + .30*struct)
  tier         <34 Low, 34-66 Medium, >=67 High

Run:  python3 scripts/audit/manual_score_check.py [n] [seed]
"""
from __future__ import annotations

import csv
import json
import pathlib
import random
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]

QSF = ('/Users/goshtasbshahriari/UF Dropbox/Goshtasb Shahriari Mehr/DTSC_Lab/'
       'Keystone_Data/Keystone_Heights_Survey_-_V1 (1).qsf')
MAY = pathlib.Path('/Users/goshtasbshahriari/UF Dropbox/Goshtasb Shahriari Mehr/'
                   'DTSC_Lab/Keystone_Data/Keystone Heights Survey - V1_May 4, 2026_16.57.csv')


# ── my own QSF decoder (not the project's) ────────────────────────────────────

def load_qsf(path: str) -> dict:
    """{qid: {code: display}} — resolving a collision to the choice that
    RecodeValues explicitly names, which is what the survey shows."""
    doc = json.loads(pathlib.Path(path).read_text(encoding='utf-8'))
    out: dict = {}
    for el in doc.get('SurveyElements', []):
        if el.get('Element') != 'SQ':
            continue
        p = el.get('Payload') or {}
        qid = p.get('QuestionID')
        if not qid:
            continue
        src = p.get('Answers') or p.get('Choices') or {}
        if isinstance(src, list):
            src = {str(i): v for i, v in enumerate(src, 1)}
        disp = {str(k): ' '.join(str((v or {}).get('Display', '')).split())
                for k, v in src.items()}
        disp = {k: v for k, v in disp.items() if v}
        if not disp:
            continue
        rec = {str(k): str(v) for k, v in (p.get('RecodeValues') or {}).items()}
        if p.get('Answers') and p.get('AnswerRecodeValues'):
            rec = {str(k): str(v) for k, v in p['AnswerRecodeValues'].items()}
        claims: dict = {}
        for k in disp:
            claims.setdefault(rec.get(k, k), []).append(k)
        codes = {}
        for code, ks in claims.items():
            if len(ks) > 1:
                explicit = [k for k in ks if k in rec]
                ks = explicit if len(explicit) == 1 else ks
            if len(ks) == 1:
                codes[code] = disp[ks[0]]
        out[qid] = codes
    return out


def read_may(path: pathlib.Path) -> tuple[list[dict], dict]:
    """Rows keyed by BOTH column name and ImportId. Only Finished rows."""
    rows = list(csv.reader(path.open(encoding='utf-8-sig')))
    names, imports = rows[0], []
    for c in rows[2]:
        c = c.strip()
        imports.append(json.loads(c).get('ImportId', '') if c.startswith('{') else '')
    fin = names.index('Finished')
    out = []
    for r in rows[3:]:
        if r[fin].strip().lower() not in ('true', '1'):
            continue
        rec = {}
        for i, v in enumerate(r):
            rec[names[i].replace('\xa0', ' ').strip()] = v
            if imports[i]:
                rec['@' + imports[i]] = v
        out.append(rec)
    return out, {}


# ── the model, written out by hand ────────────────────────────────────────────

def freq(text: str) -> int:
    v = (text or '').strip().lower()
    if 'weekly' in v:
        return 4
    if 'month' in v:
        return 3
    if 'season' in v:
        return 2
    if 'year' in v or 'annual' in v:
        return 1
    return 0


def health_score(sym: dict, hospital: str) -> tuple[int, str]:
    raw = (freq(sym['Headache']) * 0.5 + freq(sym['RespIll']) * 1.0 +
           freq(sym['asthma']) * 1.0 + freq(sym['wheeze']) * 0.8 +
           freq(sym['Tired']) * 0.3)
    s = min(raw / 14.4 * 80, 80)
    work = (f"({freq(sym['Headache'])}*.5 + {freq(sym['RespIll'])} + "
            f"{freq(sym['asthma'])} + {freq(sym['wheeze'])}*.8 + "
            f"{freq(sym['Tired'])}*.3) = {raw:g} /14.4*80 = {s:.2f}")
    if 'yes' in (hospital or '').lower():
        s = min(s + 20, 100)
        work += ' +20 hospital'
    return round(s), work


NO_MOLD = ('no', 'none', 'n/a', 'na', 'nope', '0', 'no mold',
           'not that i know', "i don't think so", 'i dont think so',
           "i don't know", 'i dont know', 'unknown', 'unsure')


def mold_evidence(mold_cell: str, other_text: str) -> tuple[bool, str]:
    """QID149 lists only SPACES plus a free-text "Other:". It has no "no mold"
    option, so a respondent with no mold says so in the text box."""
    cell = (mold_cell or '').strip()
    if not cell:
        return False, 'no answer'
    named = [p.strip() for p in cell.split(',')
             if p.strip() and p.strip().lower().rstrip(':') != 'other']
    if named:
        return True, 'named ' + '/'.join(named)
    t = (other_text or '').strip()
    if not t:
        return False, 'Other: ticked, nothing typed'
    if t.lower().rstrip('.') in NO_MOLD:
        return False, f'Other: says {t!r} — denies mold'
    return True, f'Other: {t!r}'


def iaq_score(mold_cell: str, mold_text: str, leaks: list[str],
              cool: list[str], stove: str) -> tuple[int, str]:
    """cool = the four decoded AGE answers for QID205 rows 1-4."""
    s, bits = 0.0, []
    has_mold, why = mold_evidence(mold_cell, mold_text)
    if has_mold:
        s += 30
        bits.append(f'mold +30 ({why})')
    else:
        bits.append(f'no mold ({why})')
    for i, v in enumerate(leaks, 1):
        # QID42's scale is a duration; 'none' means it never happened.
        v = (v or '').strip().lower()
        if v and v not in ('none', 'nan'):
            s += 7.5
            bits.append(f'water problem _{i} ({v}) +7.5')

    def age_given(i):
        """QID205's scale is an AGE; only a real band means they have it."""
        v = (cool[i] or '').strip().lower()
        return bool(v) and not any(t in v for t in
                                   ("don't know", 'dont know', 'not applicable'))
    central, window, fan = age_given(0), age_given(1), age_given(2)
    said_no_ac = bool((cool[3] or '').strip())
    if said_no_ac and not (central or window):
        s += 4
        bits.append('no A/C +4')
    elif (window or fan) and not central:
        s += 2
        bits.append('window/fan only, no central +2')
    if any(k in (stove or '').lower() for k in ('gas', 'propane')):
        s += 10
        bits.append('gas stove +10')
    return round(min(s, 100)), ' , '.join(bits)


def struct_score(year: str, htype: str, cond: str) -> tuple[int, str]:
    s, bits = 0, []
    y = (year or '').lower()
    if 'before 1960' in y:
        s += 30; bits.append('pre-1960 +30')
    elif '1960' in y:
        s += 20; bits.append('1960s-70s +20')
    elif '1980' in y:
        s += 10; bits.append('1980s-90s +10')
    t = (htype or '').lower()
    if 'single wide' in t:
        s += 25; bits.append('single wide +25')
    elif 'double wide' in t:
        s += 15; bits.append('double wide +15')
    elif 'non-traditional' in t or 'camper' in t:
        s += 20; bits.append('non-traditional +20')
    c = (cond or '').lower()
    if 'critical' in c or 'uninhabitable' in c:
        s += 35; bits.append('critical +35')
    elif 'poor' in c:
        s += 25; bits.append('poor +25')
    elif 'fair' in c:
        s += 15; bits.append('fair +15')
    return min(s, 100), ' , '.join(bits) or 'nothing scored'


SYMPTOM_CODES = {'1': 'weekly', '2': 'monthly', '3': 'seasonally',
                 '4': 'annually', '5': 'Never or rarely'}
HOSPITAL_CODES = {'1': 'Yes, Doctor visits for allergy.',
                  '2': 'Yes, hospitalization/visiting the emergency room for asthma attack.',
                  '3': 'Yes, Others.', '4': 'No'}
COOL_CODES = {0: 'Central Air-conditioning', 1: 'Window/Wall AC',
              2: 'Ceiling Fans', 3: 'No Air-conditioning'}


def decode(raw: str, table: dict) -> str:
    """Numeric export: the cell is a recode code."""
    v = (raw or '').strip()
    if v.endswith('.0') and v[:-2].isdigit():
        v = v[:-2]
    return table.get(v, v)


def decode_multi(raw: str, table: dict) -> str:
    """A check-all cell is a comma-joined list of codes."""
    parts = [p.strip() for p in (raw or '').split(',') if p.strip()]
    return ','.join(decode(p, table) for p in parts)


def main() -> int:
    n_want = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 21

    qsf = load_qsf(QSF)
    rows, _ = read_may(MAY)

    # What the pipeline produced for the same file.
    sys.path.insert(0, str(ROOT / 'api'))
    from _processing import load_parcel_index, process_iaq_bytes  # noqa: E402
    geo, _analysis, _s, _n, _f = process_iaq_bytes(MAY.read_bytes(), [],
                                                   load_parcel_index())
    pipeline = {f['properties']['response_id']: f['properties']
                for f in geo['features'] if f['properties'].get('response_id')}

    by_id = {r.get('ResponseId'): r for r in rows if r.get('ResponseId')}
    pool = sorted(set(by_id) & set(pipeline))
    random.Random(seed).shuffle(pool)
    picked = pool[:n_want]

    print(f'Hand-check of {len(picked)} respondents from {MAY.name} '
          f'(seed {seed}); pool of {len(pool)}\n')

    results = []
    fails = 0
    for rid in picked:
        r, got = by_id[rid], pipeline[rid]

        sym = {c: decode(r.get(c, ''), SYMPTOM_CODES)
               for c in ('Headache', 'RespIll', 'asthma', 'wheeze', 'Tired')}
        hosp = decode(r.get('Hospital Respiratory', ''), HOSPITAL_CODES)
        # QID42 / QID205 are matrices: the cell is a SCALE POINT, so decode it
        # against that question's Answers, straight out of the .qsf.
        leaks = [decode(r.get(f'Leakage 2_{i}', ''), qsf.get('QID42', {}))
                 for i in (1, 2, 3, 4)]
        cool = [decode(r.get(f'Cooling System _{i}', ''), qsf.get('QID205', {}))
                for i in (1, 2, 3, 4)]
        mold_cell = decode_multi(r.get('Mold', ''), qsf.get('QID149', {}))
        mold_text = r.get('Mold_10_TEXT', '')
        stove = decode_multi(r.get('Cooking', ''), qsf.get('QID148', {}))
        year = decode(r.get('@QID192', r.get('QID192', '')), qsf.get('QID192', {}))
        htype = decode(r.get('@QID128', r.get('QID128', '')), qsf.get('QID128', {}))
        cond = decode(r.get('@QID141', r.get('QID141', '')), qsf.get('QID141', {}))

        h, hw = health_score(sym, hosp)
        q, qw = iaq_score(mold_cell, mold_text, leaks, cool, stove)
        st, sw = struct_score(year, htype, cond)
        risk = round(0.35 * h + 0.35 * q + 0.30 * st)
        tier = 'Low' if risk < 34 else ('Medium' if risk < 67 else 'High')

        mine = {'health_score': h, 'iaq_score': q, 'struct_score': st,
                'overall_risk': risk, 'risk_tier': tier}
        bad = {k: (v, got.get(k)) for k, v in mine.items() if got.get(k) != v}
        fails += bool(bad)

        print(f"{rid}   {'MATCH' if not bad else '*** MISMATCH ***'}")
        print(f"   symptoms {sym}  hospital={hosp!r}")
        print(f"   mold={mold_cell!r} other_text={mold_text!r}")
        print(f"   water={leaks}")
        print(f"   cooling(ages)={cool}  stove={stove!r}")
        print(f"   year={year!r} type={htype!r} condition={cond!r}")
        print(f"   health {h:>3}  = {hw}")
        print(f"   iaq    {q:>3}  = {qw}")
        print(f"   struct {st:>3}  = {sw}")
        print(f"   risk   {risk:>3}  = .35*{h} + .35*{q} + .30*{st}   tier {tier}")
        if bad:
            for k, (mn, pl) in bad.items():
                print(f"   !! {k}: hand={mn!r} pipeline={pl!r}")
        print()
        results.append({'response_id': rid, 'hand': mine,
                        'pipeline': {k: got.get(k) for k in mine},
                        'match': not bad,
                        'working': {'health': hw, 'iaq': qw, 'struct': sw},
                        'inputs': {'symptoms': sym, 'hospital': hosp,
                                   'year_built': year, 'housing_type': htype,
                                   'condition': cond, 'mold': mold_cell,
                                   'mold_other_text': mold_text,
                                   'leaks': leaks, 'cooling': cool, 'stove': stove}})

    out = ROOT / 'docs' / 'plans' / 'evidence' / '2026-09-21-analysis-audit'
    out.mkdir(parents=True, exist_ok=True)
    (out / 'manual-score-check.json').write_text(json.dumps(results, indent=2))
    print(f'{len(picked) - fails}/{len(picked)} respondents match the pipeline exactly')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
