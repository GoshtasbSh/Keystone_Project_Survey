-- ════════════════════════════════════════════════════════════════════════
-- 24_active_roster_visibility.sql  (additive — defines NO new tables,
-- alters/drops NOTHING). Three read-only SECURITY DEFINER RPCs that power
-- "active-only" visibility for the team roster, team-activity panel, and
-- the field/guest team view.
--
--   active window (members/admins) = last_sign_in_at within 24h
--   active window (guests)         = expires_at > now() AND revoked_at IS NULL
-- The 24h window lives ONLY here, so the app cannot drift from it.
-- ════════════════════════════════════════════════════════════════════════

-- ── 1. list_roster() — role-aware roster for the desktop Team modal ──────
-- Non-admin members: only ACTIVE members/admins, with last_sign_in_at NULLed
--   out (do not leak activity timestamps to non-admins).
-- Admins: EVERY member/admin, with `active` flag and real last_sign_in_at
--   so the UI can show "last seen" for inactive teammates.
CREATE OR REPLACE FUNCTION list_roster()
RETURNS TABLE(
  id              UUID,
  email           TEXT,
  role            TEXT,
  joined_at       TIMESTAMPTZ,
  active          BOOLEAN,
  last_sign_in_at TIMESTAMPTZ
) LANGUAGE SQL STABLE SECURITY DEFINER
SET search_path = public, pg_temp
AS $$
  SELECT tm.id,
         u.email::text,
         tm.role,
         tm.joined_at,
         COALESCE(u.last_sign_in_at >= now() - interval '24 hours', false) AS active,
         CASE WHEN is_admin(auth.uid()) THEN u.last_sign_in_at ELSE NULL END AS last_sign_in_at
    FROM team_members tm
    JOIN auth.users   u ON u.id = tm.id
   WHERE EXISTS (SELECT 1 FROM team_members me WHERE me.id = auth.uid())
     AND (
       is_admin(auth.uid())
       OR COALESCE(u.last_sign_in_at >= now() - interval '24 hours', false)
     )
   ORDER BY (tm.role = 'admin') DESC,
            COALESCE(u.last_sign_in_at >= now() - interval '24 hours', false) DESC,
            tm.joined_at;
$$;

REVOKE ALL ON FUNCTION list_roster() FROM public;
GRANT EXECUTE ON FUNCTION list_roster() TO authenticated;

-- ── 2. active_member_ids() — UUID set of currently-active members ────────
-- No auth.uid() dependency, so the guest API (service_role, no JWT) can
-- call it. Returns ONLY ids (no PII).
CREATE OR REPLACE FUNCTION active_member_ids()
RETURNS TABLE(id UUID)
LANGUAGE SQL STABLE SECURITY DEFINER
SET search_path = public, pg_temp
AS $$
  SELECT tm.id
    FROM team_members tm
    JOIN auth.users   u ON u.id = tm.id
   WHERE u.last_sign_in_at >= now() - interval '24 hours';
$$;

REVOKE ALL ON FUNCTION active_member_ids() FROM public;
GRANT EXECUTE ON FUNCTION active_member_ids() TO authenticated, service_role;

-- ── 3. active_guests() — id + name of currently-active guest sessions ────
CREATE OR REPLACE FUNCTION active_guests()
RETURNS TABLE(id UUID, name TEXT)
LANGUAGE SQL STABLE SECURITY DEFINER
SET search_path = public, pg_temp
AS $$
  SELECT g.id, g.name
    FROM field_guest_sessions g
   WHERE g.revoked_at IS NULL
     AND g.expires_at > now();
$$;

REVOKE ALL ON FUNCTION active_guests() FROM public;
GRANT EXECUTE ON FUNCTION active_guests() TO authenticated, service_role;
