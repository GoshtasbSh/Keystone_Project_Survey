"""Lightweight survey logic helpers (no pandas/shapely dependencies)."""

from __future__ import annotations

from collections import defaultdict
from math import radians, sin, cos, sqrt, atan2


# QID141 (house condition) has an ambiguous recode in this survey: its
# RecodeValues are {'5': '1'}, so choice 5 ("Critical- Uninhabitable without
# repairs.") exports as code 1 — the code choice 1 ("Excellent") already uses.
# A numeric export therefore cannot distinguish the best answer from the worst
# one on the code alone.
#
# Resolved empirically, not assumed. For the 72 responses present in both the
# April (text) and May (numeric) exports, every one of the 11 rows carrying
# code 1 reads "Click to write Choice 5" in the text export — i.e. choice 5,
# Critical. No response maps to Excellent, and the text export contains zero
# Excellent answers across all 75 completed responses. Mapping code 1 to
# "Excellent" inverted the condition scale for the worst-off households and
# cost them 35 structural risk points each.
#
# This stays a survey-definition defect: if a respondent ever does choose
# Excellent it will also export as code 1 and be mislabelled Critical. The
# durable fix is to correct RecodeValues in Qualtrics so choice 5 recodes to 5.
#
# SUPERSEDED 2026-10-13 by the PI's decision (see the switch below): the
# respondents did pick choice 5, but the code-1 homes report the FEWEST
# problems (0/20 water leaks, 1/20 pests, against 15/22 and 16/22 for Poor),
# so the wording they answered was "Excellent". Code 1 is now read as
# Excellent, and "Critical" does not occur in this data.

# ── Shared-code switch (ONE place, one setting per question) ───────────────
# Four questions have RecodeValues that send a choice onto a code another,
# un-recoded choice already exports as. A numeric export cannot tell the two
# apart from the code alone:
#
#   QID141 code 1 -> choice 5 "Critical- Uninhabitable" (recoded)  or choice 1 "Excellent"
#   QID17  code 1 -> choice 3 "Moderately Urgent"       (recoded)  or choice 1 "Very Urgent"
#          code 2 -> choice 4 "Slightly Urgent"         (recoded)  or choice 2 "Urgent"
#   QID100 code 1 -> choice 3 "Somewhat"                (recoded)  or choice 1 "Yes"
#          code 2 -> choice 4 "Not Applicable"          (recoded)  or choice 2 "No"
#   QID221 (same scale as QID100)
#
# (QID17 code 3 is NOT shared: choice 3 recodes to 1, so a 3 can only be
# choice 5 "Not Urgent".)
#
# 'recoded_choice'  — the code means the choice RecodeValues explicitly sends
#                     there, shown with that choice's Display text.
# 'original_choice' — the code means the choice whose own ID it is. The text
#                     export's answer for the recoded choice ('Click to write
#                     Choice 5') reads the same, because it is the same pick:
#                     the April text export shows every code-1 respondent on
#                     the recoded choice, so the two formats must agree.
#
# Decided by the PI on 2026-10-13 from the April/October evidence (ledger
# "USER DECISION 2026-10-13"):
#   QID141 -> original_choice  code 1 = "Excellent- No repairs needed."
#   QID17  -> recoded_choice   1 Moderately / 2 Slightly / 3 Not Urgent (unchanged)
#   QID100 -> original_choice  1 = "Yes", 2 = "No / Not applicable"
#   QID221 -> original_choice  (same as QID100)
# To change a reading, edit this dict and re-process the CSV. Nothing else.
SHARED_CODE_RESOLUTION = {
    "QID141": "original_choice",
    "QID17":  "recoded_choice",
    "QID100": "original_choice",
    "QID221": "original_choice",
}
_SHARED_CODE_MODES = ("recoded_choice", "original_choice")

# qid -> {exported code: (recoded choice key, original choice key)}
SHARED_CODES = {
    "QID141": {"1": ("5", "1")},
    "QID17":  {"1": ("3", "1"), "2": ("4", "2")},
    "QID100": {"1": ("3", "1"), "2": ("4", "2")},
    "QID221": {"1": ("3", "1"), "2": ("4", "2")},
}

# Wording used under 'original_choice' where the code carries two answers the
# evidence cannot separate: code 2 on skirting/anchoring holds every site-built
# house (for whom "Not Applicable" fits) as well as the mobile homes saying No.
SHARED_CODE_ORIGINAL_LABELS = {
    ("QID100", "2"): "No / Not applicable",
    ("QID221", "2"): "No / Not applicable",
}

# All four readings above were confirmed by the PI on 2026-10-13, so the UI
# shows no "label unverified" note. Set False if a reading is ever reopened.
SHARED_CODE_VERIFIED = True

# The feature properties that carry a shared-code answer (QID221 has none).
SHARED_CODE_FIELDS = ["condition", "afford_urgency", "mh_skirting"]

# (qid, recoded choice key) -> the shared code that choice exports as
_RECODED_CHOICE_CODE = {
    (qid, pair[0]): code
    for qid, codes in SHARED_CODES.items() for code, pair in codes.items()
}


def _shared_code_mode(qid: str) -> str:
    """The current reading for one question. Read from the module global at
    call time so editing the switch (or a test's monkeypatch) takes effect."""
    mode = SHARED_CODE_RESOLUTION.get(qid, "recoded_choice")
    if mode not in _SHARED_CODE_MODES:
        raise ValueError(f"SHARED_CODE_RESOLUTION[{qid!r}] must be one of "
                         f"{_SHARED_CODE_MODES}, not {mode!r}")
    return mode


def shared_code_choice_key(qid, code) -> str | None:
    """Choice key a shared numeric code resolves to under the current switch,
    or None when (qid, code) is not a shared code."""
    qid = str(qid or "")
    pair = SHARED_CODES.get(qid, {}).get(str(code))
    if pair is None:
        return None
    return pair[0] if _shared_code_mode(qid) == "recoded_choice" else pair[1]


def _shared_code_label(qid: str, code: str, display: dict) -> str | None:
    """Text shown for a shared code under the current switch (None if the
    code is not shared). `display` is the question's choice-key -> Display."""
    key = shared_code_choice_key(qid, code)
    if key is None:
        return None
    if _shared_code_mode(qid) == "original_choice":
        override = SHARED_CODE_ORIGINAL_LABELS.get((qid, str(code)))
        if override:
            return override
    return display.get(key)


def shared_code_status() -> dict:
    """What the analysis reports about the shared-code questions."""
    for q in SHARED_CODES:
        _shared_code_mode(q)                      # refuse an unknown mode
    return {"resolution": {q: SHARED_CODE_RESOLUTION.get(q, "recoded_choice")
                           for q in sorted(SHARED_CODES)},
            "questions": sorted(SHARED_CODES),
            "fields": list(SHARED_CODE_FIELDS),
            "verified": bool(SHARED_CODE_VERIFIED)}


_QID141_DISPLAY = {
    "1": "Excellent- No repairs needed.",
    "2": "Good- Minor repairs needed.",
    "3": "Fair- Some repairs needed.",
    "4": "Poor- Major repairs needed.",
    "5": "Critical- Uninhabitable without repairs.",
}

# Hand-written fallback, used only if the generated QSF label map is missing.
# Code 1 follows the switch (evaluated once, at import).
QID141_RECODE_LABELS = {
    "1": _shared_code_label("QID141", "1", _QID141_DISPLAY),
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


# ── QSF-authoritative answer labels ───────────────────────────────────────
#
# The Qualtrics TEXT export writes each question's VariableNaming override
# rather than the choice text the respondent saw. In this survey those
# overrides are stale: some are placeholders ("Click to write Choice 5"),
# some belong to other questions entirely (QID21's safety scale exports as
# "Less than 6 months"; QID192's age bands are reversed). The NUMERIC export
# writes recode codes instead.
#
# api/qsf_labels.json (generated by scripts/build_qsf_label_map.py) maps both
# forms back to Choices[k].Display / Answers[k].Display — what was actually on
# screen. Anything ambiguous is left untouched rather than guessed.

_QSF_LABELS: dict | None = None


def qsf_labels() -> dict:
    """Return the generated QSF label map, or {} if it is unavailable.

    Imported rather than read from disk: a data file only ships inside a Vercel
    function when vercel.json lists it under includeFiles, and a silently empty
    map would turn the whole label correction into a no-op in production. An
    imported module is always bundled.
    """
    global _QSF_LABELS
    if _QSF_LABELS is None:
        try:
            try:
                from qsf_labels import QSF_LABELS
            except ImportError:
                from .qsf_labels import QSF_LABELS
            _QSF_LABELS = QSF_LABELS
        except ImportError:
            _QSF_LABELS = {}
    return _QSF_LABELS


def _norm_label(s) -> str:
    return ' '.join(str(s or '').replace('\xa0', ' ').split()).strip()


def _resolve_one(entry: dict, token: str, qid: str | None = None) -> str | None:
    """Resolve a single answer token to its on-screen Display text."""
    t = _norm_label(token)
    if not t:
        return None
    low = t.lower()

    keys = entry['text_to_key'].get(low)
    if keys is None:
        # Numeric export: the cell is a recode code. '6.0' is the same code
        # as '6' — pandas types these columns as float.
        code = t
        if code.endswith('.0') and code[:-2].isdigit():
            code = code[:-2]
        # A code two choices share: SHARED_CODE_RESOLUTION decides.
        forced = _shared_code_label(qid, code, entry['display']) if qid else None
        if forced is not None:
            return forced
        keys = entry['code_to_key'].get(code)
    elif qid and len(keys) == 1 and (qid, keys[0]) in _RECODED_CHOICE_CODE:
        # Text export naming the recoded choice of a shared code: it is the
        # same pick as that code, so it reads the same under the switch.
        return _shared_code_label(qid, _RECODED_CHOICE_CODE[(qid, keys[0])],
                                  entry['display'])

    if not keys or len(keys) > 1:
        return None  # unknown, or ambiguous — never guess
    return entry['display'].get(keys[0])


def resolve_answer_label(qid: str, value) -> str | None:
    """Translate an exported cell into the label the respondent saw.

    Returns None when the value cannot be resolved unambiguously, so callers
    keep the original rather than substituting a guess. Multi-select cells are
    comma-joined by Qualtrics and are only translated when EVERY part resolves
    — a partial translation would silently drop an answer.
    """
    if value is None:
        return None
    entry = qsf_labels().get(str(qid or ''))
    if not entry:
        return None

    qid = str(qid or '')
    whole = _resolve_one(entry, value, qid)
    if whole is not None:
        return whole

    raw = _norm_label(value)
    if ',' not in raw:
        return None
    parts = [p for p in (s.strip() for s in raw.split(',')) if p]
    resolved = [_resolve_one(entry, p, qid) for p in parts]
    if not resolved or any(r is None for r in resolved):
        return None
    return ','.join(resolved)
