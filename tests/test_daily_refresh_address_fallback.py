"""Tests for the I7 fix (2026-08-10): api/daily-refresh.py must select and
emit `field_survey_points.address`, tolerating migration 27 not being
applied yet — mirroring api/upload.py's `_load_all_field_features` /
`_field_row_to_feature` fallback pattern (see
tests/test_field_point_address_fallback.py).

Before this fix, `_field_row_to_feature` never read `address` at all (its
own comment claimed it "deliberately does not surface any address-like
field"), and `_run_refresh`'s SELECT never asked for the column either. A
surveyor's typed address only ever reached the community_contact blob via
a manual admin upload (api/upload.py), never via the 4x/day cron this
module backs.

api/daily-refresh.py is loaded via importlib because its filename contains
a hyphen and isn't a valid Python module path (same approach as
tests/test_iaq_match_status_refresh.py).

No network, no real Supabase client — fakes simulate PostgREST rejecting a
SELECT that references a column the live schema doesn't have.
"""
import importlib.util
import pathlib
import unittest

_MOD_PATH = pathlib.Path(__file__).resolve().parent.parent / "api" / "daily-refresh.py"
_spec = importlib.util.spec_from_file_location("_daily_refresh_for_addr_tests", _MOD_PATH)
daily_refresh = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(daily_refresh)


# ── _field_row_to_feature: reads `address` when present, None otherwise ───

class FieldRowToFeatureAddressTests(unittest.TestCase):
    def test_reads_address_when_present(self):
        f = daily_refresh._field_row_to_feature(
            {"id": 1, "lat": 1.0, "lon": 2.0, "address": "6409 Beloit Ave"})
        self.assertEqual(f["properties"]["address"], "6409 Beloit Ave")

    def test_address_is_none_when_column_missing_from_row(self):
        f = daily_refresh._field_row_to_feature({"id": 1, "lat": 1.0, "lon": 2.0})
        self.assertIsNone(f["properties"]["address"])


# ── _run_refresh: SELECT fallback + address propagation end-to-end ────────

class _FakeResult:
    def __init__(self, data):
        self.data = data


class _FakeQuery:
    """Minimal chainable stand-in for the postgrest-py query builder used
    by _run_refresh: select/eq/order/limit/gt/range/insert/upsert, all
    returning `self` except execute(), which delegates to the client."""

    def __init__(self, client, table_name):
        self._client = client
        self._table = table_name
        self._op = None
        self._select_cols = None
        self._payload = None

    def select(self, cols):
        self._op, self._select_cols = "select", cols
        return self

    def eq(self, *_a, **_k): return self
    def order(self, *_a, **_k): return self
    def limit(self, *_a, **_k): return self
    def gt(self, *_a, **_k): return self
    def range(self, *_a, **_k): return self

    def insert(self, payload):
        self._op, self._payload = "insert", payload
        return self

    def upsert(self, payload, on_conflict=None):
        self._op, self._payload = "upsert", payload
        return self

    def execute(self):
        return self._client._execute(self._table, self._op, self._select_cols, self._payload)


class _FakeSupabaseForRefresh:
    """Only implements what `_run_refresh` needs to reach the point of
    merging field rows into the community_contact blob. Anything else
    (e.g. `community_contacts` row count used by the integrity-metrics
    side effect) raises — `_persist_integrity_metrics` already wraps its
    own body in try/except, matching production's graceful-degradation
    contract, so that's expected and harmless here."""

    def __init__(self, field_rows, fail_address_select=False):
        self._field_rows = field_rows
        self._fail_address_select = fail_address_select
        self.field_select_calls = []
        self.upserts = []

    def table(self, name):
        return _FakeQuery(self, name)

    def _execute(self, table, op, cols, payload):
        if table == "keystone_analysis_versions" and op == "select":
            return _FakeResult([])  # no prior snapshot -> last_at default
        if table == "keystone_analysis_versions" and op == "insert":
            return _FakeResult([payload])
        if table == "field_survey_points" and op == "select":
            self.field_select_calls.append(cols)
            if self._fail_address_select and "address" in cols:
                raise Exception('column field_survey_points.address does not exist')
            return _FakeResult(self._field_rows)
        if table == "keystone_dashboard_data" and op == "upsert":
            self.upserts.append(payload)
            return _FakeResult([payload])
        raise Exception(f"unsupported fake query: table={table} op={op}")


class RunRefreshAddressFallbackTests(unittest.TestCase):
    def setUp(self):
        self._orig_admin = daily_refresh.supabase_admin
        self._orig_load_cached = daily_refresh.load_cached
        # No existing community_contact / iaq_survey blobs — keeps the run
        # on the simplest path (no IAQ parcel-matching machinery engaged).
        daily_refresh.load_cached = lambda *_a, **_k: None

    def tearDown(self):
        daily_refresh.supabase_admin = self._orig_admin
        daily_refresh.load_cached = self._orig_load_cached

    def test_falls_back_to_base_columns_when_address_select_fails(self):
        rows = [{"id": "p1", "lat": 29.78, "lon": -82.02, "status": "Completed",
                 "notes": "", "collector_id": None, "collector_name": "A",
                 "collected_at": "2026-08-01T00:00:00Z"}]
        sb = _FakeSupabaseForRefresh(rows, fail_address_select=True)
        daily_refresh.supabase_admin = lambda: sb

        result = daily_refresh._run_refresh()

        self.assertTrue(result.get("refreshed"))
        self.assertEqual(len(sb.field_select_calls), 2,
                         "expected an enriched attempt + a base-only retry")
        self.assertIn("address", sb.field_select_calls[0])
        self.assertNotIn("address", sb.field_select_calls[1])
        # The merged community_contact blob still builds, with address=None.
        cc_upserts = [u for u in sb.upserts if u.get("data_type") == "community_contact"]
        self.assertEqual(len(cc_upserts), 1)
        feats = cc_upserts[0]["payload"]["features"]
        self.assertEqual(len(feats), 1)
        self.assertIsNone(feats[0]["properties"]["address"])

    def test_succeeds_on_first_try_and_propagates_address_when_migration_27_applied(self):
        rows = [{"id": "p2", "lat": 29.78, "lon": -82.02, "status": "Completed",
                 "notes": "", "collector_id": None, "collector_name": "A",
                 "collected_at": "2026-08-01T00:00:00Z", "address": "6409 Beloit Ave"}]
        sb = _FakeSupabaseForRefresh(rows, fail_address_select=False)
        daily_refresh.supabase_admin = lambda: sb

        result = daily_refresh._run_refresh()

        self.assertTrue(result.get("refreshed"))
        self.assertEqual(len(sb.field_select_calls), 1,
                         "no fallback needed — should not retry")
        self.assertIn("address", sb.field_select_calls[0])
        cc_upserts = [u for u in sb.upserts if u.get("data_type") == "community_contact"]
        feats = cc_upserts[0]["payload"]["features"]
        self.assertEqual(feats[0]["properties"]["address"], "6409 Beloit Ave")


if __name__ == "__main__":
    unittest.main()
