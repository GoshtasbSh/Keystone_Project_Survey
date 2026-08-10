"""Tests for the upload audit-trail fallback (Task 5).

No network, no real Supabase client. `_FakeSupabase` below stands in for
`supabase.Client` and mimics the one failure mode we need to prove:
PostgREST rejects an INSERT that references a column the live schema
doesn't have yet (migration 26 not applied). `_insert_version_row` must
catch that and retry with only the original column set so an upload never
fails purely because the audit columns are missing.
"""
import unittest

from api.upload import _insert_version_row


class _FakeTable:
    def __init__(self, name, client):
        self._name = name
        self._client = client
        self._row = None

    def insert(self, row):
        self._row = row
        return self

    def execute(self):
        self._client._record_and_maybe_fail(self._name, self._row)
        return self


class _FakeSupabase:
    """Records every insert as (table_name, row_dict). Raises on the first
    `fail_first_n` inserts against `keystone_analysis_versions`, simulating
    PostgREST's "column does not exist" error for the enriched audit
    columns when migration 26 hasn't been run yet."""

    def __init__(self, fail_first_n=0):
        self.calls = []
        self._fail_remaining = fail_first_n

    def table(self, name):
        return _FakeTable(name, self)

    def _record_and_maybe_fail(self, name, row):
        self.calls.append((name, dict(row)))
        if name == 'keystone_analysis_versions' and self._fail_remaining > 0:
            self._fail_remaining -= 1
            raise Exception(
                'column "uploaded_by_user_id" of relation '
                '"keystone_analysis_versions" does not exist'
            )


class InsertVersionRowFallbackTests(unittest.TestCase):
    def test_falls_back_to_base_columns_when_enriched_insert_raises(self):
        sb = _FakeSupabase(fail_first_n=1)
        base = {'data_type': 'iaq_survey', 'payload': {}, 'label': 'x', 'n_points': 3}
        extra = {
            'uploaded_by_user_id': 'uid-1',
            'source_filename': 'V2_test.csv',
            'dropped_response_ids': [],
            'forced': False,
        }

        # Must not raise — the upload has to succeed even though the
        # migration 26 columns don't exist on this (simulated) schema.
        _insert_version_row(sb, base, extra)

        self.assertEqual(len(sb.calls), 2, "expected an enriched attempt + a base-only retry")
        table1, row1 = sb.calls[0]
        table2, row2 = sb.calls[1]
        self.assertEqual(table1, 'keystone_analysis_versions')
        self.assertEqual(table2, 'keystone_analysis_versions')

        # First attempt carried the enriched (audit-trail) columns...
        self.assertIn('uploaded_by_user_id', row1)
        self.assertIn('source_filename', row1)

        # ...the successful retry is the ORIGINAL column set only — no
        # unknown columns sent, nothing extra, nothing missing.
        self.assertEqual(row2, base)
        self.assertNotIn('uploaded_by_user_id', row2)
        self.assertNotIn('source_filename', row2)

    def test_succeeds_on_first_try_when_migration_26_is_applied(self):
        sb = _FakeSupabase(fail_first_n=0)
        base = {'data_type': 'iaq_survey', 'payload': {}, 'label': 'x', 'n_points': 3}
        extra = {'uploaded_by_user_id': 'uid-1', 'source_filename': 'good.csv'}

        _insert_version_row(sb, base, extra)

        self.assertEqual(len(sb.calls), 1, "no fallback needed — should not retry")
        _, row = sb.calls[0]
        self.assertEqual(row, {**base, **extra})

    def test_community_contact_insert_also_falls_back(self):
        """Same guarantee applies to the community_contact version insert
        in _handle_survey — _insert_version_row is table-agnostic."""
        sb = _FakeSupabase(fail_first_n=1)
        base = {'data_type': 'community_contact', 'payload': {}, 'label': 'y', 'n_points': 9}
        extra = {'uploaded_by_user_id': 'uid-2', 'source_row_count': 9}

        _insert_version_row(sb, base, extra)

        self.assertEqual(len(sb.calls), 2)
        self.assertEqual(sb.calls[1][1], base)


if __name__ == '__main__':
    unittest.main()
