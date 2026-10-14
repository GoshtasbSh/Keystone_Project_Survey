"""Pure helpers of scripts/prod_runbook.py — the one-off test-pin cleanup
must remove ONLY the 28 audited test pins, never a real pin or contact,
and must give back the contacts a pin had swallowed. No network."""
import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("prod_runbook", ROOT / "scripts" / "prod_runbook.py")
rb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rb)

from api._field_layer import field_row_to_feature, cell_key, rebuild_field_layer  # noqa: E402


def pin(pid, collector, lon=-82.03, lat=29.65, collector_id=None, **props):
    f = field_row_to_feature({"id": pid, "lon": lon, "lat": lat, "status": "Completed",
                              "collector_name": collector, "collector_id": collector_id})
    f["properties"].update(props)
    return f


def contact(addr, lon, lat, **props):
    return {"type": "Feature", "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": {"address": addr, "status": "Completed", **props}}


LIVE_ROW = {"id": "b0310717-8d34-453d-9fb8-706c2db13b16", "lat": 29.7785003674729,
            "lon": -82.0171521230727, "status": "Completed",
            "collector_name": "Carey Morford", "collector_id": "d3e2d803"}


def audited_blob():
    feats = [contact("6116 Harvard Avenue", -81.995533, 29.786862)]
    for pid in sorted(rb.EXPECTED_TEST_PIN_IDS):
        feats.append(pin(pid, "test8"))
    feats.append(pin(LIVE_ROW["id"], "Carey Morford", LIVE_ROW["lon"], LIVE_ROW["lat"],
                     collector_id="d3e2d803",
                     coincident_contacts=[{"source": None, "status": "Left Info",
                                           "street_name": "Cascade"}]))
    return feats


class SelectTestPinsTests(unittest.TestCase):
    def test_audited_state_has_no_problems(self):
        orphans, problems = rb.select_test_pins(audited_blob(), [LIVE_ROW])
        self.assertEqual(len(orphans), 28)
        self.assertEqual(problems, [])

    def test_an_unexpected_orphan_stops_the_cleanup(self):
        feats = audited_blob() + [pin("real-but-deleted", "Carey Morford")]
        _, problems = rb.select_test_pins(feats, [LIVE_ROW])
        self.assertTrue(any("unexpected=['real-but-deleted']" in p for p in problems))
        self.assertTrue(any("not a test/QA account" in p for p in problems))

    def test_orphan_owned_by_a_live_collector_stops_the_cleanup(self):
        feats = audited_blob()
        feats[1]["properties"]["collector_id"] = "d3e2d803"
        _, problems = rb.select_test_pins(feats, [LIVE_ROW])
        self.assertTrue(any("live collector" in p for p in problems))

    def test_test_rows_in_the_table_are_reported_not_deleted(self):
        rows = [LIVE_ROW, {"id": "t-row", "lat": 29.6, "lon": -82.3, "collector_name": "test_x"}]
        _, problems = rb.select_test_pins(audited_blob(), rows)
        self.assertTrue(any("t-row" in p for p in problems))


class RestoreLookupTests(unittest.TestCase):
    def test_newest_standalone_contact_wins_and_scan_stops_early(self):
        k = cell_key([LIVE_ROW["lon"], LIVE_ROW["lat"]])
        v_new = {"features": [pin("x", "Carey Morford", LIVE_ROW["lon"], LIVE_ROW["lat"])]}
        v_mid = {"features": [contact("6393 Cascade", -82.01715, 29.778502, status="Left Info")]}
        seen = []

        def payloads():
            for v in (v_new, v_mid, {"features": [contact("OLD", -82.01715, 29.778502)]}):
                seen.append(v)
                yield v
        found = rb.build_restore_lookup(payloads(), {k})
        self.assertEqual(found[k]["properties"]["address"], "6393 Cascade")
        self.assertEqual(len(seen), 2, "must stop once every cell is found")


class PostConditionTests(unittest.TestCase):
    def test_full_cleanup_passes_every_check(self):
        feats = audited_blob()
        k = cell_key([LIVE_ROW["lon"], LIVE_ROW["lat"]])
        lookup = {k: contact("6393 Cascade", -82.01715, 29.778502, status="Left Info")}
        new, rep = rebuild_field_layer(feats, [LIVE_ROW], restore_lookup=lookup)
        self.assertEqual(rb.verify_state(new, [LIVE_ROW]), [])
        self.assertEqual(rb.check_contacts_preserved(feats, new), [])
        self.assertEqual(len(rep["removed"]), 28)

    def test_verify_flags_leftover_test_pin_and_swallowed_contact(self):
        fails = rb.verify_state(audited_blob(), [LIVE_ROW])
        self.assertTrue(any("blob field ids != table ids" in f for f in fails))
        self.assertTrue(any("test pins still present" in f for f in fails))
        self.assertTrue(any("still holds a CSV contact" in f for f in fails))

    def test_lost_contact_is_detected(self):
        feats = audited_blob()
        self.assertEqual(rb.check_contacts_preserved(feats, feats[1:]), ["6116 Harvard Avenue"])



# ── Beyond the brief: field-point safety of rollback / reprocess, and the
# CLI dry-run paths against an in-memory fake (never the network). ───────

import contextlib  # noqa: E402
import hashlib  # noqa: E402
import io  # noqa: E402
import json  # noqa: E402
import sys  # noqa: E402
import tempfile  # noqa: E402
import types  # noqa: E402


class _Q:
    def __init__(self, sb, table):
        self.sb, self.table, self.filters, self.op, self.patch = sb, table, [], "select", None

    def select(self, *_a, **_k):
        return self

    def eq(self, col, val):
        self.filters.append((col, val))
        return self

    def order(self, *_a, **_k):
        return self

    def limit(self, *_a):
        return self

    def range(self, a, b):
        self._range = (a, b)
        return self

    def update(self, patch):
        self.op, self.patch = "update", patch
        return self

    def in_(self, col, vals):
        self.filters.append((col, tuple(vals)))
        return self

    def execute(self):
        if self.op != "select":
            self.sb.writes.append((self.table, self.op, self.patch, self.filters))
            return types.SimpleNamespace(data=[])
        rows = [r for r in self.sb.tables.get(self.table, [])
                if all(r.get(c) == v for c, v in self.filters)]
        a, b = getattr(self, "_range", (0, len(rows)))
        return types.SimpleNamespace(data=rows[a:b + 1])


class _FakeSB:
    def __init__(self, tables):
        self.tables, self.writes = tables, []

    def table(self, name):
        return _Q(self, name)

    def rpc(self, name, params):
        self.writes.append(("rpc", name, params, None))
        return types.SimpleNamespace(execute=lambda: types.SimpleNamespace(data={"version_ids": [1]}))


def _write_backup(d, tables):
    d = pathlib.Path(d)
    man = {"files": {}, "stamps": {}}
    for name, rows in tables.items():
        path = d / f"{name}.json"
        path.write_text(json.dumps(rows))
        man["files"][path.name] = {"rows": len(rows),
                                   "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    man["stamps"] = {r["data_type"]: r["updated_at"] for r in tables["keystone_dashboard_data"]}
    (d / "MANIFEST.json").write_text(json.dumps(man))


def _run(sb, argv):
    orig = rb._client
    rb._client = lambda: sb
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            rb.main(argv)
    finally:
        rb._client = orig
    return out.getvalue()


class IaqMatchedRevertTests(unittest.TestCase):
    def test_only_iaq_matched_is_reverted_never_status(self):
        backup = [{"id": "a", "status": "Not Interested", "iaq_matched": False},
                  {"id": "b", "status": "Completed", "iaq_matched": True},
                  {"id": "c", "status": "Completed", "iaq_matched": False}]
        live = [{"id": "a", "status": "Completed", "iaq_matched": True},     # surveyor + upload changed
                {"id": "b", "status": "Left Info", "iaq_matched": True},     # surveyor changed only
                {"id": "c", "status": "Completed", "iaq_matched": None},    # None == False
                {"id": "new", "status": "Completed", "iaq_matched": True}]  # collected after backup
        self.assertEqual(rb.iaq_matched_reverts(backup, live), [("a", False)])


class CliDryRunTests(unittest.TestCase):
    def setUp(self):
        self.blob = {"type": "FeatureCollection", "features": audited_blob()}
        self.tables = {
            "keystone_dashboard_data": [
                {"data_type": "community_contact", "payload": self.blob, "updated_at": "t1"},
                {"data_type": "iaq_survey", "payload": {"geojson": {"features": []}},
                 "updated_at": "t2"}],
            "field_survey_points": [dict(LIVE_ROW, iaq_matched=True)],
            "keystone_analysis_versions": [
                {"id": 2, "data_type": "community_contact",
                 "payload": {"features": [contact("6393 Cascade", -82.01715, 29.778502,
                                                  status="Left Info")]}}],
        }
        self._tmp = tempfile.TemporaryDirectory()
        _write_backup(self._tmp.name, {
            "keystone_dashboard_data": self.tables["keystone_dashboard_data"],
            "field_survey_points": [dict(LIVE_ROW, iaq_matched=False, status="Left Info")],
        })

    def tearDown(self):
        self._tmp.cleanup()

    def test_cleanup_dry_run_reports_and_writes_nothing(self):
        sb = _FakeSB(self.tables)
        out = _run(sb, ["cleanup-test-pins", "--backup-dir", self._tmp.name])
        self.assertIn("removed 28 pins, restored 1 contacts", out)
        self.assertIn("restore contact '6393 Cascade'", out)
        self.assertIn("dry run", out)
        self.assertEqual(sb.writes, [])

    def test_cleanup_refuses_a_stale_backup(self):
        self.tables["keystone_dashboard_data"][0]["updated_at"] = "t9"
        sb = _FakeSB(self.tables)
        with self.assertRaises(SystemExit) as cm:
            _run(sb, ["cleanup-test-pins", "--backup-dir", self._tmp.name])
        self.assertIn("changed after this backup", str(cm.exception))
        self.assertEqual(sb.writes, [])

    def test_rollback_dry_run_writes_nothing_and_apply_never_sends_status(self):
        sb = _FakeSB(self.tables)
        out = _run(sb, ["rollback", "--backup-dir", self._tmp.name])
        self.assertIn("dry run", out)
        self.assertEqual(sb.writes, [])
        _run(sb, ["rollback", "--backup-dir", self._tmp.name, "--apply"])
        updates = [w for w in sb.writes if w[0] == "field_survey_points"]
        self.assertEqual(updates, [("field_survey_points", "update", {"iaq_matched": False},
                                    [("id", LIVE_ROW["id"])])])

    def test_rollback_refuses_an_edited_backup_file(self):
        f = pathlib.Path(self._tmp.name) / "field_survey_points.json"
        f.write_text(f.read_text().replace("Left Info", "Completed"))
        with self.assertRaises(SystemExit) as cm:
            _run(_FakeSB(self.tables), ["rollback", "--backup-dir", self._tmp.name])
        self.assertIn("does not match MANIFEST.json", str(cm.exception))

    def test_reprocess_no_field_writeback_reaches_commit(self):
        calls = {}
        fake_upload = types.ModuleType("upload")
        fake_upload.prepare_iaq_upload = lambda sb, name, data, **kw: {
            "status": 200, "body": {"points": 1}, "blobs": [], "versions": [],
            "upgraded_ids": ["x"]}

        def commit(sb, plan, writeback_field_points=True):
            calls["writeback"] = writeback_field_points
            return {"mode": "rpc"}
        fake_upload.commit_iaq_upload = commit
        csv = pathlib.Path(self._tmp.name) / "oct.csv"
        csv.write_bytes(b"x")
        saved = sys.modules.get("upload")
        sys.modules["upload"] = fake_upload
        try:
            out = _run(_FakeSB(self.tables), ["reprocess-iaq", "--csv", str(csv), "--backup-dir",
                                              self._tmp.name, "--no-field-writeback"])
            self.assertIn("SKIPPED: --no-field-writeback", out)
            self.assertNotIn("writeback", calls, "dry run must not commit")
            _run(_FakeSB(self.tables), ["reprocess-iaq", "--csv", str(csv), "--backup-dir",
                                        self._tmp.name, "--no-field-writeback", "--apply"])
            self.assertIs(calls["writeback"], False)
        finally:
            if saved is None:
                sys.modules.pop("upload", None)
            else:
                sys.modules["upload"] = saved


if __name__ == "__main__":
    unittest.main()
