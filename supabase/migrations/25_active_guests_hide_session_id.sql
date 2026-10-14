-- Migration 25: close N1 (HIGH). active_guests() over-exposed the guest
-- session id.
--
-- Problem: migration 24's active_guests() returned field_guest_sessions.id
-- (the guest session UUID). That id is the ONLY bearer credential for the
-- guest API (POST /api/guest takes session_id in the body with no auth
-- header). Any caller could therefore list live guests' session ids and
-- then delete or edit their field points, or pull their export. Supabase
-- also grants EXECUTE on new public functions to `anon` by default, and
-- REVOKE ... FROM public does not remove that grant. A live probe on
-- 2026-10-13 confirmed anon gets 200 from rpc/active_guests. The dashboard
-- only reads the guest *name* (static/js/dashboard.js loadActiveSets()),
-- never the id.
--
-- Fix: return only `name`, and let only authenticated + service_role call it.
--
-- Why DROP first: changing RETURNS TABLE(id, name) to TABLE(name) is a
-- return-type change. CREATE OR REPLACE rejects it with 42P13, which is why
-- the first attempt failed. BEGIN/COMMIT keeps the drop and the create
-- atomic, so no caller ever sees the function missing.
-- Data safety: no table or row is touched.

BEGIN;

DROP FUNCTION IF EXISTS public.active_guests();

CREATE FUNCTION public.active_guests()
RETURNS TABLE(name TEXT)
LANGUAGE SQL STABLE SECURITY DEFINER
SET search_path = public, pg_temp
AS $$
  SELECT g.name
    FROM field_guest_sessions g
   WHERE g.revoked_at IS NULL
     AND g.expires_at > now();
$$;

-- Must come AFTER the CREATE: Supabase's default privileges re-grant anon
-- on every newly created function.
REVOKE ALL ON FUNCTION public.active_guests() FROM public;
REVOKE ALL ON FUNCTION public.active_guests() FROM anon;
GRANT EXECUTE ON FUNCTION public.active_guests() TO authenticated, service_role;

COMMIT;

NOTIFY pgrst, 'reload schema';
