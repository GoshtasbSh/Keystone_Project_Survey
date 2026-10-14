"""Audit 2026-10-13 F8 / DEP-8: every blob + version write of one upload,
refresh or restore goes through commit_dashboard_writes — one RPC
transaction (migration 29) with compare-and-set, or, when 29 is not
applied, the sequential fallback in the safest order. No network."""
import unittest

from api._dashboard_writes import (
    commit_dashboard_writes, load_blob_with_stamp, StaleWriteError,
)


class _Res:
    def __init__(self, data):
        self.data = data


class _Call:
    def __init__(self, fn):
        self._fn = fn

    def execute(self):
        return self._fn()


class _Q:
    def __init__(self, sb, table):
        self.sb, self.table, self.op, self.payload, self.cols, self.filters = sb, table, None, None, None, {}

    def select(self, cols):
        self.op, self.cols = "select", cols
        return self

    def eq(self, k, v):
        self.filters[k] = v
        return self

    def limit(self, *_a):
        return self

    def upsert(self, payload, on_conflict=None):
        self.op, self.payload = "upsert", payload
        return self

    def insert(self, payload):
        self.op, self.payload = "insert", payload
        return self

    def execute(self):
        return self.sb.run(self)


class _SeqSB:
    """No .rpc -> sequential path. Optionally rejects enriched version rows."""

    def __init__(self, stamps=None, reject_audit_cols=False, fail_upsert_of=None):
        self.stamps = stamps or {}
        self.reject_audit_cols = reject_audit_cols
        self.fail_upsert_of = fail_upsert_of
        self.log = []

    def table(self, name):
        return _Q(self, name)

    def run(self, q):
        self.log.append((q.table, q.op, q.payload if q.op != "select" else q.filters.get("data_type")))
        if q.op == "select":
            s = self.stamps.get(q.filters.get("data_type"))
            return _Res([{"updated_at": s, "payload": {}}] if s else [])
        if q.op == "upsert" and q.payload["data_type"] == self.fail_upsert_of:
            raise Exception("network down")
        if q.op == "insert" and self.reject_audit_cols and "source_filename" in q.payload:
            raise Exception('column "source_filename" does not exist')
        return _Res([q.payload])


class _RpcSB(_SeqSB):
    def __init__(self, rpc_error=None, **kw):
        super().__init__(**kw)
        self.rpc_error = rpc_error
        self.rpc_calls = []

    def rpc(self, name, params):
        def go():
            self.rpc_calls.append((name, params))
            if self.rpc_error:
                raise Exception(self.rpc_error)
            return _Res({"ok": True, "version_ids": [101, 102]})
        return _Call(go)


BLOBS = [{"data_type": "iaq_survey", "payload": {"geojson": {}}},
         {"data_type": "community_contact", "payload": {"features": []}},
         {"data_type": "analysis", "payload": {}}]
VERSIONS = [{"data_type": "iaq_survey", "payload": {}, "label": "x", "n_points": 1,
             "source_filename": "oct.csv", "forced": False},
            {"data_type": "community_contact", "payload": {}, "label": "y", "n_points": 2}]


class CommitTests(unittest.TestCase):
    def test_rpc_sends_everything_in_one_call(self):
        sb = _RpcSB()
        res = commit_dashboard_writes(sb, BLOBS, VERSIONS, expected={"community_contact": "t1"})
        self.assertEqual(res["mode"], "rpc")
        self.assertEqual(len(sb.rpc_calls), 1)
        name, params = sb.rpc_calls[0]
        self.assertEqual(name, "keystone_commit_blobs")
        self.assertEqual(params["p_blobs"], BLOBS)
        self.assertEqual(params["p_versions"], VERSIONS)
        self.assertEqual(params["p_expected"], {"community_contact": "t1"})
        self.assertEqual(sb.log, [], "no direct table writes when the RPC exists")

    def test_rpc_stale_write_raises_stale_error(self):
        sb = _RpcSB(rpc_error="{'code': '40001', 'message': 'keystone_stale_write: community_contact changed'}")
        with self.assertRaises(StaleWriteError):
            commit_dashboard_writes(sb, BLOBS, VERSIONS, expected={"community_contact": "t1"})
        self.assertEqual(sb.log, [])

    def test_rpc_other_error_propagates_and_writes_nothing(self):
        sb = _RpcSB(rpc_error="{'code': '57014', 'message': 'statement timeout'}")
        with self.assertRaises(Exception):
            commit_dashboard_writes(sb, BLOBS, VERSIONS)
        self.assertEqual(sb.log, [])

    def test_missing_rpc_falls_back_to_sequential(self):
        sb = _RpcSB(rpc_error="{'code': 'PGRST202', 'message': 'Could not find the function public.keystone_commit_blobs'}")
        res = commit_dashboard_writes(sb, BLOBS, VERSIONS)
        self.assertEqual(res["mode"], "sequential")
        self.assertEqual([t for t, op, _ in sb.log if op == "upsert"], ["keystone_dashboard_data"] * 3)
        self.assertEqual(res["versions_written"], 2)

    def test_sequential_checks_stamps_before_any_write(self):
        sb = _SeqSB(stamps={"community_contact": "t2"})
        with self.assertRaises(StaleWriteError):
            commit_dashboard_writes(sb, BLOBS, VERSIONS, expected={"community_contact": "t1"})
        self.assertFalse(any(op in ("upsert", "insert") for _, op, _ in sb.log))

    def test_sequential_absent_row_matches_none_stamp(self):
        sb = _SeqSB(stamps={})
        res = commit_dashboard_writes(sb, BLOBS, VERSIONS, expected={"community_contact": None})
        self.assertEqual(res["blobs_written"], ["iaq_survey", "community_contact", "analysis"])

    def test_sequential_writes_blobs_before_versions(self):
        sb = _SeqSB()
        commit_dashboard_writes(sb, BLOBS, VERSIONS)
        ops = [op for _, op, _ in sb.log]
        self.assertEqual(ops, ["upsert", "upsert", "upsert", "insert", "insert"])

    def test_sequential_version_insert_never_raises(self):
        sb = _SeqSB(reject_audit_cols=True)
        res = commit_dashboard_writes(sb, BLOBS, VERSIONS)
        inserts = [p for _, op, p in sb.log if op == "insert"]
        # enriched attempt, base retry, plain community_contact row
        self.assertEqual(len(inserts), 3)
        self.assertNotIn("source_filename", inserts[1])
        self.assertEqual(res["versions_written"], 2)

    def test_load_blob_with_stamp_raises_on_read_error(self):
        class Boom(_SeqSB):
            def run(self, q):
                raise Exception("timeout")
        with self.assertRaises(Exception):
            load_blob_with_stamp(Boom(), "community_contact")

    def test_load_blob_with_stamp_absent_row(self):
        self.assertEqual(load_blob_with_stamp(_SeqSB(), "community_contact"), (None, None))


if __name__ == "__main__":
    unittest.main()
