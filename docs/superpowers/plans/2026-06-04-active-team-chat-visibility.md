# Active-Only Visibility for Team & Chat — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Show only people who are "around now" in the team roster, team-activity panel, and the field/guest team view — with role-based rules — while never altering point authorship or chat history.

**Architecture:** One additive Supabase migration adds three `SECURITY DEFINER` read-only RPCs (`list_roster`, `active_member_ids`, `active_guests`). The desktop dashboard and the guest API consume them to filter people lists. No existing object is altered or dropped; no production row or cache is written by the feature. Feature 1 (Inaccessible→Completed flip) is verified, not modified, via a data-safe scoped run of the real matcher against one `test_` point.

**Tech Stack:** Supabase Postgres (PL/pgSQL + SQL functions, RLS), Python 3 Vercel serverless (`api/guest.py`, `api/_lib.py`), vanilla JS (`static/js/dashboard.js`), `vercel dev` on port 3002, Playwright MCP for screenshots, pytest/unittest.

**Hard data-safety rules (apply to EVERY task):**
- Never modify or delete any existing user, point, survey row, guest session, or chat message.
- Everything created for testing is prefixed `test_` and reported at the end for cleanup.
- The migration only `CREATE OR REPLACE`s new functions — it alters/drops nothing.
- Never trigger `/api/upload` or a full `/api/daily-refresh` against prod (they rewrite the IAQ cache and can re-flip real points).

**Definitions (single source of truth = SQL, 24h window lives only in SQL):**
- Member/admin **active** ⇔ `auth.users.last_sign_in_at >= now() - interval '24 hours'`.
- Guest **active** ⇔ `expires_at > now() AND revoked_at IS NULL`.

---

## File Structure

| File | Create/Modify | Responsibility |
|---|---|---|
| `supabase/migrations/24_active_roster_visibility.sql` | Create | The 3 read-only RPCs that define "active" and role-based visibility. |
| `api/guest.py` | Modify | Add pure `_filter_presence_active()` helper; wire `_team_list()` to filter presence to active members. |
| `tests/test_guest_visibility.py` | Create | Unit tests for the pure presence-filter helper. |
| `static/js/dashboard.js` | Modify | `loadActiveSets()` loader + globals; `loadTeamRoster()` → `list_roster`; `renderPerUserPanel()` active-only filter. |
| `final review/feature-verify/` | Create (artifacts) | Screenshots + scoped Feature 1 test script + cleanup notes. |

---

## Task 0: Bring up the app on port 3002 and sign in as a fresh `test_` admin

**Files:** none (environment + manual verification prerequisite).

- [ ] **Step 1: Confirm branch**

Run: `git -C "/Users/goshtasbshahriari/UF Dropbox/Goshtasb Shahriari Mehr/DTSC_Lab/KeyStone_project" branch --show-current`
Expected: `feat/active-team-chat-visibility`

- [ ] **Step 2: Start the dev server on 3002 (background)**

Run (background): `cd "/Users/goshtasbshahriari/UF Dropbox/Goshtasb Shahriari Mehr/DTSC_Lab/KeyStone_project" && vercel dev --listen 3002`
Expected: "Ready! Available at http://localhost:3002". (If `vercel dev` is unavailable, fall back to the project's documented local run; the api/* Python functions MUST be served for guest/upload endpoints.)

- [ ] **Step 3: Open the field/login surface and create a NEW test_ account**

Use Playwright MCP: navigate to `http://localhost:3002/login`. Sign up with email `test_keystone_qa@example.com`, password `Test1234!`. Screenshot to `final review/feature-verify/00-signup.png`.

- [ ] **Step 4: Promote the new account to admin (data-safe, additive)**

The first admin promotes others via `promote_by_email`. Using the existing admin `test@test.com / Test1234!` (already on record), sign in on the desktop `/dashboard`, open the Team modal, and "Make admin" on `test_keystone_qa@example.com`. (This adds one `team_members` row for the test_ user — additive, reported for cleanup. It does NOT touch real users.)
Expected: `test_keystone_qa@example.com` now shows role ADMIN.

- [ ] **Step 5: Record created test_ artifacts**

Append to `final review/feature-verify/CLEANUP.md`: the auth user `test_keystone_qa@example.com` and its `team_members` row (to be deleted at the end).

---

## Task 1: Migration 24 — the three read-only visibility RPCs

**Files:**
- Create: `supabase/migrations/24_active_roster_visibility.sql`

- [ ] **Step 1: Write the migration**

Create `supabase/migrations/24_active_roster_visibility.sql` with EXACTLY:

```sql
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
```

- [ ] **Step 2: Apply the migration to prod (additive, safe)**

Apply via the Supabase MCP `apply_migration` (name: `active_roster_visibility`) OR the Supabase SQL editor. Because every statement is `CREATE OR REPLACE FUNCTION` / `GRANT` / `REVOKE`, it adds functions only and cannot harm existing data.
Expected: success, no errors.

- [ ] **Step 3: Smoke-test each RPC read-only (no writes)**

Run via Supabase MCP `execute_sql` (read-only):
```sql
SELECT count(*) FROM active_member_ids();
SELECT count(*) FROM active_guests();
```
Expected: integer counts return without error (values depend on live state). Do NOT call `list_roster()` here without an auth context — it relies on `auth.uid()`; it is exercised in Task 6/7 through the signed-in browser.

- [ ] **Step 4: Commit**

```bash
git add supabase/migrations/24_active_roster_visibility.sql
git commit -m "feat(visibility): add active-only roster/guest/member RPCs (migration 24)"
```

---

## Task 2: Pure presence-filter helper in the guest API (TDD)

**Files:**
- Modify: `api/guest.py` (add a module-level pure helper near the other `_helpers`, ~after line 91)
- Test: `tests/test_guest_visibility.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_guest_visibility.py`:

```python
import unittest

from api.guest import _filter_presence_active


class FilterPresenceActiveTests(unittest.TestCase):
    def test_keeps_only_active_user_ids(self):
        presence = [
            {"user_id": "a", "display_name": "Ann",  "last_active_at": "x"},
            {"user_id": "b", "display_name": "Bob",  "last_active_at": "y"},
            {"user_id": "c", "display_name": "Cara", "last_active_at": "z"},
        ]
        active = ["a", "c"]
        out = _filter_presence_active(presence, active)
        self.assertEqual([p["user_id"] for p in out], ["a", "c"])

    def test_empty_active_set_hides_everyone(self):
        presence = [{"user_id": "a"}, {"user_id": "b"}]
        self.assertEqual(_filter_presence_active(presence, []), [])

    def test_handles_none_inputs(self):
        self.assertEqual(_filter_presence_active(None, None), [])
        self.assertEqual(_filter_presence_active([], ["a"]), [])

    def test_drops_rows_without_user_id(self):
        presence = [{"display_name": "ghost"}, {"user_id": "a"}]
        self.assertEqual(_filter_presence_active(presence, ["a"]),
                         [{"user_id": "a"}])
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `cd "/Users/goshtasbshahriari/UF Dropbox/Goshtasb Shahriari Mehr/DTSC_Lab/KeyStone_project" && python -m pytest tests/test_guest_visibility.py -v`
Expected: FAIL — `ImportError: cannot import name '_filter_presence_active'`.

- [ ] **Step 3: Implement the minimal helper**

In `api/guest.py`, immediately after `_name_safe()` (ends line 91), insert:

```python
def _filter_presence_active(presence, active_ids):
    """Return only presence rows whose user_id is in the active set.

    `active_ids` is the list of member UUIDs returned by the SQL RPC
    `active_member_ids()` (last_sign_in within 24h). Rows without a
    user_id, or for inactive/expired people, are dropped. Pure + side-
    effect-free so it is unit-testable without Supabase.
    """
    active = set(active_ids or [])
    return [p for p in (presence or [])
            if p.get("user_id") in active]
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `python -m pytest tests/test_guest_visibility.py -v`
Expected: PASS (4 passed).

- [ ] **Step 5: Commit**

```bash
git add api/guest.py tests/test_guest_visibility.py
git commit -m "feat(visibility): pure presence-active filter helper + tests"
```

---

## Task 3: Wire `_team_list()` to return active-only presence

**Files:**
- Modify: `api/guest.py` — `_team_list()` (currently lines 524–547)

- [ ] **Step 1: Replace the presence return with the filtered set**

In `api/guest.py`, change `_team_list()` so that after loading `presence`, it fetches the active member ids and filters. Replace the body from the `pres_q = ...` block through the `json_response(...)` with:

```python
    def _team_list(self, sb, sess: dict):
        try:
            pts_q = (sb.table("field_survey_points")
                       .select("collector_id,collector_name,status,collected_at")
                       .order("collected_at", desc=True)
                       .limit(5000)
                       .execute())
            pres_q = (sb.table("user_presence")
                        .select("user_id,display_name,last_active_at")
                        .order("last_active_at", desc=True)
                        .execute())
            pts      = pts_q.data or []
            presence = pres_q.data or []
        except Exception as e:
            print(f"[guest/team-list] read FAIL {type(e).__name__}: {e}")
            json_response(self, 500, {"ok": False, "error": "Could not load team activity."})
            return

        # Visibility: guests are non-admin viewers, so the presence roster
        # they see must be ACTIVE members/admins only (last_sign_in < 24h).
        # The 24h rule lives in SQL (active_member_ids); we never recompute
        # it here. Points are returned in full so the MAP keeps every pin
        # attributed to its original author (authorship is preserved).
        try:
            ami = sb.rpc("active_member_ids").execute()
            active_ids = [r["id"] for r in (ami.data or [])]
            presence = _filter_presence_active(presence, active_ids)
        except Exception as e:
            print(f"[guest/team-list] active filter FAIL {type(e).__name__}: {e}")
            # Fail safe: if the active set can't be resolved, show NO
            # presence rather than leaking everyone (privacy-preserving).
            presence = []

        _touch_session(sb, sess["id"])
        json_response(self, 200, {
            "ok":       True,
            "points":   pts,
            "presence": presence,
        })
```

- [ ] **Step 2: Re-run the unit tests (no regression)**

Run: `python -m pytest tests/test_guest_visibility.py -v`
Expected: PASS (helper unchanged).

- [ ] **Step 3: Commit**

```bash
git add api/guest.py
git commit -m "feat(visibility): guest team-list returns active-only presence"
```

---

## Task 4: Desktop roster → `list_roster()` with admin-only inactive section

**Files:**
- Modify: `static/js/dashboard.js` — `loadTeamRoster()` (lines 5635–5689)

- [ ] **Step 1: Replace `loadTeamRoster()`**

Replace the whole function body (5635–5688, keep the `window.loadTeamRoster = loadTeamRoster;` line below) with:

```javascript
async function loadTeamRoster() {
  const list = document.getElementById('team-list');
  if (!sbClient) return;
  try {
    // list_roster() is role-aware: non-admins receive ONLY active
    // members/admins (last_sign_in < 24h); admins receive everyone, with
    // an `active` flag and last_sign_in_at so we can show "last seen" for
    // inactive teammates. Guests/members never see inactive people.
    const { data, error } = await sbClient.rpc('list_roster');
    if (error) throw error;
    const members = data || [];
    if (!members.length) {
      list.innerHTML = '<div style="font-size:12px;color:var(--muted)">No active teammates right now.</div>';
      return;
    }
    const myUid   = currentUserId;
    const isAdminViewer = _myRole === 'admin';

    const lastSeen = (ts) => {
      if (!ts) return 'never signed in';
      const d = Math.floor((Date.now() - new Date(ts).getTime()) / 60000);
      if (d < 60)   return `last seen ${d}m ago`;
      if (d < 1440) return `last seen ${Math.round(d/60)}h ago`;
      return `last seen ${Math.round(d/1440)}d ago`;
    };

    const renderRow = (m) => {
      const isMe     = m.id === myUid;
      const isAdmin  = m.role === 'admin';
      const isMember = m.role === 'member';
      let tag;
      if (isAdmin) {
        tag = '<span style="font-size:10px;font-weight:700;padding:2px 7px;border-radius:5px;font-family:\'IBM Plex Mono\',monospace;background:rgba(56,189,248,.15);color:var(--accent);border:1px solid rgba(56,189,248,.28)">ADMIN</span>';
      } else if (isMember) {
        tag = '<span style="font-size:10px;font-weight:700;padding:2px 7px;border-radius:5px;font-family:\'IBM Plex Mono\',monospace;background:rgba(139,148,158,.15);color:var(--muted);border:1px solid var(--border)">MEMBER</span>';
      } else {
        tag = '<span style="font-size:10px;font-weight:700;padding:2px 7px;border-radius:5px;font-family:\'IBM Plex Mono\',monospace;background:rgba(245,158,11,.12);color:#f59e0b;border:1px solid rgba(245,158,11,.28)">NOT JOINED</span>';
      }
      const promote = (isAdminViewer && !isAdmin)
        ? `<button class="btn btn-sm" onclick="dashboardPromoteByEmail('${_esc(m.email)}')" style="font-size:11px;padding:4px 10px">Make admin</button>` : '';
      const demote  = (isAdminViewer && isAdmin && !isMe)
        ? `<button class="btn btn-sm" onclick="dashboardDemote('${_esc(m.id)}')" style="font-size:11px;padding:4px 10px;background:rgba(239,68,68,.1);color:#ef4444;border:1px solid rgba(239,68,68,.25)">Demote</button>` : '';
      // Admins additionally see a muted "last seen" line for INACTIVE rows.
      const seen = (isAdminViewer && !m.active)
        ? `<div style="font-size:10px;color:var(--muted);margin-top:2px">${_esc(lastSeen(m.last_sign_in_at))}</div>` : '';
      return `
        <div style="display:flex;align-items:center;gap:10px;padding:10px 12px;border:1px solid var(--border);border-radius:9px;background:var(--panel-2,#0d1117);opacity:${m.active ? 1 : 0.6}">
          <div style="flex:1;min-width:0">
            <div style="font-size:13px;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${_esc(m.email)}${isMe ? ' <span style="color:var(--muted);font-weight:400">(you)</span>' : ''}</div>
            ${seen}
          </div>
          ${tag}
          ${promote}${demote}
        </div>`;
    };

    const active   = members.filter(m => m.active);
    const inactive = members.filter(m => !m.active);   // admins only — non-admins never receive these rows
    let html = active.map(renderRow).join('');
    if (isAdminViewer && inactive.length) {
      html += `<div style="font-size:10px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.5px;margin:14px 2px 8px">Inactive (last 24h+)</div>`;
      html += inactive.map(renderRow).join('');
    }
    list.innerHTML = html;
  } catch (e) {
    list.innerHTML = `<div style="font-size:12px;color:#ef4444">Failed to load: ${_esc(e.message || e)}</div>`;
  }
}
```

- [ ] **Step 2: Verify it loads in the browser (Task 7 covers full assertions)**

Reload `http://localhost:3002/dashboard` as the test_ admin, open the Team modal. Expected: active teammates render; an "Inactive (last 24h+)" section appears only for the admin. No JS console errors.

- [ ] **Step 3: Commit**

```bash
git add static/js/dashboard.js
git commit -m "feat(visibility): desktop roster uses list_roster (active + admin-only inactive)"
```

---

## Task 5: Desktop team-activity panel → active-only

**Files:**
- Modify: `static/js/dashboard.js` — add globals + `loadActiveSets()` (near line 46 and after the presence load at ~836), and an active-filter at the end of `renderPerUserPanel()` (lines 929–939).

- [ ] **Step 1: Add module globals**

After line 46 (`let fieldPresence = {};`), add:

```javascript
let activeMemberIds  = new Set();  // member/admin UUIDs active (<24h), from active_member_ids()
let activeGuestNames = new Set();  // lowercased names of unexpired guests, from active_guests()
```

- [ ] **Step 2: Add the loader**

Add this function just above `function renderPerUserPanel()` (line 897):

```javascript
// Pull the active sets that gate who appears in the team-activity panel.
// Active members/admins come from active_member_ids() (last_sign_in < 24h);
// active guests come from active_guests() (unexpired, unrevoked). The map
// itself is untouched — gone people keep authoring their pins.
async function loadActiveSets() {
  if (!sbClient) return;
  try {
    const [mids, guests] = await Promise.all([
      sbClient.rpc('active_member_ids'),
      sbClient.rpc('active_guests'),
    ]);
    activeMemberIds  = new Set((mids.data   || []).map(r => r.id));
    activeGuestNames = new Set((guests.data || []).map(r => (r.name || '').toLowerCase()));
  } catch (e) {
    console.warn('loadActiveSets failed:', e);
    // Fail-safe: leave the existing sets as-is rather than blanking the panel.
  }
}
window.loadActiveSets = loadActiveSets;
```

- [ ] **Step 3: Call the loader where presence is loaded**

After the presence-load `try/catch` block that ends at line 836 (`} catch (e) { /* table may not exist yet — ignore */ }`), add:

```javascript
  // Load the active-visibility sets alongside presence.
  await loadActiveSets();
```

- [ ] **Step 4: Filter the panel rows to active people only**

In `renderPerUserPanel()`, the rows are built and sorted at lines 929–939. Immediately AFTER the `.sort((a,b) => { ... });` chain that produces `rows`, insert a filter so only active people remain. Change:

```javascript
  }).sort((a,b) => {
    if (a.is_mine !== b.is_mine) return a.is_mine ? -1 : 1;
    if (b.today !== a.today) return b.today - a.today;
    return (new Date(b.last_active_at || 0)) - (new Date(a.last_active_at || 0));
  });
```

to:

```javascript
  }).sort((a,b) => {
    if (a.is_mine !== b.is_mine) return a.is_mine ? -1 : 1;
    if (b.today !== a.today) return b.today - a.today;
    return (new Date(b.last_active_at || 0)) - (new Date(a.last_active_at || 0));
  }).filter(m =>
    // Keep myself always; otherwise show only people who are around now:
    // active members/admins (by UUID) or active guests (by name). Gone
    // guests and inactive members drop off the panel — but their pins
    // remain on the map, attributed to them (authorship preserved).
    m.is_mine
    || activeMemberIds.has(m.id)
    || activeGuestNames.has((m.name || '').toLowerCase())
  );
```

- [ ] **Step 5: Refresh active sets when presence changes (realtime)**

In the realtime `user_presence` handler (lines 849–854), make the callback refresh the active sets before re-rendering. Replace:

```javascript
    .on('postgres_changes', { event: '*', schema: 'public', table: 'user_presence' },
      ({ new: p, old: o }) => {
        const r = p || o;
        if (r && r.user_id) fieldPresence[r.user_id] = r;
        if (typeof renderPerUserPanel === 'function') renderPerUserPanel();
      })
```

with:

```javascript
    .on('postgres_changes', { event: '*', schema: 'public', table: 'user_presence' },
      ({ new: p, old: o }) => {
        const r = p || o;
        if (r && r.user_id) fieldPresence[r.user_id] = r;
        loadActiveSets().finally(() => {
          if (typeof renderPerUserPanel === 'function') renderPerUserPanel();
        });
      })
```

- [ ] **Step 6: Verify in browser (full assertions in Task 7)**

Reload the dashboard; open the Team (activity) tab. Expected: only active members/guests listed; no JS console errors; map pins unchanged.

- [ ] **Step 7: Commit**

```bash
git add static/js/dashboard.js
git commit -m "feat(visibility): team-activity panel shows active people only"
```

---

## Task 6: Verify FEATURE 1 (Inaccessible→Completed flip) — data-safe live test

**Goal:** Prove that when survey (IAQ) data matches a field point that was a non-completed type, the point auto-flips to **Completed** — exercising the REAL matcher, touching only one `test_` point, never the IAQ cache or any existing pin.

**Files:**
- Create: `final review/feature-verify/f1_scoped_flip_test.py` (throwaway harness)

- [ ] **Step 1: Read one existing IAQ response location from the cache (read-only)**

Use the Supabase MCP / a read-only Python snippet to load the cached IAQ blob via `api/_lib.load_cached('iaq_survey')` and pick ONE feature's `coordinates` (lon, lat) and `response_id`. Record them. Do NOT write anything.

- [ ] **Step 2: Add a `test_` Inaccessible field point at that location**

Insert (service role) ONE row into `field_survey_points`:
`status='Inaccessible'`, `collector_name='test_qa_flip'`, `notes='test_ flip verification — delete me'`, `lat`/`lon` = the IAQ feature's coordinates. Capture its `id`. Screenshot the map showing it RED (Inaccessible): `final review/feature-verify/f1-01-inaccessible.png`.

- [ ] **Step 3: Write the scoped flip harness**

Create `final review/feature-verify/f1_scoped_flip_test.py`:

```python
"""Data-safe Feature-1 check: run the REAL matcher against ONE test_ point
and the EXISTING cached IAQ features. Writes nothing except the single
test_ point's status. Never rewrites the IAQ cache, never calls upload/
daily-refresh, never touches another pin."""
import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[2] / "api"))
from _lib import load_cached, supabase_admin            # noqa: E402
from _processing import _apply_iaq_to_field_features    # noqa: E402

TEST_POINT_ID = "<<paste id from Step 2>>"

iaq = load_cached("iaq_survey")                          # read-only
iaq_feats = iaq["features"] if isinstance(iaq, dict) else iaq

sb = supabase_admin()
row = sb.table("field_survey_points").select("*").eq("id", TEST_POINT_ID).single().execute().data
assert row["status"] == "Inaccessible", row["status"]

# Build a GeoJSON feature for ONLY our test point and run the real matcher.
ff = {"type": "Feature",
      "geometry": {"type": "Point", "coordinates": [row["lon"], row["lat"]]},
      "properties": {"status": row["status"], "id": row["id"]}}
fc = {"type": "FeatureCollection", "features": [ff]}

# parcel_idx=None → matcher uses the 30m haversine fallback tier.
_apply_iaq_to_field_features(fc, iaq_feats, None)

new_status = fc["features"][0]["properties"]["status"]
print("matched ->", new_status)
assert new_status == "Completed", f"expected Completed, got {new_status}"

# Persist ONLY the test_ point's flip (mirrors the production upload path).
sb.table("field_survey_points").update({"status": "Completed"}).eq("id", TEST_POINT_ID).execute()
print("OK: test_ point flipped Inaccessible -> Completed (no cache/other pins touched)")
```

> NOTE: confirm the real signature of `_apply_iaq_to_field_features` before running (Explore found it at `api/_processing.py:1337`). If it expects a list of features rather than a FeatureCollection, adjust the call to match — do not change `_processing.py`.

- [ ] **Step 4: Run the harness**

Run: `cd "/Users/goshtasbshahriari/UF Dropbox/Goshtasb Shahriari Mehr/DTSC_Lab/KeyStone_project" && python "final review/feature-verify/f1_scoped_flip_test.py"`
Expected: `matched -> Completed` then `OK: test_ point flipped …`.

- [ ] **Step 5: Confirm the flip in the live app**

Reload `http://localhost:3002/dashboard`; the test point now renders GREEN (Completed). Screenshot: `final review/feature-verify/f1-02-completed.png`. If the popup exposes IAQ fields, screenshot that too.

- [ ] **Step 6: Delete the test_ point (restore clean state)**

Run (service role): delete `field_survey_points` where `id = TEST_POINT_ID`. Confirm it is gone from the map. Note the deletion in `CLEANUP.md`.

---

## Task 7: Verify FEATURE 2 (active-only visibility) — live, data-safe

**Goal:** Prove the visibility matrix end-to-end with `test_` artifacts only.

- [ ] **Step 1: Create test_ fixtures (additive)**

Via service role / the app:
1. A `test_` guest session that is ALREADY EXPIRED (insert with `expires_at = now() - interval '1 hour'`, `name='test_gone_guest'`) plus one `field_survey_points` row authored by it (`collector_name='test_gone_guest'`, `guest_session_id=<that id>`, `status='No Answer'`).
2. A `test_` guest session that is ACTIVE (`expires_at = now() + interval '2 hours'`, `name='test_active_guest'`).
3. The `test_keystone_qa@example.com` admin from Task 0 (active). Optionally a second `test_` member whose `last_sign_in_at` is >24h old to exercise the "inactive" path (if not feasible to backdate auth, rely on any genuinely-inactive existing teammate only for the ADMIN view — but do NOT modify them).
Record every id in `CLEANUP.md`.

- [ ] **Step 2: Admin view assertions (desktop, signed in as test_ admin)**

Open Team modal + activity tab. Expected & screenshot (`f2-01-admin-*.png`):
- Active teammates listed.
- An "Inactive (last 24h+)" section is present with "last seen …" lines (admin only).
- `test_gone_guest` does NOT appear in the activity panel; its `No Answer` pin still shows on the map attributed to `test_gone_guest`.
- `test_active_guest` (if it has presence/points) is eligible to appear; gone guest is not.

- [ ] **Step 3: Member/guest view assertions**

Sign in as a non-admin (a `test_` member, or use the field PWA guest claim with today's invite code as `test_member_view`). Expected & screenshot (`f2-02-member-*.png`, `f2-03-guest-*.png`):
- Only ACTIVE members/admins are visible; NO "inactive" section; no `last_sign_in` timestamps.
- `test_gone_guest` absent from team; its pin still on the map.
- Chat history is intact (no messages removed).

- [ ] **Step 4: Record results**

Write pass/fail per matrix cell into `final review/feature-verify/RESULTS.md`.

---

## Task 8: Cleanup, final report, and PR

- [ ] **Step 1: Delete every `test_` artifact**

Using `CLEANUP.md`, delete (service role): the `test_` guest sessions, their points, the `test_` field point(s), the `test_` member row(s) in `team_members`, and the `test_keystone_qa@example.com` auth user. Verify each is gone. Confirm NO non-`test_` row changed (spot-check counts of `field_survey_points`, `team_members`, `field_guest_sessions` are back to baseline).

- [ ] **Step 2: Confirm the IAQ cache is untouched**

Confirm the `iaq_survey` cache blob's `updated`/size is unchanged from the run start (we only read it). Note in `RESULTS.md`.

- [ ] **Step 3: Run the unit tests once more**

Run: `python -m pytest tests/ -v`
Expected: all pass.

- [ ] **Step 4: Commit artifacts + open PR**

```bash
git add "final review/feature-verify"
git commit -m "test(visibility): data-safe live verification of F1 flip + F2 active visibility"
```
Then push the branch and open a PR summarizing: migration 24, desktop + guest API changes, F1 verified (flip works), F2 implemented + verified, and the cleanup confirmation. (Do NOT add any AI/co-author attribution.)

---

## Self-Review

**Spec coverage:**
- §5.1 RPC → Task 1 (`list_roster`, `active_member_ids`, `active_guests`). ✓
- §5.2 desktop roster + per-user panel → Tasks 4 & 5. ✓
- §5.3 guest API presence filter (shared rule via RPC) → Tasks 2 & 3. ✓
- §4 chat history preserved → no chat code touched (Tasks 3/5 leave `chat-list`/`loadTodayMessages` alone); asserted in Task 7 Step 3. ✓
- §3 visibility matrix (admin sees inactive+last-seen; non-admin active-only) → Task 4 render logic + Task 1 RPC NULLing of `last_sign_in_at` for non-admins. ✓
- §7 testing (unit + data-safe live) → Tasks 2, 6, 7. ✓
- §8 data-safety → enforced in every task; cleanup in Task 8. ✓
- Feature 1 verification → Task 6. ✓

**Placeholder scan:** Only intentional fill-ins are `<<paste id…>>` (a runtime value) and a noted signature-confirm for `_apply_iaq_to_field_features`. No vague "add error handling" steps. ✓

**Type/name consistency:** `_filter_presence_active(presence, active_ids)` defined in Task 2, used identically in Task 3. RPC names `list_roster` / `active_member_ids` / `active_guests` consistent across Tasks 1, 3, 4, 5. Globals `activeMemberIds` / `activeGuestNames` defined (Task 5 Step 1) and used (Step 4). `loadActiveSets` defined and called in Steps 2/3/5. ✓
