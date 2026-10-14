"""Audit 2026-10-13 F4 / Q4-03 / DEP-6: the community_contact blob must hold
exactly one copy of every CURRENT field_survey_points row — deleted pins
(28 test pins in production) must disappear, CSV contacts must never be
lost, and a contact a pin had swallowed must come back as its own feature.
Pure functions only; no network."""
import unittest

from api._field_layer import (
    rebuild_field_layer, field_row_to_feature, is_field_feature,
    features_signature, load_all_field_rows, cell_key,
)


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
TEST_PIN = field_copy("b989a847-test", -82.017276, 29.783271, "test_qa_flip",
                      has_iaq_survey=True, iaq_response_id="R_5LnXMcaezhqW28F",
                      coincident_contacts=[{"status": "Completed", "street_name": "Baylor",
                                            "notes": "", "source": None,
                                            "collected_at": None, "has_iaq_survey": False}])
GNV_TEST_PIN = field_copy("c3711341-test", -82.289, 29.684, "Test Test", notes="test")




class RebuildFieldLayerTests(unittest.TestCase):
    def setUp(self):
        self.c1 = contact("6116 Harvard Avenue", -81.995533, 29.786862, "Inaccessible")
        self.blob = [self.c1, field_copy(REAL["id"], REAL["lon"], REAL["lat"], "Carey Morford"),
                     TEST_PIN, GNV_TEST_PIN]

    def test_deleted_pins_are_dropped_and_live_pins_kept(self):
        feats, rep = rebuild_field_layer(self.blob, [REAL])
        ids = [f["properties"]["field_point_id"] for f in feats if is_field_feature(f)]
        self.assertEqual(ids, [REAL["id"]])
        self.assertEqual(rep["removed"], sorted(["b989a847-test", "c3711341-test"]))
        self.assertEqual(rep["added"], [])
        self.assertEqual({d["collector"] for d in rep["removed_details"]},
                         {"test_qa_flip", "Test Test"})

    def test_csv_contacts_are_untouched(self):
        feats, _ = rebuild_field_layer(self.blob, [REAL])
        self.assertIs(feats[0], self.c1, "contacts must be passed through, not copied")

    def test_swallowed_contact_is_restored_without_iaq_link(self):
        feats, rep = rebuild_field_layer(self.blob, [REAL])
        restored = [f for f in feats if (f["properties"] or {}).get("restored_from_field_pin")]
        self.assertEqual(rep["restored_contacts"], 1)
        self.assertEqual(len(restored), 1)
        p = restored[0]["properties"]
        self.assertEqual(p["status"], "Completed")
        self.assertEqual(p["street_name"], "Baylor")
        self.assertEqual(restored[0]["geometry"]["coordinates"], [-82.017276, 29.783271])
        self.assertNotIn("has_iaq_survey", p)
        self.assertNotIn("iaq_response_id", p)
        self.assertFalse(is_field_feature(restored[0]))

    def test_restore_lookup_gives_full_fidelity_copy(self):
        full = contact("6386 Baylor", -82.017276, 29.783271,
                       status_detail="James Wesley; survey", has_iaq_survey=True,
                       iaq_response_id="R_old", match_status="matched")
        feats, _ = rebuild_field_layer(self.blob, [REAL],
                                       restore_lookup={cell_key([-82.017276, 29.783271]): full})
        restored = [f for f in feats if f["properties"].get("restored_from_field_pin")][0]
        self.assertEqual(restored["properties"]["address"], "6386 Baylor")
        self.assertEqual(restored["properties"]["status_detail"], "James Wesley; survey")
        self.assertNotIn("iaq_response_id", restored["properties"])
        self.assertNotIn("match_status", restored["properties"])
        self.assertTrue(full["properties"]["has_iaq_survey"], "lookup source must not be mutated")

    def test_new_table_row_is_added_from_table_values(self):
        new = row("new-1", -82.02, 29.78, status="Left Info", address="6409 Beloit Ave")
        feats, rep = rebuild_field_layer(self.blob, [REAL, new])
        self.assertEqual(rep["added"], ["new-1"])
        f = [x for x in feats if x["properties"].get("field_point_id") == "new-1"][0]
        self.assertEqual(f["properties"]["status"], "Left Info")
        self.assertEqual(f["properties"]["address"], "6409 Beloit Ave")

    def test_carry_iaq_link_copies_link_from_old_copy(self):
        old = field_copy(REAL["id"], REAL["lon"], REAL["lat"], "Carey Morford",
                         has_iaq_survey=True, iaq_response_id="R_6XiLZgAcnHtf16F",
                         iaq_overall_risk=50, iaq_risk_tier="Medium")
        feats, _ = rebuild_field_layer([self.c1], [dict(REAL, status="Left Info")],
                                       carry_iaq_link_from=[old])
        p = [f for f in feats if is_field_feature(f)][0]["properties"]
        self.assertEqual(p["iaq_response_id"], "R_6XiLZgAcnHtf16F")
        self.assertEqual(p["status"], "Completed")

    def test_unchanged_input_has_identical_signature(self):
        a, _ = rebuild_field_layer(self.blob, [REAL])
        b, _ = rebuild_field_layer(a, [REAL])
        self.assertEqual(features_signature(a), features_signature(b))


class _Sel:
    def __init__(self, sb, cols):
        self.sb, self.cols, self.start = sb, cols, 0

    def range(self, a, _b):
        self.start = a
        return self

    def execute(self):
        return self.sb.page(self.cols, self.start)


class _Tbl:
    def __init__(self, sb):
        self.sb = sb

    def select(self, cols):
        return _Sel(self.sb, cols)


class _PagedSB:
    def __init__(self, n_rows, reject_address=False, fail_at=None):
        self.rows = [{"id": f"id-{i:05d}", "lat": 29.7, "lon": -82.0} for i in range(n_rows)][::-1]
        self.reject_address, self.fail_at, self.calls = reject_address, fail_at, []

    def table(self, _name):
        return _Tbl(self)

    def page(self, cols, start):
        self.calls.append((cols, start))
        if self.reject_address and "address" in cols:
            raise Exception("column field_survey_points.address does not exist")
        if self.fail_at is not None and start >= self.fail_at:
            raise Exception("timeout")

        class R:
            pass
        r = R()
        r.data = self.rows[start:start + 1000]
        return r


class LoadAllFieldRowsTests(unittest.TestCase):
    def test_pages_past_1000_and_sorts_by_id(self):
        sb = _PagedSB(2500)
        rows = load_all_field_rows(sb)
        self.assertEqual(len(rows), 2500)
        self.assertEqual(rows[0]["id"], "id-00000")
        self.assertEqual([c[1] for c in sb.calls], [0, 1000, 2000])

    def test_falls_back_once_when_migration_27_missing(self):
        sb = _PagedSB(3, reject_address=True)
        self.assertEqual(len(load_all_field_rows(sb)), 3)
        self.assertIn("address", sb.calls[0][0])
        self.assertNotIn("address", sb.calls[1][0])

    def test_a_later_page_failure_raises_instead_of_returning_partial_rows(self):
        with self.assertRaises(Exception):
            load_all_field_rows(_PagedSB(2500, fail_at=1000))


if __name__ == "__main__":
    unittest.main()
