"""Security-fix regression tests for the community-contact PII redaction.

Commit 1bc5481 (dedup_contacts_at_parcel) started stamping a collapsed
household's `address`, `matched_address`, and `street_name` onto each
`coincident_contacts` entry alongside the pre-existing `notes` leak. The
top-level `_strip_pii` in both api/survey-points.py and
api/community-contacts.py only ever stripped `properties` at the top
level, so all four PII fields (and any future addition to `_PII_FIELDS`)
reached unauthenticated/guest callers through the nested list.

These tests prove `_strip_pii` now recurses into `coincident_contacts`
and drops the same `_PII_FIELDS` key set from every nested entry, while
preserving the non-PII keys the popup relies on (`status`, `collected_at`,
`source`, `has_iaq_survey`, `street_mismatch`), and that malformed shapes
(absent / null / empty / non-dict junk) never raise.

api/survey-points.py and api/community-contacts.py are loaded via
importlib because their filenames contain hyphens and aren't valid
Python module paths (same pattern as tests/test_iaq_match_status_refresh.py
uses for api/daily-refresh.py).
"""
from __future__ import annotations

import importlib.util
import pathlib
import unittest

_API_DIR = pathlib.Path(__file__).resolve().parent.parent / "api"


def _load(modname: str, filename: str):
    spec = importlib.util.spec_from_file_location(modname, _API_DIR / filename)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


survey_points = _load("_survey_points_for_pii_tests", "survey-points.py")
community_contacts = _load("_community_contacts_for_pii_tests", "community-contacts.py")


def _feature_with_coincident(coincident):
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [-82.0, 29.7]},
        "properties": {
            "address": "1 A St",
            "notes": "top-level note",
            "status": "Completed",
            "coincident_contacts": coincident,
        },
    }


def _one_leaked_entry():
    return {
        "status": "No Answer",
        "street_name": "B St",
        "notes": "loser's canvassing note",
        "collected_at": "2026-08-01",
        "source": "field",
        "has_iaq_survey": True,
        "address": "2 B St",
        "matched_address": "1 A St",
        "street_mismatch": True,
    }


class _StripPiiSharedBehavior:
    """Mixin run against both survey-points and community-contacts modules
    (they carry independent copies of `_strip_pii`/`_PII_FIELDS`)."""

    module = None  # set by subclass

    def _strip(self, geojson):
        return self.module._strip_pii(geojson)

    def test_nested_pii_fields_are_removed(self):
        fc = {"type": "FeatureCollection",
              "features": [_feature_with_coincident([_one_leaked_entry()])]}
        out = self._strip(fc)
        entry = out["features"][0]["properties"]["coincident_contacts"][0]
        for pii_key in ("address", "matched_address", "street_name", "notes"):
            self.assertNotIn(pii_key, entry, f"{pii_key} leaked through coincident_contacts")

    def test_nested_non_pii_fields_survive(self):
        fc = {"type": "FeatureCollection",
              "features": [_feature_with_coincident([_one_leaked_entry()])]}
        out = self._strip(fc)
        entry = out["features"][0]["properties"]["coincident_contacts"][0]
        self.assertEqual(entry["status"], "No Answer")
        self.assertEqual(entry["collected_at"], "2026-08-01")
        self.assertEqual(entry["source"], "field")
        self.assertIs(entry["has_iaq_survey"], True)
        self.assertIs(entry["street_mismatch"], True)

    def test_top_level_pii_still_stripped(self):
        fc = {"type": "FeatureCollection",
              "features": [_feature_with_coincident([])]}
        out = self._strip(fc)
        props = out["features"][0]["properties"]
        self.assertNotIn("address", props)
        self.assertNotIn("notes", props)

    def test_absent_coincident_contacts_does_not_raise(self):
        f = {"type": "Feature", "geometry": {"type": "Point", "coordinates": [0, 0]},
             "properties": {"address": "1 A St", "status": "Completed"}}
        out = self._strip({"type": "FeatureCollection", "features": [f]})
        self.assertNotIn("coincident_contacts", out["features"][0]["properties"])

    def test_null_coincident_contacts_does_not_raise(self):
        out = self._strip({"type": "FeatureCollection",
                            "features": [_feature_with_coincident(None)]})
        self.assertIsNone(out["features"][0]["properties"]["coincident_contacts"])

    def test_empty_list_coincident_contacts_does_not_raise(self):
        out = self._strip({"type": "FeatureCollection",
                            "features": [_feature_with_coincident([])]})
        self.assertEqual(out["features"][0]["properties"]["coincident_contacts"], [])

    def test_non_dict_junk_in_coincident_contacts_does_not_raise(self):
        junk = ["not-a-dict", 42, None, ["nested", "list"]]
        out = self._strip({"type": "FeatureCollection",
                            "features": [_feature_with_coincident(junk)]})
        cleaned = out["features"][0]["properties"]["coincident_contacts"]
        self.assertEqual(cleaned, junk)

    def test_mixed_valid_and_junk_entries_does_not_raise(self):
        mixed = [_one_leaked_entry(), "junk", None]
        out = self._strip({"type": "FeatureCollection",
                            "features": [_feature_with_coincident(mixed)]})
        cleaned = out["features"][0]["properties"]["coincident_contacts"]
        self.assertNotIn("address", cleaned[0])
        self.assertEqual(cleaned[1], "junk")
        self.assertIsNone(cleaned[2])

    def test_multiple_coincident_entries_all_stripped(self):
        entries = [_one_leaked_entry(), dict(_one_leaked_entry(), address="3 C St")]
        out = self._strip({"type": "FeatureCollection",
                            "features": [_feature_with_coincident(entries)]})
        cleaned = out["features"][0]["properties"]["coincident_contacts"]
        self.assertEqual(len(cleaned), 2)
        for entry in cleaned:
            self.assertNotIn("address", entry)


class SurveyPointsStripPiiTests(_StripPiiSharedBehavior, unittest.TestCase):
    module = survey_points


class CommunityContactsStripPiiTests(_StripPiiSharedBehavior, unittest.TestCase):
    module = community_contacts


if __name__ == "__main__":
    unittest.main()
