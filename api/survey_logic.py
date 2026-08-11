"""Lightweight survey logic helpers (no pandas/shapely dependencies)."""

from __future__ import annotations

from collections import defaultdict
from math import radians, sin, cos, sqrt, atan2


QID141_RECODE_LABELS = {
    "1": "Excellent- No repairs needed.",
    "2": "Good- Minor repairs needed.",
    "3": "Fair- Some repairs needed.",
    "4": "Poor- Major repairs needed.",
    "5": "Critical- Uninhabitable without repairs.",
}


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6_371_000
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return 2 * r * atan2(sqrt(a), sqrt(1 - a))


def compute_struct_score(parts: dict) -> int:
    score = 0
    yr = str(parts.get("QID192", "") or "").lower()
    if "before 1960" in yr:
        score += 30
    elif "1960" in yr:
        score += 20
    elif "1980" in yr:
        score += 10

    ht = str(parts.get("QID128", "") or "").lower()
    if "single wide" in ht:
        score += 25
    elif "double wide" in ht:
        score += 15
    elif "non-traditional" in ht or "camper" in ht:
        score += 20

    cond_raw = parts.get("QID141", "")
    cond = str(cond_raw or "").lower()
    if "critical" in cond or "uninhabitable" in cond:
        score += 35
    elif "poor" in cond:
        score += 25
    elif "fair" in cond:
        score += 15
    else:
        try:
            cnum = float(str(cond_raw).strip())
        except (TypeError, ValueError):
            cnum = None
        if cnum is not None:
            if cnum >= 5:
                score += 35
            elif cnum >= 4:
                score += 25
            elif cnum >= 3:
                score += 15

    return round(min(score, 100))


def symptom_frequency_score(val) -> int:
    """Map symptom frequency text to 0–4 for the health vulnerability composite.

    Numeric Qualtrics exports are recoded to labels like ``annually``; that word
    does not contain ``year``, so ``annual`` is matched explicitly alongside
    ``year`` (e.g. ``once per year``).
    """
    if val is None:
        return 0
    try:
        if isinstance(val, float) and val != val:  # NaN
            return 0
    except Exception:
        pass
    try:
        v = str(val).strip().lower()
    except Exception:
        return 0
    if not v or v in ("nan", "none", "nat"):
        return 0
    if "weekly" in v:
        return 4
    if "month" in v:
        return 3
    if "season" in v:
        return 2
    if "year" in v or "annual" in v:
        return 1
    return 0


def nearest_contact_distance_m(iaq_lon: float, iaq_lat: float, contact_features: list) -> float | None:
    best = None
    for cf in contact_features:
        try:
            c_lon, c_lat = cf["geometry"]["coordinates"]
            d = haversine_m(iaq_lat, iaq_lon, float(c_lat), float(c_lon))
        except Exception:
            continue
        if best is None or d < best:
            best = d
    return round(best, 1) if best is not None else None


def build_validation_summary(iaq_features: list, contact_features: list) -> dict:
    match_details = []
    unmatched_by_street: dict = defaultdict(int)

    for f in iaq_features:
        props = f.get("properties") or {}
        coords = (f.get("geometry") or {}).get("coordinates") or [None, None]
        lon, lat = coords[0], coords[1]
        matched = bool(props.get("iaq_matched"))
        street = props.get("street_name") or "Unknown"
        coord_source = props.get("coord_source") or "unknown"

        nearest = None
        if lon is not None and lat is not None and not matched:
            nearest = nearest_contact_distance_m(float(lon), float(lat), contact_features)
            unmatched_by_street[street] += 1

        match_details.append(
            {
                "street_name": street,
                "coord_source": coord_source,
                "matched": matched,
                "nearest_contact_m": nearest,
            }
        )

    total_iaq = len(iaq_features)
    total_completed_contacts = sum(
        1 for cf in contact_features if (cf.get("properties") or {}).get("status") == "Completed"
    )
    matched_iaq = sum(1 for d in match_details if d.get("matched"))
    unmatched_iaq = max(total_iaq - matched_iaq, 0)
    # % of IAQ surveys matched to a completed contact (same parcel).
    match_rate = round((matched_iaq / total_iaq) * 100, 1) if total_iaq else 0.0
    # % of completed canvass contacts that have at least one confirmed IAQ pairing
    # (same numerator; denominator from community layer — mirrors app.py coverage_pct).
    coverage_pct = (
        round((matched_iaq / total_completed_contacts) * 100, 1) if total_completed_contacts else 0.0
    )

    return {
        "total_iaq_responses": total_iaq,
        "total_completed_contacts": total_completed_contacts,
        "matched_iaq_responses": matched_iaq,
        "unmatched_iaq": unmatched_iaq,
        "match_rate_pct": match_rate,
        "coverage_pct": coverage_pct,
        "match_details": match_details,
        "unmatched_by_street": dict(unmatched_by_street),
    }


ORPHAN_RADIUS_M = 25.0


def orphan_iaq_features(iaq_features: list, contact_features: list,
                        radius_m: float = ORPHAN_RADIUS_M) -> list:
    """Return IAQ responses that have no *addressed* canvass record nearby.

    Deliberately ignores ``iaq_matched``. A response can be flagged matched
    purely because an anonymous field pin landed on its parcel — that is
    what happened at 6409 Beloit on 2026-07-21, and it silently removed the
    household from the manual-fix worklist without recording an address.
    Only a contact feature that actually carries an ``address`` counts as
    a rescue.

    ``radius_m`` defaults to 25 m — tighter than one suburban lot, so a
    neighbour's record never masks a genuine orphan.
    """
    addressed = []
    for cf in contact_features or []:
        props = (cf or {}).get("properties") or {}
        if not str(props.get("address") or "").strip():
            continue
        coords = ((cf.get("geometry") or {}).get("coordinates") or [None, None])
        if coords[0] is None or coords[1] is None:
            continue
        addressed.append((float(coords[0]), float(coords[1])))

    out = []
    for f in iaq_features or []:
        coords = ((f.get("geometry") or {}).get("coordinates") or [None, None])
        if coords[0] is None or coords[1] is None:
            continue
        lon, lat = float(coords[0]), float(coords[1])
        if any(haversine_m(lat, lon, c_lat, c_lon) <= radius_m
               for c_lon, c_lat in addressed):
            continue
        out.append(f)
    return out


# ── Shared parcel address-index geometry (single source of truth) ─────────
#
# Fix 2026-08-10 round 1: this ray-cast used to be duplicated in
# scripts/build_parcel_address_index.py AND api/iaq-points.py (?unmatched=1), and both
# copies only tested the outer ring — a point inside an interior ring
# (a hole, e.g. a courtyard or an easement cut out of a parcel) was wrongly
# reported as inside that parcel and handed that parcel's street address to
# a surveyor. Both call sites now import the ray-cast and lookup from here
# so a future fix only has to happen once.


def _point_in_ring(x: float, y: float, ring: list) -> bool:
    """Standard even-odd ray-cast against a single linear ring."""
    inside = False
    n = len(ring)
    j = n - 1
    for i in range(n):
        xi, yi = ring[i][0], ring[i][1]
        xj, yj = ring[j][0], ring[j][1]
        if (yi > y) != (yj > y):
            if x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-15) + xi:
                inside = not inside
        j = i
    return inside


def point_in_polygon(x: float, y: float, outer_ring: list, hole_rings: list = None) -> bool:
    """A point is inside a polygon only if it's inside the outer ring AND
    not inside any interior ring (hole). A point sitting in a hole belongs
    to no parcel, however confidently the outer-ring test alone would have
    placed it."""
    if not _point_in_ring(x, y, outer_ring):
        return False
    for hole in hole_rings or []:
        if _point_in_ring(x, y, hole):
            return False
    return True


def polygon_rings(geometry: dict) -> list:
    """Return [(outer_ring, [hole_ring, ...]), ...] for a Polygon or
    MultiPolygon GeoJSON geometry. Each *_ring is a coordinate list
    ``[[lon, lat], ...]``. Any other geometry type yields ``[]``."""
    t = (geometry or {}).get("type")
    coords = (geometry or {}).get("coordinates") or []
    if t == "Polygon":
        polys = [coords]
    elif t == "MultiPolygon":
        polys = coords
    else:
        return []
    out = []
    for poly in polys:
        if not poly:
            continue
        out.append((poly[0], poly[1:]))
    return out


def build_parcel_address_entries(feature: dict) -> list:
    """Reduce one parcel GeoJSON ``Feature`` into compact index entries —
    one per polygon part (a MultiPolygon parcel yields several). Each entry
    carries the outer ring, any interior rings (holes), and a bbox computed
    from the outer ring only (a cheap pre-filter — see ``lookup_parcel``).
    Skips parcels with no address on file."""
    props = (feature or {}).get("properties") or {}
    addr = str(props.get("address") or "").strip()
    if not addr:
        return []
    out = []
    for outer, holes in polygon_rings((feature or {}).get("geometry") or {}):
        xs = [p[0] for p in outer]
        ys = [p[1] for p in outer]
        out.append({
            "parcel_id": props.get("parcel_id"),
            "address": addr,
            "bbox": [min(xs), min(ys), max(xs), max(ys)],
            "ring": [[round(p[0], 6), round(p[1], 6)] for p in outer],
            "holes": [[[round(p[0], 6), round(p[1], 6)] for p in hole] for hole in holes],
        })
    return out


def lookup_parcel(index: dict, lon: float, lat: float):
    """Return ``(address, parcel_id)`` of the parcel containing (lon, lat),
    honouring interior rings, or ``(None, None)`` if no parcel matches
    (including a point that lands inside a hole). Cheap on a miss: the
    bbox check short-circuits before the ray-cast runs."""
    for p in (index or {}).get("parcels") or []:
        x0, y0, x1, y1 = p["bbox"]
        if not (x0 <= lon <= x1 and y0 <= lat <= y1):
            continue
        if point_in_polygon(lon, lat, p["ring"], p.get("holes")):
            return p["address"], p.get("parcel_id")
    return None, None
