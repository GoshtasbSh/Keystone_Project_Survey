"""Prove an upload lost nothing. Run before and after; it compares, not asserts blindly.

The hard restriction on this project is that no point may be lost, and field
points above all. This compares a live capture against
BASELINE_BEFORE_UPLOAD.json and fails loudly on any loss.

What an IAQ upload is actually allowed to do to field points (verified in
api/upload.py:153-177):
  - UPDATE `status` and `iaq_matched` on ids the matcher just confirmed
  - nothing else: never notes, lat, lon, collected_at, and never DELETE
    (the only delete on field_survey_points is a guest removing their own
    point, api/guest.py:494)

So: field-point IDs must be identical before and after, and their coordinates
must be unchanged. Status may only move toward Completed.

Usage:
  python3 scripts/audit/verify_no_data_loss.py <after.json>
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

EVID = (Path(__file__).resolve().parents[2] / 'docs' / 'plans' / 'evidence'
        / '2026-09-20-audit')
BASELINE = EVID / 'BASELINE_BEFORE_UPLOAD.json'


def coords(f: dict):
    c = ((f or {}).get('geometry') or {}).get('coordinates') or [None, None]
    return (round(c[0], 7) if c[0] is not None else None,
            round(c[1], 7) if c[1] is not None else None)


def index(fc: dict, key: str) -> dict:
    """Index features by their id, falling back to position+address.

    Some community contacts carry no `id`; keying on the id alone silently
    excluded them from the loss check, which is exactly the blind spot this
    script exists to prevent. Anything without an id is tracked by where it is
    and what it says instead.
    """
    out = {}
    for i, f in enumerate(fc.get('features', []) or [] if fc else []):
        p = f.get('properties') or {}
        k = p.get(key)
        if k is None:
            c = coords(f)
            k = f'@{c[0]},{c[1]}|{p.get("address") or p.get("street_name") or i}'
        out[str(k)] = f
    return out


def main() -> int:
    if not BASELINE.exists():
        print(f'FAIL: no baseline at {BASELINE}')
        return 2
    before = json.loads(BASELINE.read_text())
    after = json.loads(Path(sys.argv[1]).read_text())

    problems: list[str] = []
    notes: list[str] = []

    # ── Field points: the hard restriction ───────────────────────────────
    fb = index(before.get('field_points') or {}, 'id')
    fa = index(after.get('field_points') or {}, 'id')
    lost = sorted(set(fb) - set(fa))
    gained = sorted(set(fa) - set(fb))
    if lost:
        problems.append(f'FIELD POINTS LOST ({len(lost)}): {lost[:20]}')
    if gained:
        notes.append(f'field points added ({len(gained)}): {gained[:20]}')

    moved, wiped = [], []
    for pid in sorted(set(fb) & set(fa)):
        if coords(fb[pid]) != coords(fa[pid]):
            moved.append(pid)
        pb = fb[pid].get('properties') or {}
        pa = fa[pid].get('properties') or {}
        for field in ('notes', 'collected_at', 'collector', 'collector_id'):
            if pb.get(field) and not pa.get(field):
                wiped.append(f'{pid}.{field}')
    if moved:
        problems.append(f'FIELD POINTS MOVED ({len(moved)}): {moved[:20]}')
    if wiped:
        problems.append(f'FIELD POINT DATA WIPED ({len(wiped)}): {wiped[:20]}')

    # ── IAQ responses and community contacts ─────────────────────────────
    for name, key in (('iaq_points', 'response_id'), ('survey_points', 'id')):
        b = index(before.get(name) or {}, key)
        a = index(after.get(name) or {}, key)
        missing = sorted(set(b) - set(a))
        added = sorted(set(a) - set(b))
        if missing:
            problems.append(f'{name.upper()} LOST ({len(missing)}): {missing[:20]}')
        if added:
            notes.append(f'{name} added ({len(added)})')

    print('=' * 64)
    print(f'field points : {len(fb)} -> {len(fa)}')
    print(f'iaq responses: {len(index(before.get("iaq_points") or {}, "response_id"))} '
          f'-> {len(index(after.get("iaq_points") or {}, "response_id"))}')
    print(f'contacts     : {len(index(before.get("survey_points") or {}, "id"))} '
          f'-> {len(index(after.get("survey_points") or {}, "id"))}')
    print('=' * 64)
    for n in notes:
        print(f'  note: {n}')
    if problems:
        print()
        for p in problems:
            print(f'  *** {p}')
        print('\nRESULT: DATA LOSS DETECTED — restore from backup.')
        return 1
    print('\nRESULT: no point lost, no field point moved or wiped.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
