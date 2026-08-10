"""READ-ONLY production fingerprint.

Run before and after every change in docs/plans/2026-08-10-iaq-integrity-and-orphan-visibility.md.
Performs GET requests only — it never writes to Supabase.

    venv/bin/python scripts/integrity_fingerprint.py
    venv/bin/python scripts/integrity_fingerprint.py --save baseline.json
    venv/bin/python scripts/integrity_fingerprint.py --compare baseline.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def _sha(values) -> str:
    h = hashlib.sha256()
    for v in sorted(str(x) for x in values):
        h.update(v.encode("utf-8"))
        h.update(b"\x00")
    return h.hexdigest()


def fingerprint(contact_blob: dict, iaq_blob: dict) -> dict:
    """Pure function: derive a stable fingerprint from the two cached blobs."""
    contacts = (contact_blob or {}).get("features") or []
    iaq = ((iaq_blob or {}).get("geojson") or {}).get("features") or []

    cprops = [f.get("properties") or {} for f in contacts]
    iprops = [f.get("properties") or {} for f in iaq]

    return {
        "n_contacts": len(contacts),
        "n_contacts_field": sum(1 for p in cprops if p.get("source") == "field"),
        "n_iaq": len(iaq),
        "n_iaq_matched": sum(1 for p in iprops if p.get("iaq_matched")),
        "contact_addresses_sha256": _sha(p.get("address") for p in cprops),
        "contact_statuses_sha256": _sha(
            f"{p.get('address')}|{p.get('status')}|{p.get('has_iaq_survey')}"
            for p in cprops
        ),
        "iaq_response_ids_sha256": _sha(p.get("response_id") for p in iprops),
        "scores_sha256": _sha(
            f"{p.get('response_id')}|{p.get('overall_risk')}|{p.get('health_score')}"
            f"|{p.get('iaq_score')}|{p.get('struct_score')}"
            for p in iprops
        ),
    }


def _env() -> tuple[str, str]:
    env = {}
    env_path = REPO / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    url = os.environ.get("SUPABASE_URL") or env.get("SUPABASE_URL", "")
    key = (os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
           or env.get("SUPABASE_SERVICE_ROLE_KEY", ""))
    if not url or not key:
        sys.exit("ERROR: SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY not found.")
    return url, key


def _get(url: str, key: str, path: str):
    req = urllib.request.Request(
        f"{url}/rest/v1/{path}",
        headers={"apikey": key, "Authorization": f"Bearer {key}"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def live_fingerprint() -> dict:
    url, key = _env()
    c = _get(url, key,
             "keystone_dashboard_data?data_type=eq.community_contact&select=payload")
    i = _get(url, key,
             "keystone_dashboard_data?data_type=eq.iaq_survey&select=payload")
    return fingerprint(c[0]["payload"] if c else {}, i[0]["payload"] if i else {})


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--save")
    ap.add_argument("--compare")
    args = ap.parse_args()

    fp = live_fingerprint()
    print(json.dumps(fp, indent=2))

    if args.save:
        Path(args.save).write_text(json.dumps(fp, indent=2))
        print(f"\nsaved -> {args.save}")

    if args.compare:
        base = json.loads(Path(args.compare).read_text())
        drift = {k: (base.get(k), fp.get(k)) for k in fp if base.get(k) != fp.get(k)}
        if drift:
            print("\n!! DRIFT DETECTED — existing data changed:")
            for k, (b, a) in drift.items():
                print(f"   {k}: {b} -> {a}")
            sys.exit(1)
        print("\nOK — no drift. Existing data untouched.")


if __name__ == "__main__":
    main()
