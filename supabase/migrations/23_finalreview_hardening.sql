-- ════════════════════════════════════════════════════════════════════════
-- 23. Final-review security hardening (ADDITIVE / NON-DESTRUCTIVE)
--
-- DATA-SAFE: this migration does NOT DROP any table, DELETE any row, or
-- UPDATE any business data. It only:
--   • S6  — recreates create_member_invite() to mint tokens from a CSPRNG
--           (gen_random_uuid, OS-seeded) instead of md5(random()). Existing
--           pending invites keep their tokens; only NEW invites change.
--   • SEC7 — restricts user_presence SELECT to team members (was USING(true),
--           which let any authenticated signup enumerate presence/names).
--
-- Items intentionally NOT included (need coordinated app changes / product
-- decisions — see final review/06_bugs_and_fixes/REGISTER.md):
--   • S1  guest-write DB ownership backstop (needs app GUC + trigger)
--   • S4  team-chat-attachments bucket → private (needs client signed URLs)
--   • S5  legacy daily-code claim_membership (STILL live in login.html — do
--         not revoke; strengthen the code instead)
--   • D1  fsp→community_contacts mirror (currently benign no-op; re-enabling
--         creates rows wiped by the next CSV upload — confirm intent first)
-- ════════════════════════════════════════════════════════════════════════

-- ── S6: CSPRNG invite tokens ───────────────────────────────────────────
CREATE OR REPLACE FUNCTION public.create_member_invite(p_email text)
 RETURNS jsonb
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public', 'pg_temp'
AS $function$
DECLARE
  v_uid     UUID := auth.uid();
  v_email   TEXT := lower(trim(p_email));
  v_token   TEXT;
  v_id      UUID;
  v_expires TIMESTAMPTZ;
BEGIN
  IF NOT is_admin(v_uid) THEN
    RETURN jsonb_build_object('ok', false, 'error', 'Admin role required');
  END IF;
  IF v_email IS NULL OR v_email !~ '^[^@\s]+@[^@\s]+\.[^@\s]+$' THEN
    RETURN jsonb_build_object('ok', false, 'error', 'Invalid email');
  END IF;
  -- CSPRNG token: gen_random_uuid() is core PG (no pgcrypto/search_path
  -- quirks) and OS-CSPRNG seeded. Two UUIDs → 64 hex; keep 48 for opacity.
  v_token := substr(
    replace(gen_random_uuid()::text, '-', '') ||
    replace(gen_random_uuid()::text, '-', ''),
    1, 48
  );
  v_expires := now() + INTERVAL '14 days';
  INSERT INTO member_invites (email, token, invited_by, expires_at, status)
  VALUES (v_email, v_token, v_uid, v_expires, 'pending')
  RETURNING id INTO v_id;
  RETURN jsonb_build_object(
    'ok', true, 'id', v_id, 'email', v_email,
    'token', v_token, 'expires_at', v_expires
  );
END;
$function$;

-- ── SEC7: presence readable by team members only ───────────────────────
DROP POLICY IF EXISTS "Read all presence" ON public.user_presence;
CREATE POLICY "Team members read presence"
  ON public.user_presence FOR SELECT
  TO authenticated
  USING (public.is_team_member((select auth.uid())));
