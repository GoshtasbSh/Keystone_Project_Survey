import unittest

from scripts.build_parcel_address_index import build_index, lookup_address


SQUARE = {
    "type": "Feature",
    "properties": {"parcel_id": "P1", "address": "6409 BELOIT Ave"},
    "geometry": {"type": "Polygon", "coordinates": [[
        [-82.0193, 29.7835], [-82.0189, 29.7835],
        [-82.0189, 29.7841], [-82.0193, 29.7841], [-82.0193, 29.7835]]]},
}


class ParcelAddressIndexTests(unittest.TestCase):
    def test_index_has_one_entry_per_parcel(self):
        idx = build_index({"features": [SQUARE]})
        self.assertEqual(len(idx["parcels"]), 1)
        self.assertEqual(idx["parcels"][0]["address"], "6409 BELOIT Ave")

    def test_point_inside_the_parcel_resolves_to_its_address(self):
        idx = build_index({"features": [SQUARE]})
        self.assertEqual(lookup_address(idx, -82.0191, 29.7838), "6409 BELOIT Ave")

    def test_point_far_outside_resolves_to_none(self):
        idx = build_index({"features": [SQUARE]})
        self.assertIsNone(lookup_address(idx, -82.5, 29.9))

    def test_parcels_without_an_address_are_skipped(self):
        blank = {**SQUARE, "properties": {"parcel_id": "P2", "address": ""}}
        self.assertEqual(len(build_index({"features": [blank]})["parcels"]), 0)
