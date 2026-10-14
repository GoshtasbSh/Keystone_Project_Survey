"""Audit 2026-10-13 F4 / DEP-6 / DEP-7 / DEP-8: the nightly refresh rebuilds
the field half of the community_contact blob from field_survey_points
(deleted pins disappear), never touches CSV contacts, never treats a read
error as "empty", skips no-op writes, and refuses to overwrite an upload
that committed mid-refresh. api/daily-refresh.py is loaded via importlib
(hyphenated filename). No network."""
import importlib.util
import pathlib
import unittest

from api._field_layer import field_row_to_feature, is_field_feature

_MOD_PATH = pathlib.Path(__file__).resolve().parent.parent / "api" / "daily-refresh.py"
_spec = importlib.util.spec_from_file_location("_daily_refresh_for_rebuild_tests", _MOD_PATH)
daily_refresh = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(daily_refresh)


def contact(addr, lon, lat, status="Completed", **extra):
    return {"type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": {"address": addr, "status": status,
                           "street_name": addr.split(" ", 1)[1], **extra}}


def row(pid, lon, lat, status="Completed", collector="Carey Morford", **extra):
    return {"id": pid, "lat": lat, "lon": lon, "status": status, "notes": "",
            "collector_id": None, "collector_name": collector,
            "collected_at": "2026-05-06T22:30:52+00:00", **extra}


def field_copy(pid, lon, lat, collector, status="Completed", **extra):
    f = field_row_to_feature(row(pid, lon, lat, status, collector))
    f["properties"].update(extra)
    return f


REAL = row("b0467956-real", -82.0171, 29.7798)
GNV_TEST_PIN = field_copy("c3711341-test", -82.289, 29.684, "Test Test", notes="test")


class _Res:
    def __init__(self, data):
        self.data = data


class _Q:
    def __init__(self, sb, table):
        self.sb, self.table, self.op, self.payload, self.cols = sb, table, None, None, None
        self.filters = {}

    def select(self, cols):
        self.op, self.cols = "select", cols
        return self

    def eq(self, k, v):
        self.filters[k] = v
        return self

    def limit(self, *_a): return self
    def range(self, *_a): return self
    def order(self, *_a, **_k): return self

    def upsert(self, payload, on_conflict=None):
        self.op, self.payload = "upsert", payload
        return self

    def insert(self, payload):
        self.op, self.payload = "insert", payload
        return self

    def execute(self):
        return self.sb.run(self)


class _FakeSB:
    """field_survey_points + keystone_dashboard_data with updated_at stamps.
    No .rpc attribute -> commit_dashboard_writes uses its sequential path."""

    def __init__(self, rows, blobs):
        self.rows = rows
        self.blobs = {k: {"payload": v, "updated_at": f"2026-10-13T16:32:1{i}+00:00"}
                      for i, (k, v) in enumerate(blobs.items())}
        self.upserts, self.inserts = [], []

    def table(self, name):
        return _Q(self, name)

    def run(self, q):
        if q.table == "field_survey_points" and q.op == "select":
            return _Res(list(self.rows))
        if q.table == "keystone_dashboard_data" and q.op == "select":
            b = self.blobs.get(q.filters.get("data_type"))
            if not b:
                return _Res([])
            return _Res([{"payload": b["payload"], "updated_at": b["updated_at"]}])
        if q.table == "keystone_dashboard_data" and q.op == "upsert":
            self.upserts.append(q.payload)
            self.blobs[q.payload["data_type"]] = {"payload": q.payload["payload"],
                                                  "updated_at": "2026-10-14T04:00:00+00:00"}
            return _Res([q.payload])
        if q.table == "keystone_analysis_versions" and q.op == "insert":
            self.inserts.append(q.payload)
            return _Res([q.payload])
        if q.table == "community_contacts":
            raise Exception("not needed")
        raise Exception(f"unsupported: {q.table} {q.op}")


class RunRefreshRebuildTests(unittest.TestCase):
    def setUp(self):
        self._orig = daily_refresh.supabase_admin
        self._orig_match = daily_refresh._match_field_to_iaq
        daily_refresh._match_field_to_iaq = lambda field, iaq: 0  # no parcel index in unit tests

    def tearDown(self):
        daily_refresh.supabase_admin = self._orig
        daily_refresh._match_field_to_iaq = self._orig_match

    def _blob(self):
        c = contact("6116 Harvard Avenue", -81.995533, 29.786862, "Inaccessible")
        return {"type": "FeatureCollection",
                "features": [c, field_copy(REAL["id"], REAL["lon"], REAL["lat"], "Carey Morford"),
                             GNV_TEST_PIN]}

    def test_cron_removes_deleted_pin_and_keeps_contacts(self):
        sb = _FakeSB([REAL], {"community_contact": self._blob()})
        daily_refresh.supabase_admin = lambda: sb
        res = daily_refresh._run_refresh()
        self.assertTrue(res["refreshed"], res)
        self.assertEqual(res["removed_field_points"], 1)
        self.assertEqual(res["new_field_points"], 0)
        cc = [u for u in sb.upserts if u["data_type"] == "community_contact"][0]["payload"]
        ids = [f["properties"].get("field_point_id") for f in cc["features"] if is_field_feature(f)]
        self.assertEqual(ids, [REAL["id"]])
        self.assertEqual(sum(1 for f in cc["features"] if not is_field_feature(f)), 1)
        self.assertIn("1 deleted pins removed", sb.inserts[0]["label"])

    def test_second_run_is_a_no_op(self):
        sb = _FakeSB([REAL], {"community_contact": self._blob()})
        daily_refresh.supabase_admin = lambda: sb
        daily_refresh._run_refresh()
        data_writes = lambda: [u for u in sb.upserts if u["data_type"] != "integrity_metrics"]
        n_up, n_ins = len(data_writes()), len(sb.inserts)
        res = daily_refresh._run_refresh()
        self.assertFalse(res["refreshed"])
        # Only the daily integrity heartbeat row may be written on a no-op tick.
        self.assertEqual((len(data_writes()), len(sb.inserts)), (n_up, n_ins))

    def test_blob_read_error_aborts_without_writing(self):
        sb = _FakeSB([REAL], {"community_contact": self._blob()})
        orig_run = sb.run

        def failing(q):
            if q.table == "keystone_dashboard_data" and q.op == "select":
                raise Exception("timeout")
            return orig_run(q)
        sb.run = failing
        daily_refresh.supabase_admin = lambda: sb
        res = daily_refresh._run_refresh()
        self.assertFalse(res["refreshed"])
        self.assertEqual(sb.upserts, [])

    def test_concurrent_upload_makes_refresh_retry_then_skip(self):
        sb = _FakeSB([REAL], {"community_contact": self._blob()})
        orig_run = sb.run

        def racing(q):
            # Every stamp re-check sees a newer updated_at, as if an upload
            # committed between the read and the write.
            if (q.table == "keystone_dashboard_data" and q.op == "select"
                    and q.cols == "updated_at"):
                return _Res([{"updated_at": "2026-10-14T04:00:30+00:00"}])
            return orig_run(q)
        sb.run = racing
        daily_refresh.supabase_admin = lambda: sb
        res = daily_refresh._run_refresh_with_retry()
        self.assertFalse(res["refreshed"])
        self.assertIn("concurrent", res["reason"])
        self.assertEqual([u for u in sb.upserts if u["data_type"] == "community_contact"], [])


if __name__ == "__main__":
    unittest.main()
