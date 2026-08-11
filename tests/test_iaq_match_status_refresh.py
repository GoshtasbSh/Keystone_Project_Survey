"""Tests for Task 15: api/daily-refresh.py's `_refresh_iaq_match_status`.

Two responses currently have `iaq_matched=true` with a stale stored
`match_status='iaq_only'` — the field-point match pass can flip
`iaq_matched` after the IAQ blob was first tagged at upload time, and
only the browser's client-side backfill (_backfillIaqMatchStatus in
static/js/dashboard.js) ever corrected it. This proves the server-side
re-derivation matches that same rule
(`'matched' if iaq_matched else 'iaq_only'`) and mutates in place.

api/daily-refresh.py is loaded via importlib because its filename
contains a hyphen and isn't a valid Python module path.
"""
import importlib.util
import pathlib
import unittest

_MOD_PATH = pathlib.Path(__file__).resolve().parent.parent / "api" / "daily-refresh.py"
_spec = importlib.util.spec_from_file_location("_daily_refresh_for_tests", _MOD_PATH)
daily_refresh = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(daily_refresh)

_refresh_iaq_match_status = daily_refresh._refresh_iaq_match_status


class RefreshIaqMatchStatusTests(unittest.TestCase):
    def test_stale_iaq_only_becomes_matched_when_iaq_matched_true(self):
        feats = [{"properties": {"iaq_matched": True, "match_status": "iaq_only"}}]
        _refresh_iaq_match_status(feats)
        self.assertEqual(feats[0]["properties"]["match_status"], "matched")

    def test_unmatched_feature_stays_iaq_only(self):
        feats = [{"properties": {"iaq_matched": False}}]
        _refresh_iaq_match_status(feats)
        self.assertEqual(feats[0]["properties"]["match_status"], "iaq_only")

    def test_a_stale_matched_tag_is_downgraded_if_iaq_matched_is_now_false(self):
        """Symmetric correctness — the derivation is not one-directional;
        it always reflects the current iaq_matched value."""
        feats = [{"properties": {"iaq_matched": False, "match_status": "matched"}}]
        _refresh_iaq_match_status(feats)
        self.assertEqual(feats[0]["properties"]["match_status"], "iaq_only")

    def test_handles_missing_properties_without_raising(self):
        feats = [{"geometry": {}}, {"properties": None}]
        try:
            _refresh_iaq_match_status(feats)
        except Exception as e:  # pragma: no cover
            self.fail(f"must not raise on a feature with no properties, but raised {e!r}")

    def test_handles_none_and_empty_list(self):
        _refresh_iaq_match_status(None)
        _refresh_iaq_match_status([])

    def test_mutates_in_place_does_not_return_a_copy(self):
        feats = [{"properties": {"iaq_matched": True}}]
        result = _refresh_iaq_match_status(feats)
        self.assertIsNone(result)
        self.assertEqual(feats[0]["properties"]["match_status"], "matched")


if __name__ == '__main__':
    unittest.main()
