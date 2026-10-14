-- ════════════════════════════════════════════════════════════════════
-- 29. Atomic dashboard writes + compare-and-set for the cron.
--
-- Additive only: one new function, plus the migration-26 audit columns
-- re-stated with IF NOT EXISTS so the function below can reference them
-- even on a project where 26 was never applied. No existing row is
-- modified by this migration.
--
-- keystone_commit_blobs() performs every keystone_dashboard_data upsert
-- and every keystone_analysis_versions insert of ONE upload / refresh /
-- restore inside a single transaction, so a failure part-way through can
-- no longer leave iaq_survey replaced while community_contact / analysis
-- still hold the previous data (audit 2026-10-13, finding F8).
--
-- p_expected = {"<data_type>": "<updated_at read earlier>" | null}. When
-- given, the write is refused (SQLSTATE 40001, message starts with
-- 'keystone_stale_write') if that row's updated_at changed since the
-- caller read it — this closes the midnight cron vs. upload overwrite
-- race (audit DEP-8). null means "the row did not exist when I read it".
--
-- All writers (this function and the migration-30 delete trigger) take
-- the same transaction-scoped advisory lock, so they serialise.
-- ════════════════════════════════════════════════════════════════════

ALTER TABLE public.keystone_analysis_versions
  ADD COLUMN IF NOT EXISTS uploaded_by_user_id  uuid REFERENCES auth.users(id) ON DELETE SET NULL,
  ADD COLUMN IF NOT EXISTS uploaded_by_email    text,
  ADD COLUMN IF NOT EXISTS source_filename      text,
  ADD COLUMN IF NOT EXISTS source_row_count     integer,
  ADD COLUMN IF NOT EXISTS geocoded_count       integer,
  ADD COLUMN IF NOT EXISTS failed_geocodes      jsonb,
  ADD COLUMN IF NOT EXISTS dropped_response_ids jsonb,
  ADD COLUMN IF NOT EXISTS forced               boolean;

CREATE OR REPLACE FUNCTION public.keystone_commit_blobs(
  p_blobs    jsonb,
  p_versions jsonb DEFAULT '[]'::jsonb,
  p_expected jsonb DEFAULT '{}'::jsonb
) RETURNS jsonb
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  k        text;
  v        jsonb;
  cur      timestamptz;
  ids      integer[] := '{}';
  new_id   integer;
BEGIN
  PERFORM pg_advisory_xact_lock(hashtext('keystone_dashboard_data_writers'));

  FOR k, v IN SELECT key, value FROM jsonb_each(COALESCE(p_expected, '{}'::jsonb)) LOOP
    SELECT updated_at INTO cur FROM keystone_dashboard_data WHERE data_type = k;
    IF cur IS DISTINCT FROM (CASE WHEN jsonb_typeof(v) = 'null' THEN NULL
                                  ELSE (v #>> '{}')::timestamptz END) THEN
      RAISE EXCEPTION 'keystone_stale_write: % changed since it was read', k
        USING ERRCODE = '40001';
    END IF;
  END LOOP;

  FOR v IN SELECT value FROM jsonb_array_elements(COALESCE(p_blobs, '[]'::jsonb)) LOOP
    IF COALESCE(v->>'data_type', '') = '' OR v->'payload' IS NULL
       OR jsonb_typeof(v->'payload') = 'null' THEN
      RAISE EXCEPTION 'keystone_commit_blobs: blob without data_type/payload';
    END IF;
    INSERT INTO keystone_dashboard_data (data_type, payload)
    VALUES (v->>'data_type', v->'payload')
    ON CONFLICT (data_type) DO UPDATE SET payload = EXCLUDED.payload;
  END LOOP;

  FOR v IN SELECT value FROM jsonb_array_elements(COALESCE(p_versions, '[]'::jsonb)) LOOP
    INSERT INTO keystone_analysis_versions (
      data_type, payload, label, n_points,
      uploaded_by_user_id, uploaded_by_email, source_filename,
      source_row_count, geocoded_count, failed_geocodes,
      dropped_response_ids, forced)
    VALUES (
      v->>'data_type', v->'payload', v->>'label',
      COALESCE((v->>'n_points')::integer, 0),
      NULLIF(v->>'uploaded_by_user_id', '')::uuid,
      v->>'uploaded_by_email', v->>'source_filename',
      (v->>'source_row_count')::integer, (v->>'geocoded_count')::integer,
      v->'failed_geocodes', v->'dropped_response_ids',
      (v->>'forced')::boolean)
    RETURNING id INTO new_id;
    ids := ids || new_id;
  END LOOP;

  RETURN jsonb_build_object('ok', true, 'version_ids', to_jsonb(ids));
END;
$$;

REVOKE ALL ON FUNCTION public.keystone_commit_blobs(jsonb, jsonb, jsonb) FROM PUBLIC;
REVOKE ALL ON FUNCTION public.keystone_commit_blobs(jsonb, jsonb, jsonb) FROM anon, authenticated;
GRANT EXECUTE ON FUNCTION public.keystone_commit_blobs(jsonb, jsonb, jsonb) TO service_role;
