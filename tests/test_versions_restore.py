"""Audit 2026-10-13 F4: restoring an old community_contact version must not
bring back field pins deleted since (e.g. the 28 test pins in versions
73-83), and must not lose a contact a pin had swallowed. No network."""
import unittest

from api.versions import build_contact_restore
from api._field_layer import field_row_to_feature, is_field_feature

LIVE = {"id": "b0467956-live", "lat": 29.7798, "lon": -82.0171, "status": "Completed",
        "collector_name": "Carey Morford"}


def pin(pid, collector, **props):
    f = field_row_to_feature({"id": pid, "lat": 29.65, "lon": -82.03, "status": "Completed",
                              "collector_name": collector})
    f["properties"].update(props)
    return f


class BuildContactRestoreTests(unittest.TestCase):
    def setUp(self):
        self.contact = {"type": "Feature", "geometry": {"type": "Point", "coordinates": [-82.0, 29.78]},
                        "properties": {"address": "6116 Harvard Avenue", "status": "Inaccessible"}}
        self.version = {"type": "FeatureCollection",
                        "features": [self.contact,
                                     pin("c3711341-test", "Test Test"),
                                     pin("b989a847-test", "test_qa_flip",
                                         coincident_contacts=[{"source": None, "status": "Completed",
                                                               "street_name": "Baylor"}])]}
        live_copy = field_row_to_feature(LIVE)
        live_copy["properties"].update(has_iaq_survey=True, iaq_response_id="R_6XiLZgAcnHtf16F",
                                       iaq_overall_risk=50, iaq_risk_tier="Medium")
        self.current = {"type": "FeatureCollection", "features": [self.contact, live_copy]}

    def test_deleted_pins_in_the_snapshot_are_not_restored(self):
        out, rep = build_contact_restore(self.version, self.current, [LIVE])
        ids = [f["properties"]["field_point_id"] for f in out["features"] if is_field_feature(f)]
        self.assertEqual(ids, ["b0467956-live"])
        self.assertEqual(sorted(rep["removed"]), ["b989a847-test", "c3711341-test"])

    def test_snapshot_contacts_and_swallowed_contact_survive(self):
        out, _ = build_contact_restore(self.version, self.current, [LIVE])
        contacts = [f for f in out["features"] if not is_field_feature(f)]
        self.assertIs(contacts[0], self.contact)
        self.assertEqual(contacts[1]["properties"]["street_name"], "Baylor")

    def test_live_pin_keeps_its_current_survey_link(self):
        out, _ = build_contact_restore(self.version, self.current, [LIVE])
        p = [f for f in out["features"] if is_field_feature(f)][0]["properties"]
        self.assertEqual(p["iaq_response_id"], "R_6XiLZgAcnHtf16F")
        self.assertEqual(p["iaq_overall_risk"], 50)



# ── Handler level: the restore writes the rebuilt blob in one commit ────
import api.versions as V  # noqa: E402


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
        if self.t == "keystone_analysis_versions":
            return _Res([self.sb.version])
        if self.t == "keystone_dashboard_data":
            return _Res([{"payload": self.sb.current, "updated_at": "t0"}])
        if self.t == "field_survey_points":
            return _Res(list(self.sb.rows))
        raise AssertionError(self.t)


class _Call:
    def __init__(self, fn):
        self.fn = fn

    def execute(self):
        return self.fn()


class _SB:
    def __init__(self, version, current, rows):
        self.version, self.current, self.rows, self.rpcs = version, current, rows, []

    def table(self, t):
        return _Q(self, t)

    def rpc(self, name, params):
        def go():
            self.rpcs.append(params)
            return _Res({"ok": True, "version_ids": []})
        return _Call(go)


class RestoreHandlerTests(unittest.TestCase):
    setUp = BuildContactRestoreTests.setUp

    def test_handler_commits_contacts_plus_live_pins_only(self):
        sb = _SB({"id": 75, "label": "v75", "data_type": "community_contact",
                  "payload": self.version, "created_at": "x"}, self.current, [LIVE])
        sent = []
        saved = (V.require_admin, V.supabase_admin, V.json_response, V.merge_preserve_analysis)
        V.require_admin = lambda _h: "uid"
        V.supabase_admin = lambda: sb
        V.json_response = lambda _h, status, body: sent.append((status, body))
        V.merge_preserve_analysis = lambda a: a
        try:
            h = V.handler.__new__(V.handler)
            h.path = "/api/versions?id=75"
            h.do_POST()
        finally:
            V.require_admin, V.supabase_admin, V.json_response, V.merge_preserve_analysis = saved
        status, body = sent[0]
        self.assertEqual(status, 200)
        self.assertEqual(body["field_points_removed"], 2)
        self.assertEqual(body["points"], 3)  # contact + restored Baylor + live pin
        self.assertEqual(len(sb.rpcs), 1)
        blobs = sb.rpcs[0]["p_blobs"]
        self.assertEqual([b["data_type"] for b in blobs], ["community_contact", "analysis"])
        ids = [f["properties"].get("field_point_id") for f in blobs[0]["payload"]["features"]
               if is_field_feature(f)]
        self.assertEqual(ids, ["b0467956-live"])


if __name__ == "__main__":
    unittest.main()
