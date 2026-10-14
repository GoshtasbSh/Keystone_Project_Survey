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
    def __init__(self, contact_blob, rpc_error=None):
        self.contact_blob = contact_blob
        self.rpc_error = rpc_error
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
            return _Res([dict(LIVE)])
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

    def test_commit_is_one_rpc_then_the_field_status_sweep(self):
        sb = _SB(self.blob)
        plan = U.prepare_iaq_upload(sb, "oct.csv", b"x")
        U.commit_iaq_upload(sb, plan)
        self.assertEqual([w[0] for w in sb.writes], ["rpc", "update"])
        self.assertEqual(sb.writes[0][1], "keystone_commit_blobs")
        self.assertEqual(sb.writes[1][2], {"status": "Completed", "iaq_matched": True})

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


if __name__ == "__main__":
    unittest.main()
