-- ════════════════════════════════════════════════════════════════════
-- 26. Upload audit trail
--
-- Additive only. No existing row is modified; every new column is
-- nullable with no default backfill, so historical rows keep reading
-- exactly as they do today.
--
-- Motivation: the 2026-05-06 incident (a 60-response `V2_test` export
-- replaced a 75-response real export and hid 15 households for 75 days)
-- cannot be attributed to anyone, because the versions table records
-- no uploader and no source row counts.
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

CREATE INDEX IF NOT EXISTS idx_kav_uploaded_by
  ON public.keystone_analysis_versions(uploaded_by_user_id);
