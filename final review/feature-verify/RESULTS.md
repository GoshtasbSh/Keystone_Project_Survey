# Feature verification results — 2026-06-04

Local server: custom venv server on :3002 (vercel dev's Python toolchain was
broken in this env — see NOTES). Live DB: keystore_Field (ioejtwseqsgidefkeyji).
All test artifacts prefixed `test_`; no existing row modified.

## Feature 1 — survey match auto-flips a non-completed pin to Completed  ✅ PASS
Method (data-safe, real matcher): `f1_scoped_flip_test.py`
- Read ONE existing IAQ response from cache (read-only): resp `R_5LnXMcaezhqW28F` @ (-82.017276, 29.783271). 75 IAQ features in cache.
- Added a `test_` field point **Inaccessible** at that coordinate (id `64d0a8ef-…`).
- Ran the production matcher `_apply_iaq_to_field_features([pt], iaq_feats, None)`.
- Result: `upgraded=1`, status **Inaccessible → Completed**, `has_iaq_survey=true`.
- Persisted ONLY that point's status (mirrors `api/upload.py`). DB confirmed `Completed`.
- IAQ cache never rewritten; no other pin touched.

## Feature 2 — hide gone/inactive people from team & chat  ✅ PASS
DB layer (live RPC checks):
- `active_member_ids()` / `active_guests()` execute; with no recent logins → 0 active members, 5 total.
- `active_guests()` returns only `test_active_guest`; the expired `test_gone_guest` is excluded. ✅

Admin view (signed in as test@test.com, admin) — `f2-01-admin-roster.png`:
- Active section: me (test@test.com) shown active.
- "Inactive (last 24h+)" section (admin-only) lists the 5 real members with "last seen 43d/30d/7d/41d ago". ✅
- 0 console errors.

Member view (signed in as test_member_qa, non-admin) — `f2-02-member-dashboard.png`, `f2-03-member-team-active-only.png`:
- Admin Team modal button hidden for member. ✅
- Analysis "Team" panel shows ONLY active people: `test_member_qa` (you) + `test2`/test@test.com (active admin). "2 surveyors". ✅
- The 4 inactive admins are NOT shown; no last-seen timestamps leaked to the member. ✅
- Session has 322 points loaded (incl. the gone-guest pin), yet NO `test_gone_guest` row in the team panel → filtered by activeGuestNames while its pin stays on the map (authorship preserved). ✅

Guest field-PWA view — verified by component, not full E2E (claiming a guest would
require touching today's operational invite code → avoided for data-safety):
- `_filter_presence_active()` unit-tested (4 cases, tests/test_guest_visibility.py).
- `api/guest.py _team_list()` calls `active_member_ids()` (live-verified) then
  `_filter_presence_active(presence, ids)` — same rule as desktop, enforced server-side.

## Authorship preservation  ✅
- Gone guest `test_gone_guest` removed from team panel but its `No Answer` pin remains
  on the map attributed to it (point count 321→322).

## IAQ cache integrity  ✅
- Only read via `load_cached('iaq_survey')`; never written. (No upload/daily-refresh run.)
