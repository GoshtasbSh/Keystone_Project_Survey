"""POST /api/upload?type={iaq|survey|results} — admin-only upload pipeline.

Consolidates the three previous endpoints (api/upload/iaq.py, .../survey.py,
.../results.py) into a single Vercel function so we stay within the Hobby
plan's 12-function ceiling. Behavior per branch is unchanged:

  ?type=iaq     — Qualtrics IAQ CSV. Score formulas, 4-tier geocoding,
                  IAQ↔contact upgrade, field_survey_points status sweep.
  ?type=survey  — Community contact Excel/CSV. Geocoding + community_contacts
                  table mirror so the mobile field app stays in sync.
  ?type=results — Generic survey results CSV/Excel. PII_COLS stripped before
                  persisting under data_type='survey_results'.

Auth: admin role required (require_admin) for every branch — uploads
overwrite production data via the service-role key.
"""
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timezone
from pathlib import Path
import io
import sys
import traceback

sys.path.append(str(Path(__file__).parent))
from _lib import (
    supabase_admin, supabase_anon, load_cached, json_response,
    require_admin, check_upload_size, merge_preserve_analysis,
)
from _processing import (
    parse_multipart_file, load_parcel_index,
    process_iaq_bytes, process_survey_bytes, compute_contact_analysis,
    _apply_iaq_to_field_features, tag_contact_match_status,
    dedup_contacts_at_parcel, PII_COLS,
)
from _field_layer import (
    FIELD_COLS_BASE as _FIELD_COLS_BASE,
    FIELD_COLS_ENRICHED as _FIELD_COLS_ENRICHED,
    field_row_to_feature, load_all_field_rows, rebuild_field_layer,
    is_field_feature, features_signature,
)
from _dashboard_writes import commit_dashboard_writes, load_blob_with_stamp

try:
    import pandas as _pd
    _PD_PARSE_ERR = (_pd.errors.ParserError, _pd.errors.EmptyDataError)
    _HAS_PANDAS = True
except Exception:
    _PD_PARSE_ERR = ()
    _HAS_PANDAS = False


def _sync_community_contacts(sb, features: list) -> None:
    """Replace community_contacts rows so the mobile field app stays in sync.
    Insert-first / delete-orphans so a partial INSERT never empties the table."""
    if not features:
        return
    rows = []
    for f in features:
        p = f.get('properties', {})
        coords = f.get('geometry', {}).get('coordinates', [None, None])
        rows.append({
            'lon':             coords[0],
            'lat':             coords[1],
            'address':         p.get('address', ''),
            'status':          p.get('status', 'Unknown'),
            'status_detail':   p.get('status_detail') or None,
            'second_attempt': p.get('second_attempt') or None,
            'notes':           p.get('notes') or None,
            'survey_date':     p.get('date') or None,
            'street_name':     p.get('street_name', ''),
            'matched_address': p.get('matched_address') or None,
            'color':           p.get('color', '#9ca3af'),
        })
    try:
        batch = 500
        inserted_ids: list[int] = []
        for i in range(0, len(rows), batch):
            result = sb.table('community_contacts').insert(rows[i:i + batch]).execute()
            inserted_ids.extend(r['id'] for r in (result.data or []) if r.get('id'))
        if inserted_ids:
            sb.table('community_contacts').delete().not_.in_('id', inserted_ids).execute()
    except Exception as e:
        print(f'[upload/survey] community_contacts sync WARN {type(e).__name__}: {e}')


def _field_row_to_feature(row: dict):
    """Kept for importers/tests; the one definition lives in _field_layer."""
    return field_row_to_feature(row)


def _load_all_field_features(sb) -> list:
    """Every field_survey_points row as a GeoJSON feature (migration-27
    `address` column tolerated — see _field_layer.load_all_field_rows)."""
    return [f for f in (field_row_to_feature(r)
                        for r in load_all_field_rows(sb, "[upload]")) if f is not None]


def _upgrade_field_points_iaq_matched(sb, upgraded_ids: list) -> None:
    """Bulk-mark field_survey_points rows Completed + iaq_matched=true.

    Task 14: migration 22 added `field_survey_points.iaq_matched` but no
    code path ever wrote it (stuck `false` on all rows). This is the
    ONE place the codebase UPDATEs an existing field_survey_points row —
    it already set `status: 'Completed'` for `upgraded_ids` (the ids the
    IAQ matcher just confirmed this pass); we extend that SAME update to
    also set `iaq_matched: true`, rather than adding a second write.

    Guarantees:
      - Touches ONLY `status` and `iaq_matched` — never `notes`, `lat`,
        `lon`, or `collected_at`.
      - Only ever sets iaq_matched false -> true: `upgraded_ids` is
        already the just-matched set, and there is no code path here
        that flips it back to false.
      - Never widens which rows are touched — same `upgraded_ids` list
        the pre-existing status update used.
      - Never raises — a failed bulk upgrade must not fail the upload
        (the real IAQ data was already saved before this runs).
    """
    if not upgraded_ids:
        return
    try:
        sb.table('field_survey_points').update(
            {'status': 'Completed', 'iaq_matched': True}
        ).in_('id', upgraded_ids).execute()
    except Exception as e:
        print(f"[upload/iaq] bulk field-point upgrade failed n={len(upgraded_ids)}: {e}")


def _all_iaq_features(geojson) -> list:
    """Every stored response: drawn features plus the superseded (earlier
    repeat) responses kept alongside them. Used by the upload safety guard."""
    g = geojson if isinstance(geojson, dict) else {}
    return list(g.get('features') or []) + list(g.get('superseded_features') or [])


def _is_field_feature(f: dict) -> bool:
    return is_field_feature(f)


def evaluate_iaq_upload_safety(stored_features: list, incoming_features: list,
                               analysis: dict, filename: str,
                               force: bool) -> dict:
    """Decide whether an IAQ upload may replace the stored blob.

    Two independent blocks, both overridable with ?force=1:

      1. response_regression — the incoming export is missing ResponseIds
         that the stored blob has. This is the 2026-05-06 failure: a
         60-response test export replaced a 75-response real one and hid
         15 households for 75 days.
      2. degraded_export — Qualtrics gave us a file with missing question
         columns (their scores silently default to 0). The V2_test file
         carried exactly this warning and it was stored and ignored.

    Returns {"allowed": bool, "reason": str|None, "detail": str, "diff": {...}}.
    """
    from _processing import diff_iaq_response_ids

    diff = diff_iaq_response_ids(stored_features, incoming_features)
    missing = ((analysis or {}).get('validation_warnings') or {}).get('missing_columns') or {}

    if diff['is_regression'] and not force:
        lost = diff['dropped']
        preview = ', '.join(lost[:10]) + ('…' if len(lost) > 10 else '')
        return {
            'allowed': False,
            'reason': 'response_regression',
            'detail': (
                f"Refused: '{filename}' is missing {len(lost)} response(s) that are "
                f"already stored, so uploading it would delete them from the map. "
                f"Missing ResponseIds: {preview}. "
                f"If this is intentional, re-upload with ?force=1."
            ),
            'diff': diff,
        }

    if missing and not force:
        return {
            'allowed': False,
            'reason': 'degraded_export',
            'detail': (
                f"Refused: '{filename}' is missing expected Qualtrics columns "
                f"({missing}); scores for those questions would default to 0. "
                f"Re-export from Qualtrics with all question blocks included, "
                f"or re-upload with ?force=1."
            ),
            'diff': diff,
        }

    return {'allowed': True, 'reason': None, 'detail': '', 'diff': diff}


def _insert_version_row(sb, base_fields: dict, extra_fields: dict) -> None:
    """Insert a keystone_analysis_versions row, tolerating migration 26
    (the upload-audit-trail columns) not having been applied yet.

    `base_fields` is the original, always-present column set (data_type,
    payload, label, n_points). `extra_fields` is the new audit-trail data
    (uploaded_by_user_id, source_filename, dropped_response_ids, ...).

    We try the enriched insert first. PostgREST rejects inserts that
    reference columns the schema doesn't have, and this code ships before
    the migration is guaranteed to be applied — so on ANY exception we log
    it and retry with only `base_fields`, so an upload never fails purely
    because the audit columns don't exist yet.

    The version row is an audit convenience, not the upload's real data
    (that's `keystone_dashboard_data`, already upserted by the caller
    before this runs). So neither insert is allowed to raise: if the base
    retry *also* fails, we log it and return normally rather than let the
    exception escape to `do_POST`'s outer handler — a missing audit row
    must never turn into a false "your upload failed" 500 for the admin.
    """
    try:
        sb.table('keystone_analysis_versions').insert({**base_fields, **extra_fields}).execute()
        return
    except Exception as e:
        print(f"[upload] enriched version insert failed ({type(e).__name__}: {e}) — "
              f"retrying with base columns only (migration 26 not applied?)")
    try:
        sb.table('keystone_analysis_versions').insert(base_fields).execute()
    except Exception as e:
        print(f"[upload] base version insert ALSO failed ({type(e).__name__}: {e}) — "
              f"giving up on the audit row for this upload; the real data "
              f"was already saved to keystone_dashboard_data.")


def _resolve_uploader_email(sb, uid):
    """Best-effort lookup of the uploader's email for the audit trail.

    Uses the Supabase Auth Admin API (`sb.auth.admin.get_user_by_id`),
    which is only reachable with a service-role client. `team_members`
    has no email column (see supabase/migrations/09_team_membership.sql)
    and `require_auth`/`require_team_member`/`require_admin` intentionally
    return only a bare uid — widening those signatures would touch every
    other caller across the codebase, so this is a small, self-contained
    helper instead.

    This must NEVER raise and NEVER block the upload: on any failure
    (missing client, missing uid, the installed supabase-py version not
    exposing `.auth.admin`, a network/permissions error, ...) it logs and
    returns None so `uploaded_by_email` stays NULL, same as before.
    """
    if not sb or not uid:
        return None
    try:
        admin_api = getattr(getattr(sb, 'auth', None), 'admin', None)
        get_user_by_id = getattr(admin_api, 'get_user_by_id', None)
        if not callable(get_user_by_id):
            return None
        resp = get_user_by_id(uid)
        user = getattr(resp, 'user', None)
        email = getattr(user, 'email', None) if user else None
        return email or None
    except Exception as e:
        print(f"[upload] uploader email lookup failed ({type(e).__name__}: {e}) — "
              f"leaving uploaded_by_email NULL")
        return None


def _reject(status: int, detail: str, **extra) -> dict:
    return {'status': status, 'body': {'detail': detail, **extra}}


def prepare_iaq_upload(sb, filename: str, csv_bytes: bytes, *, force: bool = False,
                       admin_uid=None, uploader_email=None, parcel_idx=None) -> dict:
    """Everything a Qualtrics upload does EXCEPT writing.

    Returns {'status': 200, 'body': <response JSON>, 'blobs': [...],
    'versions': [...], 'upgraded_ids': [...], 'field_report': {...}} or
    {'status': 4xx/5xx, 'body': {'detail': ...}}. All reads and all
    computation happen here, so commit_iaq_upload is one transaction
    (audit 2026-10-13 F8). scripts/prod_runbook.py calls this same
    function, so a scripted re-run is byte-for-byte the real path.
    """
    if Path(filename or '').suffix.lower() != '.csv':
        return _reject(400, (
            f'Received a {Path(filename or "").suffix.upper() or "non-CSV"} file. '
            'Please export from Qualtrics as CSV: '
            'Data → Export & Import → Export Data → CSV format.'))

    try:
        contact_blob, _ = load_blob_with_stamp(sb, 'community_contact')
        stored_iaq, _ = load_blob_with_stamp(sb, 'iaq_survey')
        field_rows = load_all_field_rows(sb, '[upload/iaq]')
    except Exception as e:
        print(f"[upload/iaq] read FAIL {type(e).__name__}: {e}")
        return _reject(500, 'Could not read the stored dashboard data — nothing was changed. '
                            'Check Vercel logs.')
    contact_blob = contact_blob or {}
    old_contact_feats = list(contact_blob.get('features') or [])
    # Signature BEFORE processing: process_iaq_bytes and the tagger mutate
    # the contact dicts in place.
    old_contact_sig = features_signature(old_contact_feats)
    # Field half rebuilt from the table: deleted pins drop out, pins that
    # swallowed a CSV contact give it back (audit F4 / Q4-03).
    rebuilt, field_report = rebuild_field_layer(old_contact_feats, field_rows)
    contact_only_feats = [f for f in rebuilt if not _is_field_feature(f)]
    field_feats = [f for f in rebuilt if _is_field_feature(f)]
    print(f"[upload/iaq] contacts={len(contact_only_feats)} field={len(field_feats)} "
          f"field_removed={len(field_report['removed'])} "
          f"restored={field_report['restored_contacts']}")
    if not contact_only_feats:
        return _reject(400, ('No Community Contact data found. Upload the Community '
                             'Contact CSV/XLSX first, then re-upload the Qualtrics file.'))

    if parcel_idx is None:
        try:
            parcel_idx = load_parcel_index()
        except Exception as e:
            tb = traceback.format_exc()
            print(f"[upload/iaq] parcel-index FAIL {type(e).__name__}: {e}\n{tb[:1500]}")
            return _reject(500, 'Could not load parcel index — check Vercel logs.')

    try:
        geojson, analysis, streets, n_upgraded, failed_geocodes = process_iaq_bytes(
            csv_bytes, contact_only_feats, parcel_idx)
    except _PD_PARSE_ERR as e:
        print(f"[upload/iaq] pandas parse error: {e}")
        return _reject(400, 'Could not parse CSV. Re-export from Qualtrics as CSV (UTF-8).')
    except ValueError as e:
        print(f"[upload/iaq] validation error: {e}")
        return _reject(400, str(e))
    except Exception as e:
        tb = traceback.format_exc()
        print(f"[upload/iaq] processing FAIL {type(e).__name__}: {e}\n{tb[:2000]}")
        return _reject(500, 'Processing failed — check Vercel logs.')

    # ── SAFETY GUARD — before anything is queued for writing ────────
    stored_feats = ((stored_iaq or {}).get('geojson') or {}).get('features') or []
    safety = evaluate_iaq_upload_safety(
        stored_feats, geojson.get('features', []), analysis, filename, force)
    print(f"[upload/iaq] safety={safety['reason'] or 'ok'} "
          f"dropped={len(safety['diff']['dropped'])} added={len(safety['diff']['added'])} "
          f"force={force}")
    if not safety['allowed']:
        return _reject(409, safety['detail'],
                       reason=safety['reason'],
                       dropped_response_ids=safety['diff']['dropped'],
                       added_response_ids=safety['diff']['added'])

    iaq_feats = geojson.get('features', [])
    n = len(iaq_feats)
    today = datetime.now(timezone.utc).date().isoformat()

    # Field pins are matched against THIS upload's responses, so the
    # scores copied onto a pin can never go stale (audit F5), and a
    # response linked only by a field pin is saved as 'matched' (Q2-F9).
    n_field_upgraded = 0
    if iaq_feats and field_feats:
        n_field_upgraded = _apply_iaq_to_field_features(
            field_feats, iaq_feats, parcel_idx=parcel_idx)
        for f in iaq_feats:
            p = f.get('properties') or {}
            p['match_status'] = 'matched' if p.get('iaq_matched') else 'iaq_only'
    upgraded_ids = [
        ff['properties']['field_point_id'] for ff in field_feats
        if ff['properties'].get('has_iaq_survey')
        and ff['properties'].get('status') == 'Completed'
    ]

    # Tag + parcel-dedup CONTACTS only (never field pins — a pin must not
    # swallow a CSV contact; see dedup_contacts_at_parcel docstring).
    tag_contact_match_status(contact_only_feats)
    contact_only_feats = dedup_contacts_at_parcel(contact_only_feats)
    updated_feats = list(contact_only_feats) + list(field_feats)
    updated_contact = {**contact_blob, 'type': 'FeatureCollection', 'features': updated_feats}

    validation = analysis.get('validation', {}) or {}
    warn = analysis.get('validation_warnings', {}) or {}
    if warn:
        validation = {**validation, 'warnings': warn}
    payload = {
        'geojson':         geojson,
        'analysis':        analysis,
        'street_stats':    streets,
        'validation':      validation,
        'source_filename': filename,
    }
    audit = {
        'uploaded_by_user_id': admin_uid,
        'uploaded_by_email':   uploader_email,  # best-effort — see _resolve_uploader_email
        'source_filename':     filename,
    }
    blobs = [{'data_type': 'iaq_survey', 'payload': payload}]
    versions = [{
        'data_type': 'iaq_survey',
        'payload':   payload,
        'label':     f'Vercel Upload {today} — {n} responses · {filename}',
        'n_points':  n,
        **audit,
        'source_row_count':     n,
        'geocoded_count':       n,
        'failed_geocodes':      failed_geocodes or [],
        'dropped_response_ids': safety['diff']['dropped'],
        'forced':               force,
    }]
    if old_contact_sig != features_signature(updated_feats):
        n_removed = len(field_report['removed'])
        blobs.append({'data_type': 'community_contact', 'payload': updated_contact})
        versions.append({
            'data_type': 'community_contact',
            'payload':   updated_contact,
            'label':     (f'IAQ-merged {today} — {n_upgraded} contacts upgraded'
                          + (f', {n_removed} deleted pins removed' if n_removed else '')
                          + f' · {filename}'),
            'n_points':  len(updated_feats),
            **audit,
        })
        # compute_contact_analysis returns parcel_stats: {} (no geopandas on
        # Vercel) — merge so the Parcels tab stays populated.
        blobs.append({'data_type': 'analysis',
                      'payload': merge_preserve_analysis(compute_contact_analysis(updated_feats))})
    if n_field_upgraded > 0:
        versions.append({
            'data_type': 'field_survey',
            'payload':   {'n_field_upgraded': n_field_upgraded},
            'label':     f'IAQ-merged {today} — {n_field_upgraded} field points completed · {filename}',
            'n_points':  n_field_upgraded,
            **audit,
        })

    n_streets = len([s for s, d in streets.items() if not d.get('insufficient_data')])
    if failed_geocodes:
        print(f"[upload/iaq] {len(failed_geocodes)} addresses failed geocoding: {failed_geocodes[:10]}")
    print(f"[upload/iaq] prepared n={n} streets={n_streets} field_upgraded={n_field_upgraded}")
    return {
        'status': 200,
        'body': {
            'status':               'ok',
            'points':               n,
            'streets_analyzed':     n_streets,
            'mean_risk':            analysis.get('scores', {}).get('mean_risk', 0),
            'n_upgraded':           n_upgraded,
            'n_field_upgraded':     n_field_upgraded,
            'field_points_removed': len(field_report['removed']),
            'validation':           validation,
            'failed_geocodes':      failed_geocodes,
        },
        'blobs': blobs,
        'versions': versions,
        'upgraded_ids': upgraded_ids,
        'field_report': field_report,
    }


def commit_iaq_upload(sb, plan: dict) -> dict:
    """Write a prepare_iaq_upload plan: all blobs + version rows in one
    transaction, then the (idempotent, never-raising) field-point status
    sweep, which must only run once the data it reflects is saved."""
    result = commit_dashboard_writes(sb, plan['blobs'], plan['versions'])
    _upgrade_field_points_iaq_matched(sb, plan['upgraded_ids'])
    print(f"[upload/iaq] committed mode={result['mode']} blobs={result['blobs_written']} "
          f"versions={result['versions_written']}")
    return result


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            return self._dispatch()
        except Exception as e:
            tb = traceback.format_exc()
            print(f"[upload] UNCAUGHT {type(e).__name__}: {e}\n{tb[:2000]}")
            return json_response(self, 500, {
                'detail': 'Internal server error during upload — check Vercel logs.',
            })

    # ── Dispatcher ──────────────────────────────────────────────────────
    def _dispatch(self):
        # Captured for the audit-trail columns (migration 26) — the caller's
        # auth.users id, so `keystone_analysis_versions.uploaded_by_user_id`
        # can name who uploaded a given file. require_admin() only surfaces
        # the id (widening it would touch every other caller — see
        # _resolve_uploader_email's docstring), so the email is resolved
        # separately, once per upload, via a best-effort Auth Admin API
        # lookup that never raises and never blocks the upload on failure.
        admin_uid = require_admin(self)
        if admin_uid is None:
            return
        uploader_email = _resolve_uploader_email(supabase_admin(), admin_uid)
        qs   = parse_qs(urlparse(self.path).query)
        kind = (qs.get('type', ['iaq'])[0] or 'iaq').lower()

        ct = self.headers.get('Content-Type', '')
        length = check_upload_size(self)
        if length is None:
            return
        body = self.rfile.read(length)
        ct_log = ct[:80].replace('\r', ' ').replace('\n', ' ')
        print(f"[upload/{kind}] start n_bytes={length} ct={ct_log}")

        filename, file_bytes = parse_multipart_file(ct, body)
        if not file_bytes:
            return json_response(self, 400, {'detail': 'No file received.'})

        if kind == 'iaq':
            return self._handle_iaq(filename, file_bytes, admin_uid, uploader_email)
        if kind == 'survey':
            return self._handle_survey(filename, file_bytes, admin_uid, uploader_email)
        if kind == 'results':
            return self._handle_results(filename, file_bytes)
        return json_response(self, 400, {'detail': f"Unknown ?type={kind!r}"})

    # ── IAQ ─────────────────────────────────────────────────────────────
    def _handle_iaq(self, filename: str, csv_bytes: bytes, admin_uid=None, uploader_email=None):
        sb = supabase_admin() or supabase_anon()
        if not sb:
            return json_response(self, 500, {'detail': 'Supabase not configured.'})
        force = (parse_qs(urlparse(self.path).query).get('force', ['0'])[0] or '').lower() \
            in ('1', 'true', 'yes')
        plan = prepare_iaq_upload(sb, filename, csv_bytes, force=force,
                                  admin_uid=admin_uid, uploader_email=uploader_email)
        if plan['status'] != 200:
            return json_response(self, plan['status'], plan['body'])
        try:
            commit_iaq_upload(sb, plan)
        except Exception as e:
            tb = traceback.format_exc()
            print(f"[upload/iaq] commit FAIL {type(e).__name__}: {e}\n{tb[:2000]}")
            return json_response(self, 500, {
                'detail': ('Saving the upload failed. With migration 29 applied nothing '
                           'was changed; check Vercel logs, then upload again.'),
            })
        return json_response(self, 200, plan['body'])

    # ── Survey (community contacts) ────────────────────────────────────
    def _handle_survey(self, filename: str, file_bytes: bytes, admin_uid=None, uploader_email=None):
        suf = Path(filename or '').suffix.lower()
        if suf not in ('.xlsx', '.xls', '.csv'):
            return json_response(self, 400, {'detail': 'Upload an Excel (.xlsx/.xls) or CSV file.'})
        sb = supabase_admin() or supabase_anon()
        if not sb:
            return json_response(self, 500, {'detail': 'Supabase not configured.'})
        try:
            parcel_idx = load_parcel_index()
        except Exception as e:
            tb = traceback.format_exc()
            print(f"[upload/survey] parcel-index FAIL {type(e).__name__}: {e}\n{tb[:1500]}")
            return json_response(self, 500, {'detail': 'Could not load parcel index — check Vercel logs.'})
        try:
            survey_data, failed_geocodes = process_survey_bytes(file_bytes, filename, parcel_idx)
        except ValueError as e:
            print(f"[upload/survey] validation error: {e}")
            return json_response(self, 400, {'detail': str(e)})
        except Exception as e:
            tb = traceback.format_exc()
            print(f"[upload/survey] processing FAIL {type(e).__name__}: {e}\n{tb[:2000]}")
            return json_response(self, 500, {'detail': 'Processing failed — check Vercel logs.'})

        n     = len(survey_data.get('features', []))
        today = datetime.now(timezone.utc).date().isoformat()
        label = f'Vercel Upload {today} — {n} contacts · {filename}'
        print(f"[upload/survey] processed n={n}")

        # Fresh CSV upload starts with no IAQ tags. Mark every Completed
        # contact as 'contact_only' so the desktop map shows them with
        # the amber G2 stroke until the next IAQ upload promotes them.
        # Then dedup at the parcel rep-point so multiple CSV rows
        # sharing a parcel collapse to a single dot (highest-priority
        # status wins; the rest move to coincident_contacts on the
        # survivor). See dedup_contacts_at_parcel() docstring for why.
        contact_feats = survey_data.get('features', [])
        tag_contact_match_status(contact_feats)
        contact_feats = dedup_contacts_at_parcel(contact_feats)

        # Keep dashboard community points as "CSV contacts + existing field points"
        # so users always see one combined layer immediately after CSV upload.
        field_feats = _load_all_field_features(sb)
        # Keep CSV contacts authoritative (already tagged + deduped).
        # Append field features as-is so both datasets are visible/countable
        # without cross-source winner-take-all dedup side effects.
        merged_feats = list(contact_feats) + list(field_feats)

        survey_data['features'] = merged_feats
        n = len(merged_feats)

        sb.table('keystone_dashboard_data').upsert(
            {'data_type': 'community_contact', 'payload': survey_data},
            on_conflict='data_type',
        ).execute()
        _insert_version_row(
            sb,
            base_fields={
                'data_type': 'community_contact',
                'payload':   survey_data,
                'label':     label,
                'n_points':  n,
            },
            extra_fields={
                'uploaded_by_user_id':  admin_uid,
                'uploaded_by_email':    uploader_email,  # best-effort — see _resolve_uploader_email
                'source_filename':      filename,
                'source_row_count':     len(contact_feats),
                'geocoded_count':       n,
                'failed_geocodes':      failed_geocodes or [],
            },
        )
        contact_analysis = compute_contact_analysis(survey_data.get('features', []))
        # Same parcel-preservation merge as the IAQ branch — without
        # this, every survey CSV upload zeros out the Parcels tab on
        # the dashboard until scripts/ingest.py is rerun locally.
        contact_analysis = merge_preserve_analysis(contact_analysis)
        sb.table('keystone_dashboard_data').upsert(
            {'data_type': 'analysis', 'payload': contact_analysis},
            on_conflict='data_type',
        ).execute()
        _sync_community_contacts(sb, contact_feats)

        if failed_geocodes:
            print(f"[upload/survey] {len(failed_geocodes)} addresses failed geocoding: {failed_geocodes[:10]}")
        return json_response(self, 200, {
            'status':          'ok',
            'points':          n,
            'contact_points':  len(contact_feats),
            'field_points':    len(field_feats),
            'filename':        filename,
            'failed_geocodes': failed_geocodes,
        })

    # ── Results (generic CSV/XLSX) ─────────────────────────────────────
    def _handle_results(self, filename: str, file_bytes: bytes):
        if not _HAS_PANDAS:
            return json_response(self, 500, {'detail': 'pandas not available on this function.'})
        suf = Path(filename or '').suffix.lower()
        try:
            if suf == '.csv':
                df = _pd.read_csv(io.BytesIO(file_bytes))
            else:
                df = _pd.read_excel(io.BytesIO(file_bytes))
        except Exception as e:
            return json_response(self, 400, {'detail': f'Could not parse file: {e}'})

        pii = [c for c in PII_COLS if c in df.columns]
        if pii:
            df = df.drop(columns=pii)

        payload = {
            'columns':     list(df.columns),
            'rows':        df.fillna('').to_dict('records'),
            'count':       len(df),
            'dropped_pii': pii,
        }

        sb = supabase_admin() or supabase_anon()
        if not sb:
            return json_response(self, 500, {'detail': 'Supabase not configured — data not saved.'})
        sb.table('keystone_dashboard_data').upsert(
            {'data_type': 'survey_results', 'payload': payload},
            on_conflict='data_type',
        ).execute()
        return json_response(self, 200, {
            'status':  'ok',
            'rows':    len(df),
            'columns': list(df.columns),
        })
