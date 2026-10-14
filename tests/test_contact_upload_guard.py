"""Audit 2026-10-13 F6: on 2026-07-20 a Qualtrics export dropped into the
Community Contact box replaced all 277 contacts with 0 (version 77).
The contacts upload must refuse a file with no Address column, refuse 0
placeable contacts, and refuse a large drop unless forced. No network."""
import io
import unittest

import pandas as pd

from api.upload import evaluate_contact_upload_safety, CONTACT_REGRESSION_RATIO
from api._processing import process_survey_bytes, ParcelIndex


def _csv(df):
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    return buf.getvalue().encode()


class ProcessSurveyBytesSchemaTests(unittest.TestCase):
    def test_qualtrics_export_is_rejected_with_a_clear_message(self):
        q = _csv(pd.DataFrame({"StartDate": ["x"], "ResponseId": ["R_1"],
                               "Finished": ["1"], "Q212": ["6386 Baylor"]}))
        with self.assertRaises(ValueError) as cm:
            process_survey_bytes(q, "Keystone Heights Survey - V1_July 20, 2026_09.41.csv",
                                 ParcelIndex())
        self.assertIn("Qualtrics", str(cm.exception))

    def test_file_without_address_column_is_rejected(self):
        f = _csv(pd.DataFrame({"Street": ["Baylor"], "First attempt": ["survey"]}))
        with self.assertRaises(ValueError) as cm:
            process_survey_bytes(f, "contacts.csv", ParcelIndex())
        self.assertIn("'Address'", str(cm.exception))


class ContactSafetyTests(unittest.TestCase):
    def test_zero_contacts_is_always_refused_even_with_force(self):
        for force in (False, True):
            v = evaluate_contact_upload_safety(277, 0, "x.csv", force)
            self.assertFalse(v["allowed"])
            self.assertEqual(v["status"], 400)
            self.assertEqual(v["reason"], "no_contacts")

    def test_large_drop_is_refused_without_force(self):
        v = evaluate_contact_upload_safety(277, 100, "x.csv", False)
        self.assertFalse(v["allowed"])
        self.assertEqual(v["status"], 409)
        self.assertEqual(v["reason"], "contact_regression")
        self.assertIn("277", v["detail"])

    def test_large_drop_is_allowed_with_force(self):
        self.assertTrue(evaluate_contact_upload_safety(277, 100, "x.csv", True)["allowed"])

    def test_normal_growth_and_small_drop_are_allowed(self):
        self.assertTrue(evaluate_contact_upload_safety(277, 331, "x.csv", False)["allowed"])
        at_ratio = int(277 * CONTACT_REGRESSION_RATIO) + 1
        self.assertTrue(evaluate_contact_upload_safety(277, at_ratio, "x.csv", False)["allowed"])

    def test_first_ever_upload_is_allowed(self):
        self.assertTrue(evaluate_contact_upload_safety(0, 5, "x.csv", False)["allowed"])



# ── Handler level: the guard runs before any write (no network) ─────────
import api.upload as U  # noqa: E402


def _contact(i):
    return {"type": "Feature",
            "geometry": {"type": "Point", "coordinates": [-82.0 + i * 1e-3, 29.78]},
            "properties": {"address": f"{i} Test St", "status": "No Answer"}}


class _Res:
    def __init__(self, data):
        self.data = data


class _Q:
    def __init__(self, sb, t):
        self.sb, self.t, self.f = sb, t, {}

    def select(self, *_a):
        return self

    def eq(self, k, v):
        self.f[k] = v
        return self

    def limit(self, *_a):
        return self

    def range(self, *_a):
        return self

    def execute(self):
        if self.t == "keystone_dashboard_data":
            p = self.sb.blobs.get(self.f.get("data_type"))
            return _Res([{"payload": p, "updated_at": "t0"}] if p is not None else [])
        if self.t == "field_survey_points":
            return _Res([])
        raise AssertionError(f"unexpected table {self.t}")


class _Call:
    def __init__(self, fn):
        self.fn = fn

    def execute(self):
        return self.fn()


class _SB:
    def __init__(self, stored_contacts):
        self.blobs = {"community_contact": {"type": "FeatureCollection",
                                            "features": [_contact(i) for i in range(stored_contacts)]}}
        self.rpcs = []

    def table(self, t):
        return _Q(self, t)

    def rpc(self, name, params):
        def go():
            self.rpcs.append((name, params))
            return _Res({"ok": True, "version_ids": [1]})
        return _Call(go)


class HandleSurveyTests(unittest.TestCase):
    def setUp(self):
        self._saved = {k: getattr(U, k) for k in (
            "supabase_admin", "load_parcel_index", "process_survey_bytes",
            "json_response", "_sync_community_contacts", "compute_contact_analysis",
            "merge_preserve_analysis")}
        self.sent = []
        self.synced = []
        U.load_parcel_index = lambda: ParcelIndex()
        U.json_response = lambda _h, status, body: self.sent.append((status, body))
        U._sync_community_contacts = lambda _sb, feats: self.synced.append(len(feats))
        U.compute_contact_analysis = lambda feats: {"n": len(feats)}
        U.merge_preserve_analysis = lambda a: a

    def tearDown(self):
        for k, v in self._saved.items():
            setattr(U, k, v)

    def _run(self, sb, incoming, query=""):
        U.supabase_admin = lambda: sb
        U.process_survey_bytes = lambda *_a: (
            {"type": "FeatureCollection", "features": [_contact(i) for i in range(incoming)]}, [])
        h = U.handler.__new__(U.handler)
        h.path = "/api/upload?type=survey" + query
        h._handle_survey("contacts.csv", b"x")
        self.assertEqual(len(self.sent), 1)
        return self.sent[0]

    def test_large_drop_is_refused_before_any_write(self):
        sb = _SB(277)
        status, body = self._run(sb, 100)
        self.assertEqual(status, 409)
        self.assertEqual(body["reason"], "contact_regression")
        self.assertEqual((body["stored_contacts"], body["incoming_contacts"]), (277, 100))
        self.assertEqual(sb.rpcs, [])
        self.assertEqual(self.synced, [])

    def test_zero_contacts_is_refused_even_with_force(self):
        sb = _SB(277)
        status, body = self._run(sb, 0, "&force=1")
        self.assertEqual(status, 400)
        self.assertEqual(body["reason"], "no_contacts")
        self.assertEqual(sb.rpcs, [])

    def test_forced_drop_is_one_commit_marked_forced_with_audit_trail(self):
        sb = _SB(277)
        status, body = self._run(sb, 100, "&force=1")
        self.assertEqual(status, 200)
        self.assertEqual(body["contact_points"], 100)
        self.assertEqual(body["audit_trail"]["status"], "full")
        self.assertEqual(len(sb.rpcs), 1)
        params = sb.rpcs[0][1]
        self.assertEqual([b["data_type"] for b in params["p_blobs"]],
                         ["community_contact", "analysis"])
        self.assertTrue(params["p_versions"][0]["forced"])
        self.assertEqual(self.synced, [100])

    def test_contacts_upload_keeps_the_stored_survey_links(self):
        # U9a: fresh contacts carry no has_iaq_survey; without re-linking every
        # Completed contact became contact_only until the next IAQ upload.
        sb = _SB(277)
        c = _contact(150)
        sb.blobs["iaq_survey"] = {"geojson": {"type": "FeatureCollection", "features": [
            {"type": "Feature", "geometry": dict(c["geometry"]),
             "properties": {"response_id": "R_kept", "house_number": "150", "overall_risk": 30,
                            "risk_tier": "Low", "iaq_matched": True, "match_status": "matched"}}]}}
        status, body = self._run(sb, 277)
        self.assertEqual(status, 200)
        feats = sb.rpcs[0][1]["p_blobs"][0]["payload"]["features"]
        p = feats[150]["properties"]
        self.assertEqual((p["iaq_response_id"], p["match_status"], p["status"]),
                         ("R_kept", "matched", "Completed"))
        self.assertNotIn("has_iaq_survey", feats[151]["properties"])


if __name__ == "__main__":
    unittest.main()
