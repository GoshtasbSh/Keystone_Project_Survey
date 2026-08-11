"""Tests for GET /api/iaq-points?unmatched=1 (api/iaq-points.py).

2026-08-10 (I6 fix): this route used to be its own serverless function,
api/unmatched-iaq.py. This project sits at Vercel's 12-function Hobby-plan
ceiling, so the route was folded into api/iaq-points.py as a query flag
instead of shipping a 13th handler. The pure builder is still named
`build_unmatched_iaq` and still lives at module scope so it stays
unit-testable without an HTTP handler or a live Supabase connection.

The module filename has a hyphen (it's a Vercel serverless route, one file
per URL path — matches api/survey-points.py, api/field-points.py), so it
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
    "api_iaq_points_unmatched", API_DIR / "iaq-points.py")
iaq_points = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(iaq_points)


def iaq(rid, lon, lat, **extra_props):
    props = {"response_id": rid, "iaq_matched": False,
              "overall_risk": 27, "risk_tier": "Low",
              "tired_freq": "weekly"}
    props.update(extra_props)
    return {"type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": props}


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
        out = iaq_points.build_unmatched_iaq(
            [iaq("R_1", -82.0191, 29.7838)], [], None)
        self.assertEqual(len(out["features"]), 1)
        self.assertEqual(out["features"][0]["properties"]["parcel_address"],
                         "Address not on file")

    def test_empty_index_payload_also_degrades_gracefully(self):
        out = iaq_points.build_unmatched_iaq(
            [iaq("R_1", -82.0191, 29.7838)], [], {})
        self.assertEqual(out["features"][0]["properties"]["parcel_address"],
                         "Address not on file")

    def test_point_inside_a_known_parcel_resolves_the_cadastral_address(self):
        out = iaq_points.build_unmatched_iaq(
            [iaq("R_1", -82.0191, 29.7838)], [], SQUARE_INDEX)
        self.assertEqual(out["features"][0]["properties"]["parcel_address"],
                         "6409 BELOIT Ave")

    def test_no_orphans_returns_empty_feature_collection(self):
        out = iaq_points.build_unmatched_iaq([], [], SQUARE_INDEX)
        self.assertEqual(out, {"type": "FeatureCollection", "features": []})

    def test_survey_answer_fields_are_stripped(self):
        out = iaq_points.build_unmatched_iaq(
            [iaq("R_1", -82.0191, 29.7838)], [], SQUARE_INDEX)
        self.assertNotIn("tired_freq", out["features"][0]["properties"])

    def test_orphan_flag_and_parcel_id_are_attached(self):
        out = iaq_points.build_unmatched_iaq(
            [iaq("R_1", -82.0191, 29.7838)], [], SQUARE_INDEX)
        props = out["features"][0]["properties"]
        self.assertTrue(props["orphan"])
        self.assertEqual(props["parcel_id"], "P1")

    def test_point_inside_a_hole_falls_back_not_the_hole_parcels_address(self):
        """2026-08-10 finding: a confidently wrong address is worse than the
        fallback — a point sitting inside an interior ring must never be
        handed that parcel's street address."""
        out = iaq_points.build_unmatched_iaq(
            [iaq("R_1", -82.0191, 29.7838)], [], SQUARE_WITH_HOLE_INDEX)
        self.assertEqual(out["features"][0]["properties"]["parcel_address"],
                         "Address not on file")

    def test_point_in_the_solid_part_of_a_parcel_with_a_hole_still_resolves(self):
        out = iaq_points.build_unmatched_iaq(
            [iaq("R_1", -82.01925, 29.7836)], [], SQUARE_WITH_HOLE_INDEX)
        self.assertEqual(out["features"][0]["properties"]["parcel_address"],
                         "6411 BELOIT Ave")

    def test_health_fields_are_never_emitted_even_when_present(self):
        """I2 fix: a blacklist (strip_survey_answers) is not enough — it
        never covered has_mold/respiratory_ill/asthma_freq/wheeze_freq/
        headache_freq/hospital_visit/health_score, so a feature carrying
        those would ship publicly, now stamped with a street address. The
        builder must use an explicit WHITELIST so unknown/unlisted fields
        are dropped by default, not opted out one at a time."""
        f = iaq("R_1", -82.0191, 29.7838,
                has_mold=True, respiratory_ill="yes", asthma_freq="weekly",
                wheeze_freq="never", headache_freq="daily",
                hospital_visit="yes", health_score=42,
                raw_address="123 Secret Ln", afford_strategy="skip meals")
        out = iaq_points.build_unmatched_iaq([f], [], SQUARE_INDEX)
        props = out["features"][0]["properties"]
        for leaked_key in ("has_mold", "respiratory_ill", "asthma_freq",
                           "wheeze_freq", "headache_freq", "hospital_visit",
                           "health_score", "raw_address", "afford_strategy"):
            self.assertNotIn(leaked_key, props)
        # And the fields the two map consumers actually need are still there.
        for kept_key in ("response_id", "parcel_address", "parcel_id",
                         "orphan", "overall_risk", "risk_tier"):
            self.assertIn(kept_key, props)

    def test_unmatched_route_reachable_via_query_flag_on_iaq_points_handler(self):
        """I6 fix: the route folds into api/iaq-points.py as ?unmatched=1
        instead of shipping as its own Vercel function (13th handler would
        risk the whole deploy on the 12-function Hobby ceiling)."""
        self.assertTrue(hasattr(iaq_points, "handler"))
        self.assertTrue(hasattr(iaq_points, "build_unmatched_iaq"))


if __name__ == "__main__":
    unittest.main()
