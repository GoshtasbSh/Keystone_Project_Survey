"""Tests for api/unmatched-iaq.py.

The module filename has a hyphen (it's a Vercel serverless route, one file
per URL path — matches api/iaq-points.py, api/survey-points.py), so it
can't be imported with a normal dotted `import`. Load it by file path
instead, the same way `final review/feature-verify/local_dev_server.py`
does for local dev.
"""
import importlib.util
import pathlib
import unittest

API_DIR = pathlib.Path(__file__).resolve().parent.parent / "api"

import sys
sys.path.insert(0, str(API_DIR))

_spec = importlib.util.spec_from_file_location(
    "api_unmatched_iaq", API_DIR / "unmatched-iaq.py")
unmatched_iaq = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(unmatched_iaq)


def iaq(rid, lon, lat):
    return {"type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": {"response_id": rid, "iaq_matched": False,
                           "overall_risk": 27, "risk_tier": "Low",
                           "tired_freq": "weekly"}}


SQUARE_INDEX = {
    "version": 1,
    "parcels": [{
        "parcel_id": "P1",
        "address": "6409 BELOIT Ave",
        "bbox": [-82.0193, 29.7835, -82.0189, 29.7841],
        "ring": [[-82.0193, 29.7835], [-82.0189, 29.7835],
                 [-82.0189, 29.7841], [-82.0193, 29.7841], [-82.0193, 29.7835]],
        "holes": [],
    }],
}

# Same outer boundary, with an interior ring (hole) around the point
# SQUARE_INDEX's own tests use as "inside" — proves the endpoint honours
# holes end-to-end, not just the shared lookup_parcel() helper in isolation.
SQUARE_WITH_HOLE_INDEX = {
    "version": 1,
    "parcels": [{
        "parcel_id": "P3",
        "address": "6411 BELOIT Ave",
        "bbox": [-82.0193, 29.7835, -82.0189, 29.7841],
        "ring": [[-82.0193, 29.7835], [-82.0189, 29.7835],
                 [-82.0189, 29.7841], [-82.0193, 29.7841], [-82.0193, 29.7835]],
        "holes": [[[-82.01915, 29.7837], [-82.01905, 29.7837],
                   [-82.01905, 29.7839], [-82.01915, 29.7839], [-82.01915, 29.7837]]],
    }],
}


class UnmatchedIaqTests(unittest.TestCase):
    def test_missing_index_degrades_gracefully(self):
        """The parcel_address_index blob hasn't been published yet in
        production. The endpoint must still return the orphan, with the
        fallback address, and must not raise."""
        out = unmatched_iaq.build_unmatched_iaq(
            [iaq("R_1", -82.0191, 29.7838)], [], None)
        self.assertEqual(len(out["features"]), 1)
        self.assertEqual(out["features"][0]["properties"]["parcel_address"],
                         "Address not on file")

    def test_empty_index_payload_also_degrades_gracefully(self):
        out = unmatched_iaq.build_unmatched_iaq(
            [iaq("R_1", -82.0191, 29.7838)], [], {})
        self.assertEqual(out["features"][0]["properties"]["parcel_address"],
                         "Address not on file")

    def test_point_inside_a_known_parcel_resolves_the_cadastral_address(self):
        out = unmatched_iaq.build_unmatched_iaq(
            [iaq("R_1", -82.0191, 29.7838)], [], SQUARE_INDEX)
        self.assertEqual(out["features"][0]["properties"]["parcel_address"],
                         "6409 BELOIT Ave")

    def test_no_orphans_returns_empty_feature_collection(self):
        out = unmatched_iaq.build_unmatched_iaq([], [], SQUARE_INDEX)
        self.assertEqual(out, {"type": "FeatureCollection", "features": []})

    def test_survey_answer_fields_are_stripped(self):
        out = unmatched_iaq.build_unmatched_iaq(
            [iaq("R_1", -82.0191, 29.7838)], [], SQUARE_INDEX)
        self.assertNotIn("tired_freq", out["features"][0]["properties"])

    def test_orphan_flag_and_parcel_id_are_attached(self):
        out = unmatched_iaq.build_unmatched_iaq(
            [iaq("R_1", -82.0191, 29.7838)], [], SQUARE_INDEX)
        props = out["features"][0]["properties"]
        self.assertTrue(props["orphan"])
        self.assertEqual(props["parcel_id"], "P1")

    def test_point_inside_a_hole_falls_back_not_the_hole_parcels_address(self):
        """2026-08-10 finding: a confidently wrong address is worse than the
        fallback — a point sitting inside an interior ring must never be
        handed that parcel's street address."""
        out = unmatched_iaq.build_unmatched_iaq(
            [iaq("R_1", -82.0191, 29.7838)], [], SQUARE_WITH_HOLE_INDEX)
        self.assertEqual(out["features"][0]["properties"]["parcel_address"],
                         "Address not on file")

    def test_point_in_the_solid_part_of_a_parcel_with_a_hole_still_resolves(self):
        out = unmatched_iaq.build_unmatched_iaq(
            [iaq("R_1", -82.01925, 29.7836)], [], SQUARE_WITH_HOLE_INDEX)
        self.assertEqual(out["features"][0]["properties"]["parcel_address"],
                         "6411 BELOIT Ave")
