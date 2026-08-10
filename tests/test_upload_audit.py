"""Tests for the upload audit-trail fallback (Task 5) and its two review
follow-up fixes:

  - `_insert_version_row` must never raise, even if BOTH the enriched
    insert and the base-only retry fail (Finding 1).
  - `_resolve_uploader_email` must never raise and must return None on
    any failure — missing client, missing uid, no admin API on the
    installed supabase-py client, or the Auth Admin API call itself
    raising (Finding 2).

No network, no real Supabase client. `_FakeSupabase` below stands in for
`supabase.Client` and mimics the one failure mode we need to prove:
PostgREST rejects an INSERT that references a column the live schema
doesn't have yet (migration 26 not applied). `_insert_version_row` must
catch that and retry with only the original column set so an upload never
fails purely because the audit columns are missing.
"""
import unittest

from api.upload import _insert_version_row, _resolve_uploader_email


class _FakeTable:
    def __init__(self, name, client):
        self._name = name
        self._client = client
        self._row = None

    def insert(self, row):
        self._row = row
        return self

    def execute(self):
        self._client._record_and_maybe_fail(self._name, self._row)
        return self


class _FakeSupabase:
    """Records every insert as (table_name, row_dict). Raises on the first
    `fail_first_n` inserts against `keystone_analysis_versions`, simulating
    PostgREST's "column does not exist" error for the enriched audit
    columns when migration 26 hasn't been run yet."""

    def __init__(self, fail_first_n=0):
        self.calls = []
        self._fail_remaining = fail_first_n

    def table(self, name):
        return _FakeTable(name, self)

    def _record_and_maybe_fail(self, name, row):
        self.calls.append((name, dict(row)))
        if name == 'keystone_analysis_versions' and self._fail_remaining > 0:
            self._fail_remaining -= 1
            raise Exception(
                'column "uploaded_by_user_id" of relation '
                '"keystone_analysis_versions" does not exist'
            )


class InsertVersionRowFallbackTests(unittest.TestCase):
    def test_falls_back_to_base_columns_when_enriched_insert_raises(self):
        sb = _FakeSupabase(fail_first_n=1)
        base = {'data_type': 'iaq_survey', 'payload': {}, 'label': 'x', 'n_points': 3}
        extra = {
            'uploaded_by_user_id': 'uid-1',
            'source_filename': 'V2_test.csv',
            'dropped_response_ids': [],
            'forced': False,
        }

        # Must not raise — the upload has to succeed even though the
        # migration 26 columns don't exist on this (simulated) schema.
        _insert_version_row(sb, base, extra)

        self.assertEqual(len(sb.calls), 2, "expected an enriched attempt + a base-only retry")
        table1, row1 = sb.calls[0]
        table2, row2 = sb.calls[1]
        self.assertEqual(table1, 'keystone_analysis_versions')
        self.assertEqual(table2, 'keystone_analysis_versions')

        # First attempt carried the enriched (audit-trail) columns...
        self.assertIn('uploaded_by_user_id', row1)
        self.assertIn('source_filename', row1)

        # ...the successful retry is the ORIGINAL column set only — no
        # unknown columns sent, nothing extra, nothing missing.
        self.assertEqual(row2, base)
        self.assertNotIn('uploaded_by_user_id', row2)
        self.assertNotIn('source_filename', row2)

    def test_succeeds_on_first_try_when_migration_26_is_applied(self):
        sb = _FakeSupabase(fail_first_n=0)
        base = {'data_type': 'iaq_survey', 'payload': {}, 'label': 'x', 'n_points': 3}
        extra = {'uploaded_by_user_id': 'uid-1', 'source_filename': 'good.csv'}

        _insert_version_row(sb, base, extra)

        self.assertEqual(len(sb.calls), 1, "no fallback needed — should not retry")
        _, row = sb.calls[0]
        self.assertEqual(row, {**base, **extra})

    def test_community_contact_insert_also_falls_back(self):
        """Same guarantee applies to the community_contact version insert
        in _handle_survey — _insert_version_row is table-agnostic."""
        sb = _FakeSupabase(fail_first_n=1)
        base = {'data_type': 'community_contact', 'payload': {}, 'label': 'y', 'n_points': 9}
        extra = {'uploaded_by_user_id': 'uid-2', 'source_row_count': 9}

        _insert_version_row(sb, base, extra)

        self.assertEqual(len(sb.calls), 2)
        self.assertEqual(sb.calls[1][1], base)

    def test_swallows_exception_when_both_inserts_raise(self):
        """Finding 1 (review): the base-only retry was previously unguarded
        — if it also raised, the exception escaped _insert_version_row into
        do_POST's outer handler and the admin got a false 500, even though
        the real data (keystone_dashboard_data) was already saved. Prove
        that when BOTH the enriched insert and the base-only retry raise,
        _insert_version_row still returns normally instead of propagating."""
        sb = _FakeSupabase(fail_first_n=2)
        base = {'data_type': 'iaq_survey', 'payload': {}, 'label': 'x', 'n_points': 3}
        extra = {'uploaded_by_user_id': 'uid-1', 'source_filename': 'V2_test.csv'}

        try:
            _insert_version_row(sb, base, extra)
        except Exception as e:  # pragma: no cover — this is exactly what must not happen
            self.fail(f"_insert_version_row must swallow both failures, but raised {e!r}")

        # Both attempts were made (enriched, then base-only), both failed,
        # and the caller never sees an exception.
        self.assertEqual(len(sb.calls), 2)
        self.assertEqual(sb.calls[0][0], 'keystone_analysis_versions')
        self.assertEqual(sb.calls[1][0], 'keystone_analysis_versions')


# ── Finding 2: uploaded_by_email resolution ────────────────────────────────

class _FakeAuthUser:
    def __init__(self, email):
        self.email = email


class _FakeAuthUserResponse:
    def __init__(self, email):
        self.user = _FakeAuthUser(email)


class _FakeAdminAPI:
    """Stands in for supabase_auth's SyncGoTrueAdminAPI.get_user_by_id."""

    def __init__(self, email=None, exc=None):
        self._email = email
        self._exc = exc
        self.calls = []

    def get_user_by_id(self, uid):
        self.calls.append(uid)
        if self._exc is not None:
            raise self._exc
        return _FakeAuthUserResponse(self._email)


class _FakeAuthNamespace:
    def __init__(self, admin=None):
        self.admin = admin


class _FakeSupabaseWithAuth:
    """A fake client exposing `.auth.admin.get_user_by_id`, matching the
    shape confirmed against the installed supabase==2.28.3 client
    (`sb.auth.admin` is a SyncGoTrueAdminAPI with `get_user_by_id(uid) ->
    UserResponse`, and `UserResponse.user.email` is the field we want)."""

    def __init__(self, admin=None):
        self.auth = _FakeAuthNamespace(admin)


class ResolveUploaderEmailTests(unittest.TestCase):
    def test_returns_email_on_success(self):
        admin = _FakeAdminAPI(email='admin@example.com')
        sb = _FakeSupabaseWithAuth(admin)

        result = _resolve_uploader_email(sb, 'uid-1')

        self.assertEqual(result, 'admin@example.com')
        self.assertEqual(admin.calls, ['uid-1'])

    def test_returns_none_when_admin_api_raises(self):
        """The Auth Admin API call itself failing (network, permissions,
        unknown uid, ...) must never raise out of the helper — the upload
        must proceed with uploaded_by_email left NULL."""
        admin = _FakeAdminAPI(exc=Exception('permission denied for auth admin API'))
        sb = _FakeSupabaseWithAuth(admin)

        try:
            result = _resolve_uploader_email(sb, 'uid-1')
        except Exception as e:  # pragma: no cover — this is exactly what must not happen
            self.fail(f"_resolve_uploader_email must swallow the failure, but raised {e!r}")

        self.assertIsNone(result)

    def test_returns_none_when_client_has_no_admin_api(self):
        """Fallback for a supabase-py version that doesn't expose
        `.auth.admin` (or exposes `.auth` without an admin API) — the
        lookup must degrade to None silently rather than guessing at a
        method name that isn't there."""
        sb = _FakeSupabaseWithAuth(admin=None)

        result = _resolve_uploader_email(sb, 'uid-1')

        self.assertIsNone(result)

    def test_returns_none_when_client_is_none(self):
        self.assertIsNone(_resolve_uploader_email(None, 'uid-1'))

    def test_returns_none_when_uid_is_none(self):
        admin = _FakeAdminAPI(email='admin@example.com')
        sb = _FakeSupabaseWithAuth(admin)

        result = _resolve_uploader_email(sb, None)

        self.assertIsNone(result)
        self.assertEqual(admin.calls, [], "must not even attempt the lookup without a uid")


if __name__ == '__main__':
    unittest.main()
