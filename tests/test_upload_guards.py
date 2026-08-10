import unittest

from api._processing import diff_iaq_response_ids


def feat(rid):
    return {"type": "Feature",
            "geometry": {"type": "Point", "coordinates": [-82.0, 29.7]},
            "properties": {"response_id": rid}}


class DiffResponseIdsTests(unittest.TestCase):
    def test_no_regression_when_incoming_is_a_superset(self):
        d = diff_iaq_response_ids([feat("R_1"), feat("R_2")],
                                  [feat("R_1"), feat("R_2"), feat("R_3")])
        self.assertEqual(d["dropped"], [])
        self.assertEqual(d["added"], ["R_3"])
        self.assertFalse(d["is_regression"])

    def test_regression_when_incoming_drops_a_response(self):
        d = diff_iaq_response_ids([feat("R_1"), feat("R_2"), feat("R_3")],
                                  [feat("R_1"), feat("R_2")])
        self.assertEqual(d["dropped"], ["R_3"])
        self.assertTrue(d["is_regression"])

    def test_first_ever_upload_is_never_a_regression(self):
        d = diff_iaq_response_ids([], [feat("R_1")])
        self.assertFalse(d["is_regression"])
        self.assertEqual(d["added"], ["R_1"])

    def test_missing_response_ids_are_ignored_not_counted_as_dropped(self):
        """Pre-2026-05 blobs have no response_id — must not trigger a false alarm."""
        old = [{"properties": {}}, {"properties": {}}]
        d = diff_iaq_response_ids(old, [feat("R_1")])
        self.assertFalse(d["is_regression"])
        self.assertEqual(d["dropped"], [])

    def test_identical_upload_is_a_no_op(self):
        d = diff_iaq_response_ids([feat("R_1")], [feat("R_1")])
        self.assertFalse(d["is_regression"])
        self.assertEqual(d["dropped"], [])
        self.assertEqual(d["added"], [])
