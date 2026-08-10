import unittest

from scripts.build_parcel_address_index import build_index, lookup_address


SQUARE = {
    "type": "Feature",
    "properties": {"parcel_id": "P1", "address": "6409 BELOIT Ave"},
    "geometry": {"type": "Polygon", "coordinates": [[
        [-82.0193, 29.7835], [-82.0189, 29.7835],
        [-82.0189, 29.7841], [-82.0193, 29.7841], [-82.0193, 29.7835]]]},
}

# Same outer boundary as SQUARE, but with a small interior ring (a hole —
# e.g. a courtyard or an easement cut out of the parcel) around the exact
# point the plain-SQUARE tests use as "inside".
SQUARE_WITH_HOLE = {
    "type": "Feature",
    "properties": {"parcel_id": "P3", "address": "6411 BELOIT Ave"},
    "geometry": {"type": "Polygon", "coordinates": [
        [[-82.0193, 29.7835], [-82.0189, 29.7835],
         [-82.0189, 29.7841], [-82.0193, 29.7841], [-82.0193, 29.7835]],
        [[-82.01915, 29.7837], [-82.01905, 29.7837],
         [-82.01905, 29.7839], [-82.01915, 29.7839], [-82.01915, 29.7837]],
    ]},
}

# One parcel made of two disjoint squares (e.g. split by a road) — the
# MultiPolygon case.
MULTI_SQUARE = {
    "type": "Feature",
    "properties": {"parcel_id": "P4", "address": "10 MULTI Rd"},
    "geometry": {"type": "MultiPolygon", "coordinates": [
        [[[-82.0193, 29.7835], [-82.0189, 29.7835],
          [-82.0189, 29.7841], [-82.0193, 29.7841], [-82.0193, 29.7835]]],
        [[[-82.0500, 29.8000], [-82.0490, 29.8000],
          [-82.0490, 29.8010], [-82.0500, 29.8010], [-82.0500, 29.8000]]],
    ]},
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

    def test_point_inside_a_hole_resolves_to_none(self):
        """2026-08-10 finding: a point inside an interior ring (hole) must
        NOT resolve to that parcel's address, even though it sits inside
        the outer ring."""
        idx = build_index({"features": [SQUARE_WITH_HOLE]})
        self.assertIsNone(lookup_address(idx, -82.0191, 29.7838))

    def test_point_in_the_solid_part_of_a_parcel_with_a_hole_still_resolves(self):
        idx = build_index({"features": [SQUARE_WITH_HOLE]})
        self.assertEqual(lookup_address(idx, -82.01925, 29.7836), "6411 BELOIT Ave")

    def test_multipolygon_parcel_resolves_from_either_part(self):
        idx = build_index({"features": [MULTI_SQUARE]})
        self.assertEqual(len(idx["parcels"]), 2)
        self.assertEqual(lookup_address(idx, -82.0191, 29.7838), "10 MULTI Rd")
        self.assertEqual(lookup_address(idx, -82.0495, 29.8005), "10 MULTI Rd")

    def test_multipolygon_point_between_the_two_parts_resolves_to_none(self):
        idx = build_index({"features": [MULTI_SQUARE]})
        self.assertIsNone(lookup_address(idx, -82.03, 29.79))
