"""Which CSV column feeds which number in the Analysis panel.

Built by reading the code, not by guessing: every entry names the section of
`analysis` it lands in, the field on the IAQ feature, the QID, the CSV column
that QID resolves to in a given export, and the aggregation applied.

Run:  python3 scripts/audit/analysis_provenance.py <csv>
"""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'api'))

from _processing import (  # noqa: E402
    EXPERIENCE_FIELDS, IAQ_FEATURE_POPUP_LABELS, INTERVENTION_FIELDS,
    RELOC_FIELDS, SURVEY_QUESTIONS, _read_qualtric_csv,
)

# section → (chart/stat, how it is aggregated, the feature fields it reads)
# Mirrors _compute_iaq_analysis() line for line.
SECTIONS: list[tuple[str, str, str, tuple[str, ...]]] = [
    ('scores', 'mean_risk', 'mean of overall_risk = round(.35*health + .35*iaq + .30*struct)',
     ('health_score', 'iaq_score', 'struct_score')),
    ('scores', 'mean_health', 'mean of health_score', ('health_score',)),
    ('scores', 'mean_iaq', 'mean of iaq_score', ('iaq_score',)),
    ('scores', 'mean_struct', 'mean of struct_score', ('struct_score',)),
    ('risk_tiers', 'low / medium / high', 'count overall_risk <34 / 34-66 / >=67',
     ('overall_risk',)),
    ('health', 'respiratory_pct', "% whose answer contains weekly|month|season",
     ('respiratory_ill',)),
    ('health', 'asthma_pct', "% whose answer contains weekly|month|season",
     ('asthma_freq',)),
    ('health', 'wheeze_pct', "% whose answer contains weekly|month|season",
     ('wheeze_freq',)),
    ('health', 'mold_pct', '% with any non-empty Mold cell', ('has_mold',)),
    ('health', 'hospital_pct', "% where hospital_visit == 'yes'", ('hospital_visit',)),
    ('housing', 'types', "substring bucket: single wide / double wide / site+built / Other",
     ('housing_type',)),
    ('housing', 'conditions', 'substring bucket: good / fair / poor / critical|uninhabitable',
     ('condition',)),
    ('housing', 'year_built', "substring bucket: before 1960 / 1960 / 1980 / 2000",
     ('year_built',)),
    ('ownership', 'owner / renter / other', "exact 'Owner', exact 'Renter', remainder",
     ('ownership',)),
    ('residency', 'years_in_hre', 'n/mean/median + fixed bins over parsed float',
     ('years_in_hre',)),
    ('residency', 'anticipated_stay', 'value counts', ('anticipated_stay',)),
    ('residency', 'mh_skirting', 'value counts', ('mh_skirting',)),
    ('residency', 'reloc_factors', 'value counts per item', RELOC_FIELDS),
    ('housing_safety', 'env / social', 'value counts', ('safety_env', 'safety_social')),
    ('affordability', 'urgency / strategy', 'value counts',
     ('afford_urgency', 'afford_strategy')),
    ('interventions', 'pct_want', '% positive (numeric > max(scale/2, 3.5); text want-tokens)',
     INTERVENTION_FIELDS),
    ('experiences', 'pct_yes', '% positive (numeric > max(scale/2, 3.5); text yes/frequency)',
     EXPERIENCE_FIELDS),
    ('mobility', 'car_access / hurricane_transport', 'yes/no/not_sure/other/na',
     ('car_access', 'hurricane_transport')),
    ('demographics_ext', 'education / employment', 'value counts',
     ('education', 'employment')),
]

# Feature fields that are NOT from SURVEY_QUESTIONS: read by CSV column NAME
# in process_iaq_bytes / the score helpers.
BY_COLUMN_NAME: dict[str, str] = {
    'housing_type': 'QID128', 'year_built': 'QID192', 'condition': 'QID141',
    'ownership': 'Ownership', 'has_mold': 'Mold',
    'respiratory_ill': 'RespIll', 'asthma_freq': 'asthma',
    'wheeze_freq': 'wheeze', 'headache_freq': 'Headache', 'tired_freq': 'Tired',
    'hospital_visit': 'Hospital Respiratory',
    'health_score': 'Headache, RespIll, asthma, wheeze, Tired, Hospital Respiratory',
    'iaq_score': ('Mold, Leakage 2_1..2_4, Cooling System _1.._4, Cooking'),
    'struct_score': 'QID192, QID128, QID141',
    'overall_risk': '(derived from the three scores)',
}


def build(csv_path: pathlib.Path) -> list[dict]:
    """Resolve every analysis input to the actual column in THIS export."""
    raw, qmap = _read_qualtric_csv(csv_path.read_bytes())
    cols = list(raw.columns)

    def resolve(field: str) -> tuple[str, str, str]:
        """→ (qid, csv column, how the column was found)"""
        if field in SURVEY_QUESTIONS:
            meta = SURVEY_QUESTIONS[field]
            idx, qid = (meta[0], meta[1]) if len(meta) == 3 else (meta[0], '')
            col = qmap.get(qid)
            how = 'ImportId'
            if col is None and qid.endswith('_TEXT'):
                col = qmap.get(qid[:-5])
                how = 'ImportId (base QID)'
            if col is None:
                col, how = idx, 'HARDCODED INDEX (fallback)'
            name = cols[col] if 0 <= col < len(cols) else '<out of range>'
            return qid, f'[{col}] {name}', how
        if field in BY_COLUMN_NAME:
            name = BY_COLUMN_NAME[field]
            present = all(
                any(str(c).replace('\xa0', ' ').strip() == p.strip() for c in cols)
                for p in name.split(',')
            ) if ',' in name or name in [str(c).strip() for c in cols] else None
            return '—', name, 'by column NAME' + ('' if present is None else
                                                  ('' if present else ' — MISSING'))
        return '—', '<unknown>', '—'

    out = []
    for section, stat, agg, fields in SECTIONS:
        for f in fields:
            qid, col, how = resolve(f)
            out.append({
                'section': section, 'stat': stat, 'aggregation': agg,
                'field': f, 'qid': qid, 'column': col, 'resolved_by': how,
                'question': (SURVEY_QUESTIONS[f][-1] if f in SURVEY_QUESTIONS
                             else IAQ_FEATURE_POPUP_LABELS.get(f, '')),
            })
    return out


if __name__ == '__main__':
    path = pathlib.Path(sys.argv[1])
    rows = build(path)
    print(f'{len(rows)} analysis inputs for {path.name}\n')
    bad = [r for r in rows if 'HARDCODED' in r['resolved_by'] or 'MISSING' in r['resolved_by']]
    for r in rows:
        print(f"{r['section']:<16} {r['stat']:<34} {r['field']:<22} "
              f"{r['qid']:<12} {r['column'][:58]:<58} {r['resolved_by']}")
    print(f"\nfallback / missing: {len(bad)}")
    for r in bad:
        print('  !', r['field'], r['qid'], r['column'], r['resolved_by'])
