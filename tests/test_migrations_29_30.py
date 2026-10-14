"""Migrations 29 (keystone_commit_blobs: one-transaction writes with
compare-and-set) and 30 (deleting a field pin prunes its blob copy),
exercised against a throwaway local PostgreSQL. Skipped when the
PostgreSQL server binaries are not installed. Never touches Supabase."""
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

PIN_A = "11111111-1111-1111-1111-111111111111"   # plain pin -> pruned
PIN_B = "22222222-2222-2222-2222-222222222222"   # pin holding a swallowed contact -> kept
PIN_C = "33333333-3333-3333-3333-333333333333"   # untouched pin


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

    # Supabase stand-ins, then the real migrations under test.
    run("CREATE ROLE anon; CREATE ROLE authenticated; CREATE ROLE service_role;"
        "CREATE SCHEMA auth; CREATE TABLE auth.users(id uuid primary key);")
    run((MIG / "02_keystone_dashboard_data.sql").read_text())
    run((MIG / "03_analysis_versions.sql").read_text())
    run("CREATE TABLE field_survey_points (id uuid primary key default gen_random_uuid(),"
        " lat double precision not null, lon double precision not null, status text,"
        " collector_name text, collected_at timestamptz not null default now());")
    for name in ("29_atomic_dashboard_writes.sql", "30_field_pin_delete_prunes_blob.sql"):
        if (MIG / name).exists():
            run((MIG / name).read_text())
            run((MIG / name).read_text())       # idempotent: safe to re-run
    yield run
    subprocess.run([BINS["pg_ctl"], "-D", str(data), "-m", "immediate", "stop"],
                   capture_output=True)
    tmp.cleanup()


def _stamp(sql, data_type):
    return sql(f"select coalesce(to_jsonb(updated_at)::text, 'null') from keystone_dashboard_data "
               f"where data_type = '{data_type}'") or "null"


def test_commit_writes_blobs_and_versions_together(sql):
    out = sql("""select keystone_commit_blobs(
        '[{"data_type":"iaq_survey","payload":{"geojson":{"features":[]}}},
          {"data_type":"community_contact","payload":{"type":"FeatureCollection","features":[]}}]',
        '[{"data_type":"iaq_survey","payload":{},"label":"Vercel Upload","n_points":114,
           "source_filename":"oct.csv","forced":false,"dropped_response_ids":[]}]',
        '{}')""")
    assert '"ok": true' in out
    assert sql("select count(*) from keystone_dashboard_data") == "2"
    assert sql("select source_filename || '|' || n_points from keystone_analysis_versions") == "oct.csv|114"


def test_a_failing_version_row_rolls_back_the_blobs(sql):
    before = sql("select payload::text from keystone_dashboard_data where data_type='iaq_survey'")
    r = sql("""select keystone_commit_blobs(
        '[{"data_type":"iaq_survey","payload":{"geojson":{"features":[1]}}}]',
        '[{"data_type":null,"payload":{},"label":"broken"}]', '{}')""", ok=False)
    assert r.returncode != 0
    assert sql("select payload::text from keystone_dashboard_data where data_type='iaq_survey'") == before


def test_compare_and_set_refuses_a_stale_write(sql):
    stamp = _stamp(sql, "community_contact")
    sql("select keystone_commit_blobs('[{\"data_type\":\"community_contact\",\"payload\":{\"features\":[]}}]','[]','{}')")
    r = sql(f"""select keystone_commit_blobs('[{{"data_type":"analysis","payload":{{}}}}]', '[]',
              jsonb_build_object('community_contact', '{stamp}'::jsonb))""", ok=False)
    assert r.returncode != 0 and "keystone_stale_write" in r.stderr
    assert sql("select count(*) from keystone_dashboard_data where data_type='analysis'") == "0"
    fresh = _stamp(sql, "community_contact")
    sql(f"""select keystone_commit_blobs('[{{"data_type":"analysis","payload":{{}}}}]', '[]',
          jsonb_build_object('community_contact', '{fresh}'::jsonb))""")
    assert sql("select count(*) from keystone_dashboard_data where data_type='analysis'") == "1"


def test_null_stamp_means_row_must_still_be_absent(sql):
    r = sql("""select keystone_commit_blobs('[{"data_type":"x","payload":{}}]','[]',
              '{"community_contact": null}')""", ok=False)
    assert r.returncode != 0 and "keystone_stale_write" in r.stderr


def test_rpc_is_not_callable_by_anon_or_authenticated(sql):
    for role in ("anon", "authenticated"):
        r = sql(f"set role {role}; select keystone_commit_blobs('[]','[]','{{}}')", ok=False)
        assert r.returncode != 0 and "permission denied" in r.stderr


def test_deleting_a_pin_prunes_only_that_pin(sql):
    sql(f"insert into field_survey_points(id,lat,lon,status,collector_name) values "
        f"('{PIN_A}',29.7,-82.0,'Completed','test_a'),('{PIN_B}',29.7,-82.0,'Completed','test_b'),"
        f"('{PIN_C}',29.7,-82.0,'Completed','Carey Morford')")
    blob = ('{"type":"FeatureCollection","features":['
            '{"type":"Feature","geometry":{"type":"Point","coordinates":[-82,29.7]},'
            '"properties":{"address":"1 A St","status":"Completed"}},'
            f'{{"type":"Feature","geometry":{{"type":"Point","coordinates":[-82,29.7]}},'
            f'"properties":{{"source":"field","field_point_id":"{PIN_A}"}}}},'
            f'{{"type":"Feature","geometry":{{"type":"Point","coordinates":[-82,29.7]}},'
            f'"properties":{{"source":"field","field_point_id":"{PIN_B}",'
            f'"coincident_contacts":[{{"source":null,"status":"Left Info"}}]}}}},'
            f'{{"type":"Feature","geometry":{{"type":"Point","coordinates":[-82,29.7]}},'
            f'"properties":{{"source":"field","field_point_id":"{PIN_C}"}}}}]}}')
    sql(f"update keystone_dashboard_data set payload = '{blob}'::jsonb where data_type='community_contact'")
    sql(f"delete from field_survey_points where id in ('{PIN_A}','{PIN_B}')")
    ids = sql("select string_agg(coalesce(f->'properties'->>'field_point_id', f->'properties'->>'address'), ',' order by o) "
              "from keystone_dashboard_data, jsonb_array_elements(payload->'features') with ordinality as t(f,o) "
              "where data_type='community_contact'")
    # contact kept, A pruned, B kept (holds a swallowed contact), C untouched
    assert ids == f"1 A St,{PIN_B},{PIN_C}"


def test_deleting_an_unknown_pin_is_a_no_op(sql):
    before = _stamp(sql, "community_contact")
    sql("delete from field_survey_points where id = '99999999-9999-9999-9999-999999999999'")
    assert _stamp(sql, "community_contact") == before


def test_a_malformed_blob_never_blocks_a_pin_delete(sql):
    pin = "44444444-4444-4444-4444-444444444444"
    sql(f"insert into field_survey_points(id,lat,lon,status,collector_name) values "
        f"('{pin}',29.7,-82.0,'Completed','test_d')")
    sql("update keystone_dashboard_data set payload = '{\"features\":{\"not\":\"a list\"}}'::jsonb "
        "where data_type='community_contact'")
    before = _stamp(sql, "community_contact")
    sql(f"delete from field_survey_points where id = '{pin}'")
    assert sql(f"select count(*) from field_survey_points where id = '{pin}'") == "0"
    assert _stamp(sql, "community_contact") == before


def test_trigger_function_is_not_granted_to_anon_or_authenticated(sql):
    for role in ("anon", "authenticated"):
        assert sql(f"select has_function_privilege('{role}', "
                   f"'public._kd_prune_deleted_field_pin()', 'execute')") == "f"
