"""Create/normalize ADDITIVE test_ fixtures for Feature-2 verification.
Idempotent. Prints every id so they can be deleted. Touches NO existing
non-test_ row."""
import os, pathlib, json, sys
from datetime import datetime, timezone, timedelta

ROOT = pathlib.Path("/Users/goshtasbshahriari/UF Dropbox/Goshtasb Shahriari Mehr/DTSC_Lab/KeyStone_project")
for line in (ROOT / ".env").read_text().splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())
sys.path.insert(0, str(ROOT / "api"))
from supabase import create_client

sb = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_ROLE_KEY"])
now = datetime.now(timezone.utc)
created = {}

# 1) test_ non-admin MEMBER (already created earlier; ensure member role)
uid = None
for usr in sb.auth.admin.list_users():
    if getattr(usr, "email", None) == "test_member_qa@example.com":
        uid = usr.id; break
sb.table("team_members").upsert({"id": uid, "role": "member"}).execute()
created["member_auth_uid"] = uid
print("member:", uid)

# 2) gone guest — normalize ALL test_gone_guest rows to EXPIRED
rows = sb.table("field_guest_sessions").select("id").eq("name", "test_gone_guest").execute().data or []
if not rows:
    r = sb.table("field_guest_sessions").insert({
        "name": "test_gone_guest",
        "invite_date": now.date().isoformat(),
        "created_at": (now - timedelta(hours=3)).isoformat(),
        "expires_at": (now - timedelta(hours=1)).isoformat(),
    }).execute().data[0]
    rows = [r]
for r in rows:
    sb.table("field_guest_sessions").update({
        "created_at": (now - timedelta(hours=3)).isoformat(),
        "expires_at": (now - timedelta(hours=1)).isoformat(),
    }).eq("id", r["id"]).execute()
gone_id = rows[0]["id"]
created["gone_guest_ids"] = [r["id"] for r in rows]
print("gone guest (expired):", created["gone_guest_ids"])

# 2b) one point authored by the gone guest
pts = sb.table("field_survey_points").select("id").eq("collector_name", "test_gone_guest").execute().data or []
if not pts:
    pt = sb.table("field_survey_points").insert({
        "lat": 29.7790, "lon": -82.0300, "status": "No Answer",
        "collector_name": "test_gone_guest", "guest_session_id": gone_id,
        "notes": "test_ gone-guest authorship — delete me",
    }).execute().data[0]
    pts = [pt]
created["gone_guest_point_ids"] = [p["id"] for p in pts]
print("gone guest point:", created["gone_guest_point_ids"])

# 3) test_ ACTIVE guest session (unexpired)
arows = sb.table("field_guest_sessions").select("id").eq("name", "test_active_guest").execute().data or []
if not arows:
    a = sb.table("field_guest_sessions").insert({
        "name": "test_active_guest",
        "invite_date": now.date().isoformat(),
        "expires_at": (now + timedelta(hours=2)).isoformat(),
    }).execute().data[0]
    arows = [a]
created["active_guest_ids"] = [r["id"] for r in arows]
print("active guest:", created["active_guest_ids"])

print("\nCREATED_JSON=" + json.dumps(created))
