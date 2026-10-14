-- ════════════════════════════════════════════════════════════════════
-- 30. Deleting a field pin removes its copy from the dashboard blob.
--
-- Field pins are deleted straight from the field app (supabase-js
-- .delete(), RLS-gated) or via /api/guest — no server code runs, so the
-- copy inside keystone_dashboard_data.community_contact used to live on
-- until the next upload (audit 2026-10-13: 28 deleted test pins were
-- still drawn and counted). This AFTER DELETE trigger prunes the copy in
-- the same transaction as the delete.
--
-- Safety:
--   * Only removes features with source='field' AND field_point_id =
--     the deleted id. Contacts are never touched (COALESCE: a contact's
--     NULL source must not turn the filter NULL and drop it).
--   * A field feature that still carries a non-field entry in
--     coincident_contacts (a CSV contact swallowed by the pre-fix cron
--     dedup) is LEFT in place; the Python rebuild
--     (api/_field_layer.rebuild_field_layer) restores that contact and
--     drops the pin on the next refresh/upload.
--   * Takes the same advisory lock as keystone_commit_blobs() (migration 29).
--   * Never blocks the delete: a blob whose `features` is not an array is
--     left alone, and any other error in the prune is logged as a WARNING
--     and swallowed (the next refresh/upload rebuild removes the pin).
--
-- Additive and idempotent: one function + one trigger, no row is
-- modified by applying this file.
-- ════════════════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION public._kd_prune_deleted_field_pin()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  BEGIN
    PERFORM pg_advisory_xact_lock(hashtext('keystone_dashboard_data_writers'));
    UPDATE keystone_dashboard_data d
       SET payload = jsonb_set(
             d.payload, '{features}',
             COALESCE((
               SELECT jsonb_agg(f ORDER BY ord)
                 FROM jsonb_array_elements(
                        CASE WHEN jsonb_typeof(d.payload->'features') = 'array'
                             THEN d.payload->'features' ELSE '[]'::jsonb END)
                      WITH ORDINALITY AS t(f, ord)
                WHERE NOT (
                      COALESCE(f->'properties'->>'source', '') = 'field'
                  AND COALESCE(f->'properties'->>'field_point_id', '') = OLD.id::text
                  AND NOT EXISTS (
                        SELECT 1
                          FROM jsonb_array_elements(
                                 CASE WHEN jsonb_typeof(f->'properties'->'coincident_contacts') = 'array'
                                      THEN f->'properties'->'coincident_contacts'
                                      ELSE '[]'::jsonb END) AS c(e)
                         WHERE COALESCE(e->>'source', '') <> 'field'))
             ), '[]'::jsonb))
     WHERE d.data_type = 'community_contact'
       AND jsonb_typeof(d.payload->'features') = 'array'
       AND EXISTS (
             SELECT 1
               FROM jsonb_array_elements(
                      CASE WHEN jsonb_typeof(d.payload->'features') = 'array'
                           THEN d.payload->'features' ELSE '[]'::jsonb END) AS x(f)
              WHERE COALESCE(f->'properties'->>'source', '') = 'field'
                AND f->'properties'->>'field_point_id' = OLD.id::text);
  EXCEPTION WHEN OTHERS THEN
    RAISE WARNING '_kd_prune_deleted_field_pin(%): % (%) - blob copy left for the next rebuild',
      OLD.id, SQLERRM, SQLSTATE;
  END;
  RETURN OLD;
END;
$$;

REVOKE ALL ON FUNCTION public._kd_prune_deleted_field_pin() FROM PUBLIC;
REVOKE ALL ON FUNCTION public._kd_prune_deleted_field_pin() FROM anon, authenticated;

DROP TRIGGER IF EXISTS trg_fsp_prune_blob_on_delete ON public.field_survey_points;
CREATE TRIGGER trg_fsp_prune_blob_on_delete
  AFTER DELETE ON public.field_survey_points
  FOR EACH ROW EXECUTE FUNCTION public._kd_prune_deleted_field_pin();
