"""launch_snapshot: real field points must never change; test pins must not appear."""
from __future__ import annotations

import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts' / 'audit'))

import launch_snapshot as LS  # noqa: E402


ROW = {'id': 'f1', 'lat': 29.78, 'lon': -82.01, 'status': 'Completed', 'notes': '6280 done',
       'collector_id': 'u1', 'collector_name': 'Carey Morford', 'collected_at': '2026-05-01T10:00:00Z',
       'is_offline': False, 'guest_session_id': None, 'synced_at': None, 'iaq_matched': False,
       'updated_at': '2026-05-01T10:00:00Z'}


def test_field_points_unchanged_passes():
    assert LS.compare_field_points([ROW], [dict(ROW)]) == []


def test_iaq_matched_false_to_true_and_updated_at_are_allowed():
    after = dict(ROW, iaq_matched=True, updated_at='2026-10-14T00:00:00Z', address=None)
    assert LS.compare_field_points([ROW], [after]) == []


@pytest.mark.parametrize('col,val', [('notes', 'edited'), ('lat', 29.0), ('status', 'Vacant'),
                                     ('collected_at', '2026-10-14T00:00:00Z')])
def test_any_immutable_change_fails(col, val):
    fails = LS.compare_field_points([ROW], [dict(ROW, **{col: val})])
    assert fails and col in fails[0]


def test_deleted_real_point_fails_and_matched_flag_cannot_drop():
    assert LS.compare_field_points([ROW], []) == ['field point f1 DELETED']
    assert 'True -> False' in LS.compare_field_points([dict(ROW, iaq_matched=True)], [ROW])[0]


def test_new_rows_only_fail_for_test_accounts():
    real = dict(ROW, id='f2')
    assert LS.compare_field_points([ROW], [ROW, real]) == []
    for name in ('test3', 'QA Tester', 'test_qa_flip', 'Test Test'):
        assert LS.compare_field_points([ROW], [ROW, dict(ROW, id='f3', collector_name=name)])


def test_total_hash_is_order_independent():
    b = dict(ROW, id='f2')
    assert LS.total_hash([ROW, b]) == LS.total_hash([b, ROW])
