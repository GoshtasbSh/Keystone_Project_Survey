"""Static checks on the hand-applied Supabase migrations.

These migrations are run by hand in the Supabase SQL editor, so CI never
executes them. These tests catch the two kinds of mistake that already
happened here before they reach production:
  - migration 25 used CREATE OR REPLACE to change active_guests()'s
    return type, which Postgres rejects with 42P13;
  - a lockdown migration that silently leaves anon access open.
They also check the data-safety rule: no security migration may contain
row-level DML (INSERT/UPDATE/DELETE/TRUNCATE).
"""
import re
import unittest
from pathlib import Path

MIG = Path(__file__).resolve().parent.parent / 'supabase' / 'migrations'


def _sql(name):
    """Migration text with `--` comments removed, so the prose in a
    header comment can neither satisfy nor break an assertion."""
    text = (MIG / name).read_text(encoding='utf-8')
    return re.sub(r'--[^\n]*', '', text)


_DML = re.compile(r'^\s*(INSERT\s+INTO|UPDATE\s+\S+\s+SET|DELETE\s+FROM|TRUNCATE)\b',
                  re.IGNORECASE | re.MULTILINE)


class Migration25ActiveGuestsTests(unittest.TestCase):
    NAME = '25_active_guests_hide_session_id.sql'

    def setUp(self):
        self.s = _sql(self.NAME)

    def test_drops_old_function_before_creating_new_one(self):
        # Changing RETURNS TABLE(id, name) -> TABLE(name) with CREATE OR
        # REPLACE fails with 42P13 "cannot change return type".
        d = self.s.find('DROP FUNCTION IF EXISTS public.active_guests()')
        c = self.s.find('CREATE FUNCTION public.active_guests()')
        self.assertNotEqual(d, -1, 'missing DROP FUNCTION IF EXISTS public.active_guests()')
        self.assertNotEqual(c, -1, 'missing CREATE FUNCTION public.active_guests()')
        self.assertLess(d, c, 'DROP must come before CREATE')

    def test_does_not_use_create_or_replace(self):
        self.assertIsNone(re.search(r'CREATE\s+OR\s+REPLACE\s+FUNCTION\s+(public\.)?active_guests',
                                    self.s, re.IGNORECASE))

    def test_returns_name_only(self):
        self.assertRegex(self.s, re.compile(r'RETURNS\s+TABLE\(\s*name\s+TEXT\s*\)', re.IGNORECASE))
        self.assertIsNone(re.search(r'SELECT\s+g\.id', self.s, re.IGNORECASE))

    def test_revokes_anon_after_create(self):
        # Supabase gives anon EXECUTE on every new public function by default;
        # REVOKE ... FROM public does not remove it. Live probe 2026-10-13:
        # anon POST rpc/active_guests -> 200.
        m = re.search(r'REVOKE\s+ALL\s+ON\s+FUNCTION\s+public\.active_guests\(\)\s+FROM\s+anon',
                      self.s, re.IGNORECASE)
        self.assertIsNotNone(m, 'must REVOKE ALL ON FUNCTION public.active_guests() FROM anon')
        self.assertGreater(m.start(), self.s.find('CREATE FUNCTION public.active_guests()'))

    def test_keeps_authenticated_and_service_role(self):
        self.assertRegex(self.s, re.compile(
            r'GRANT\s+EXECUTE\s+ON\s+FUNCTION\s+public\.active_guests\(\)\s+TO\s+authenticated,\s*service_role',
            re.IGNORECASE))

    def test_is_one_transaction(self):
        self.assertRegex(self.s, re.compile(r'^\s*BEGIN\s*;', re.IGNORECASE | re.MULTILINE))
        self.assertRegex(self.s, re.compile(r'^\s*COMMIT\s*;', re.IGNORECASE | re.MULTILINE))

    def test_no_row_dml(self):
        self.assertIsNone(_DML.search(self.s))


class Migration28DashboardDataLockdownTests(unittest.TestCase):
    NAME = '28_dashboard_data_rls_lockdown.sql'
    TABLES = ('keystone_dashboard_data', 'keystone_analysis_versions')

    def setUp(self):
        path = MIG / self.NAME
        self.assertTrue(path.exists(), f'{self.NAME} not written yet')
        self.s = _sql(self.NAME)

    def test_enables_rls_on_both_tables(self):
        for t in self.TABLES:
            self.assertRegex(self.s, re.compile(
                rf'ALTER\s+TABLE\s+public\.{t}\s+ENABLE\s+ROW\s+LEVEL\s+SECURITY', re.IGNORECASE), t)

    def test_drops_every_existing_policy_dynamically(self):
        # The stray live policy's name is unknown (pg_policies could not be
        # read on 2026-10-13), so drop them all by looping over pg_policies.
        for t in self.TABLES:
            self.assertRegex(self.s, re.compile(
                rf"FROM\s+pg_policies\s+WHERE\s+schemaname\s*=\s*'public'\s+AND\s+tablename\s*=\s*'{t}'",
                re.IGNORECASE), t)
        self.assertRegex(self.s, re.compile(r"EXECUTE\s+format\('DROP POLICY %I ON", re.IGNORECASE))

    def test_recreates_team_member_select_policy_only(self):
        for t in self.TABLES:
            self.assertRegex(self.s, re.compile(
                rf'ON\s+public\.{t}\s+FOR\s+SELECT\s+TO\s+authenticated\s+'
                rf'USING\s*\(\s*public\.is_team_member\(\(select auth\.uid\(\)\)\)\s*\)',
                re.IGNORECASE), t)
        self.assertIsNone(re.search(r'CREATE\s+POLICY[^;]*FOR\s+(INSERT|UPDATE|DELETE|ALL)\b',
                                    self.s, re.IGNORECASE))

    def test_revokes_anon_and_public_table_privileges(self):
        for t in self.TABLES:
            self.assertRegex(self.s, re.compile(
                rf'REVOKE\s+ALL\s+ON\s+TABLE\s+public\.{t}\s+FROM\s+anon,\s*public', re.IGNORECASE), t)
            self.assertRegex(self.s, re.compile(
                rf'GRANT\s+SELECT\s+ON\s+TABLE\s+public\.{t}\s+TO\s+authenticated', re.IGNORECASE), t)

    def test_never_grants_anon_or_true_policy(self):
        self.assertIsNone(re.search(r'\bTO\s+anon\b', self.s, re.IGNORECASE))
        self.assertIsNone(re.search(r'USING\s*\(\s*true\s*\)', self.s, re.IGNORECASE))

    def test_revokes_anon_execute_on_team_only_rpcs(self):
        for fn in ('active_member_ids', 'list_roster'):
            self.assertRegex(self.s, re.compile(
                rf'REVOKE\s+ALL\s+ON\s+FUNCTION\s+public\.{fn}\(\)\s+FROM\s+anon,\s*public',
                re.IGNORECASE), fn)

    def test_has_self_check_that_aborts_the_transaction(self):
        self.assertIn('relrowsecurity', self.s)
        self.assertRegex(self.s, re.compile(r"has_table_privilege\('anon'", re.IGNORECASE))
        self.assertRegex(self.s, re.compile(r"has_function_privilege\('anon'", re.IGNORECASE))
        self.assertGreaterEqual(len(re.findall(r'RAISE\s+EXCEPTION', self.s, re.IGNORECASE)), 4)
        self.assertRegex(self.s, re.compile(r'^\s*BEGIN\s*;', re.IGNORECASE | re.MULTILINE))
        self.assertRegex(self.s, re.compile(r'^\s*COMMIT\s*;', re.IGNORECASE | re.MULTILINE))

    def test_no_row_dml(self):
        self.assertIsNone(_DML.search(self.s))


class AdditiveMigrationsNoDmlTests(unittest.TestCase):
    """26 and 27 are pending for production; prove they only add columns."""

    def test_26_and_27_are_additive_only(self):
        for name in ('26_upload_audit_trail.sql', '27_field_point_address.sql'):
            s = _sql(name)
            self.assertIsNone(_DML.search(s), name)
            self.assertIsNone(re.search(r'\bDROP\b', s, re.IGNORECASE), name)
            self.assertRegex(s, re.compile(r'ADD\s+COLUMN\s+IF\s+NOT\s+EXISTS', re.IGNORECASE), name)


if __name__ == '__main__':
    unittest.main()
