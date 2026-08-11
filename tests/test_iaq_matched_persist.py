"""Tests for Task 14: field_survey_points.iaq_matched (added by migration 22)
was `false` on all rows because no code path ever wrote it. This proves the
one-and-only UPDATE this plan makes against an existing field_survey_points
row (`_upgrade_field_points_iaq_matched` in api/upload.py, extending the
pre-existing `status: 'Completed'` bulk update) is scoped exactly as the
ruling requires:

  - touches ONLY `status` and `iaq_matched` — never `notes`, `lat`, `lon`,
    or `collected_at`
  - only ever sets iaq_matched to True (never False)
  - only touches the rows in `upgraded_ids` — no widening
  - issues no write at all when `upgraded_ids` is empty
  - never raises, even if the update itself fails

No network, no real Supabase client — `_FakeSupabase` records every
update as (table_name, ids, patch_dict) so we can assert on it directly.
"""
import unittest

from api.upload import _upgrade_field_points_iaq_matched


class _FakeUpdateQuery:
    def __init__(self, client, name, patch):
        self._client = client
        self._name = name
        self._patch = patch
        self._ids = None

    def in_(self, _col, ids):
        self._ids = list(ids)
        return self

    def execute(self):
        return self._client._record_update(self._name, self._ids, self._patch)


class _FakeTable:
    def __init__(self, name, client):
        self._name = name
        self._client = client

    def update(self, patch):
        return _FakeUpdateQuery(self._client, self._name, patch)


class _FakeSupabase:
    def __init__(self, raise_on_update=False):
        self.update_calls = []
        self._raise_on_update = raise_on_update

    def table(self, name):
        return _FakeTable(name, self)

    def _record_update(self, name, ids, patch):
        self.update_calls.append((name, ids, dict(patch)))
        if self._raise_on_update:
            raise Exception("simulated Supabase failure")


class UpgradeFieldPointsIaqMatchedTests(unittest.TestCase):
    def test_sets_status_and_iaq_matched_only(self):
        sb = _FakeSupabase()
        _upgrade_field_points_iaq_matched(sb, ["id-1", "id-2"])

        self.assertEqual(len(sb.update_calls), 1)
        table, ids, patch = sb.update_calls[0]
        self.assertEqual(table, "field_survey_points")
        self.assertEqual(set(ids), {"id-1", "id-2"})
        # Exactly these two keys — never notes/lat/lon/collected_at.
        self.assertEqual(set(patch.keys()), {"status", "iaq_matched"})
        self.assertEqual(patch["status"], "Completed")
        self.assertIs(patch["iaq_matched"], True)

    def test_never_sets_iaq_matched_false(self):
        sb = _FakeSupabase()
        _upgrade_field_points_iaq_matched(sb, ["id-1"])
        _, _, patch = sb.update_calls[0]
        self.assertTrue(patch["iaq_matched"])

    def test_only_touches_the_given_ids_no_widening(self):
        sb = _FakeSupabase()
        _upgrade_field_points_iaq_matched(sb, ["only-this-id"])
        _, ids, _ = sb.update_calls[0]
        self.assertEqual(ids, ["only-this-id"])

    def test_empty_upgraded_ids_issues_no_write(self):
        sb = _FakeSupabase()
        _upgrade_field_points_iaq_matched(sb, [])
        self.assertEqual(sb.update_calls, [], "must not touch the table at all with nothing to upgrade")

    def test_none_upgraded_ids_issues_no_write(self):
        sb = _FakeSupabase()
        _upgrade_field_points_iaq_matched(sb, None)
        self.assertEqual(sb.update_calls, [])

    def test_swallows_exception_instead_of_failing_the_upload(self):
        sb = _FakeSupabase(raise_on_update=True)
        try:
            _upgrade_field_points_iaq_matched(sb, ["id-1"])
        except Exception as e:  # pragma: no cover — must not happen
            self.fail(f"_upgrade_field_points_iaq_matched must swallow the failure, but raised {e!r}")
        self.assertEqual(len(sb.update_calls), 1, "the attempt was still made")


if __name__ == '__main__':
    unittest.main()
