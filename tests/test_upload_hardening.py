"""Audit 2026-10-13 low-priority hardening (F11, F12, F13, F14, DEP-9).
No network."""
import pathlib
import shutil
import subprocess
import tempfile
import unittest

import pandas as pd

import api._processing as P

ROOT = pathlib.Path(__file__).resolve().parent.parent


class CensusGuardTests(unittest.TestCase):
    """F11: text that cannot be an address must never be sent to Census."""

    def setUp(self):
        self.calls = []
        self._orig = P._census_geocode
        P._census_geocode = lambda addr: (self.calls.append(addr), (None, None, None))[1]

    def tearDown(self):
        P._census_geocode = self._orig

    def test_email_and_sentence_are_not_sent(self):
        idx = P.ParcelIndex()
        for text in ("jjbodyguard99@gmail.com", "I guess my land lord is Spencer Hoursman",
                     "First house right bowdoin", "12@example.com"):
            self.assertEqual(idx.geocode(text)[3], "failed")
        self.assertEqual(self.calls, [])

    def test_real_address_text_still_reaches_census(self):
        idx = P.ParcelIndex()
        idx.geocode("6406 bucknelle Ave\n Keystone Hieghts fl.\n32656")
        idx.geocode("7166 Pen BrooksSt")
        self.assertEqual(len(self.calls), 2)


class ResultsPiiTests(unittest.TestCase):
    """F13: the generic results upload must strip the typed address, GPS
    and contact block; the IAQ pipeline must still be able to read Q212."""

    def test_results_set_covers_address_gps_and_contact_columns(self):
        for col in ("Q212", "LocationLatitude", "LocationLongitude",
                    "Participation IAQ_1", "Participation IAQ_2", "Participation IAQ_6",
                    "RecipientEmail", "IPAddress"):
            self.assertIn(col, P.RESULTS_PII_COLS)

    def test_iaq_pipeline_set_does_not_drop_q212(self):
        self.assertNotIn("Q212", P.PII_COLS)


class PositionalFallbackTests(unittest.TestCase):
    """F12: a QID missing from an export WITH ImportId metadata must read as
    unanswered, never as the cell at the stale hardcoded index."""

    def _row(self):
        return pd.Series([f"cell{i}" for i in range(160)])

    def test_missing_qid_with_metadata_is_blank_and_logged(self):
        qmap = {meta[1]: meta[0] + 2 for meta in P.SURVEY_QUESTIONS.values()}
        qmap.pop("QID178")                       # 'education' vanished from the export
        miss = []
        out = P._extract_survey_extras(self._row(), qmap, miss_log=miss)
        self.assertEqual(out["education"], "")   # NOT 'cell142'
        self.assertEqual(miss, ["QID178"])
        self.assertEqual(out["employment"], "cell145")

    def test_legacy_export_without_metadata_keeps_positional_read(self):
        out = P._extract_survey_extras(self._row(), {}, miss_log=[])
        self.assertEqual(out["education"], "cell142")


if __name__ == "__main__":
    unittest.main()
