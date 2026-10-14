"""recompute_independent: the independent analysis must encode the launch decisions."""
from __future__ import annotations

import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts' / 'audit'))

import recompute_independent as RI  # noqa: E402

DATA = pathlib.Path('/Users/goshtasbshahriari/UF Dropbox/Goshtasb Shahriari Mehr/DTSC_Lab/Keystone_Data')
QSF = DATA / 'Shimberg_Handover_2026-10-07' / '2_qualtrics_october_2026' / 'Keystone_Heights_Survey_V1.qsf'
OCT = DATA / 'Keystone Heights Survey - V1_October 7, 2026_00.47.csv'
HAVE_OCT = QSF.exists() and OCT.exists()


@pytest.mark.parametrize('raw,want', [
    ('1', 1.0), ('5 years', 5.0), ('40yrs', 40.0), ('4 years ', 4.0), ('7 y', 7.0),
    ('2.5 years', 2.5), ('.5', 0.5), ('2 1/2 years', 2.5),
    ('5 months', 5 / 12), ('2months ', 2 / 12), ('3 mo', 3 / 12), ('2mo', 2 / 12),
    ('6/25', None), ('No answer', None), ('Last montj', None), ('', None),
])
def test_years_value(raw, want):
    got = RI.years_value(raw)
    assert got == pytest.approx(want) if want is not None else got is None


@pytest.mark.parametrize('codes,text,want', [
    (['10'], 'no evidence to my knowledge', False),
    (['10'], 'No evidence', False),
    (['10'], 'none', False),
    (['10'], 'bathroom ceiling', True),
    (['3'], '', True),
    (['3', '10'], 'no evidence', True),
    ([], '', False),
])
def test_is_mold(codes, text, want):
    assert RI.is_mold(codes, text) is want


def test_half_up_rounds_halves_up():
    assert RI.half_up(18.35, 1) == 18.4
    assert RI.half_up(2.5) == 3
    assert RI.half_up(3.5) == 4


def test_half_up_ignores_float_noise():
    assert RI.half_up(0.35 * 90) == 32          # 31.499999999999996 is really 31.5
    assert RI.half_up(0.35 * 90 + 0.35 * 0 + 0.30 * 0) == 32


def test_risk_matches_integer_half_up():
    for h, i, s in ((0, 90, 0), (1, 29, 0), (2, 28, 0), (94, 17, 25)):
        assert RI.risk_score(h, i, s) == (35 * h + 35 * i + 30 * s + 50) // 100


def test_risk_matches_integer_half_up_over_the_whole_grid():
    # PROC-8's exact formula; the float half_up path disagreed on 531 of these.
    for h in range(101):
        for i in range(101):
            for s in range(0, 101, 5):
                assert RI.risk_score(h, i, s) == (35 * h + 35 * i + 30 * s + 50) // 100


def test_superseded_keeps_latest_recorded_date():
    feats = [{'geometry': {'coordinates': [-82.0, 29.7]}, 'properties': {'response_id': 'A'}},
             {'geometry': {'coordinates': [-82.0, 29.7]}, 'properties': {'response_id': 'B'}},
             {'geometry': {'coordinates': [-82.1, 29.7]}, 'properties': {'response_id': 'C'}}]
    rec = {'A': '2026-07-20 09:01:52', 'B': '2026-01-17 09:00:26', 'C': '2026-01-01 00:00:00'}
    assert RI.superseded_ids(feats, rec) == {'B': 'A'}


def test_struct_points_follow_the_resolved_condition_label():
    assert RI.condition_points('Critical- Uninhabitable without repairs.') == 35
    assert RI.condition_points('Poor- Major repairs needed.') == 25
    assert RI.condition_points('Fair- Some repairs needed.') == 15
    assert RI.condition_points('Excellent- No repairs needed.') == 0
    assert RI.condition_points('Good- Minor repairs needed.') == 0
    assert RI.condition_points('') == 0


def test_default_shared_code_is_the_pi_decision():
    assert RI.DEFAULT_SHARED_CODE == 'decided'
    d = RI.SHARED_CODE_CHOICES['decided']
    # PI decision 2026-10-13: QID141 code 1 = Excellent (choice 1); QID100 /
    # QID221 codes 1/2 = choices 1/2; QID17 keeps the current reading.
    assert d['QID141'] == {'1': '1'}
    assert d['QID17'] == RI.SHARED_CODE_CHOICES['current']['QID17']
    assert d['QID100'] == d['QID221'] == {'1': '1', '2': '2'}
    assert RI.SHARED_CODE_LABELS['decided'] == {('QID100', '2'): 'No / Not applicable',
                                                ('QID221', '2'): 'No / Not applicable'}


def test_decided_mode_matches_the_repo_switch():
    """The gate's default must be the reading the pipeline ships (VER contract:
    '--shared-code must match the repo constant'). Only this TEST reads api/;
    the gate script itself never imports it."""
    sys.path.insert(0, str(ROOT / 'api'))
    import survey_logic as SL
    d = RI.SHARED_CODE_CHOICES['decided']
    for qid, codes in SL.SHARED_CODES.items():
        for code in codes:
            assert SL.shared_code_choice_key(qid, code) == d[qid][code], (qid, code)
    for (qid, code), label in RI.SHARED_CODE_LABELS['decided'].items():
        assert SL.SHARED_CODE_ORIGINAL_LABELS[(qid, code)] == label
        assert SL.SHARED_CODE_RESOLUTION[qid] == 'original_choice'


@pytest.mark.skipif(not HAVE_OCT, reason='October CSV/QSF not on this machine')
def test_shared_code_switch_flips_only_the_colliding_codes():
    cur = RI.Survey(str(OCT), str(QSF), 'current')
    alt = RI.Survey(str(OCT), str(QSF), 'alternate')
    assert cur.maps['QID141']['1'].startswith('Critical')
    assert alt.maps['QID141']['1'].startswith('Excellent')
    for q in ('QID141', 'QID17', 'QID100', 'QID221'):
        changed = {c for c in cur.maps[q] if cur.maps[q][c] != alt.maps[q][c]}
        assert changed == set(RI.SHARED_CODE_CHOICES['current'][q]), q


@pytest.mark.skipif(not HAVE_OCT, reason='October CSV/QSF not on this machine')
def test_decided_labels_and_struct_points():
    dec = RI.Survey(str(OCT), str(QSF))
    assert dec.shared_code == 'decided'
    assert dec.maps['QID141']['1'].startswith('Excellent')
    assert dec.maps['QID100'] == {**dec.maps['QID100'], '1': 'Yes', '2': 'No / Not applicable'}
    assert dec.maps['QID221']['2'] == 'No / Not applicable'
    cur = RI.Survey(str(OCT), str(QSF), 'current')
    assert dec.maps['QID17'] == cur.maps['QID17']
    row = next(r for r in dec.eligible() if dec.v(r, 'QID141') == '1')
    assert cur.score(row)['struct'] - dec.score(row)['struct'] == 35


def _feat(rid, xy, **props):
    return {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': list(xy)},
            'properties': {'response_id': rid, **props}}


def test_superseded_check_reads_the_blobs_superseded_features():
    """MATCH-3 moves earlier answers to geojson.superseded_features with
    superseded_by=<kept id>. The gate must find them there, and flag a blob
    whose choice of kept answer disagrees with the latest RecordedDate."""
    rec = {'A': '2026-07-20 09:01:52', 'B': '2026-01-17 09:00:26', 'C': '2026-01-01 00:00:00'}
    geo = {'features': [_feat('A', (-82.0, 29.7)), _feat('C', (-82.1, 29.7))],
           'superseded_features': [_feat('B', (-82.0, 29.7), superseded=True, superseded_by='A')]}
    feats, sup, problems = RI.placed_and_superseded(geo, rec)
    assert [f['properties']['response_id'] for f in feats] == ['A', 'C', 'B']
    assert sup == {'B': 'A'} and problems == []
    # the blob kept the EARLIER answer and hid the latest one
    bad = {'features': [_feat('B', (-82.0, 29.7)), _feat('C', (-82.1, 29.7))],
           'superseded_features': [_feat('A', (-82.0, 29.7), superseded=True, superseded_by='B')]}
    _, sup, problems = RI.placed_and_superseded(bad, rec)
    paths = {p[0] for p in problems}
    assert sup == {'B': 'A'}
    assert 'superseded.B' in paths and 'superseded.A' in paths
