"""Tests for the Task 13 migration-27 fallback: `field_survey_points.address`
is authored (supabase/migrations/27_field_point_address.sql) but NOT applied
to production as part of this change. Every code path that reads or writes
that column must tolerate its absence — degrade to not sending/reading it
rather than erroring, mirroring migration 26's `_insert_version_row` pattern
(see tests/test_upload_audit.py).

No network, no real Supabase client — fakes simulate PostgREST rejecting a
SELECT/INSERT that references a column the live schema doesn't have.
"""
import unittest

from api.upload import _load_all_field_features, _field_row_to_feature
from api.guest import _insert_field_point_row


# ── api/upload.py: _load_all_field_features (SELECT fallback) ─────────────

class _FakeSelectQuery:
    def __init__(self, client, cols):
        self._client = client
        self._cols = cols

    def range(self, *_a, **_k):
        return self

    def execute(self):
        return self._client._select(self._cols)


class _FakeTable:
    def __init__(self, client):
        self._client = client

    def select(self, cols):
        return _FakeSelectQuery(self._client, cols)


class _FakeResult:
    def __init__(self, data):
        self.data = data


class _FakeSupabaseSelect:
    """Rejects any SELECT that mentions `address` — simulating migration 27
    not being applied — and returns real rows for the base column set."""

    def __init__(self, rows):
        self._rows = rows
        self.select_calls = []

    def table(self, _name):
        return _FakeTable(self)

    def _select(self, cols):
        self.select_calls.append(cols)
        if 'address' in cols:
            raise Exception('column field_survey_points.address does not exist')
        return _FakeResult(self._rows)


class LoadAllFieldFeaturesFallbackTests(unittest.TestCase):
    def test_falls_back_to_base_columns_when_address_select_fails(self):
        rows = [{'id': 1, 'lat': 29.78, 'lon': -82.02, 'status': 'Completed',
                 'notes': '', 'collector_id': None, 'collector_name': 'A',
                 'collected_at': '2026-08-01T00:00:00Z'}]
        sb = _FakeSupabaseSelect(rows)

        feats = _load_all_field_features(sb)

        self.assertEqual(len(sb.select_calls), 2, "expected an enriched attempt + a base-only retry")
        self.assertIn('address', sb.select_calls[0])
        self.assertNotIn('address', sb.select_calls[1])
        self.assertEqual(len(feats), 1)
        # Falls back cleanly — the feature still builds, with no address.
        self.assertIsNone(feats[0]['properties']['address'])
        self.assertEqual(feats[0]['properties']['field_point_id'], 1)

    def test_succeeds_on_first_try_when_migration_27_is_applied(self):
        rows = [{'id': 2, 'lat': 29.78, 'lon': -82.02, 'status': 'Completed',
                 'notes': '', 'collector_id': None, 'collector_name': 'A',
                 'collected_at': '2026-08-01T00:00:00Z', 'address': '6409 Beloit Ave'}]

        class _FakeSupabaseOk(_FakeSupabaseSelect):
            def _select(self, cols):
                self.select_calls.append(cols)
                return _FakeResult(self._rows)

        sb = _FakeSupabaseOk(rows)
        feats = _load_all_field_features(sb)

        self.assertEqual(len(sb.select_calls), 1, "no fallback needed — should not retry")
        self.assertEqual(feats[0]['properties']['address'], '6409 Beloit Ave')


class FieldRowToFeatureTests(unittest.TestCase):
    def test_reads_address_when_present(self):
        f = _field_row_to_feature({'id': 1, 'lat': 1.0, 'lon': 2.0, 'address': '1 Main St'})
        self.assertEqual(f['properties']['address'], '1 Main St')

    def test_address_is_none_when_column_missing_from_row(self):
        f = _field_row_to_feature({'id': 1, 'lat': 1.0, 'lon': 2.0})
        self.assertIsNone(f['properties']['address'])


# ── api/guest.py: _insert_field_point_row (INSERT fallback) ───────────────

class _FakeInsertTable:
    def __init__(self, name, client):
        self._name = name
        self._client = client
        self._row = None

    def insert(self, row):
        self._row = row
        return self

    def execute(self):
        return self._client._insert(self._name, self._row)


class _FakeSupabaseInsert:
    """Rejects the first `fail_first_n` inserts against field_survey_points,
    simulating PostgREST's "column does not exist" error for `address` when
    migration 27 hasn't been run yet."""

    def __init__(self, fail_first_n=0):
        self.calls = []
        self._fail_remaining = fail_first_n

    def table(self, name):
        return _FakeInsertTable(name, self)

    def _insert(self, name, row):
        self.calls.append((name, dict(row)))
        if name == 'field_survey_points' and self._fail_remaining > 0:
            self._fail_remaining -= 1
            raise Exception('column "address" of relation "field_survey_points" does not exist')
        return _FakeResult([{**row, 'id': 'row-1'}])


class InsertFieldPointRowFallbackTests(unittest.TestCase):
    def test_falls_back_to_base_fields_when_enriched_insert_raises(self):
        sb = _FakeSupabaseInsert(fail_first_n=1)
        base = {'lat': 29.78, 'lon': -82.02, 'status': 'Completed',
                'notes': None, 'collector_id': None, 'collector_name': 'Carey',
                'guest_session_id': 'g1', 'is_offline': False}

        row = _insert_field_point_row(sb, base, '6409 Beloit Ave')

        self.assertEqual(len(sb.calls), 2, "expected an enriched attempt + a base-only retry")
        table1, row1 = sb.calls[0]
        table2, row2 = sb.calls[1]
        self.assertEqual(table1, 'field_survey_points')
        self.assertEqual(table2, 'field_survey_points')
        self.assertIn('address', row1)
        self.assertNotIn('address', row2, "the successful retry must not send the missing column")
        self.assertEqual(row2, base)
        self.assertEqual(row['id'], 'row-1')

    def test_succeeds_on_first_try_when_address_column_exists(self):
        sb = _FakeSupabaseInsert(fail_first_n=0)
        base = {'lat': 29.78, 'lon': -82.02, 'status': 'Completed',
                'notes': None, 'collector_id': None, 'collector_name': 'Carey',
                'guest_session_id': 'g1', 'is_offline': False}

        row = _insert_field_point_row(sb, base, '6409 Beloit Ave')

        self.assertEqual(len(sb.calls), 1, "no fallback needed — should not retry")
        _, sent = sb.calls[0]
        self.assertEqual(sent['address'], '6409 Beloit Ave')

    def test_no_address_given_skips_enriched_attempt_entirely(self):
        sb = _FakeSupabaseInsert(fail_first_n=0)
        base = {'lat': 29.78, 'lon': -82.02, 'status': 'Completed',
                'notes': None, 'collector_id': None, 'collector_name': 'Carey',
                'guest_session_id': 'g1', 'is_offline': False}

        _insert_field_point_row(sb, base, None)

        self.assertEqual(len(sb.calls), 1)
        _, sent = sb.calls[0]
        self.assertNotIn('address', sent)


if __name__ == '__main__':
    unittest.main()
