# Active-Only Visibility for Team & Chat — Design

**Date:** 2026-06-04
**Status:** Approved (pending written-spec review)
**Scope:** Filter the team roster, team-activity presence, and chat participant visibility so that only people who are "around now" are shown, with role-based rules. Expired guests stay attributed as point authors but disappear from team/chat.

---

## 1. Problem

Today nothing filters out people who are no longer around:

- `list_team()` / `list_all_signups()` return **every** member/admin regardless of when they last signed in.
- The desktop team-activity panel (`renderPerUserPanel()`) and the field/guest `team-list` endpoint return **all** `user_presence` rows.
- Expired/revoked guest sessions still surface anywhere their presence or messages appear.

The user wants team + chat to reflect **who is currently in the app**, while never losing the record of **who authored each point**.

## 2. Definitions

- **Member/admin `active`** ⇔ `auth.users.last_sign_in_at >= now() - interval '24 hours'`. Otherwise **inactive**.
- **Guest `active`** ⇔ `expires_at > now() AND revoked_at IS NULL`. Otherwise **gone**.
- **Authorship** = `field_survey_points.collector_id` / `collector_name` / `guest_session_id`. **Never modified by this feature.** Map pins and popups always show the original author.

## 3. Visibility Rule (approved)

| Viewer | active members | active admins | inactive members/admins | gone guests |
|---|---|---|---|---|
| **Guest** | shown | shown | hidden | hidden |
| **Member** | shown | shown | hidden | hidden |
| **Admin** | shown | shown | shown + `last_sign_in_at` displayed | hidden from team/chat list; still in the admin-only guest-session audit panel |

Notes captured from the user:
- **Active admins are visible to everyone, including guests.**
- **Inactive admins/members are visible only to admins**, who see each one's last-sign-in time so they know when other admins/members were last around.
- Guests never see inactive members/admins or gone guests.

## 4. Chat Behavior (approved)

Chat is a per-day message log with no separate participant roster. When a guest goes (expires), **their already-sent messages remain in today's chat as history** — non-destructive. They simply stop appearing in any team/online roster. No message is hidden or deleted by this feature.

## 5. Surfaces & Changes

### 5.1 Database — new migration `24_active_roster_visibility.sql`
- Add a `SECURITY DEFINER STABLE` RPC `list_roster()`:
  - Reads `team_members` JOIN `auth.users` (so it can see `last_sign_in_at`, which RLS otherwise hides).
  - Computes `active := (u.last_sign_in_at >= now() - interval '24 hours')`.
  - **If caller is admin** (`is_admin(auth.uid())`): return all members/admins with `active` flag and `last_sign_in_at` (so the UI can show last-sign-in for inactive rows).
  - **If caller is a non-admin member**: return only rows where `active = true`, and **do not** expose `last_sign_in_at` (return `NULL`) to avoid leaking activity timestamps to non-admins.
  - Caller must be a team member (`EXISTS` check, same guard as `list_team`).
  - Columns: `id, email, role, joined_at, active, last_sign_in_at`.
- `REVOKE ALL ... FROM public; GRANT EXECUTE ... TO authenticated;`
- Leave `list_team()` and `list_all_signups()` **unchanged** so nothing else breaks; the desktop roster switches to `list_roster()`.
- Idempotent (`CREATE OR REPLACE`, guarded), additive only. No data writes, no schema drops.

### 5.2 Desktop dashboard — `static/js/dashboard.js` (+ `static/index.html` if markup needed)
- `loadTeamRoster()` calls `list_roster()` instead of `list_team` / `list_all_signups`.
  - Render **active** people normally.
  - For **admin viewers only**, render an "inactive / last seen" section showing each inactive member/admin with a humanized `last_sign_in_at`.
  - Non-admin viewers get only the active list.
- `renderPerUserPanel()` (team-activity tab): the live **presence** portion shows only active people. Point **counts/contributions stay** for everyone who collected points (authorship), but a gone guest / inactive member is not shown as "present/online."
- Map points, popups, and per-point author labels: **no change**.

### 5.3 Field PWA + guest API — `api/guest.py`
- `_team_list()` filters the returned `presence` array to **active** members/admins before responding. (Guests are non-admin viewers → active-only, no inactive rows.)
- **Consistency with the desktop rule:** "active" must mean the same thing in both places — `last_sign_in_at` within 24h. The guest endpoint already uses a service-role client, so it will resolve active membership by reading `auth.users.last_sign_in_at` (service role bypasses RLS) and keep only `user_presence` rows whose `user_id` is active. A single shared constant `ACTIVE_WINDOW_HOURS = 24` backs both the SQL RPC and this code path so they cannot drift.
- `points` array still returned in full for the map (authorship preserved).
- `_chat_list()` / `_chat_poll()`: **unchanged** (history preserved per §4).
- Apply the same active-window constant server-side so the client cannot bypass it.

## 6. Out of Scope (YAGNI)
- No change to how guests are created, how sessions expire, or the sliding-TTL heartbeat.
- No change to chat storage, message retention, or the daily chat window.
- No change to point authorship columns or RLS on `field_survey_points`.
- No new presence heartbeat for members (we reuse `last_sign_in_at`).

## 7. Testing
- **Unit/SQL:** verify `list_roster()` returns active-only for a non-admin caller and active+inactive for an admin caller, using `test_`-prefixed rows; assert non-admins get `last_sign_in_at = NULL`.
- **Live (data-safe):** on port 3002 against prod, sign in as a `test_` admin, confirm an inactive `test_` member appears only for the admin view and not for a member/guest view; confirm a gone `test_` guest is absent from team/chat but its `test_` point still shows on the map with the guest's name. Remove all `test_` artifacts afterward and report them.
- All test artifacts prefixed `test_`; no existing row touched.

## 8. Data-Safety Constraints (hard)
- Never modify or delete any existing user, point, survey row, guest session, or chat message.
- Everything created for testing is `test_`-prefixed and reported for cleanup.
- Migration 24 is additive (one new function); it does not alter or drop existing objects.
