-- ════════════════════════════════════════════════════════════════════════
-- 28_dashboard_data_rls_lockdown.sql
--
-- P1 (audit 2026-10-13): the public anon key, which /api/config serves to
-- every browser, could read EVERY keystone_dashboard_data row through
-- PostgREST. That included the full iaq_survey blob: 114 households at
-- parcel coordinates with health, employment and law-enforcement answers.
-- Live probe: GET /rest/v1/keystone_dashboard_data?select=data_type with
-- the anon key returned HTTP 200 and 6 rows. Migration 17 meant the table
-- to be team-only, so either RLS was switched off or an extra policy was
-- added outside the repo. This migration fixes both cases.
--
-- Who still reads these tables after this migration:
--   * every /api/* function: service_role, which bypasses RLS, so unchanged
--   * static/js/dashboard.js renderDataSummary(): an authenticated team
--     member, allowed by the policy below
--   * nobody reads them as anon, and nobody writes them from a client
--
-- Also closes anon EXECUTE on two team-only RPCs (Supabase's default
-- privileges grant anon EXECUTE on new public functions).
--
-- Data safety: changes permissions and policies only. No row is touched.
-- ════════════════════════════════════════════════════════════════════════

BEGIN;

-- ── 1. keystone_dashboard_data ─────────────────────────────────────────
ALTER TABLE public.keystone_dashboard_data ENABLE ROW LEVEL SECURITY;

DO $$
DECLARE p record;
BEGIN
  FOR p IN
    SELECT policyname FROM pg_policies WHERE schemaname = 'public' AND tablename = 'keystone_dashboard_data'
  LOOP
    EXECUTE format('DROP POLICY %I ON public.keystone_dashboard_data', p.policyname);
  END LOOP;
END $$;

CREATE POLICY "Team members read dashboard data"
  ON public.keystone_dashboard_data FOR SELECT TO authenticated
  USING (public.is_team_member((select auth.uid())));

REVOKE ALL ON TABLE public.keystone_dashboard_data FROM anon, public;
REVOKE INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER
  ON TABLE public.keystone_dashboard_data FROM authenticated;
GRANT SELECT ON TABLE public.keystone_dashboard_data TO authenticated;
GRANT ALL    ON TABLE public.keystone_dashboard_data TO service_role;

-- ── 2. keystone_analysis_versions (each row holds a full payload snapshot)
ALTER TABLE public.keystone_analysis_versions ENABLE ROW LEVEL SECURITY;

DO $$
DECLARE p record;
BEGIN
  FOR p IN
    SELECT policyname FROM pg_policies WHERE schemaname = 'public' AND tablename = 'keystone_analysis_versions'
  LOOP
    EXECUTE format('DROP POLICY %I ON public.keystone_analysis_versions', p.policyname);
  END LOOP;
END $$;

CREATE POLICY "Team members read analysis versions"
  ON public.keystone_analysis_versions FOR SELECT TO authenticated
  USING (public.is_team_member((select auth.uid())));

REVOKE ALL ON TABLE public.keystone_analysis_versions FROM anon, public;
REVOKE INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER
  ON TABLE public.keystone_analysis_versions FROM authenticated;
GRANT SELECT ON TABLE public.keystone_analysis_versions TO authenticated;
GRANT ALL    ON TABLE public.keystone_analysis_versions TO service_role;

-- ── 3. Team-only RPCs that anon could still call (live probe: 200) ─────
REVOKE ALL ON FUNCTION public.active_member_ids() FROM anon, public;
GRANT EXECUTE ON FUNCTION public.active_member_ids() TO authenticated, service_role;

REVOKE ALL ON FUNCTION public.list_roster() FROM anon, public;
GRANT EXECUTE ON FUNCTION public.list_roster() TO authenticated;

-- ── 4. Self-check: any failure aborts and rolls back the whole migration
DO $$
DECLARE t text;
BEGIN
  FOREACH t IN ARRAY ARRAY['keystone_dashboard_data', 'keystone_analysis_versions'] LOOP
    IF NOT (SELECT c.relrowsecurity
              FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
             WHERE n.nspname = 'public' AND c.relname = t) THEN
      RAISE EXCEPTION 'lockdown failed: RLS still disabled on %', t;
    END IF;
    IF has_table_privilege('anon', format('public.%I', t), 'SELECT') THEN
      RAISE EXCEPTION 'lockdown failed: anon still has SELECT on %', t;
    END IF;
    IF EXISTS (SELECT 1 FROM pg_policies
                WHERE schemaname = 'public' AND tablename = t
                  AND (roles && ARRAY['anon', 'public']::name[] OR qual = 'true')) THEN
      RAISE EXCEPTION 'lockdown failed: an anon/public or always-true (qual = true) policy remains on %', t;
    END IF;
  END LOOP;
  IF has_function_privilege('anon', 'public.active_member_ids()', 'EXECUTE')
     OR has_function_privilege('anon', 'public.list_roster()', 'EXECUTE')
     OR has_function_privilege('anon', 'public.active_guests()', 'EXECUTE') THEN
    RAISE EXCEPTION 'lockdown failed: anon can still EXECUTE a team-only RPC (apply migration 25 first)';
  END IF;
END $$;

COMMIT;

NOTIFY pgrst, 'reload schema';
