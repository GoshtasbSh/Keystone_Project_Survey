-- ════════════════════════════════════════════════════════════════════
-- 27. Optional address on a field pin.
--
-- Additive only. No existing row is modified; the new column is
-- nullable with no default backfill, so every historical row keeps
-- reading exactly as it does today (NULL).
--
-- Motivation: surveyors currently have no way to record a known street
-- address on a field pin — Carey had to write "6409 Beloit" into the
-- free-text notes field, which nothing else reads or displays. This
-- gives the add-point flow a real, optional address field instead.
--
-- NOTE (2026-08-10): this migration is authored but intentionally NOT
-- applied to production as part of this change. Every code path that
-- writes or selects `address` on field_survey_points must therefore
-- tolerate the column not existing yet — see the try/enriched-then-
-- fallback pattern in api/upload.py (_load_all_field_features) and
-- api/guest.py (_add_point), mirroring migration 26's
-- _insert_version_row fallback.
-- ════════════════════════════════════════════════════════════════════

ALTER TABLE public.field_survey_points
  ADD COLUMN IF NOT EXISTS address text;
