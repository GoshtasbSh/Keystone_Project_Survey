"""KeyStone production data runbook (October 2026 launch).

Every subcommand is DRY-RUN unless --apply is given. Writes go only
through api/_dashboard_writes.commit_dashboard_writes (one transaction
when migration 29 is applied). Nothing here ever deletes or edits a
community_contacts row, a survey response or a keystone_analysis_versions
row, and nothing here ever changes a field point's `status` (user rule
2026-10-13): `reprocess-iaq` may only set `iaq_matched` (switch it off with
--no-field-writeback) and `rollback` only re-sets `iaq_matched` on field
rows it finds changed since the backup.

    ./.venv/bin/python scripts/prod_runbook.py backup  --out backups/2026-10-XX-prelaunch
    ./.venv/bin/python scripts/prod_runbook.py cleanup-test-pins --backup-dir DIR [--apply]
    ./.venv/bin/python scripts/prod_runbook.py reprocess-iaq --csv PATH --backup-dir DIR [--apply] [--force] [--no-field-writeback]
    ./.venv/bin/python scripts/prod_runbook.py verify
    ./.venv/bin/python scripts/prod_runbook.py rollback --backup-dir DIR [--apply]

Backups hold the full contact list (names, phones, addresses): keep them
under backups/, which is in both .gitignore and .vercelignore.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "api"))

from _field_layer import (  # noqa: E402
    is_field_feature, cell_key, rebuild_field_layer, load_all_field_rows,
    features_signature,
)
from _dashboard_writes import commit_dashboard_writes, load_blob_with_stamp  # noqa: E402

# The 28 deleted test pins found in the community_contact blob on
# 2026-10-13 (audit F4 / Q4-03). The cleanup refuses to run if the set of
# blob pins missing from field_survey_points is not EXACTLY this set, so a
# real pin deleted since then can never be removed by this script unseen.
EXPECTED_TEST_PIN_IDS = frozenset({
    "081751dd-70b5-475b-ad0b-f56769230d1f", "1098e13e-9264-4e1c-b392-3fe13335d6a5",
    "145d226d-af10-4088-a5a5-0e2f3b1bf2a7", "194f5430-188d-4d89-8cf6-101fcfc164e6",
    "28ac7696-c791-4d51-ad3e-da4aa1342eb6", "2b48e25a-726f-4f1a-b520-4676c984eae5",
    "39fff2dc-7aa2-47ad-94e4-17263328941b", "417339c1-f4a2-4a88-a1ad-4d4078d4ebfe",
    "56663918-c490-4d60-b5f1-5667ea091c23", "5a647954-148d-4adf-964a-a3a63b0eaeb8",
    "6baf055f-bc8f-4b59-85d5-1241d79e9ad9", "6ca63e1c-5c0f-43ce-b959-41e379b92329",
    "6ca991bd-9fb1-4295-aba5-fcbd526f9b5b", "70759c69-225a-4fbc-8404-cdc51e66ab17",
    "71208ddd-1595-4da8-91d4-5419e5ffe716", "89db8de6-59be-4b4d-85b8-7f0937becff7",
    "93f31699-650a-4d31-80f3-1f10234459d2", "95236d0b-e154-41c8-bac4-2a5d27f0387d",
    "956ff214-8501-4754-87e9-c4a6e5cf3a9f", "b989a847-2d01-4121-ad7c-9eedff36fd38",
    "ba74b8fe-bc09-46b0-b6d8-c0c5fa49816e", "c3711341-ed90-45a5-bc55-2886d539c518",
    "c902d618-c2cf-40f2-9b6d-23667e12a002", "cb4783e1-b9af-4110-a5d2-8f2bcd785feb",
    "d082063a-d9de-43dc-b1c2-06ab2e015b87", "d671b9ef-2db8-4f08-94c9-29321ec7c25a",
    "e31020f0-384a-40d0-b4b3-78c2705c5620", "ec1db343-7c4a-4df6-b58a-51149fffea41",
})
TEST_COLLECTOR_RE = re.compile(r"(?i)^\s*(test|qa)")
BACKUP_TABLES = ("keystone_dashboard_data", "keystone_analysis_versions",
                 "field_survey_points", "community_contacts")


# ── pure helpers (unit-tested in tests/test_prod_runbook.py) ────────────

def select_test_pins(blob_features: list, table_rows: list) -> tuple:
    """Return (orphans, problems). An orphan is a blob field feature whose
    field_point_id is not in field_survey_points. `problems` lists every
    reason the cleanup must NOT run automatically."""
    table_ids = {str(r.get("id")) for r in table_rows}
    real_collectors = {r.get("collector_id") for r in table_rows if r.get("collector_id")}
    orphans = [f for f in blob_features
               if is_field_feature(f)
               and str((f.get("properties") or {}).get("field_point_id")) not in table_ids]
    problems = []
    ids = {str(f["properties"].get("field_point_id")) for f in orphans}
    if ids != EXPECTED_TEST_PIN_IDS:
        problems.append(f"orphan set differs from the audited 28: "
                        f"unexpected={sorted(ids - EXPECTED_TEST_PIN_IDS)} "
                        f"already-gone={sorted(EXPECTED_TEST_PIN_IDS - ids)}")
    for f in orphans:
        p = f["properties"]
        if not TEST_COLLECTOR_RE.match(str(p.get("collector") or "")):
            problems.append(f"{p.get('field_point_id')}: collector {p.get('collector')!r} "
                            f"is not a test/QA account")
        if p.get("collector_id") and p.get("collector_id") in real_collectors:
            problems.append(f"{p.get('field_point_id')}: collector_id belongs to a live collector")
    test_rows = [r for r in table_rows if TEST_COLLECTOR_RE.match(str(r.get("collector_name") or ""))]
    if test_rows:
        problems.append("field_survey_points holds rows from test accounts — review by hand: "
                        + ", ".join(f"{r['id']} ({r.get('collector_name')})" for r in test_rows))
    return orphans, problems


def swallowed_cells(blob_features: list) -> set:
    """Cells of field pins that carry a non-field coincident contact."""
    out = set()
    for f in blob_features:
        p = (f.get("properties") or {}) if is_field_feature(f) else {}
        if any(isinstance(e, dict) and e.get("source") != "field"
               for e in p.get("coincident_contacts") or []):
            out.add(cell_key(f["geometry"]["coordinates"]))
    return out


def build_restore_lookup(version_payloads, needed: set) -> dict:
    """Scan community_contact version payloads NEWEST FIRST and keep, for
    each needed cell, the newest stand-alone CSV contact found there."""
    found: dict = {}
    for payload in version_payloads:
        for f in (payload or {}).get("features") or []:
            if is_field_feature(f):
                continue
            try:
                k = cell_key(f["geometry"]["coordinates"])
            except Exception:
                continue
            if k in needed and k not in found:
                found[k] = f
        if len(found) == len(needed):
            break
    return found


def check_contacts_preserved(before: list, after: list) -> list:
    """Every CSV contact present before must be present after, unchanged."""
    after_sigs = {features_signature([f]) for f in after if not is_field_feature(f)}
    return [f["properties"].get("address") for f in before
            if not is_field_feature(f) and features_signature([f]) not in after_sigs]


def verify_state(blob_features: list, table_rows: list) -> list:
    """Post-condition checks shared by `verify` and the --apply paths."""
    fails = []
    field = [f for f in blob_features if is_field_feature(f)]
    ids = [str(f["properties"].get("field_point_id")) for f in field]
    table_ids = sorted(str(r["id"]) for r in table_rows)
    if sorted(ids) != table_ids:
        fails.append(f"blob field ids != table ids (blob {len(ids)}, table {len(table_ids)})")
    if len(ids) != len(set(ids)):
        fails.append("duplicate field pins in blob")
    leftover = EXPECTED_TEST_PIN_IDS & set(ids)
    if leftover:
        fails.append(f"test pins still present: {sorted(leftover)}")
    for f in blob_features:
        if not is_field_feature(f):
            continue
        for e in f["properties"].get("coincident_contacts") or []:
            if isinstance(e, dict) and e.get("source") != "field":
                fails.append(f"pin {f['properties'].get('field_point_id')} still holds a CSV contact")
    return fails


def iaq_matched_reverts(backup_rows: list, live_rows: list) -> list:
    """(id, backup iaq_matched) for every live field row whose iaq_matched
    differs from the backup. `status` is deliberately NOT compared: no
    runbook or upload path changes it, so a status that differs from the
    backup was set by a surveyor and must be kept (user rule 2026-10-13)."""
    backup = {str(r.get("id")): r for r in backup_rows}
    out = []
    for r in live_rows:
        b = backup.get(str(r.get("id")))
        if b is not None and bool(r.get("iaq_matched")) != bool(b.get("iaq_matched")):
            out.append((r["id"], bool(b.get("iaq_matched"))))
    return out


# ── I/O ─────────────────────────────────────────────────────────────────

def _client():
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    from supabase import create_client
    url, key = os.environ.get("SUPABASE_URL", ""), os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    if not url or not key:
        sys.exit("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in .env")
    if "ioejtwseqsgidefkeyji" not in url:
        sys.exit(f"refusing: {url} is not the live KeyStone project (ioejtwseqsgidefkeyji)")
    return create_client(url, key)


def _fetch_all(sb, table: str, cols: str = "*", order: str = "id", page: int = 500) -> list:
    rows, start = [], 0
    while True:
        batch = (sb.table(table).select(cols).order(order)
                   .range(start, start + page - 1).execute().data) or []
        rows.extend(batch)
        if len(batch) < page:
            return rows
        start += page


def _version_payloads_newest_first(sb):
    ids = [r["id"] for r in (sb.table("keystone_analysis_versions").select("id")
                               .eq("data_type", "community_contact")
                               .order("id", desc=True).execute().data or [])]
    for vid in ids:
        rows = (sb.table("keystone_analysis_versions").select("payload")
                  .eq("id", vid).execute().data) or []
        if rows:
            yield rows[0]["payload"]


def _load_backup_file(d: Path, name: str):
    """A backup file, refused if its bytes no longer match MANIFEST.json."""
    man = json.loads((d / "MANIFEST.json").read_text())
    raw = (d / name).read_bytes()
    want = (man.get("files") or {}).get(name, {}).get("sha256")
    if want != hashlib.sha256(raw).hexdigest():
        sys.exit(f"refusing: {d / name} does not match MANIFEST.json (edited or truncated?)")
    return json.loads(raw)


def _require_fresh_backup(sb, backup_dir: str) -> dict:
    d = ROOT / backup_dir
    man = json.loads((d / "MANIFEST.json").read_text())
    _, cc_stamp = load_blob_with_stamp(sb, "community_contact")
    _, iaq_stamp = load_blob_with_stamp(sb, "iaq_survey")
    if man["stamps"].get("community_contact") != cc_stamp or man["stamps"].get("iaq_survey") != iaq_stamp:
        sys.exit("refusing: the dashboard data changed after this backup — take a new backup first")
    return man


def cmd_backup(sb, args):
    out = ROOT / args.out
    out.mkdir(parents=True, exist_ok=False)
    manifest = {"taken_at": datetime.now(timezone.utc).isoformat(), "files": {}, "stamps": {}}
    for table in BACKUP_TABLES:
        order = "data_type" if table == "keystone_dashboard_data" else "id"
        # Version rows carry full payloads (~0.4 MB each): small pages.
        page = 20 if table == "keystone_analysis_versions" else 500
        rows = _fetch_all(sb, table, order=order, page=page)
        path = out / f"{table}.json"
        path.write_text(json.dumps(rows, ensure_ascii=False, default=str))
        manifest["files"][path.name] = {"rows": len(rows),
                                        "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        if table == "keystone_dashboard_data":
            manifest["stamps"] = {r["data_type"]: r["updated_at"] for r in rows}
    (out / "MANIFEST.json").write_text(json.dumps(manifest, indent=2))
    print(json.dumps(manifest, indent=2))


def cmd_cleanup(sb, args):
    _require_fresh_backup(sb, args.backup_dir)
    blob, stamp = load_blob_with_stamp(sb, "community_contact")
    rows = load_all_field_rows(sb, "[cleanup]")
    feats = blob["features"]
    orphans, problems = select_test_pins(feats, rows)
    for f in orphans:
        p = f["properties"]
        print(f"  remove {p['field_point_id']}  {p.get('collector')!r:16} {str(p.get('status')):14} "
              f"{str(p.get('collected_at'))[:10]}  {f['geometry']['coordinates']}")
    if problems:
        sys.exit("STOP — needs human review:\n  " + "\n  ".join(problems))
    lookup = build_restore_lookup(_version_payloads_newest_first(sb), swallowed_cells(feats))
    # Surviving pins keep their current survey link; reprocess-iaq re-derives it.
    new_feats, report = rebuild_field_layer(
        feats, rows, restore_lookup=lookup,
        carry_iaq_link_from=[f for f in feats if is_field_feature(f)])
    restored = [f for f in new_feats if (f.get("properties") or {}).get("restored_from_field_pin")]
    for f in restored:
        p = f["properties"]
        print(f"  restore contact {p.get('address')!r} ({p.get('status')}) from pin {p['restored_from_field_pin']}")
    if len(restored) != len(lookup) or any(not f["properties"].get("address") for f in restored):
        sys.exit("STOP — a swallowed contact has no full copy in version history")
    lost = check_contacts_preserved(feats, new_feats)
    fails = verify_state(new_feats, rows)
    if lost or fails:
        sys.exit(f"STOP — post-condition failed: lost contacts={lost} checks={fails}")
    print(f"before {len(feats)} features → after {len(new_feats)} "
          f"(removed {len(report['removed'])} pins, restored {len(restored)} contacts)")
    if not args.apply:
        print("dry run — re-run with --apply to write")
        return
    from _lib import merge_preserve_analysis
    from _processing import compute_contact_analysis
    payload = {**blob, "features": new_feats}
    today = datetime.now(timezone.utc).date().isoformat()
    res = commit_dashboard_writes(
        sb,
        [{"data_type": "community_contact", "payload": payload},
         {"data_type": "analysis",
          "payload": merge_preserve_analysis(compute_contact_analysis(new_feats))}],
        [{"data_type": "community_contact", "payload": payload,
          "label": (f"Cleanup {today} — removed {len(report['removed'])} deleted test pins, "
                    f"restored {len(restored)} contacts"),
          "n_points": len(new_feats)}],
        expected={"community_contact": stamp},
    )
    after, _ = load_blob_with_stamp(sb, "community_contact")
    fails = verify_state(after["features"], load_all_field_rows(sb, "[cleanup]"))
    print(res, "verify:", fails or "OK")


def cmd_reprocess(sb, args):
    _require_fresh_backup(sb, args.backup_dir)
    import upload as U
    csv_path = Path(args.csv)
    plan = U.prepare_iaq_upload(sb, csv_path.name, csv_path.read_bytes(), force=args.force,
                                admin_uid=None, uploader_email="runbook (service key)")
    print(json.dumps({k: v for k, v in plan["body"].items() if k != "validation"}, indent=1, default=str))
    if plan["status"] != 200:
        sys.exit(f"STOP — upload refused ({plan['status']})")
    print("blobs:", [b["data_type"] for b in plan["blobs"]])
    print("versions:", [v["label"] for v in plan["versions"]])
    # GAP-3: the write-back sets ONLY iaq_matched=true, never status.
    print("field pins to mark iaq_matched=true"
          + (" (SKIPPED: --no-field-writeback)" if args.no_field_writeback else "")
          + ":", plan["upgraded_ids"])
    if not args.apply:
        print("dry run — re-run with --apply to write")
        return
    print(U.commit_iaq_upload(sb, plan, writeback_field_points=not args.no_field_writeback))


def cmd_verify(sb, args):
    blob, _ = load_blob_with_stamp(sb, "community_contact")
    rows = load_all_field_rows(sb, "[verify]")
    iaq, _ = load_blob_with_stamp(sb, "iaq_survey")
    feats = (blob or {}).get("features") or []
    geo = (iaq or {}).get("geojson") or {}
    fails = verify_state(feats, rows)
    n_contacts = sum(1 for f in feats if not is_field_feature(f))
    print(f"contacts={n_contacts} field={len(rows)} "
          f"iaq={len(geo.get('features') or [])} "
          f"superseded={len(geo.get('superseded_features') or [])} "
          f"source={(iaq or {}).get('source_filename')}")
    print("verify:", fails or "OK")
    if fails:
        sys.exit(1)


def cmd_rollback(sb, args):
    d = ROOT / args.backup_dir
    rows = {r["data_type"]: r for r in _load_backup_file(d, "keystone_dashboard_data.json")}
    blobs = [{"data_type": t, "payload": rows[t]["payload"]}
             for t in ("iaq_survey", "community_contact", "analysis") if t in rows]
    fsp = _load_backup_file(d, "field_survey_points.json")
    live = _fetch_all(sb, "field_survey_points", "id, iaq_matched")
    revert = iaq_matched_reverts(fsp, live)
    print("restore blobs:", [b["data_type"] for b in blobs])
    print("revert field iaq_matched (status is never touched):", revert)
    if not args.apply:
        print("dry run — re-run with --apply to write")
        return
    today = datetime.now(timezone.utc).date().isoformat()
    commit_dashboard_writes(sb, blobs, [
        {"data_type": b["data_type"], "payload": b["payload"],
         "label": f"Rollback {today} to backup {d.name}",
         "n_points": len((b["payload"].get("geojson") or b["payload"]).get("features") or [])}
        for b in blobs if b["data_type"] in ("iaq_survey", "community_contact")])
    for i, matched in revert:
        sb.table("field_survey_points").update({"iaq_matched": matched}).eq("id", i).execute()
    print("rolled back")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("backup"); b.add_argument("--out", required=True)
    c = sub.add_parser("cleanup-test-pins"); c.add_argument("--backup-dir", required=True)
    c.add_argument("--apply", action="store_true")
    r = sub.add_parser("reprocess-iaq"); r.add_argument("--csv", required=True)
    r.add_argument("--backup-dir", required=True); r.add_argument("--apply", action="store_true")
    r.add_argument("--force", action="store_true")
    r.add_argument("--no-field-writeback", action="store_true",
                   help="do not set iaq_matched=true on linked field_survey_points rows")
    sub.add_parser("verify")
    rb = sub.add_parser("rollback"); rb.add_argument("--backup-dir", required=True)
    rb.add_argument("--apply", action="store_true")
    args = ap.parse_args(argv)
    sb = _client()
    {"backup": cmd_backup, "cleanup-test-pins": cmd_cleanup, "reprocess-iaq": cmd_reprocess,
     "verify": cmd_verify, "rollback": cmd_rollback}[args.cmd](sb, args)


if __name__ == "__main__":
    main()
