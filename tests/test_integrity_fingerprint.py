import unittest

from scripts.integrity_fingerprint import fingerprint


class FingerprintTests(unittest.TestCase):
    def _blobs(self):
        contacts = {"features": [
            {"geometry": {"coordinates": [-82.0, 29.7]},
             "properties": {"address": "1 A St", "status": "Completed",
                            "has_iaq_survey": True}},
            {"geometry": {"coordinates": [-82.1, 29.7]},
             "properties": {"address": "2 A St", "status": "No Answer"}},
        ]}
        iaq = {"geojson": {"features": [
            {"geometry": {"coordinates": [-82.0, 29.7]},
             "properties": {"response_id": "R_1", "iaq_matched": True,
                            "overall_risk": 40}},
            {"geometry": {"coordinates": [-82.2, 29.7]},
             "properties": {"response_id": "R_2", "iaq_matched": False,
                            "overall_risk": 10}},
        ]}}
        return contacts, iaq

    def test_fingerprint_is_stable_for_identical_input(self):
        c, i = self._blobs()
        self.assertEqual(fingerprint(c, i), fingerprint(c, i))

    def test_fingerprint_counts_are_reported(self):
        c, i = self._blobs()
        fp = fingerprint(c, i)
        self.assertEqual(fp["n_contacts"], 2)
        self.assertEqual(fp["n_iaq"], 2)
        self.assertEqual(fp["iaq_response_ids_sha256"],
                         fingerprint(c, i)["iaq_response_ids_sha256"])

    def test_fingerprint_changes_when_a_response_disappears(self):
        c, i = self._blobs()
        before = fingerprint(c, i)
        i["geojson"]["features"].pop()
        after = fingerprint(c, i)
        self.assertNotEqual(before["iaq_response_ids_sha256"],
                            after["iaq_response_ids_sha256"])

    def test_fingerprint_changes_when_a_risk_score_changes(self):
        c, i = self._blobs()
        before = fingerprint(c, i)
        i["geojson"]["features"][0]["properties"]["overall_risk"] = 99
        self.assertNotEqual(before["scores_sha256"], fingerprint(c, i)["scores_sha256"])
