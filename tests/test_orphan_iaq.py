import unittest

from api.survey_logic import orphan_iaq_features


def iaq(rid, lon, lat, matched=False):
    return {"type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": {"response_id": rid, "iaq_matched": matched,
                           "overall_risk": 27, "risk_tier": "Low"}}


def contact(addr, lon, lat, source=None):
    return {"type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": {"address": addr, "source": source,
                           "status": "Completed"}}


class OrphanIaqTests(unittest.TestCase):
    def test_response_with_no_contact_nearby_is_an_orphan(self):
        out = orphan_iaq_features([iaq("R_1", -82.0191, 29.7838)], [])
        self.assertEqual([f["properties"]["response_id"] for f in out], ["R_1"])

    def test_response_with_an_addressed_contact_on_the_same_spot_is_not_an_orphan(self):
        out = orphan_iaq_features(
            [iaq("R_1", -82.0191, 29.7838)],
            [contact("6409 Beloit Ave", -82.0191, 29.7838)])
        self.assertEqual(out, [])

    def test_a_nameless_field_pin_does_not_rescue_an_orphan(self):
        """The 2026-07-21 regression: an anonymous field pin flipped
        iaq_matched=true and the 'needs manual fix' flag vanished, even
        though no address was ever recorded."""
        out = orphan_iaq_features(
            [iaq("R_1", -82.0191, 29.7838, matched=True)],
            [contact(None, -82.0191, 29.7838, source="field")])
        self.assertEqual([f["properties"]["response_id"] for f in out], ["R_1"])

    def test_a_contact_on_a_different_parcel_does_not_rescue_an_orphan(self):
        out = orphan_iaq_features(
            [iaq("R_1", -82.0191, 29.7838)],
            [contact("6405 Beloit Ave", -82.0187, 29.7838)])
        self.assertEqual(len(out), 1)

    def test_orphans_are_returned_with_their_geometry_intact(self):
        out = orphan_iaq_features([iaq("R_1", -82.0191, 29.7838)], [])
        self.assertEqual(out[0]["geometry"]["coordinates"], [-82.0191, 29.7838])
