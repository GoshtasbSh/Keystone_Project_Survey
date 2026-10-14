"""Independent recompute of the KeyStone IAQ survey analysis (launch gate).

Reads the raw Qualtrics CSV and QSF with its OWN parser and decoding. It never
imports api/*, so a bug in the pipeline cannot hide itself here. It encodes the
post-fix semantics agreed for launch (2026-10-13):

  * preview filter: Status in {1, 2, 8, 9, 17} excluded; Status 0 and 16 kept
  * latest-per-household: of the placed responses that share one point, only
    the newest RecordedDate is analysed (the others are "superseded"). The
    blob keeps them in geojson.superseded_features with superseded_by=<kept
    id>; the gate checks that the blob's choice agrees with this one.
  * years in HRE: a bare number is years ("1" -> 1); "N mo/months" -> N/12
  * mold "Other" text: "no evidence ..." is a denial
  * cooling: a cell counts as having that system if ANY selected part is an
    age band (so "<10 yrs" + "Don't know" is AC)
  * cooking: "propane" typed in the Other box (QID148_4_TEXT) scores as gas
  * anticipated stay (QID47) is multi-answer: each choice counted separately
  * means rounded half-up to 1 decimal; per-response scores rounded half-up
    after a 9-place pre-round (0.35*90 is 31.5, not 31.4999...); risk is the
    exact integer (35h + 35i + 30s + 50) // 100, as PROC-8 computes it
  * shared-code labels: --shared-code picks which of the two choices a
    colliding code means. "decided" (the default) is the PI's reading of
    2026-10-13 that the pipeline ships: QID141 code 1 = Excellent, QID100 /
    QID221 code 1 = Yes and code 2 = "No / Not applicable", QID17 as before.
    "current" is the pre-decision dashboard reading (code 1 = Critical).
    Structural points follow the resolved condition label.

Placement (which responses are on the map) is NOT recomputed: the 15 unplaced
responses are left as is by decision, so the placed set is read from the blob
and only checked against the expected ResponseId lists by reconcile_responses.

Usage:
  .venv/bin/python scripts/audit/recompute_independent.py \
      --csv  "../Keystone_Data/Keystone Heights Survey - V1_October 7, 2026_00.47.csv" \
      --qsf  "../Keystone_Data/Shimberg_Handover_2026-10-07/2_qualtrics_october_2026/Keystone_Heights_Survey_V1.qsf" \
      --blob "$GATE/after/dd_iaq_survey.json" \
      --allow "$GATE/recompute_allowlist.json" \
      [--shared-code decided|current|alternate] [--rounding half_up|half_even]
Exit 0 = no unexplained mismatch.
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import re
import sys
from decimal import Decimal, ROUND_HALF_EVEN, ROUND_HALF_UP

PREVIEW_STATUSES = {'1', '2', '8', '9', '17'}

# code -> QSF choice id, for codes that RecodeValues gives to two choices.
# "current" is what the dashboard showed before the PI decision (verified
# against the April text export for every overlapping respondent).
# "alternate" is the other choice of each collision. "decided" is the PI's
# per-question reading of 2026-10-13 (api/survey_logic.SHARED_CODE_RESOLUTION;
# a test keeps the two equal without this script importing api/).
SHARED_CODE_CHOICES = {
    'current':   {'QID141': {'1': '5'}, 'QID17': {'1': '3', '2': '4'},
                  'QID100': {'1': '3', '2': '4'}, 'QID221': {'1': '3', '2': '4'}},
    'alternate': {'QID141': {'1': '1'}, 'QID17': {'1': '1', '2': '2'},
                  'QID100': {'1': '1', '2': '2'}, 'QID221': {'1': '1', '2': '2'}},
    'decided':   {'QID141': {'1': '1'}, 'QID17': {'1': '3', '2': '4'},
                  'QID100': {'1': '1', '2': '2'}, 'QID221': {'1': '1', '2': '2'}},
}
# Wording the PI decided for a code whose two choices the evidence cannot
# separate (code 2 holds every site-built house as well as mobile homes
# answering No), by mode: (qid, code) -> label.
SHARED_CODE_LABELS = {
    'current': {},
    'alternate': {},
    'decided': {('QID100', '2'): 'No / Not applicable',
                ('QID221', '2'): 'No / Not applicable'},
}
DEFAULT_SHARED_CODE = 'decided'

FREQ = {'1': 4, '2': 3, '3': 2, '4': 1, '5': 0}
NO_MOLD = re.compile(
    r"^(no|none|n/?a|nope|0|no mold|not that i know(\s+of)?|(i\s+)?don'?t (think so|know)"
    r"|unknown|unsure|no\s*where\s+vis[ai]ble|nowhere\s+vis[ai]ble|(none|not)\s+vis[ai]ble"
    r"|no evidence(\s+(to my knowledge|of (any )?mold))?)\.?$", re.I)
PROPANE = re.compile(r'\bpropane\b', re.I)
YEARS_RE = re.compile(
    r'^\s*(?P<n>\d+(?:\.\d+)?|\.\d+)(?:\s+(?P<fn>\d)/(?P<fd>\d))?\s*'
    r'(?P<unit>months?|mos?|years?|yrs?|y)?\b', re.I)


ROUNDING = {'mode': ROUND_HALF_UP}   # set by --rounding


def half_up(x: float, places: int = 0) -> float:
    """Launch rounding rule. Rounds to 9 places first so binary noise
    (0.35*90 = 31.499999999999996) cannot flip a true half — the same
    rule as api/_processing._round_half_up."""
    q = Decimal('1') if places == 0 else Decimal('1.' + '0' * places)
    v = Decimal(repr(round(float(x), 9))).quantize(q, rounding=ROUNDING['mode'])
    return int(v) if places == 0 else float(v)


def risk_score(health: int, iaq: int, struct: int) -> int:
    """0.35/0.35/0.30 weighting. Exact integer half-up, as the pipeline does."""
    if ROUNDING['mode'] == ROUND_HALF_UP:
        return (35 * health + 35 * iaq + 30 * struct + 50) // 100
    return round(0.35 * health + 0.35 * iaq + 0.30 * struct)


def condition_points(label: str) -> int:
    """Structural points for the resolved QID141 label."""
    t = (label or '').strip().lower()
    if t.startswith('critical') or 'uninhabitable' in t:
        return 35
    if t.startswith('poor'):
        return 25
    if t.startswith('fair'):
        return 15
    return 0


def years_value(raw: str):
    """Years in HRE from free text, or None if it holds no leading number."""
    s = (raw or '').strip()
    m = YEARS_RE.match(s)
    if not m:
        return None
    rest = s[m.end():].strip()
    if rest.startswith('/'):            # "6/25" is a date, not a duration
        return None
    n = float(m.group('n'))
    if m.group('fn'):
        n += int(m.group('fn')) / int(m.group('fd'))
    unit = (m.group('unit') or '').lower()
    return n / 12 if unit.startswith('mo') else n


def is_mold(codes: list[str], other_text: str) -> bool:
    named = [c for c in codes if c != '10']
    if named:
        return True
    if '10' not in codes:
        return False
    t = re.sub(r'\s+', ' ', other_text or '').strip()
    if not t:
        return False
    sq = re.sub(r'(?<=[a-z])0(?=[a-z])', 'o', t, flags=re.I)
    sq = re.sub(r'(.)\1+', r'\1', sq)
    return not (NO_MOLD.match(t) or NO_MOLD.match(sq))


def _strip(s) -> str:
    return ' '.join(re.sub('<[^>]+>', '', str(s)).replace('\xa0', ' ').replace('&nbsp;', ' ').split())


class Survey:
    def __init__(self, csv_path: str, qsf_path: str, shared_code: str = DEFAULT_SHARED_CODE):
        with open(csv_path, encoding='utf-8-sig') as fh:
            rows = list(csv.reader(fh))
        imp = [json.loads(c).get('ImportId') for c in rows[2]]
        self.col = {k: i for i, k in enumerate(imp)}
        self.rows = rows[3:]
        with open(qsf_path, encoding='utf-8') as fh:
            qsf = json.load(fh)
        self.Q = {e['Payload']['QuestionID']: e['Payload']
                  for e in qsf['SurveyElements'] if e.get('Element') == 'SQ'}
        self.shared_code = shared_code
        self.choice_pick = SHARED_CODE_CHOICES[shared_code]
        self.label_override = SHARED_CODE_LABELS[shared_code]
        self.maps = {}
        for q in ['QID134', 'QID47', 'QID100', 'QID221', 'QID192', 'QID128', 'QID141', 'QID21',
                  'QID194', 'QID17', 'QID19', 'QID148', 'QID149', 'QID59', 'QID211', 'QID219',
                  'QID178', 'QID176']:
            self.maps[q] = self._mc_map(q)
        for q in ['QID181', 'QID195', 'QID124', 'QID205', 'QID42', 'QID43']:
            p = self.Q[q]; rv = p.get('RecodeValues') or {}
            self.maps[q] = {str(rv.get(k, k)): _strip(a['Display']) for k, a in p['Answers'].items()}

    def _mc_map(self, qid):
        p = self.Q[qid]; ch = p['Choices']; rv = p.get('RecodeValues') or {}
        by_code = collections.defaultdict(list)
        for k in ch:
            by_code[str(rv.get(k, k))].append(k)
        out = {}
        for code, keys in by_code.items():
            k = self.choice_pick[qid][code] if len(keys) > 1 else keys[0]
            out[code] = self.label_override.get((qid, code)) or _strip(ch[k]['Display'])
        return out

    def v(self, r, imp_id):
        return r[self.col[imp_id]].strip()

    def codes(self, r, imp_id):
        raw = self.v(r, imp_id)
        return [p.strip() for p in raw.split(',') if p.strip()] if raw else []

    def rid(self, r):
        return self.v(r, '_recordId')

    def label(self, r, imp_id, base):
        return ','.join(self.maps[base].get(c, '?' + c) for c in self.codes(r, imp_id))

    def eligible(self):
        """Finished, non-preview responses."""
        return [r for r in self.rows
                if self.v(r, 'finished') == '1' and self.v(r, 'status') not in PREVIEW_STATUSES]

    def score(self, r):
        v, codes = self.v, self.codes
        h = (FREQ.get(v(r, 'QID43_1'), 0) * 0.5 + FREQ.get(v(r, 'QID43_6'), 0) * 1.0
             + FREQ.get(v(r, 'QID43_5'), 0) * 1.0 + FREQ.get(v(r, 'QID43_8'), 0) * 0.8
             + FREQ.get(v(r, 'QID43_7'), 0) * 0.3)
        hs = min(h / 14.4 * 80, 80)
        hosp = v(r, 'QID59') in ('1', '2', '3')
        if hosp:
            hs = min(hs + 20, 100)
        health = half_up(hs)
        mold = is_mold(codes(r, 'QID149'), v(r, 'QID149_11_TEXT'))
        i = 30 if mold else 0
        i += 7.5 * sum(1 for k in ('QID42_1', 'QID42_2', 'QID42_3', 'QID42_4')
                       if v(r, k) and v(r, k) != '4')
        has_age = lambda k: any(x in ('1', '2', '3') for x in codes(r, k))
        cen, win, fan = has_age('QID205_1'), has_age('QID205_2'), has_age('QID205_3')
        noac = bool(v(r, 'QID205_4'))
        if noac and not (cen or win):
            i += 4
        elif (win or fan) and not cen:
            i += 2
        gas = '1' in codes(r, 'QID148') or bool(PROPANE.search(v(r, 'QID148_4_TEXT')))
        if gas:
            i += 10
        iaq = half_up(min(i, 100))
        s = {'4': 30, '3': 20, '2': 10}.get(v(r, 'QID192'), 0)
        s += {'1': 25, '2': 15, '4': 20}.get(v(r, 'QID128'), 0)
        cond = v(r, 'QID141')
        s += condition_points(self.maps['QID141'].get(cond, '')) if cond else 0
        struct = half_up(min(s, 100))
        risk = risk_score(health, iaq, struct)
        return {'health': health, 'iaq': iaq, 'struct': struct, 'risk': risk,
                'mold': mold, 'hosp': hosp}


def superseded_ids(features: list, recorded: dict) -> dict:
    """{earlier ResponseId: kept ResponseId} for placed responses sharing a point."""
    by_pt = collections.defaultdict(list)
    for f in features:
        by_pt[tuple(round(c, 7) for c in f['geometry']['coordinates'])].append(
            f['properties']['response_id'])
    out = {}
    for ids in by_pt.values():
        if len(ids) < 2:
            continue
        keep = max(ids, key=lambda x: recorded.get(x, ''))
        for x in ids:
            if x != keep:
                out[x] = keep
    return out


def placed_and_superseded(geojson: dict, recorded: dict):
    """(every placed feature, my {earlier: kept}, superseded problems).

    Placed = drawn ``features`` + ``superseded_features`` (MATCH-3 keeps the
    earlier answers there). A feature in ``features`` that carries
    ``superseded_by`` (the older contract) also counts as flagged. Each
    disagreement between the blob's flags and the latest-RecordedDate rule is
    one problem ``superseded.<rid>``."""
    feats = list(geojson.get('features') or []) + list(geojson.get('superseded_features') or [])
    sup = superseded_ids(feats, recorded)
    held = {f['properties']['response_id'] for f in geojson.get('superseded_features') or []}
    flagged = {}
    for f in feats:
        p = f['properties']
        if p['response_id'] in held or p.get('superseded_by') or p.get('superseded'):
            flagged[p['response_id']] = p.get('superseded_by') or '<no superseded_by>'
    problems = [(f'superseded.{rid}', sup.get(rid), flagged.get(rid))
                for rid in sorted(set(sup) | set(flagged)) if sup.get(rid) != flagged.get(rid)]
    return feats, sup, problems


def aggregate(sv: Survey, R: list, S: dict) -> dict:
    v, C = sv.v, collections.Counter
    n = len(R)
    sc = [S[sv.rid(r)] for r in R]
    mean = lambda L: half_up(sum(L) / len(L), 1) if L else 0
    pct = lambda k: half_up(k / n * 100, 1) if n else 0
    A = {'n_responses': n}
    A['scores'] = {'mean_risk': mean([s['risk'] for s in sc]), 'mean_health': mean([s['health'] for s in sc]),
                   'mean_iaq': mean([s['iaq'] for s in sc]), 'mean_struct': mean([s['struct'] for s in sc])}
    rk = [s['risk'] for s in sc]
    A['risk_tiers'] = {'low': sum(x < 34 for x in rk), 'medium': sum(34 <= x < 67 for x in rk),
                       'high': sum(x >= 67 for x in rk)}
    act = lambda q: pct(sum(v(r, q) in ('1', '2', '3') for r in R))
    A['health'] = {'respiratory_pct': act('QID43_6'), 'asthma_pct': act('QID43_5'), 'wheeze_pct': act('QID43_8'),
                   'mold_pct': pct(sum(s['mold'] for s in sc)), 'hospital_pct': pct(sum(s['hosp'] for s in sc))}
    cond_lab = sv.maps['QID141']
    A['housing'] = {
        'types': dict(C({'1': 'Single Wide', '2': 'Double Wide', '3': 'Site Built'}.get(v(r, 'QID128'), 'Other') for r in R)),
        'conditions': dict(C({'2': 'Good', '3': 'Fair', '4': 'Poor'}.get(v(r, 'QID141'),
                             _short_condition(cond_lab.get(v(r, 'QID141'), ''))) for r in R)),
        'year_built': dict(C({'4': 'Before 1960', '3': '1960–1979', '2': '1980–1999', '1': '2000+'}.get(v(r, 'QID192'), 'Unknown') for r in R)),
    }
    ow = C(v(r, 'QID134') for r in R)
    A['ownership'] = {'owner': ow['1'], 'renter': ow['2'], 'other': n - ow['1'] - ow['2']}
    yv = [y for y in (years_value(v(r, 'QID12_TEXT')) for r in R) if y is not None]
    ys = sorted(yv); k = len(ys)
    med = (ys[k // 2] if k % 2 else (ys[k // 2 - 1] + ys[k // 2]) / 2) if k else 0
    bins = C('<1 yr' if x < 1 else '1–4' if x < 5 else '5–9' if x < 10 else '10–19' if x < 20
             else '20–29' if x < 30 else '30+' for x in yv)

    def single(q, base=None):
        c = C()
        for r in R:
            if v(r, q):
                c[sv.label(r, q, base or q)] += 1
        return dict(c)

    def multi(q):
        c = C()
        for r in R:
            for p in sv.codes(r, q):
                c[sv.maps[q][p]] += 1
        return dict(c)

    RF = ['reloc_factor_emp', 'reloc_factor_aff', 'reloc_factor_qol', 'reloc_factor_fam',
          'reloc_factor_ret', 'reloc_factor_env', 'reloc_factor_inh', 'reloc_factor_oth']
    A['residency'] = {
        'years_in_hre': {'n_valid': k, 'mean': half_up(sum(yv) / k, 1) if k else 0,
                         'median': half_up(med, 1), 'distribution': dict(bins)},
        'anticipated_stay': multi('QID47'), 'mh_skirting': single('QID100'),
        'reloc_factors': {f: single('QID181_%d' % i, 'QID181') for i, f in enumerate(RF, 1)}}
    A['housing_safety'] = {'env': single('QID21'), 'social': single('QID194')}
    A['affordability'] = {'urgency': single('QID17'), 'strategy': multi('QID19')}
    IF = ['intv_roof_walls', 'intv_windows_doors', 'intv_rain_gardens', 'intv_hvac', 'intv_plumbing_elec',
          'intv_well_septic', 'intv_ccua_water', 'intv_fence', 'intv_trees_shade', 'intv_trim_trees', 'intv_drainage']
    EF = ['exp_flooding', 'exp_flood_help', 'exp_extreme_heat', 'exp_school_change', 'exp_law_enf',
          'exp_insurance_loss', 'exp_well_dry', 'exp_pests', 'exp_water_leaks', 'exp_loose_animals']
    A['interventions'] = {'pct_want': {f: pct(sum(v(r, 'QID195_%d' % i) == '6' for r in R)) for i, f in enumerate(IF, 1)}}
    A['experiences'] = {'pct_yes': {f: pct(sum(v(r, 'QID124_%d' % i) == '1' for r in R)) for i, f in enumerate(EF, 1)}}

    def yn(q):
        o = {'yes': 0, 'no': 0, 'not_sure': 0, 'other': 0, 'na': 0}
        for r in R:
            o[{'': 'na', '1': 'yes', '2': 'no', '3': 'not_sure'}.get(v(r, q), 'other')] += 1
        return o
    A['mobility'] = {'car_access': yn('QID211'), 'hurricane_transport': yn('QID219')}
    A['demographics_ext'] = {'education': single('QID178'), 'employment': single('QID176')}
    return A


def _short_condition(label: str) -> str:
    # "Critical - Uninhabitable" -> "Critical", "Excellent- No repairs" -> "Excellent"
    return re.split(r'\s*-\s*', label, maxsplit=1)[0].strip() or 'Unknown'


COMPARED_KEYS = ['n_responses', 'scores', 'risk_tiers', 'health', 'housing', 'ownership', 'residency',
                 'housing_safety', 'affordability', 'interventions', 'experiences', 'mobility',
                 'demographics_ext']


def diff(mine, live, path=''):
    """Leaf-level differences; keys only in the live blob's dicts that we do
    not compute (order, highlights, ...) are ignored."""
    out = []
    if isinstance(mine, dict):
        live = live if isinstance(live, dict) else {}
        for k in sorted(set(mine) | {x for x in live if x in mine}):
            out += diff(mine.get(k), live.get(k), f'{path}.{k}' if path else k)
        # a bin present live but absent here is also a mismatch (e.g. a combined multi-answer bar)
        if mine and all(not isinstance(x, dict) for x in mine.values()):
            for k in sorted(set(live) - set(mine)):
                if not isinstance(live[k], (dict, list)):
                    out.append((f'{path}.{k}', None, live[k]))
        return out
    if mine != live:
        out.append((path, mine, live))
    return out


def run(csv_path, qsf_path, blob, allow, shared_code=DEFAULT_SHARED_CODE):
    sv = Survey(csv_path, qsf_path, shared_code)
    rows = {sv.rid(r): r for r in sv.rows}
    recorded = {k: sv.v(r, 'recordedDate') for k, r in rows.items()}
    feats, sup, problems = placed_and_superseded(blob['geojson'], recorded)
    elig = {sv.rid(r) for r in sv.eligible()}
    placed = [f['properties']['response_id'] for f in feats]
    for x in placed:
        if x not in rows:
            problems.append((f'placed.{x}', 'in CSV', 'not in CSV'))
        elif x not in elig:
            problems.append((f'placed.{x}', 'eligible', 'not eligible (unfinished or preview)'))
    analysed = [x for x in placed if x not in sup and x in elig]
    S = {x: sv.score(rows[x]) for x in placed if x in rows}
    for f in feats:
        p = f['properties']
        s = S.get(p['response_id'])
        if s is None:
            continue
        for a, b in (('health', 'health_score'), ('iaq', 'iaq_score'), ('struct', 'struct_score'),
                     ('risk', 'overall_risk'), ('mold', 'has_mold')):
            if s[a] != p.get(b):
                problems.append((f"feature.{p['response_id']}.{b}", s[a], p.get(b)))
    mine = aggregate(sv, [rows[x] for x in analysed], S)
    for key in COMPARED_KEYS:
        problems += diff(mine[key], blob['analysis'].get(key), key)
    unexplained = [p for p in problems if p[0] not in allow]
    return {'superseded': sup, 'n_placed': len(placed), 'n_analysed': len(analysed),
            'mine': mine, 'problems': problems, 'unexplained': unexplained}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--csv', required=True)
    ap.add_argument('--qsf', required=True)
    ap.add_argument('--blob', required=True, help='keystone_dashboard_data.iaq_survey payload (JSON)')
    ap.add_argument('--allow', default=None, help='JSON {mismatch path: reason}')
    ap.add_argument('--shared-code', default=DEFAULT_SHARED_CODE, choices=sorted(SHARED_CODE_CHOICES))
    ap.add_argument('--rounding', default='half_up', choices=['half_up', 'half_even'])
    a = ap.parse_args(argv)
    ROUNDING['mode'] = ROUND_HALF_UP if a.rounding == 'half_up' else ROUND_HALF_EVEN
    with open(a.blob) as fh:
        blob = json.load(fh)
    blob = blob.get('payload', blob)
    allow = {}
    if a.allow:
        with open(a.allow) as fh:
            allow = json.load(fh)
    res = run(a.csv, a.qsf, blob, allow, a.shared_code)
    print(f"shared_code={a.shared_code} rounding={a.rounding} placed={res['n_placed']} "
          f"analysed={res['n_analysed']} superseded={len(res['superseded'])}")
    for p in res['problems']:
        tag = 'ALLOWED' if p[0] in allow else 'MISMATCH'
        print(f'{tag}\t{p[0]}\tmine={p[1]!r}\tlive={p[2]!r}' + (f'\t# {allow[p[0]]}' if p[0] in allow else ''))
    print(f"unexplained={len(res['unexplained'])}")
    return 1 if res['unexplained'] else 0


if __name__ == '__main__':
    sys.exit(main())
