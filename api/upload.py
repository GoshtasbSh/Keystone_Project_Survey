"""POST /api/upload?type={iaq|survey|results} — admin-only upload pipeline.

Consolidates the three previous endpoints (api/upload/iaq.py, .../survey.py,
.../results.py) into a single Vercel function so we stay within the Hobby
plan's 12-function ceiling. Behavior per branch is unchanged:

  ?type=iaq     — Qualtrics IAQ CSV. Score formulas, 4-tier geocoding,
                  IAQ↔contact upgrade, field pins rebuilt and re-linked,
                  linked field_survey_points rows flagged iaq_matched
                  (their status is never changed).
  ?type=survey  — Community contact Excel/CSV. Geocoding + community_contacts
                  table mirror so the mobile field app stays in sync.
                  Refuses a file with no Address column or 0 placeable
                  contacts, and a large drop unless ?force=1.
  ?type=results — Generic survey results CSV/Excel. RESULTS_PII_COLS stripped before
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
    dedup_contacts_at_parcel, RESULTS_PII_COLS, _build_validation_summary,
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
    """Mark field_survey_points rows iaq_matched=true for the ids the IAQ
    matcher linked this pass.

    Guarantees:
      - Touches ONLY `iaq_matched`. The surveyor's `status`, `notes`,
        position and times are never changed (user rule 2026-10-13).
      - Only ever sets true; no path sets it back to false.
      - Only the given ids; no write when the list is empty.
      - Never raises: the survey data was already saved.
    """
    if not upgraded_ids:
        return
    try:
        sb.table('field_survey_points').update(
            {'iaq_matched': True}
        ).in_('id', upgraded_ids).execute()
    except Exception as e:
        print(f"[upload/iaq] field-point iaq_matched update failed n={len(upgraded_ids)}: {e}")


def _all_iaq_features(geojson) -> list:
    """Every stored response: drawn features plus the superseded (earlier
    repeat) responses kept alongside them. Used by the upload safety guard."""
    g = geojson if isinstance(geojson, dict) else {}
    return list(g.get('features') or []) + list(g.get('superseded_features') or [])


def _finalize_iaq_match_state(geojson: dict, analysis: dict, contact_feats: list) -> None:
    """Re-derive match_status from iaq_matched (same rule as daily-refresh)
    and refresh the stored matched/unmatched counts after the field pass may
    have linked more responses (audit P22). Other validation keys
    (completed_in_csv, responses_mapped, ...) are kept. Mutates in place."""
    feats = (geojson or {}).get('features') or []
    for f in feats:
        p = f.setdefault('properties', {})
        p['match_status'] = 'matched' if p.get('iaq_matched') else 'iaq_only'
    validation = analysis.setdefault('validation', {})
    validation.update(_build_validation_summary(feats, contact_feats))


def _with_audit_trail(body: dict, commit_result: dict) -> dict:
    return {**body, 'audit_trail': _audit_trail_summary(
        (commit_result or {}).get('version_statuses') or [])}


def _is_field_feature(f: dict) -> bool:
    return is_field_feature(f)


# A contacts upload that would shrink the stored contact set below this
# fraction is refused unless ?force=1 (2026-07-20: a Qualtrics export
# dropped into the contacts box replaced 277 contacts with 0).
CONTACT_REGRESSION_RATIO = 0.8


def evaluate_contact_upload_safety(stored_contact_count: int,
                                   incoming_contact_count: int,
                                   filename: str, force: bool) -> dict:
    """Decide whether a Community Contact upload may replace the stored
    contacts. Mirrors evaluate_iaq_upload_safety.

      * 0 placeable contacts -> always refused (400), even with force:
        there is no legitimate reason to wipe every contact.
      * fewer than CONTACT_REGRESSION_RATIO x the stored count -> 409
        unless force.
    """
    if incoming_contact_count <= 0:
        return {
            'allowed': False, 'status': 400, 'reason': 'no_contacts',
            'detail': (
                f"Refused: no address in '{filename}' could be placed on the map, "
                f"so saving it would delete all {stored_contact_count} stored "
                f"community contacts. Check that this is the Community Contact sheet."
            ),
        }
    if (stored_contact_count and not force
            and incoming_contact_count < stored_contact_count * CONTACT_REGRESSION_RATIO):
        return {
            'allowed': False, 'status': 409, 'reason': 'contact_regression',
            'detail': (
                f"Refused: '{filename}' has {incoming_contact_count} contacts but "
                f"{stored_contact_count} are stored, so saving it would remove "
                f"{stored_contact_count - incoming_contact_count} from the map. "
                f"If this is intentional, confirm the upload (re-sent with ?force=1)."
            ),
        }
    return {'allowed': True, 'status': 200, 'reason': None, 'detail': ''}


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


def _audit_trail_summary(statuses) -> dict:
    """Fold the per-version statuses (commit_dashboard_writes(...)
    ['version_statuses']) into the `audit_trail` field of the upload
    response. The worst status wins."""
    statuses = list(statuses)
    if 'failed' in statuses:
        return {
            'status': 'missing',
            'detail': ('Your data was saved, but no History entry was written for at '
                       'least one dataset, so this upload cannot be restored from '
                       'History. Check the Vercel logs.'),
        }
    if 'base_only' in statuses:
        return {
            'status': 'degraded',
            'detail': ('Your data was saved, but the uploader, filename and '
                       'dropped-response audit fields were not recorded: the database '
                       'is missing migration 26 (supabase/migrations/26_upload_audit_trail.sql).'),
        }
    return {'status': 'full', 'detail': ''}


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
    # Superseded (earlier repeat) responses stay stored in
    # geojson['superseded_features'], so they count on both sides —
    # otherwise the first deduplicated upload reads as 8 deleted responses.
    safety = evaluate_iaq_upload_safety(
        _all_iaq_features((stored_iaq or {}).get('geojson')),
        _all_iaq_features(geojson), analysis, filename, force)
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
    _finalize_iaq_match_state(geojson, analysis, contact_only_feats)
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


def commit_iaq_upload(sb, plan: dict, writeback_field_points: bool = True) -> dict:
    """Write a prepare_iaq_upload plan: all blobs + version rows in one
    transaction, then (unless switched off) mark linked field rows
    iaq_matched=true. That flag is the only field_survey_points column an
    upload may change."""
    result = commit_dashboard_writes(sb, plan['blobs'], plan['versions'])
    if writeback_field_points:
        _upgrade_field_points_iaq_matched(sb, plan['upgraded_ids'])
    else:
        print(f"[upload/iaq] field write-back skipped for {len(plan['upgraded_ids'])} rows")
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
            result = commit_iaq_upload(sb, plan)
        except Exception as e:
            tb = traceback.format_exc()
            print(f"[upload/iaq] commit FAIL {type(e).__name__}: {e}\n{tb[:2000]}")
            return json_response(self, 500, {
                'detail': ('Saving the upload failed. With migration 29 applied nothing '
                           'was changed; check Vercel logs, then upload again.'),
            })
        return json_response(self, 200, _with_audit_trail(plan['body'], result))

    # ── Survey (community contacts) ────────────────────────────────────
    def _handle_survey(self, filename: str, file_bytes: bytes, admin_uid=None, uploader_email=None):
        suf = Path(filename or '').suffix.lower()
        if suf not in ('.xlsx', '.xls', '.csv'):
            return json_response(self, 400, {'detail': 'Upload an Excel (.xlsx/.xls) or CSV file.'})
        sb = supabase_admin() or supabase_anon()
        if not sb:
            return json_response(self, 500, {'detail': 'Supabase not configured.'})
        force = (parse_qs(urlparse(self.path).query).get('force', ['0'])[0] or '').lower() \
            in ('1', 'true', 'yes')
        try:
            stored_blob, _ = load_blob_with_stamp(sb, 'community_contact')
            stored_iaq, _ = load_blob_with_stamp(sb, 'iaq_survey')
        except Exception as e:
            print(f"[upload/survey] read FAIL {type(e).__name__}: {e}")
            return json_response(self, 500, {
                'detail': 'Could not read the stored contacts — nothing was changed. Check Vercel logs.'})
        stored_contacts = sum(1 for f in (stored_blob or {}).get('features') or []
                              if not _is_field_feature(f))
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

        # Fresh CSV upload starts with no IAQ tags (Completed -> 'contact_only'
        # until the next IAQ upload), then parcel dedup of CONTACTS only.
        contact_feats = survey_data.get('features', [])
        tag_contact_match_status(contact_feats)
        contact_feats = dedup_contacts_at_parcel(contact_feats)

        safety = evaluate_contact_upload_safety(stored_contacts, len(contact_feats), filename, force)
        print(f"[upload/survey] safety={safety['reason'] or 'ok'} stored={stored_contacts} "
              f"incoming={len(contact_feats)} force={force}")
        if not safety['allowed']:
            return json_response(self, safety['status'], {
                'detail': safety['detail'], 'reason': safety['reason'],
                'stored_contacts': stored_contacts, 'incoming_contacts': len(contact_feats),
            })

        # Field half straight from the table, linked to the stored responses
        # so a pin keeps its survey link across a contacts upload.
        try:
            field_feats = _load_all_field_features(sb)
        except Exception as e:
            print(f"[upload/survey] field read FAIL {type(e).__name__}: {e}")
            return json_response(self, 500, {
                'detail': 'Could not read the field survey points — nothing was changed. Check Vercel logs.'})
        iaq_feats = ((stored_iaq or {}).get('geojson') or {}).get('features') or []
        if iaq_feats and field_feats:
            _apply_iaq_to_field_features(field_feats, iaq_feats, parcel_idx=parcel_idx)
        merged_feats = list(contact_feats) + list(field_feats)
        survey_data['features'] = merged_feats
        n = len(merged_feats)
        today = datetime.now(timezone.utc).date().isoformat()

        try:
            result = commit_dashboard_writes(
                sb,
                blobs=[
                    {'data_type': 'community_contact', 'payload': survey_data},
                    # parcel_stats preserved — see merge_preserve_analysis.
                    {'data_type': 'analysis',
                     'payload': merge_preserve_analysis(compute_contact_analysis(merged_feats))},
                ],
                versions=[{
                    'data_type': 'community_contact',
                    'payload':   survey_data,
                    'label':     f'Vercel Upload {today} — {len(contact_feats)} contacts · {filename}',
                    'n_points':  n,
                    'uploaded_by_user_id': admin_uid,
                    'uploaded_by_email':   uploader_email,
                    'source_filename':     filename,
                    'source_row_count':    len(contact_feats),
                    'geocoded_count':      n,
                    'failed_geocodes':     failed_geocodes or [],
                    'forced':              force,
                }],
            )
        except Exception as e:
            tb = traceback.format_exc()
            print(f"[upload/survey] commit FAIL {type(e).__name__}: {e}\n{tb[:2000]}")
            return json_response(self, 500, {
                'detail': ('Saving the upload failed. With migration 29 applied nothing '
                           'was changed; check Vercel logs, then upload again.'),
            })
        _sync_community_contacts(sb, contact_feats)

        if failed_geocodes:
            print(f"[upload/survey] {len(failed_geocodes)} addresses failed geocoding: {failed_geocodes[:10]}")
        return json_response(self, 200, _with_audit_trail({
            'status':          'ok',
            'points':          n,
            'contact_points':  len(contact_feats),
            'field_points':    len(field_feats),
            'filename':        filename,
            'failed_geocodes': failed_geocodes,
        }, result))

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

        pii = [c for c in RESULTS_PII_COLS if c in df.columns]
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
        commit_dashboard_writes(sb, [{'data_type': 'survey_results', 'payload': payload}], [])
        return json_response(self, 200, {
            'status':  'ok',
            'rows':    len(df),
            'columns': list(df.columns),
        })
