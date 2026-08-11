import unittest
from api._processing import dedup_contacts_at_parcel


def c(addr, status, lon=-82.0191, lat=29.7838):
    return {"type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": {"address": addr, "status": status,
                           "street_name": addr.split(" ", 1)[1]}}


class DedupAddressTests(unittest.TestCase):
    def test_collapsed_row_keeps_its_address(self):
        out = dedup_contacts_at_parcel([c("1 A St", "Completed"), c("2 B St", "No Answer")])
        self.assertEqual(len(out), 1)
        co = out[0]["properties"]["coincident_contacts"]
        self.assertEqual(co[0]["address"], "2 B St")

    def test_cross_street_collapse_is_flagged(self):
        out = dedup_contacts_at_parcel([c("1 A St", "Completed"), c("2 B St", "No Answer")])
        self.assertTrue(out[0]["properties"]["coincident_contacts"][0]["street_mismatch"])

    def test_same_street_collapse_is_not_flagged(self):
        out = dedup_contacts_at_parcel([c("1 A St", "Completed"), c("3 A St", "No Answer")])
        self.assertFalse(out[0]["properties"]["coincident_contacts"][0]["street_mismatch"])

    def test_matched_address_records_the_survivor(self):
        out = dedup_contacts_at_parcel([c("1 A St", "Completed"), c("2 B St", "No Answer")])
        self.assertEqual(out[0]["properties"]["coincident_contacts"][0]["matched_address"], "1 A St")


if __name__ == '__main__':
    unittest.main()
