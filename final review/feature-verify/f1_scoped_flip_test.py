"""Feature-1 data-safe check: run the REAL matcher against ONE test_ point
+ the EXISTING cached IAQ features. Writes only the single test_ point's
status. Never rewrites the IAQ cache, never calls upload/daily-refresh,
never touches another pin."""
import os, pathlib, sys, json
ROOT = pathlib.Path("/Users/goshtasbshahriari/UF Dropbox/Goshtasb Shahriari Mehr/DTSC_Lab/KeyStone_project")
for line in (ROOT / ".env").read_text().splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())
sys.path.insert(0, str(ROOT / "api"))
from _lib import load_cached, supabase_admin
from _processing import _apply_iaq_to_field_features

iaq = load_cached("iaq_survey")
if isinstance(iaq, dict) and "geojson" in iaq:
    iaq_feats = iaq["geojson"]["features"]
elif isinstance(iaq, dict) and "features" in iaq:
    iaq_feats = iaq["features"]
else:
    iaq_feats = iaq
assert iaq_feats, "no IAQ features in cache"
print("cached IAQ features:", len(iaq_feats))

# pick one existing IAQ response location (read-only)
target = iaq_feats[0]
tlon, tlat = target["geometry"]["coordinates"]
print("target IAQ coord:", tlon, tlat, "resp:", target["properties"].get("response_id"))

sb = supabase_admin()
# add a test_ Inaccessible field point AT that coordinate
pt = sb.table("field_survey_points").insert({
    "lat": tlat, "lon": tlon,
    "status": "Inaccessible",
    "collector_name": "test_qa_flip",
    "notes": "test_ F1 flip verification — delete me",
}).execute().data[0]
pid = pt["id"]
print("created test_ point:", pid, "status BEFORE:", pt["status"])
assert pt["status"] == "Inaccessible"

# run the REAL matcher on ONLY this point (parcel_idx=None -> 30m fallback,
# but coords are identical so distance = 0)
ff = [{"type": "Feature",
       "geometry": {"type": "Point", "coordinates": [tlon, tlat]},
       "properties": {"status": pt["status"], "id": pid}}]
upgraded = _apply_iaq_to_field_features(ff, iaq_feats, None)
new_status = ff[0]["properties"]["status"]
print("matcher upgraded count:", upgraded, "| status AFTER match:", new_status)
assert new_status == "Completed", f"expected Completed, got {new_status}"

# persist ONLY the test_ point (mirrors api/upload.py production behaviour)
sb.table("field_survey_points").update({"status": "Completed"}).eq("id", pid).execute()
chk = sb.table("field_survey_points").select("status").eq("id", pid).single().execute().data
print("DB status now:", chk["status"])
print("\nRESULT_JSON=" + json.dumps({"point_id": pid, "before": "Inaccessible",
      "after": chk["status"], "has_iaq_survey": ff[0]["properties"].get("has_iaq_survey")}))
