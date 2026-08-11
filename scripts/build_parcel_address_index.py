"""Build a compact parcel rep-point -> address index and publish it under a
NEW Supabase data_type ('parcel_address_index').

Why: output/parcels_keystone.geojson is 8.9 MB — far too heavy for a
serverless read endpoint. This index is ~1 MB and answers the only
question the orphan-visibility feature needs: "which county address is
this Qualtrics response sitting on?"

SAFETY: writes ONLY to data_type='parcel_address_index'. It never reads,
updates or deletes community_contact, iaq_survey or analysis.

The point-in-polygon ray-cast and index-entry shape live in
api/survey_logic.py (build_parcel_address_entries / lookup_parcel) — the
single source of truth shared with api/iaq-points.py (?unmatched=1), so a geometry fix
(e.g. honouring interior-ring holes) only has to be made once. This script
imports from api/ (not the other way around).

    venv/bin/python scripts/build_parcel_address_index.py            # dry run
    venv/bin/python scripts/build_parcel_address_index.py --publish  # upsert
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PARCELS = REPO / "output" / "parcels_keystone.geojson"

sys.path.insert(0, str(REPO))
from api.survey_logic import build_parcel_address_entries, lookup_parcel  # noqa: E402


def build_index(parcel_geojson: dict) -> dict:
    """Reduce the cadastre to compact per-polygon entries (address, bbox,
    outer ring, and any interior-ring holes) via the shared builder in
    api/survey_logic.py."""
    out = []
    for f in (parcel_geojson or {}).get("features") or []:
        out.extend(build_parcel_address_entries(f))
    return {"version": 1, "parcels": out}


def lookup_address(index: dict, lon: float, lat: float) -> str | None:
    """Return the county address of the parcel containing (lon, lat), or
    None (including when the point falls inside a hole)."""
    return lookup_parcel(index, lon, lat)[0]


def _env() -> tuple[str, str]:
    env = {}
    p = REPO / ".env"
    if p.exists():
        for line in p.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    if not env.get("SUPABASE_URL") or not env.get("SUPABASE_SERVICE_ROLE_KEY"):
        sys.exit("ERROR: SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY missing.")
    return env["SUPABASE_URL"], env["SUPABASE_SERVICE_ROLE_KEY"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--publish", action="store_true")
    args = ap.parse_args()

    idx = build_index(json.loads(PARCELS.read_text()))
    blob = json.dumps(idx)
    print(f"parcels with an address: {len(idx['parcels'])}")
    print(f"serialized size: {len(blob) / 1_000_000:.2f} MB")

    if not args.publish:
        print("\ndry run — pass --publish to upsert data_type='parcel_address_index'")
        return

    url, key = _env()
    req = urllib.request.Request(
        f"{url}/rest/v1/keystone_dashboard_data?on_conflict=data_type",
        data=json.dumps({"data_type": "parcel_address_index", "payload": idx}).encode(),
        headers={
            "apikey": key, "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        print("published:", r.status)


if __name__ == "__main__":
    main()
