"""Tests for Task 16: daily integrity metrics.

Covers `_compute_integrity_metrics` (pure), `_table_row_count`, and
`_persist_integrity_metrics` in api/daily-refresh.py. Confirms:

  - the metrics row reuses `orphan_iaq_features` (single source of truth
    shared with /api/iaq-points?unmatched=1 and the mobile "Already Responded"
    list) rather than re-deriving orphan logic
  - n_contacts / n_field_points split correctly on `source == 'field'`
  - the write goes ONLY to a NEW data_type='integrity_metrics' row —
    never to community_contact / iaq_survey / analysis /
    parcel_address_index
  - both the row-count query and the upsert never raise, even on
    failure (a monitoring write must not break the refresh)

api/daily-refresh.py is loaded via importlib because its filename
contains a hyphen and isn't a valid Python module path.
"""
import importlib.util
import pathlib
import unittest

_MOD_PATH = pathlib.Path(__file__).resolve().parent.parent / "api" / "daily-refresh.py"
_spec = importlib.util.spec_from_file_location("_daily_refresh_for_metrics_tests", _MOD_PATH)
daily_refresh = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(daily_refresh)

_compute_integrity_metrics = daily_refresh._compute_integrity_metrics
_table_row_count = daily_refresh._table_row_count
_persist_integrity_metrics = daily_refresh._persist_integrity_metrics


def iaq(rid, lon, lat, matched=False):
    return {"type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": {"response_id": rid, "iaq_matched": matched,
                           "overall_risk": 27, "risk_tier": "Low"}}


def contact(addr, lon, lat, source=None):
    return {"type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": {"address": addr, "source": source,
                           "status": "Completed"}}


class ComputeIntegrityMetricsTests(unittest.TestCase):
    def test_counts_and_orphans(self):
        iaq_feats = [
            iaq("R_1", -82.0191, 29.7838),                  # orphan — no addressed contact nearby
            iaq("R_2", -82.0200, 29.7900, matched=True),
        ]
        features = [
            contact("6405 Beloit Ave", -82.0200, 29.7900),          # regular contact
            contact(None, -82.0191, 29.7838, source="field"),       # anonymous field pin — no address
        ]
        m = _compute_integrity_metrics(iaq_feats, features, contacts_table_rows=42)

        self.assertEqual(m["n_iaq"], 2)
        self.assertEqual(m["n_orphans"], 1)
        self.assertEqual(m["n_contacts"], 1)
        self.assertEqual(m["n_field_points"], 1)
        self.assertEqual(m["contacts_table_rows"], 42)
        self.assertIn("computed_at", m)

    def test_a_field_pin_never_rescues_an_orphan_from_the_metric(self):
        """Same 6409 Beloit-style regression the orphan_iaq_features
        docstring guards against — an anonymous field pin at the exact
        orphan coordinate must not zero out n_orphans."""
        iaq_feats = [iaq("R_1", -82.0191, 29.7838, matched=True)]
        features = [contact(None, -82.0191, 29.7838, source="field")]
        m = _compute_integrity_metrics(iaq_feats, features, contacts_table_rows=0)
        self.assertEqual(m["n_orphans"], 1)

    def test_no_iaq_no_orphans(self):
        m = _compute_integrity_metrics([], [], contacts_table_rows=0)
        self.assertEqual(m["n_iaq"], 0)
        self.assertEqual(m["n_orphans"], 0)
        self.assertEqual(m["n_contacts"], 0)
        self.assertEqual(m["n_field_points"], 0)


# ── I/O wrappers (fake Supabase client) ────────────────────────────────

class _FakeResult:
    def __init__(self, count=0, data=None):
        self.data = data or []
        self.count = count


class _FakeSelectQuery:
    """Supports the two SELECT shapes daily-refresh.py issues here:
    `.select("id", count="exact")` (row count) and
    `.select("payload").eq(...).limit(...)` (previous metrics row)."""

    def __init__(self, client, table, cols):
        self._client = client
        self._table = table
        self._cols = cols

    def eq(self, *_a, **_k):
        return self

    def limit(self, *_a, **_k):
        return self

    def order(self, *_a, **_k):
        return self

    def execute(self):
        return self._client._select(self._table, self._cols)


class _FakeUpsertQuery:
    def __init__(self, client, table, row):
        self._client = client
        self._table = table
        self._row = row

    def execute(self):
        return self._client._upsert(self._table, self._row)


class _FakeTable:
    def __init__(self, name, client):
        self._name = name
        self._client = client

    def select(self, cols, **_k):
        return _FakeSelectQuery(self._client, self._name, cols)

    def upsert(self, row, **_k):
        return _FakeUpsertQuery(self._client, self._name, row)


class _FakeSupabase:
    def __init__(self, counts=None, prev_metrics=None,
                 raise_on_select=False, raise_on_upsert=False):
        self._counts = counts or {}
        self._prev_metrics = prev_metrics  # None, or a stored integrity_metrics payload
        self.upsert_calls = []
        self._raise_on_select = raise_on_select
        self._raise_on_upsert = raise_on_upsert

    def table(self, name):
        return _FakeTable(name, self)

    def _select(self, table, cols):
        if self._raise_on_select:
            raise Exception("select failed")
        if table == "keystone_dashboard_data" and cols == "payload":
            if self._prev_metrics is None:
                return _FakeResult()
            return _FakeResult(data=[{"payload": self._prev_metrics}])
        return _FakeResult(count=self._counts.get(table, 0))

    def _upsert(self, table, row):
        if self._raise_on_upsert:
            raise Exception("upsert failed")
        self.upsert_calls.append((table, dict(row)))
        return _FakeResult()


class TableRowCountTests(unittest.TestCase):
    def test_returns_the_count(self):
        sb = _FakeSupabase(counts={"community_contacts": 321})
        self.assertEqual(_table_row_count(sb, "community_contacts"), 321)

    def test_returns_zero_and_never_raises_on_failure(self):
        sb = _FakeSupabase(raise_on_select=True)
        self.assertEqual(_table_row_count(sb, "community_contacts"), 0)


class PersistIntegrityMetricsTests(unittest.TestCase):
    def test_writes_only_a_new_integrity_metrics_row(self):
        sb = _FakeSupabase(counts={"community_contacts": 321})
        iaq_feats = [iaq("R_1", -82.0191, 29.7838)]
        features = [contact("6405 Beloit Ave", -82.0200, 29.7900)]

        result = _persist_integrity_metrics(sb, iaq_feats, features)

        self.assertEqual(len(sb.upsert_calls), 1, "must write exactly one row")
        table, row = sb.upsert_calls[0]
        self.assertEqual(table, "keystone_dashboard_data")
        self.assertEqual(row["data_type"], "integrity_metrics")
        # Never any of the existing shared blobs.
        self.assertNotIn(row["data_type"],
                          ("community_contact", "iaq_survey", "analysis", "parcel_address_index"))
        self.assertEqual(row["payload"]["n_iaq"], 1)
        self.assertEqual(row["payload"]["contacts_table_rows"], 321)
        self.assertEqual(result["n_iaq"], 1)

    def test_never_raises_when_the_upsert_fails(self):
        sb = _FakeSupabase(raise_on_upsert=True)
        try:
            result = _persist_integrity_metrics(sb, [], [])
        except Exception as e:  # pragma: no cover
            self.fail(f"must not raise, but raised {e!r}")
        self.assertIsNone(result)

    def test_never_raises_when_the_row_count_query_fails(self):
        sb = _FakeSupabase(raise_on_select=True)
        result = _persist_integrity_metrics(sb, [], [])
        self.assertIsNotNone(result)
        self.assertEqual(result["contacts_table_rows"], 0)

    def test_logs_a_warning_when_response_count_drops(self):
        sb = _FakeSupabase(prev_metrics={"n_iaq": 110})
        iaq_feats = [iaq(f"R_{i}", -82.02, 29.78) for i in range(90)]  # dropped from 110 -> 90

        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            result = _persist_integrity_metrics(sb, iaq_feats, [])

        self.assertEqual(result["n_iaq"], 90)
        self.assertIn("Response count dropped from 110 to 90", buf.getvalue())
        # Still writes the row — a drop is a warning, not a blocked write.
        self.assertEqual(len(sb.upsert_calls), 1)

    def test_no_warning_when_response_count_holds_or_grows(self):
        sb = _FakeSupabase(prev_metrics={"n_iaq": 90})
        iaq_feats = [iaq(f"R_{i}", -82.02, 29.78) for i in range(110)]  # grew 90 -> 110

        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            _persist_integrity_metrics(sb, iaq_feats, [])

        self.assertNotIn("dropped", buf.getvalue())

    def test_no_warning_on_first_ever_run_with_no_history(self):
        sb = _FakeSupabase(prev_metrics=None)
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            _persist_integrity_metrics(sb, [iaq("R_1", -82.02, 29.78)], [])
        self.assertNotIn("dropped", buf.getvalue())


if __name__ == '__main__':
    unittest.main()
