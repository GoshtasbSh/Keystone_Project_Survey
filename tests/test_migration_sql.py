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


if __name__ == '__main__':
    unittest.main()
