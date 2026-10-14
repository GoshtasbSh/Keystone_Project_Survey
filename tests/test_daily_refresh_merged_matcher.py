"""The cron must link with the shared matcher (nearest first, never the
first survey within 30 m) even when the parcel index is unavailable, and
keep the stored matched counts in step with the field pass."""
import importlib.util
import pathlib
import unittest

_MOD = pathlib.Path(__file__).resolve().parent.parent / "api" / "daily-refresh.py"
_spec = importlib.util.spec_from_file_location("_daily_refresh_merged", _MOD)
daily_refresh = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(daily_refresh)

LON0, LAT0 = -82.0112103523915, 29.7792023806237
M_PER_DEG_LAT = 6_371_000 * 3.141592653589793 / 180


def _iaq(rid, metres_north):
    return {"type": "Feature",
            "geometry": {"type": "Point", "coordinates": [LON0, LAT0 + metres_north / M_PER_DEG_LAT]},
            "properties": {"response_id": rid, "overall_risk": 20, "risk_tier": "Low",
                           "health_score": 1, "iaq_score": 2, "struct_score": 3,
                           "iaq_matched": False, "house_number": "", "street_name": "Dennison Ave"}}


def _pin():
    return {"type": "Feature", "geometry": {"type": "Point", "coordinates": [LON0, LAT0]},
            "properties": {"source": "field", "field_point_id": "p", "status": "Completed", "notes": ""}}


def _no_index():
    raise RuntimeError("no parcel index")


class MergedMatcherTests(unittest.TestCase):
    def test_nearest_wins_without_parcel_index(self):
        pin = _pin()
        n = daily_refresh._match_field_to_iaq([pin], [_iaq("R_far", 25), _iaq("R_near", 10)],
                                              parcel_loader=_no_index)
        self.assertEqual(n, 1)
        self.assertEqual(pin["properties"]["iaq_response_id"], "R_near")

    def test_no_first_within_30m_loop_left(self):
        self.assertNotIn("haversine_m", _MOD.read_text())

    def test_validation_counts_follow_the_field_flip(self):
        feats = [_iaq("R_1", 0)]
        feats[0]["properties"]["iaq_matched"] = True
        payload = {"validation": {"completed_in_csv": 126, "matched_iaq_responses": 0},
                   "analysis": {"validation": {"matched_iaq_responses": 0}}}
        daily_refresh._refresh_iaq_validation_counts(payload, feats, [])
        self.assertEqual(payload["validation"]["matched_iaq_responses"], 1)
        self.assertEqual(payload["validation"]["completed_in_csv"], 126)
        self.assertEqual(payload["analysis"]["validation"]["matched_iaq_responses"], 1)


class _Res:
    def __init__(self, data):
        self.data = data


class _Q:
    def __init__(self, sb, table):
        self.sb, self.table, self.op, self.payload, self.filters = sb, table, None, None, {}

    def select(self, *_a, **_k):
        self.op = "select"
        return self

    def eq(self, k, v):
        self.filters[k] = v
        return self

    def limit(self, *_a): return self
    def range(self, *_a): return self

    def upsert(self, payload, on_conflict=None):
        self.op, self.payload = "upsert", payload
        return self

    def insert(self, payload):
        self.op, self.payload = "insert", payload
        return self

    def execute(self):
        return self.sb.run(self)


class _SB:
    """One field pin, one IAQ response, no .rpc (sequential write path)."""

    def __init__(self, blobs):
        self.blobs = blobs
        self.upserts = []

    def table(self, name):
        return _Q(self, name)

    def run(self, q):
        if q.table == "field_survey_points":
            return _Res([{"id": "p", "lat": LAT0, "lon": LON0, "status": "Completed",
                          "notes": "", "collector_id": None, "collector_name": "A",
                          "collected_at": "2026-05-06T22:30:52+00:00"}])
        if q.table == "keystone_dashboard_data" and q.op == "select":
            b = self.blobs.get(q.filters.get("data_type"))
            return _Res([{"payload": b, "updated_at": "t0"}] if b is not None else [])
        if q.op in ("upsert", "insert"):
            self.upserts.append(q.payload)
            return _Res([q.payload])
        raise Exception(f"unsupported: {q.table} {q.op}")


class RunRefreshWiringTests(unittest.TestCase):
    def setUp(self):
        self._orig = (daily_refresh.supabase_admin, daily_refresh._match_field_to_iaq)
        self.sb = _SB({"community_contact": {"type": "FeatureCollection", "features": []},
                       "iaq_survey": {"geojson": {"features": [_iaq("R_1", 0)]},
                                      "validation": {"completed_in_csv": 126,
                                                     "matched_iaq_responses": 0},
                                      "analysis": {"validation": {"matched_iaq_responses": 0}}}})
        daily_refresh.supabase_admin = lambda: self.sb

    def tearDown(self):
        daily_refresh.supabase_admin, daily_refresh._match_field_to_iaq = self._orig

    def test_matcher_failure_writes_nothing(self):
        # The pins were rebuilt without their links; writing would strip them all.
        def boom(field, iaq):
            raise ImportError("no _processing in this bundle")
        daily_refresh._match_field_to_iaq = boom
        res = daily_refresh._run_refresh()
        self.assertFalse(res["refreshed"])
        self.assertIn("matching failed", res["reason"])
        self.assertEqual(self.sb.upserts, [])

    def test_stored_counts_follow_the_cron_flip(self):
        def flip(field, iaq):
            iaq[0]["properties"]["iaq_matched"] = True
            return 1
        daily_refresh._match_field_to_iaq = flip
        res = daily_refresh._run_refresh()
        self.assertTrue(res["refreshed"], res)
        iaq = [u for u in self.sb.upserts if u.get("data_type") == "iaq_survey"][0]["payload"]
        self.assertEqual(iaq["validation"]["matched_iaq_responses"], 1)
        self.assertEqual(iaq["validation"]["completed_in_csv"], 126)
        self.assertEqual(iaq["analysis"]["validation"]["matched_iaq_responses"], 1)
        self.assertEqual(iaq["geojson"]["features"][0]["properties"]["match_status"], "matched")
