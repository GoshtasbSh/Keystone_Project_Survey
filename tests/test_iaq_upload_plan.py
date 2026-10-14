"""Audit 2026-10-13 F4/F5/F8/Q2-F9: the Qualtrics upload computes everything
first (prepare_iaq_upload — no writes), then commits all blobs + version
rows in ONE call (commit_iaq_upload), with the field half rebuilt from
field_survey_points and re-linked to THIS upload's responses. No network:
the heavy pipeline pieces are stubbed."""
import unittest

import api.upload as U
from api._field_layer import field_row_to_feature, is_field_feature

LIVE = {"id": "b0467956-live", "lat": 29.7798, "lon": -82.0171, "status": "Completed",
        "notes": "", "collector_id": None, "collector_name": "Carey Morford",
        "collected_at": "2026-05-06T22:30:52+00:00"}


class _Res:
    def __init__(self, data):
        self.data = data


class _Q:
    def __init__(self, sb, t):
        self.sb, self.t, self.f, self.op, self.payload = sb, t, {}, "select", None

    def select(self, *_a):
        return self

    def eq(self, k, v):
        self.f[k] = v
        return self

    def in_(self, k, v):
        self.f[k] = v
        return self

    def limit(self, *_a):
        return self

    def range(self, *_a):
        return self

    def update(self, payload):
        self.op, self.payload = "update", payload
        return self

    def execute(self):
        return self.sb.run(self)


class _Call:
    def __init__(self, fn):
        self.fn = fn

    def execute(self):
        return self.fn()


class _SB:
    def __init__(self, contact_blob, rpc_error=None, field_rows=None):
        self.contact_blob = contact_blob
        self.rpc_error = rpc_error
        self.field_rows = field_rows if field_rows is not None else [LIVE]
        self.writes = []

    def table(self, t):
        return _Q(self, t)

    def rpc(self, name, params):
        def go():
            self.writes.append(("rpc", name, params))
            if self.rpc_error:
                raise Exception(self.rpc_error)
            return _Res({"ok": True, "version_ids": [1, 2, 3]})
        return _Call(go)

    def run(self, q):
        if q.op == "update":
            self.writes.append(("update", q.t, q.payload, q.f))
            return _Res([])
        if q.t == "field_survey_points":
            return _Res([dict(r) for r in self.field_rows])
        if q.t == "keystone_dashboard_data":
            if q.f.get("data_type") == "community_contact":
                return _Res([{"payload": self.contact_blob, "updated_at": "t0"}])
            return _Res([])
        raise AssertionError(f"unexpected read {q.t}")


def _contact():
    return {"type": "Feature", "geometry": {"type": "Point", "coordinates": [-82.0, 29.78]},
            "properties": {"address": "6116 Harvard Avenue", "status": "Completed"}}


def _test_pin():
    f = field_row_to_feature({"id": "c3711341-test", "lat": 29.68, "lon": -82.29,
                              "status": "Completed", "collector_name": "Test Test"})
    return f


class IaqUploadPlanTests(unittest.TestCase):
    def setUp(self):
        self._saved = {k: getattr(U, k) for k in (
            "load_parcel_index", "process_iaq_bytes", "_apply_iaq_to_field_features",
            "merge_preserve_analysis")}
        U.load_parcel_index = lambda: object()
        iaq = {"type": "Feature", "geometry": {"type": "Point", "coordinates": [-82.0171, 29.7798]},
               "properties": {"response_id": "R_bt9KhSC0xqF2xuS", "iaq_matched": False,
                              "match_status": "iaq_only", "overall_risk": 17, "risk_tier": "Low"}}

        def fake_process(csv_bytes, contacts, idx):
            return ({"type": "FeatureCollection", "features": [iaq]},
                    {"scores": {"mean_risk": 17}}, {}, 0, [])
        U.process_iaq_bytes = fake_process

        def fake_link(field_feats, iaq_feats, parcel_idx=None):
            for ff in field_feats:
                ff["properties"].update(has_iaq_survey=True, status="Completed",
                                        iaq_response_id="R_bt9KhSC0xqF2xuS", iaq_overall_risk=17)
                iaq_feats[0]["properties"]["iaq_matched"] = True
            return len(field_feats)
        U._apply_iaq_to_field_features = fake_link
        U.merge_preserve_analysis = lambda a: a
        self.blob = {"type": "FeatureCollection",
                     "features": [_contact(), field_row_to_feature(LIVE), _test_pin()]}

    def tearDown(self):
        for k, v in self._saved.items():
            setattr(U, k, v)

    def test_prepare_writes_nothing_and_plans_one_consistent_set(self):
        sb = _SB(self.blob)
        plan = U.prepare_iaq_upload(sb, "oct.csv", b"x")
        self.assertEqual(plan["status"], 200, plan["body"])
        self.assertEqual(sb.writes, [], "prepare must not write")
        self.assertEqual([b["data_type"] for b in plan["blobs"]],
                         ["iaq_survey", "community_contact", "analysis"])
        cc = plan["blobs"][1]["payload"]["features"]
        self.assertEqual([f["properties"]["field_point_id"] for f in cc if is_field_feature(f)],
                         ["b0467956-live"])
        self.assertEqual(plan["body"]["field_points_removed"], 1)
        # Q2-F9: a response linked only through a field pin is saved 'matched'.
        iaq_p = plan["blobs"][0]["payload"]["geojson"]["features"][0]["properties"]
        self.assertEqual(iaq_p["match_status"], "matched")
        self.assertEqual(plan["upgraded_ids"], ["b0467956-live"])
        labels = [v["label"] for v in plan["versions"]]
        self.assertTrue(any("1 deleted pins removed" in l for l in labels), labels)
        self.assertEqual(plan["versions"][0]["source_filename"], "oct.csv")

    def test_linked_pin_keeps_its_status_and_is_still_written_back(self):
        # A pin the surveyor marked otherwise keeps that status in the blob,
        # and its row still gets iaq_matched (the link, not the status).
        def link_keep_status(field_feats, iaq_feats, parcel_idx=None):
            for ff in field_feats:
                ff["properties"].update(has_iaq_survey=True, iaq_response_id="R_bt9KhSC0xqF2xuS")
            iaq_feats[0]["properties"]["iaq_matched"] = True
            return len(field_feats)
        U._apply_iaq_to_field_features = link_keep_status
        row = dict(LIVE, status="Not Interested")
        blob = {"type": "FeatureCollection", "features": [_contact(), field_row_to_feature(row)]}
        plan = U.prepare_iaq_upload(_SB(blob, field_rows=[row]), "oct.csv", b"x")
        self.assertEqual(plan["upgraded_ids"], ["b0467956-live"])
        pin = [f for f in plan["blobs"][1]["payload"]["features"] if is_field_feature(f)][0]
        self.assertEqual(pin["properties"]["status"], "Not Interested")

    def test_commit_is_one_rpc_then_the_field_status_sweep(self):
        sb = _SB(self.blob)
        plan = U.prepare_iaq_upload(sb, "oct.csv", b"x")
        U.commit_iaq_upload(sb, plan)
        self.assertEqual([w[0] for w in sb.writes], ["rpc", "update"])
        self.assertEqual(sb.writes[0][1], "keystone_commit_blobs")
        self.assertEqual(sb.writes[1][2], {"iaq_matched": True})

    def test_failed_commit_skips_the_field_status_sweep(self):
        sb = _SB(self.blob, rpc_error="{'code': '57014', 'message': 'statement timeout'}")
        plan = U.prepare_iaq_upload(sb, "oct.csv", b"x")
        with self.assertRaises(Exception):
            U.commit_iaq_upload(sb, plan)
        self.assertEqual([w[0] for w in sb.writes], ["rpc"])

    def test_unreadable_blob_is_a_500_not_an_empty_dataset(self):
        sb = _SB(self.blob)
        orig = sb.run

        def boom(q):
            if q.t == "keystone_dashboard_data":
                raise Exception("timeout")
            return orig(q)
        sb.run = boom
        plan = U.prepare_iaq_upload(sb, "oct.csv", b"x")
        self.assertEqual(plan["status"], 500)
        self.assertEqual(sb.writes, [])

    def test_non_csv_is_rejected_before_any_read(self):
        plan = U.prepare_iaq_upload(_SB(self.blob), "oct.xlsx", b"x")
        self.assertEqual(plan["status"], 400)


from api.upload import _finalize_iaq_match_state, _with_audit_trail  # noqa: E402


def _iaq_feat(rid, matched=False):
    return {"type": "Feature", "geometry": {"type": "Point", "coordinates": [-82.0171, 29.7798]},
            "properties": {"response_id": rid, "iaq_matched": matched, "match_status": "iaq_only",
                           "overall_risk": 17, "risk_tier": "Low", "street_name": "Beloit Ave"}}


class _SBWithIaq(_SB):
    def __init__(self, contact_blob, iaq_blob, **kw):
        super().__init__(contact_blob, **kw)
        self.iaq_blob = iaq_blob

    def run(self, q):
        if (q.op == "select" and q.t == "keystone_dashboard_data"
                and q.f.get("data_type") == "iaq_survey"):
            return _Res([{"payload": self.iaq_blob, "updated_at": "t1"}])
        return super().run(q)


class MergedIaqUploadTests(unittest.TestCase):
    setUp = IaqUploadPlanTests.setUp
    tearDown = IaqUploadPlanTests.tearDown

    def test_superseded_responses_do_not_trip_the_regression_guard(self):
        stored = {"geojson": {"features": [_iaq_feat("R_old"), _iaq_feat("R_bt9KhSC0xqF2xuS")]}}

        def process(csv_bytes, contacts, idx):
            return ({"type": "FeatureCollection", "features": [_iaq_feat("R_bt9KhSC0xqF2xuS")],
                     "superseded_features": [_iaq_feat("R_old")]}, {"scores": {}}, {}, 0, [])
        U.process_iaq_bytes = process
        plan = U.prepare_iaq_upload(_SBWithIaq(self.blob, stored), "oct.csv", b"x")
        self.assertEqual(plan["status"], 200, plan["body"])
        self.assertEqual(plan["versions"][0]["dropped_response_ids"], [])

    def test_validation_counts_follow_the_field_link(self):
        plan = U.prepare_iaq_upload(_SB(self.blob), "oct.csv", b"x")
        self.assertEqual(plan["blobs"][0]["payload"]["validation"]["matched_iaq_responses"], 1)
        self.assertEqual(plan["body"]["validation"]["matched_iaq_responses"], 1)

    def test_finalize_rederives_match_status_and_keeps_other_counts(self):
        gj = {"features": [_iaq_feat("R_1", matched=True), _iaq_feat("R_2")]}
        analysis = {"validation": {"completed_in_csv": 126}}
        _finalize_iaq_match_state(gj, analysis, [])
        self.assertEqual([f["properties"]["match_status"] for f in gj["features"]],
                         ["matched", "iaq_only"])
        self.assertEqual(analysis["validation"]["matched_iaq_responses"], 1)
        self.assertEqual(analysis["validation"]["completed_in_csv"], 126)

    def test_response_body_carries_the_audit_trail(self):
        body = _with_audit_trail({"status": "ok"}, {"version_statuses": ["full", "base_only"]})
        self.assertEqual(body["audit_trail"]["status"], "degraded")
        self.assertEqual(_with_audit_trail({}, {"version_statuses": ["full"]})["audit_trail"]["status"], "full")


class WritebackSwitchTests(unittest.TestCase):
    setUp = IaqUploadPlanTests.setUp
    tearDown = IaqUploadPlanTests.tearDown

    def test_writeback_can_be_skipped(self):
        sb = _SB(self.blob)
        plan = U.prepare_iaq_upload(sb, "oct.csv", b"x")
        U.commit_iaq_upload(sb, plan, writeback_field_points=False)
        self.assertEqual([w[0] for w in sb.writes], ["rpc"])


if __name__ == "__main__":
    unittest.main()
