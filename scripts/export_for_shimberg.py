"""
Export the live KeyStone Supabase database into a plain-Postgres hand-over package.

READ-ONLY. Nothing in Supabase is modified.

Usage (from the project root, with .env holding SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY):

    ./.venv/bin/python scripts/export_for_shimberg.py [out_dir]

Produces, under out_dir (default exports/shimberg_<date>/):

  raw/<table>.csv + raw/<table>.json      every row of each research-data table, as stored
  derived/parcels.csv / .geojson          11k parcel polygons decoded from the cached blob
  derived/community_contact_points.*      321 door-knock points decoded from the cached blob
  derived/iaq_responses.*                 Qualtrics IAQ responses (latest per household) decoded from the cached blob
  derived/iaq_responses_superseded.*      earlier answers of households that answered twice, flagged superseded
  derived/field_survey_points.geojson     live field app points
  derived/street_stats.csv                per-street IAQ summary
  derived/status_counts.csv               door-knock status totals
  sql/01_schema.sql                       CREATE SCHEMA keystone + CREATE TABLE (plain Postgres, no RLS/auth)
  sql/02_load.sql                         psql \\copy commands that load the CSVs
  README.md                               what each file is and how to load it
  MANIFEST.json                           row counts, timestamps, sha256 of every file
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent


def _load_env() -> None:
    env = ROOT / ".env"
    if not env.exists():
        return
    for line in env.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


_load_env()
from supabase import create_client  # noqa: E402
from shimberg_helpers import superseded_collection  # noqa: E402

URL = os.environ.get("SUPABASE_URL", "")
KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
if not URL or not KEY:
    sys.exit("ERROR: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in .env")

sb = create_client(URL, KEY)
PROJECT_REF = URL.split("//")[-1].split(".")[0]

# Research-data tables handed to Shimberg. App-internal tables (team_members,
# invite_codes, field_guest_sessions, user_presence, team_chat_messages,
# member_invites, report_*, daily_report_runs) hold staff emails / session ids
# and are deliberately NOT exported.
RAW_TABLES = [
    "field_survey_points",
    "community_contacts",
    "iaq_surveys",
    "survey_responses",
    "parcels",
    "keystone_dashboard_data",
    "keystone_analysis_versions",
]

PAGE = 1000


def fetch_all(table: str, order: str | None = None) -> list[dict]:
    rows: list[dict] = []
    start = 0
    while True:
        q = sb.table(table).select("*")
        if order:
            q = q.order(order)
        r = q.range(start, start + PAGE - 1).execute()
        rows.extend(r.data)
        if len(r.data) < PAGE:
            return rows
        start += PAGE


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def pg_type(series: pd.Series) -> str:
    if series.map(lambda v: isinstance(v, (dict, list))).any():
        return "jsonb"
    s = series.dropna()
    if s.empty:
        return "text"
    if pd.api.types.is_bool_dtype(s):
        return "boolean"
    if pd.api.types.is_integer_dtype(s):
        return "bigint"
    if pd.api.types.is_float_dtype(s):
        # floats that are all whole numbers came from ints with NULLs
        return "bigint" if (s == s.round()).all() and s.abs().max() < 9e18 else "double precision"
    return "text"


def normalize(df: pd.DataFrame) -> pd.DataFrame:
    """Float columns that only hold whole numbers (ints with NULLs) become nullable Int64,
    so the CSV writes 26136000 rather than 26136000.0 and matches the bigint DDL."""
    out = df.copy()
    for c in out.columns:
        s = out[c]
        if pd.api.types.is_float_dtype(s):
            nn = s.dropna()
            if not nn.empty and (nn == nn.round()).all() and nn.abs().max() < 9e18:
                out[c] = s.astype("Int64")
    return out


def write_csv(df: pd.DataFrame, path: Path) -> None:
    out = df.copy()
    for c in out.columns:
        if out[c].map(lambda v: isinstance(v, (dict, list))).any():
            out[c] = out[c].map(lambda v: json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v)
    out.to_csv(path, index=False, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")


def ddl(table: str, df: pd.DataFrame, pk: str | None, type_overrides: dict[str, str] | None = None) -> str:
    overrides = type_overrides or {}
    cols = []
    for c in df.columns:
        t = overrides.get(c) or pg_type(df[c])
        cols.append(f"  {quote(c)} {t}{' PRIMARY KEY' if c == pk else ''}")
    return f"CREATE TABLE keystone.{quote(table)} (\n" + ",\n".join(cols) + "\n);\n"


def quote(ident: str) -> str:
    return '"' + ident.replace('"', '""') + '"'


def main() -> None:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "exports" / f"shimberg_{today}"
    raw_dir, der_dir, sql_dir = out / "raw", out / "derived", out / "sql"
    for d in (raw_dir, der_dir, sql_dir):
        d.mkdir(parents=True, exist_ok=True)

    manifest: dict = {
        "exported_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": f"Supabase project {PROJECT_REF} (read-only export via service role)",
        "tables": {},
        "files": {},
    }
    schema_sql: list[str] = [
        "-- KeyStone research data — plain PostgreSQL schema (no Supabase auth/RLS).",
        f"-- Generated {manifest['exported_at_utc']} from Supabase project {PROJECT_REF}.",
        "CREATE SCHEMA IF NOT EXISTS keystone;",
        "",
    ]
    load_sql: list[str] = [
        "-- Run from the package root with psql, e.g.:",
        "--   psql \"$SHIMBERG_DATABASE_URL\" -f sql/01_schema.sql",
        "--   psql \"$SHIMBERG_DATABASE_URL\" -f sql/02_load.sql",
        "\\set ON_ERROR_STOP on",
        "",
    ]

    type_overrides = {
        "field_survey_points": {"id": "uuid", "collector_id": "uuid", "guest_session_id": "uuid",
                                "collected_at": "timestamptz", "synced_at": "timestamptz", "updated_at": "timestamptz",
                                "lat": "double precision", "lon": "double precision"},
        "community_contacts": {"survey_date": "date", "uploaded_at": "timestamptz", "created_at": "timestamptz",
                               "updated_at": "timestamptz", "added_by_user_id": "uuid",
                               "added_by_guest_session_id": "uuid", "lat": "double precision", "lon": "double precision"},
        "keystone_dashboard_data": {"payload": "jsonb", "updated_at": "timestamptz"},
        "keystone_analysis_versions": {"payload": "jsonb", "created_at": "timestamptz"},
    }
    pks = {"field_survey_points": "id", "community_contacts": "id", "iaq_surveys": "id",
           "survey_responses": "id", "parcels": "id", "keystone_dashboard_data": "data_type",
           "keystone_analysis_versions": "id"}

    # ── 1. raw tables ────────────────────────────────────────────────────────
    blobs: dict[str, dict] = {}
    for t in RAW_TABLES:
        rows = fetch_all(t, order=pks.get(t))
        print(f"[raw] {t:30s} {len(rows):6d} rows")
        manifest["tables"][t] = {"rows": len(rows)}
        (raw_dir / f"{t}.json").write_text(json.dumps(rows, ensure_ascii=False, indent=None))
        df = pd.DataFrame(rows)
        if df.empty:
            # keep the table in the schema with its documented columns
            cols = {
                "iaq_surveys": ["id", "street_name", "health_score", "iaq_score", "struct_score", "overall_risk",
                                "risk_tier", "ownership", "housing_type", "year_built", "condition", "has_mold",
                                "lat", "lon", "color", "uploaded_at", "created_at", "updated_at", "uploaded_by_user_id"],
                "parcels": ["id", "parcel_id", "address", "land_use", "just_value", "assessed_value", "living_area",
                            "year_built", "geometry"],
                "survey_responses": ["id", "response_id", "raw_answers", "computed_scores", "uploaded_by_user_id"],
            }.get(t, ["id"])
            df = pd.DataFrame(columns=cols)
        df = normalize(df)
        write_csv(df, raw_dir / f"{t}.csv")
        schema_sql.append(ddl(t, df, pks.get(t), type_overrides.get(t)))
        load_sql.append(f"\\copy keystone.{quote(t)} FROM 'raw/{t}.csv' WITH (FORMAT csv, HEADER true)")
        if t == "keystone_dashboard_data":
            blobs = {r["data_type"]: r for r in rows}

    # ── 2. derived (decoded blobs) ───────────────────────────────────────────
    def fc_to_df(fc: dict, id_from_feature: bool = False) -> pd.DataFrame:
        recs = []
        for f in fc.get("features", []):
            p = dict(f.get("properties") or {})
            if id_from_feature and "id" in f:
                p = {"feature_id": f["id"], **p}
            g = f.get("geometry") or {}
            if g.get("type") == "Point":
                p["lon"], p["lat"] = g["coordinates"][0], g["coordinates"][1]
            else:
                p["geometry_geojson"] = g
            recs.append(p)
        return pd.DataFrame(recs)

    def emit_derived(name: str, df: pd.DataFrame, fc: dict | None, overrides: dict | None = None, note: str = "") -> None:
        print(f"[derived] {name:30s} {len(df):6d} rows")
        df = normalize(df)
        write_csv(df, der_dir / f"{name}.csv")
        if fc is not None:
            (der_dir / f"{name}.geojson").write_text(json.dumps(fc, ensure_ascii=False))
        manifest["tables"][f"derived.{name}"] = {"rows": len(df), "note": note}
        schema_sql.append(ddl(name, df, None, overrides))
        load_sql.append(f"\\copy keystone.{quote(name)} FROM 'derived/{name}.csv' WITH (FORMAT csv, HEADER true)")

    if "parcels" in blobs:
        fc = blobs["parcels"]["payload"]
        df = fc_to_df(fc, id_from_feature=True)
        emit_derived("parcels_decoded", df, fc, {"geometry_geojson": "jsonb"},
                     f"Clay County cadastral parcels for the study area; blob updated {blobs['parcels']['updated_at']}")

    if "community_contact" in blobs:
        fc = blobs["community_contact"]["payload"]
        emit_derived("community_contact_points", fc_to_df(fc), fc, None,
                     f"Door-knock outcomes shown on the dashboard; blob updated {blobs['community_contact']['updated_at']}")

    if "iaq_survey" in blobs:
        pl = blobs["iaq_survey"]["payload"]
        fc = pl["geojson"]
        emit_derived("iaq_responses", fc_to_df(fc), fc, None,
                     f"Qualtrics IAQ survey responses, geocoded; source file {pl.get('source_filename')}; "
                     f"blob updated {blobs['iaq_survey']['updated_at']}")
        sfc = superseded_collection(pl)
        if sfc:
            emit_derived("iaq_responses_superseded", fc_to_df(sfc), sfc, None,
                         "Earlier answers from households that answered twice; excluded from "
                         "every statistic (the latest RecordedDate is kept in iaq_responses)")
        ss = pd.DataFrame([{"street": k, **v} for k, v in (pl.get("street_stats") or {}).items()])
        emit_derived("street_stats", ss, None, {"housing_types": "jsonb"}, "Per-street IAQ summary")
        (der_dir / "iaq_analysis_summary.json").write_text(json.dumps(pl.get("analysis"), ensure_ascii=False, indent=2))
        (der_dir / "iaq_validation.json").write_text(json.dumps(pl.get("validation"), ensure_ascii=False, indent=2))

    if "survey_points" in blobs:
        fc = blobs["survey_points"]["payload"]
        emit_derived("survey_points_cached", fc_to_df(fc), fc, None,
                     f"Legacy cached field points; blob updated {blobs['survey_points']['updated_at']}")

    if "analysis" in blobs:
        a = blobs["analysis"]["payload"]
        sc = pd.DataFrame([{"status": k, "count": v, "color": (a.get("status_colors") or {}).get(k)}
                           for k, v in (a.get("status_counts") or {}).items()])
        emit_derived("status_counts", sc, None, None, "Door-knock status totals from the dashboard analysis blob")
        (der_dir / "analysis_summary.json").write_text(json.dumps(a, ensure_ascii=False, indent=2))

    # live field points as GeoJSON too
    fsp = json.loads((raw_dir / "field_survey_points.json").read_text())
    fc = {"type": "FeatureCollection", "features": [
        {"type": "Feature", "geometry": {"type": "Point", "coordinates": [r["lon"], r["lat"]]},
         "properties": {k: v for k, v in r.items() if k not in ("lat", "lon")}} for r in fsp]}
    (der_dir / "field_survey_points.geojson").write_text(json.dumps(fc, ensure_ascii=False))

    # ── 3. SQL + README + manifest ───────────────────────────────────────────
    (sql_dir / "01_schema.sql").write_text("\n".join(schema_sql) + "\n")
    (sql_dir / "02_load.sql").write_text("\n".join(load_sql) + "\n")

    readme = f"""# KeyStone research data — hand-over package

Exported {manifest['exported_at_utc']} from the live KeyStone database
(Supabase project `{PROJECT_REF}`, read-only). Nothing in the source was changed.

## What is in here

| Folder | Contents |
|---|---|
| `raw/` | Every row of each research table, exactly as stored, as CSV and JSON. |
| `derived/` | The dashboard's cached data blobs decoded into flat tables and GeoJSON. **This is where the parcels, door-knock points and IAQ survey responses actually are** (the relational `parcels` and `iaq_surveys` tables are empty by design; the app serves everything from the `keystone_dashboard_data` blobs). |
| `sql/` | Plain-PostgreSQL schema and a psql loader. No Supabase extensions, no PostGIS, no auth or RLS. |

Row counts are in `MANIFEST.json`.

## Loading into Shimberg's Postgres

From this folder:

```bash
psql "$DATABASE_URL" -f sql/01_schema.sql
psql "$DATABASE_URL" -f sql/02_load.sql
```

Everything lands in a `keystone` schema. Geometry is stored as GeoJSON text in
`jsonb` columns (`geometry_geojson`) plus plain `lat`/`lon` doubles for points.
If Shimberg's database has PostGIS, convert with
`ST_SetSRID(ST_GeomFromGeoJSON(geometry_geojson::text), 4326)`.

## Key tables

- `keystone.parcels_decoded` — cadastral parcel polygons with owner, land use, values, year built.
- `keystone.community_contact_points` — door-knock outcomes (status, address, street, date).
- `keystone.iaq_responses` — geocoded Qualtrics IAQ survey responses with computed scores (the latest response per household; these are the analysed rows).
- `keystone.iaq_responses_superseded` — earlier answers of households that answered twice (`superseded = true`, `superseded_by` = the kept response). Kept for the record, excluded from every statistic.
- `keystone.field_survey_points` — points logged live from the mobile field app.
- `keystone.community_contacts` — the relational contacts table (the blob above is the merged, de-duplicated view the dashboard shows).
- `keystone.keystone_analysis_versions` — every historical snapshot (upload / nightly merge), payload as jsonb.

## Not included

Team roster, invite codes, guest sessions, presence, chat and report settings
are app-internal and contain staff emails and session identifiers; they were
left out on purpose.
"""
    (out / "README.md").write_text(readme)

    for p in sorted(out.rglob("*")):
        if p.is_file() and p.name != "MANIFEST.json":
            manifest["files"][str(p.relative_to(out))] = {"bytes": p.stat().st_size, "sha256": sha256(p)}
    (out / "MANIFEST.json").write_text(json.dumps(manifest, indent=2))
    print(f"\nDone → {out}")


if __name__ == "__main__":
    main()
