"""One write path for keystone_dashboard_data + keystone_analysis_versions.

`commit_dashboard_writes` sends every blob upsert and version insert of one
upload / refresh / restore to the migration-29 RPC `keystone_commit_blobs`,
which applies them in ONE transaction (all or nothing) and, when
`expected` is given, refuses the write if any of those rows changed since
the caller read them (compare-and-set; closes the cron-vs-upload race).

If migration 29 is not applied yet (PostgREST PGRST202 / SQLSTATE 42883,
or a client without .rpc) it falls back to the previous sequential
writes, still in the safest order: compare-and-set check first, then the
data blobs, then the (never-raising) audit version rows.
"""
from __future__ import annotations

RPC_NAME = "keystone_commit_blobs"

# Columns that exist only after migration 26. The sequential fallback
# retries a version insert without them; the RPC (migration 29) creates them.
VERSION_AUDIT_KEYS = (
    "uploaded_by_user_id", "uploaded_by_email", "source_filename",
    "source_row_count", "geocoded_count", "failed_geocodes",
    "dropped_response_ids", "forced",
)


class StaleWriteError(Exception):
    """A row named in `expected` changed between the caller's read and its write."""


def _err_text(err: Exception) -> str:
    """postgrest-py's APIError keeps code/message as attributes; str() of
    it differs between versions, so look at all of them."""
    parts = [str(err)] + [str(getattr(err, a, "") or "") for a in ("code", "message", "details")]
    return " ".join(p for p in parts if p)


def _rpc_missing(err: Exception) -> bool:
    msg = _err_text(err)
    return ("PGRST202" in msg or "42883" in msg
            or "Could not find the function" in msg)


def load_blob_with_stamp(sb, data_type: str) -> tuple:
    """(payload, updated_at) of one keystone_dashboard_data row, or
    (None, None) when the row does not exist. RAISES on a read error —
    unlike _lib.load_cached — so a transient failure can never be taken
    for "no data" and overwrite the blob with an empty one."""
    r = (sb.table("keystone_dashboard_data")
           .select("payload, updated_at")
           .eq("data_type", data_type)
           .limit(1)
           .execute())
    rows = getattr(r, "data", None) or []
    if not rows:
        return None, None
    return rows[0].get("payload"), rows[0].get("updated_at")


def _check_stamps_sequential(sb, expected: dict) -> None:
    for data_type, stamp in (expected or {}).items():
        r = (sb.table("keystone_dashboard_data")
               .select("updated_at")
               .eq("data_type", data_type)
               .limit(1)
               .execute())
        rows = getattr(r, "data", None) or []
        current = rows[0].get("updated_at") if rows else None
        if current != stamp:
            raise StaleWriteError(f"keystone_stale_write: {data_type} changed since it was read")


def _insert_version_sequential(sb, version: dict) -> bool:
    base = {k: v for k, v in version.items() if k not in VERSION_AUDIT_KEYS}
    try:
        sb.table("keystone_analysis_versions").insert(version).execute()
        return True
    except Exception as e:
        if base == version:
            print(f"[writes] version insert failed ({type(e).__name__}: {e})")
            return False
        print(f"[writes] enriched version insert failed ({type(e).__name__}: {e}) — "
              f"retrying with base columns only (migration 26 not applied?)")
    try:
        sb.table("keystone_analysis_versions").insert(base).execute()
        return True
    except Exception as e:
        print(f"[writes] base version insert ALSO failed ({type(e).__name__}: {e}); "
              f"the data blobs were saved, only the audit row is missing.")
        return False


def commit_dashboard_writes(sb, blobs: list, versions: list,
                            expected: dict | None = None) -> dict:
    """blobs    = [{"data_type": str, "payload": dict}, ...]
    versions = [{"data_type", "payload", "label", "n_points", <audit keys>}, ...]
    expected = {"<data_type>": "<updated_at as read>" | None}

    Returns {"mode": "rpc"|"sequential", "blobs_written": [...],
             "versions_written": int}. Raises StaleWriteError on a
    compare-and-set conflict; any other blob-write error propagates.
    """
    rpc = getattr(sb, "rpc", None)
    if callable(rpc):
        try:
            res = rpc(RPC_NAME, {
                "p_blobs": blobs,
                "p_versions": versions,
                "p_expected": expected or {},
            }).execute()
            data = getattr(res, "data", None) or {}
            ids = data.get("version_ids") if isinstance(data, dict) else None
            return {"mode": "rpc",
                    "blobs_written": [b["data_type"] for b in blobs],
                    "versions_written": len(ids) if ids is not None else len(versions)}
        except Exception as e:
            if "keystone_stale_write" in _err_text(e):
                raise StaleWriteError(str(e)) from e
            if not _rpc_missing(e):
                raise
            print(f"[writes] {RPC_NAME} not installed (migration 29) — sequential fallback")

    if expected:
        _check_stamps_sequential(sb, expected)
    written = []
    for b in blobs:
        sb.table("keystone_dashboard_data").upsert(
            {"data_type": b["data_type"], "payload": b["payload"]},
            on_conflict="data_type",
        ).execute()
        written.append(b["data_type"])
    n_versions = sum(1 for v in versions if _insert_version_sequential(sb, v))
    return {"mode": "sequential", "blobs_written": written, "versions_written": n_versions}
