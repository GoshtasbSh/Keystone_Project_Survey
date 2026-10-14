"""Migrations 25 (active_guests() returns name only, anon revoked) and 28
(keystone_dashboard_data / keystone_analysis_versions locked to team
members), executed against a throwaway local PostgreSQL that mimics
Supabase's roles and default privileges. Skipped when the PostgreSQL
server binaries are not installed. Never touches Supabase.

The static checks in test_migration_sql.py prove the text says the right
things; this file proves the SQL actually runs, in order, on top of
migration 24, and leaves the permissions the live probes in
test_live_db_security.py expect.

The tests run in file order on one database (module-scoped fixture), the
same pattern as test_migrations_29_30.py."""
import pathlib
import shutil
import socket
import subprocess
import tempfile

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
MIG = ROOT / "supabase" / "migrations"
BINS = {b: shutil.which(b) for b in ("initdb", "pg_ctl", "psql")}
pytestmark = pytest.mark.skipif(not all(BINS.values()),
                                reason="local PostgreSQL binaries not installed")

MEMBER = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
OUTSIDER = "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"
TABLES = ("keystone_dashboard_data", "keystone_analysis_versions")
M25 = "25_active_guests_hide_session_id.sql"
M28 = "28_dashboard_data_rls_lockdown.sql"

# Supabase stand-ins: the three API roles (service_role bypasses RLS), an
# auth schema whose uid() reads the JWT claim GUC, and Supabase's default
# privileges, which grant anon/authenticated/service_role everything on
# every new public table and function. That default grant is what keeps
# anon's EXECUTE alive after `REVOKE ... FROM public`.
SUPABASE = """
CREATE ROLE anon NOLOGIN;
CREATE ROLE authenticated NOLOGIN;
CREATE ROLE service_role NOLOGIN BYPASSRLS;
CREATE SCHEMA auth;
CREATE TABLE auth.users (id uuid PRIMARY KEY, email text, last_sign_in_at timestamptz);
CREATE FUNCTION auth.uid() RETURNS uuid LANGUAGE sql STABLE AS
  $$ SELECT nullif(current_setting('request.jwt.claim.sub', true), '')::uuid $$;
GRANT USAGE ON SCHEMA auth, public TO anon, authenticated, service_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES    TO anon, authenticated, service_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO anon, authenticated, service_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO anon, authenticated, service_role;
CREATE TABLE team_members (id uuid PRIMARY KEY REFERENCES auth.users(id), role text,
                           joined_at timestamptz NOT NULL DEFAULT now());
CREATE TABLE field_guest_sessions (id uuid PRIMARY KEY DEFAULT gen_random_uuid(), name text,
                                   revoked_at timestamptz, expires_at timestamptz);
-- is_admin / is_team_member exactly as migrations 09/17 define them.
CREATE FUNCTION is_admin(uid uuid) RETURNS boolean LANGUAGE sql STABLE SECURITY DEFINER
  SET search_path = public, pg_temp AS
  $$ SELECT EXISTS (SELECT 1 FROM team_members WHERE id = uid AND role = 'admin') $$;
CREATE FUNCTION is_team_member(uid uuid) RETURNS boolean LANGUAGE sql STABLE SECURITY DEFINER
  SET search_path = public, pg_temp AS
  $$ SELECT EXISTS (SELECT 1 FROM team_members WHERE id = uid) $$;
REVOKE ALL ON FUNCTION is_team_member(uuid) FROM public;
GRANT EXECUTE ON FUNCTION is_team_member(uuid) TO authenticated, service_role;
"""


def _free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


@pytest.fixture(scope="module")
def sql():
    tmp = tempfile.TemporaryDirectory()
    data = pathlib.Path(tmp.name) / "data"
    subprocess.run([BINS["initdb"], "-D", str(data), "-U", "postgres", "-A", "trust"],
                   check=True, capture_output=True)
    port = _free_port()
    # TCP only: the pytest tmp path is too long for a unix socket on macOS.
    subprocess.run([BINS["pg_ctl"], "-D", str(data), "-w", "-l", str(data / "log"),
                    "-o", f"-p {port} -c listen_addresses=127.0.0.1 -c unix_socket_directories=''",
                    "start"], check=True, capture_output=True)

    def run(text, ok=True):
        r = subprocess.run([BINS["psql"], "-h", "127.0.0.1", "-p", str(port), "-U", "postgres",
                            "-d", "postgres", "-v", "ON_ERROR_STOP=1", "-qAt", "-c", text],
                           capture_output=True, text=True)
        if ok:
            assert r.returncode == 0, r.stderr
            return r.stdout.strip()
        return r

    run(SUPABASE)
    for name in ("02_keystone_dashboard_data.sql", "03_analysis_versions.sql",
                 "24_active_roster_visibility.sql"):
        run((MIG / name).read_text())
    run(f"INSERT INTO auth.users VALUES ('{MEMBER}', 'm@x', now()), ('{OUTSIDER}', 'o@x', now());"
        f"INSERT INTO team_members (id, role) VALUES ('{MEMBER}', 'member');"
        "INSERT INTO field_guest_sessions (name, expires_at) VALUES ('Guest A', now() + interval '1 day');"
        "INSERT INTO keystone_dashboard_data (data_type, payload) VALUES"
        " ('iaq_survey', '{\"n\": 1}'), ('analysis', '{\"n\": 2}');"
        "INSERT INTO keystone_analysis_versions (data_type, payload, label) VALUES"
        " ('iaq_survey', '{\"n\": 1}', 'v1');"
        # Reproduce the 2026-10-13 live state: RLS off on one table, a stray
        # out-of-repo anon/public policy on both.
        "ALTER TABLE keystone_dashboard_data DISABLE ROW LEVEL SECURITY;"
        "CREATE POLICY \"stray public read\" ON keystone_dashboard_data FOR SELECT TO public USING (true);"
        "CREATE POLICY \"stray anon read\" ON keystone_analysis_versions FOR SELECT TO anon USING (true);")
    yield run
    subprocess.run([BINS["pg_ctl"], "-D", str(data), "-m", "immediate", "stop"],
                   capture_output=True)
    tmp.cleanup()


def _as(role, query, uid=None):
    claim = f"select set_config('request.jwt.claim.sub', '{uid or ''}', false);"
    return f"{claim} set role {role}; {query}"


def _snapshot(sql):
    return sql("select string_agg(data_type || '=' || payload::text, ';' order by data_type) "
               "from keystone_dashboard_data") + "|" + \
        sql("select string_agg(id || '=' || payload::text, ';' order by id) from keystone_analysis_versions")


def test_harness_reproduces_the_live_leak(sql):
    # Same as the live probes: anon reads the blob table and calls the RPCs.
    assert sql(_as("anon", "select count(*) from keystone_dashboard_data")).splitlines()[-1] == "2"
    assert sql(_as("anon", "select count(*) from active_guests()")).splitlines()[-1] == "1"
    assert sql(_as("anon", "select count(*) from active_member_ids()")).splitlines()[-1] == "1"


def test_migration_28_before_25_aborts_and_changes_nothing(sql):
    before = _snapshot(sql)
    r = sql((MIG / M28).read_text(), ok=False)
    assert r.returncode != 0 and "apply migration 25 first" in r.stderr
    # Rolled back as a whole: RLS still off, stray policy still there.
    assert sql("select relrowsecurity from pg_class where relname = 'keystone_dashboard_data'") == "f"
    assert sql("select count(*) from pg_policies where policyname = 'stray public read'") == "1"
    assert _snapshot(sql) == before


def test_old_create_or_replace_form_of_25_is_rejected(sql):
    # Why migration 25 must DROP first: Postgres refuses the return-type change.
    r = sql("CREATE OR REPLACE FUNCTION active_guests() RETURNS TABLE(name TEXT) "
            "LANGUAGE SQL STABLE AS $$ SELECT 'x'::text $$", ok=False)
    assert r.returncode != 0 and "cannot change return type" in r.stderr


def test_migration_25_applies_on_top_of_24_and_reruns(sql):
    sql((MIG / M25).read_text())
    sql((MIG / M25).read_text())
    assert sql("select has_function_privilege('anon', 'public.active_guests()', 'EXECUTE')") == "f"
    r = sql(_as("anon", "select * from active_guests()"), ok=False)
    assert r.returncode != 0 and "permission denied" in r.stderr
    out = sql(_as("authenticated", "select string_agg(name, ',') from active_guests()", MEMBER))
    assert out.splitlines()[-1] == "Guest A"
    r = sql(_as("authenticated", "select id from active_guests()", MEMBER), ok=False)
    assert r.returncode != 0 and "does not exist" in r.stderr
    assert sql(_as("service_role", "select count(*) from active_guests()")).splitlines()[-1] == "1"


def test_migration_28_applies_and_reruns_without_touching_rows(sql):
    before = _snapshot(sql)
    sql((MIG / M28).read_text())
    sql((MIG / M28).read_text())
    assert _snapshot(sql) == before
    for t in TABLES:
        assert sql(f"select relrowsecurity from pg_class where relname = '{t}'") == "t"
        pols = sql(f"select string_agg(policyname || ':' || cmd || ':' || array_to_string(roles, ','), ';') "
                   f"from pg_policies where tablename = '{t}'")
        assert pols.count(":SELECT:authenticated") == 1 and ";" not in pols, pols


@pytest.mark.parametrize("table", TABLES)
def test_anon_is_denied_the_tables(sql, table):
    r = sql(_as("anon", f"select count(*) from {table}"), ok=False)
    assert r.returncode != 0 and "permission denied" in r.stderr


@pytest.mark.parametrize("fn", ["active_guests", "active_member_ids", "list_roster"])
def test_anon_is_denied_the_team_only_rpcs(sql, fn):
    r = sql(_as("anon", f"select * from {fn}()"), ok=False)
    assert r.returncode != 0 and "permission denied" in r.stderr


def test_team_member_reads_and_outsider_sees_nothing(sql):
    q = "select count(*) from keystone_dashboard_data"
    assert sql(_as("authenticated", q, MEMBER)).splitlines()[-1] == "2"
    assert sql(_as("authenticated", q, OUTSIDER)).splitlines()[-1] == "0"
    v = "select count(*) from keystone_analysis_versions"
    assert sql(_as("authenticated", v, MEMBER)).splitlines()[-1] == "1"
    assert sql(_as("authenticated", v, OUTSIDER)).splitlines()[-1] == "0"
    # The dashboard's own calls keep working for a member.
    assert sql(_as("authenticated", "select count(*) from active_member_ids()", MEMBER)).splitlines()[-1] == "1"
    assert sql(_as("authenticated", "select count(*) from list_roster()", MEMBER)).splitlines()[-1] == "1"


@pytest.mark.parametrize("stmt", [
    "insert into keystone_dashboard_data (data_type, payload) values ('x', '{}')",
    "update keystone_dashboard_data set payload = '{}'",
    "delete from keystone_dashboard_data",
    "insert into keystone_analysis_versions (data_type, payload) values ('x', '{}')",
    "delete from keystone_analysis_versions",
])
def test_member_cannot_write(sql, stmt):
    r = sql(_as("authenticated", stmt, MEMBER), ok=False)
    assert r.returncode != 0 and "permission denied" in r.stderr


def test_service_role_reads_and_the_commit_rpc_still_works(sql):
    assert sql(_as("service_role", "select count(*) from keystone_dashboard_data")).splitlines()[-1] == "2"
    assert sql(_as("service_role", "select count(*) from keystone_analysis_versions")).splitlines()[-1] == "1"
    # Migration 29's writer (SECURITY DEFINER, service_role only) is unaffected.
    sql((MIG / "29_atomic_dashboard_writes.sql").read_text())
    out = sql(_as("service_role", "select keystone_commit_blobs("
                  "'[{\"data_type\":\"integrity_metrics\",\"payload\":{}}]', '[]', '{}')"))
    assert '"ok": true' in out
    assert sql("select count(*) from keystone_dashboard_data") == "3"
