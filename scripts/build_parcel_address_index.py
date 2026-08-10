"""Build a compact parcel rep-point -> address index and publish it under a
NEW Supabase data_type ('parcel_address_index').

Why: output/parcels_keystone.geojson is 8.9 MB — far too heavy for a
serverless read endpoint. This index is ~1 MB and answers the only
question the orphan-visibility feature needs: "which county address is
this Qualtrics response sitting on?"

SAFETY: writes ONLY to data_type='parcel_address_index'. It never reads,
updates or deletes community_contact, iaq_survey or analysis.

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


def _rings(geom: dict) -> list:
    t = (geom or {}).get("type")
    if t == "Polygon":
        return [geom["coordinates"]]
    if t == "MultiPolygon":
        return list(geom["coordinates"])
    return []


def _point_in_ring(x: float, y: float, ring: list) -> bool:
    inside = False
    n = len(ring)
    j = n - 1
    for i in range(n):
        xi, yi = ring[i][0], ring[i][1]
        xj, yj = ring[j][0], ring[j][1]
        if (yi > y) != (yj > y):
            if x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-15) + xi:
                inside = not inside
        j = i
    return inside


def build_index(parcel_geojson: dict) -> dict:
    """Reduce the cadastre to {parcel_id, address, bbox, ring} entries."""
    out = []
    for f in (parcel_geojson or {}).get("features") or []:
        props = f.get("properties") or {}
        addr = str(props.get("address") or "").strip()
        if not addr:
            continue
        for poly in _rings(f.get("geometry") or {}):
            ring = poly[0]
            xs = [p[0] for p in ring]
            ys = [p[1] for p in ring]
            out.append({
                "parcel_id": props.get("parcel_id"),
                "address": addr,
                "bbox": [min(xs), min(ys), max(xs), max(ys)],
                "ring": [[round(p[0], 6), round(p[1], 6)] for p in ring],
            })
    return {"version": 1, "parcels": out}


def lookup_address(index: dict, lon: float, lat: float) -> str | None:
    """Return the county address of the parcel containing (lon, lat)."""
    for p in (index or {}).get("parcels") or []:
        x0, y0, x1, y1 = p["bbox"]
        if x0 <= lon <= x1 and y0 <= lat <= y1 and _point_in_ring(lon, lat, p["ring"]):
            return p["address"]
    return None


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
