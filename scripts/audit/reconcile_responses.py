"""Per-ResponseId reconciliation of the October export against production.

Every ResponseId in the CSV must land in exactly ONE disposition, and the
production blobs must agree with it:

  unfinished (8) -> preview (3) -> unplaced (12, left as is by decision)
  -> superseded (8, earlier answer of a household that answered twice)
  -> analysed (106)

It also checks the contact/field links the launch fixes promised:
  * a contact is linked only to a response with the SAME house number
    (6306<->6318 Amherst and 6376<->6378 Antioch must not be linked)
  * no contact or field pin is linked to a superseded response
  * the kept second-submissions at confirmed parcels are matched
  * field-pin copies of IAQ scores equal the IAQ feature's scores
  * blob field pins == field_survey_points rows (the 28 test pins are gone)

Usage:
  .venv/bin/python scripts/audit/reconcile_responses.py \
      --csv "../Keystone_Data/Keystone Heights Survey - V1_October 7, 2026_00.47.csv" \
      --snap "$GATE/after"
Exit 0 = every check passed.
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import math
import re
import sys
from pathlib import Path

# The property the de-duplication task (MATCH-3) sets on an earlier
# (superseded) response. MATCH-3 moves those responses to
# geojson['superseded_features']; they are read from there too. If a later
# change removes them from the geojson altogether, absence is accepted.
SUPERSEDED_KEY = 'superseded_by'

PREVIEW_STATUSES = {'1', '2', '8', '9', '17'}

EXPECTED_UNFINISHED = {
    'R_1PAVCFsfkWStMFI', 'R_56baDqL1NfPpTT4', 'R_1VCurkFFQdm9r8S', 'R_60TLGJw996jdfRr',
    'R_3zvt8mOIR6KLTwd', 'R_3ilbN3FDaK3fCRH', 'R_6fN3AoLgkuG6ZI0', 'R_5sbvvJYuZv17jmq'}
EXPECTED_PREVIEW = {'R_78IEP3v2S0sfWk9', 'R_7dXknXZ9AtNEPvF', 'R_7duCmfU1iGEFEXI'}
EXPECTED_UNPLACED = {
    'R_36odEmwEgEqSNDB', 'R_0ZTdLDAT7zhyRrg', 'R_74gpoiI1SxEL9Hr', 'R_14eq9tAvPi8UAPq',
    'R_gFfly1ltLjBCwg0', 'R_2V4bkJCukVdMRmf', 'R_7QwS4Wcwpxbyb1X', 'R_jtGYC8JWA2WZXsB',
    'R_2EZtivGKl7DF3lQ', 'R_66nxsikshX47qBz', 'R_6s4nbfZyVrBrmFu', 'R_5Yb7oAQxmwr5VYH'}
# earlier -> kept (latest RecordedDate)
EXPECTED_SUPERSEDED = {
    'R_5LnXMcaezhqW28F': 'R_j1xG6QD0Gw1G3uU', 'R_6pRawZol21jqapc': 'R_3915ZWsZpRAwPi9',
    'R_1E4YReRP6XTeX06': 'R_0U4XyfXUNDttX9a', 'R_kZXrW8v3LxbbUTV': 'R_hv0cc021NGKRc5M',
    'R_6s0PVusMDUucFQY': 'R_h6cnt2kXgSK5Bbg', 'R_iB2E7Yzs7PSGMlr': 'R_ju3Amx8yBiJ45L0',
    'R_2KqXYjOIYV1zFdH': 'R_5oBDIEcTfYUvj8n', 'R_mLTilJCf3lIPEoI': 'R_6Nqhz2mzupemk9v'}
# kept second submissions whose parcel has a real canvass contact; 6386 Baylor's
# contact is restored from test pin b989a847 by the UP-11 cleanup, so its kept
# answer R_j1xG6QD0Gw1G3uU is matched too.
EXPECTED_NOW_MATCHED = {'R_0U4XyfXUNDttX9a', 'R_hv0cc021NGKRc5M', 'R_h6cnt2kXgSK5Bbg',
                        'R_ju3Amx8yBiJ45L0', 'R_5oBDIEcTfYUvj8n', 'R_6Nqhz2mzupemk9v',
                        'R_j1xG6QD0Gw1G3uU'}
# coordinate-only links with a different house number: must NOT be matched
FORBIDDEN_LINKS = {'R_36hwtQ5ZQOhBucE': '6306', 'R_mT2CaA2cdWYOmij': '6376'}
EXPECTED_MATCHED_CONTACTS = 85   # 86 - 6 earlier - 2 forbidden + 6 kept + restored Baylor;
                                 # confirm against the UP-12 R7 dry run, never < 84
EXPECTED_ANALYSED = 106
TEST_PIN_IDS = {
    '081751dd-70b5-475b-ad0b-f56769230d1f', '1098e13e-9264-4e1c-b392-3fe13335d6a5',
    '145d226d-af10-4088-a5a5-0e2f3b1bf2a7', '194f5430-188d-4d89-8cf6-101fcfc164e6',
    '28ac7696-c791-4d51-ad3e-da4aa1342eb6', '2b48e25a-726f-4f1a-b520-4676c984eae5',
    '39fff2dc-7aa2-47ad-94e4-17263328941b', '417339c1-f4a2-4a88-a1ad-4d4078d4ebfe',
    '56663918-c490-4d60-b5f1-5667ea091c23', '5a647954-148d-4adf-964a-a3a63b0eaeb8',
    '6baf055f-bc8f-4b59-85d5-1241d79e9ad9', '6ca63e1c-5c0f-43ce-b959-41e379b92329',
    '6ca991bd-9fb1-4295-aba5-fcbd526f9b5b', '70759c69-225a-4fbc-8404-cdc51e66ab17',
    '71208ddd-1595-4da8-91d4-5419e5ffe716', '89db8de6-59be-4b4d-85b8-7f0937becff7',
    '93f31699-650a-4d31-80f3-1f10234459d2', '95236d0b-e154-41c8-bac4-2a5d27f0387d',
    '956ff214-8501-4754-87e9-c4a6e5cf3a9f', 'b989a847-2d01-4121-ad7c-9eedff36fd38',
    'ba74b8fe-bc09-46b0-b6d8-c0c5fa49816e', 'c3711341-ed90-45a5-bc55-2886d539c518',
    'c902d618-c2cf-40f2-9b6d-23667e12a002', 'cb4783e1-b9af-4110-a5d2-8f2bcd785feb',
    'd082063a-d9de-43dc-b1c2-06ab2e015b87', 'd671b9ef-2db8-4f08-94c9-29321ec7c25a',
    'e31020f0-384a-40d0-b4b3-78c2705c5620', 'ec1db343-7c4a-4df6-b58a-51149fffea41'}
# popup fields read from the QID42 water matrix: a non-empty CSV cell must
# never reach the popup as an empty value (the "none" -> "—" bug)
WATER_FIELDS = {'leakage_roof': 'QID42_1', 'leakage_walls': 'QID42_2',
                'leakage_windows': 'QID42_3', 'leakage_floor': 'QID42_4'}


def house_no(s) -> str | None:
    m = re.match(r'\s*(\d+)', str(s or ''))
    return m.group(1) if m else None


def metres(a, b) -> float:
    la1, lo1, la2, lo2 = map(math.radians, (a[1], a[0], b[1], b[0]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371000 * math.asin(math.sqrt(h))


def load_csv(path):
    with open(path, encoding='utf-8-sig') as fh:
        rows = list(csv.reader(fh))
    imp = [json.loads(c).get('ImportId') for c in rows[2]]
    col = {k: i for i, k in enumerate(imp)}
    return {r[col['_recordId']]: {k: r[i].strip() for k, i in col.items() if k} for r in rows[3:]}


def dispositions(R: dict, placed: set, superseded: dict) -> dict:
    out = {}
    for rid, r in R.items():
        if r['finished'] != '1':
            out[rid] = 'unfinished'
        elif r['status'] in PREVIEW_STATUSES:
            out[rid] = 'preview'
        elif rid not in placed:
            out[rid] = 'unplaced'
        elif rid in superseded:
            out[rid] = 'superseded'
        else:
            out[rid] = 'analysed'
    return out


def check(R, iaq, contacts, field_rows):
    fails, info = [], {}
    geo = iaq['geojson']
    feats = list(geo.get('features') or [])
    held = list(geo.get('superseded_features') or [])
    held_ids = {f['properties']['response_id'] for f in held}
    P = {f['properties']['response_id']: f['properties'] for f in feats + held}
    drawn = {f['properties']['response_id'] for f in feats
             if not f['properties'].get(SUPERSEDED_KEY) and not f['properties'].get('superseded')}
    flagged = {k: p.get(SUPERSEDED_KEY) for k, p in P.items()
               if k in held_ids or p.get(SUPERSEDED_KEY) or p.get('superseded')}
    placed = set(P) | set(EXPECTED_SUPERSEDED)       # superseded may be absent from the geojson
    disp = dispositions(R, placed, EXPECTED_SUPERSEDED)
    cnt = collections.Counter(disp.values())
    info['dispositions'] = dict(cnt)

    def expect(name, got, want):
        if got != want:
            fails.append(f'{name}: got {got!r}, want {want!r}')

    expect('csv rows', len(R), 137)
    expect('unfinished', {k for k, d in disp.items() if d == 'unfinished'}, EXPECTED_UNFINISHED)
    expect('preview', {k for k, d in disp.items() if d == 'preview'}, EXPECTED_PREVIEW)
    expect('unplaced', {k for k, d in disp.items() if d == 'unplaced'}, EXPECTED_UNPLACED)
    expect('analysed count', cnt['analysed'], EXPECTED_ANALYSED)
    expect('drawn ids', drawn, {k for k, d in disp.items() if d == 'analysed'})
    expect('superseded flags kept in blob', flagged, {k: v for k, v in EXPECTED_SUPERSEDED.items() if k in P})
    a = iaq.get('analysis') or {}
    expect('analysis.n_responses', a.get('n_responses'), EXPECTED_ANALYSED)
    val = a.get('validation') or iaq.get('validation') or {}
    expect('validation.completed_in_csv', val.get('completed_in_csv'), 126)
    expect('validation.dropped_no_geocode', val.get('dropped_no_geocode'), 12)
    expect('validation.charted_pct_of_completed', val.get('charted_pct_of_completed'), 90.5)
    info['coord_source'] = dict(collections.Counter(P[k].get('coord_source') for k in drawn))
    expect('coord_source sums to drawn', sum(info['coord_source'].values()), len(drawn))

    # popup water-matrix cells
    for rid in sorted(drawn):
        for prop, qcol in WATER_FIELDS.items():
            cell = R.get(rid, {}).get(qcol)
            if cell and not str(P[rid].get(prop) or '').strip():
                fails.append(f'popup {rid}.{prop}: CSV has {cell!r}, popup value empty')

    # contacts
    cf = contacts['features']
    canvass = [f['properties'] for f in cf if f['properties'].get('source') != 'field']
    pins = [f['properties'] for f in cf if f['properties'].get('source') == 'field']
    matched = [c for c in canvass if c.get('match_status') == 'matched' and c.get('iaq_response_id')]
    expect('matched canvass contacts', len(matched), EXPECTED_MATCHED_CONTACTS)
    linked = {c['iaq_response_id'] for c in matched}
    for c in matched:
        rid = c['iaq_response_id']
        if rid in EXPECTED_SUPERSEDED:
            fails.append(f"contact {c.get('id')} linked to superseded {rid}")
        typed = house_no(R.get(rid, {}).get('QID225_TEXT'))
        own = house_no(c.get('address'))
        if own and typed and own != typed:
            fails.append(f"contact {c.get('id')} ({c.get('address')}) linked to {rid} typed {typed}")
    for rid, hn in FORBIDDEN_LINKS.items():
        if any(c['iaq_response_id'] == rid and house_no(c.get('address')) == hn for c in matched):
            fails.append(f'forbidden coordinate-only link still present: {rid} <-> {hn}')
    missing = EXPECTED_NOW_MATCHED - linked
    if missing:
        fails.append(f'kept second submissions not matched: {sorted(missing)}')
    for rid in sorted(drawn):
        if rid in linked and P[rid].get('match_status') != 'matched':
            fails.append(f"iaq {rid} linked by a contact but match_status={P[rid].get('match_status')}")

    # field pins
    table_ids = {str(r['id']) for r in field_rows}
    blob_ids = {str(p.get('field_point_id')) for p in pins}
    expect('blob field pins == table rows', blob_ids, table_ids)
    left = blob_ids & TEST_PIN_IDS
    if left:
        fails.append(f'test pins still in blob: {sorted(left)}')
    G = {f['properties']['response_id']: f['geometry']['coordinates'] for f in feats}
    for f in cf:
        p = f['properties']
        rid = p.get('iaq_response_id')
        here = (f.get('geometry') or {}).get('coordinates')
        if p.get('source') != 'field' or not rid or not here or rid not in G or rid not in drawn:
            continue
        nearest = min(drawn, key=lambda k: metres(here, G[k]))
        typed = house_no(R.get(rid, {}).get('QID225_TEXT'))
        if nearest != rid and not (typed and typed in str(p.get('notes') or '')):
            fails.append(f"pin {str(p.get('field_point_id'))[:8]} linked to {rid} "
                         f"({metres(here, G[rid]):.1f} m) but nearest is {nearest} ({metres(here, G[nearest]):.1f} m)")
    for p in pins:
        rid = p.get('iaq_response_id')
        if not rid:
            continue
        pid = str(p.get('field_point_id'))[:8]
        if rid in EXPECTED_SUPERSEDED:
            fails.append(f"pin {pid} linked to superseded {rid}")
        elif rid in P and p.get('iaq_overall_risk') != P[rid].get('overall_risk'):
            fails.append(f"pin {pid} stale risk {p.get('iaq_overall_risk')} != {P[rid].get('overall_risk')}")
    if not P.get('R_bt9KhSC0xqF2xuS', {}).get('iaq_matched'):
        fails.append('R_bt9KhSC0xqF2xuS (linked by real pin 4130a5d7) is not iaq_matched')
    return fails, info


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--csv', required=True)
    ap.add_argument('--snap', required=True, help='folder written by launch_snapshot.py')
    a = ap.parse_args(argv)
    snap = Path(a.snap)
    R = load_csv(a.csv)
    with open(snap / 'dd_iaq_survey.json') as fh:
        iaq = json.load(fh)['payload']
    with open(snap / 'dd_community_contact.json') as fh:
        contacts = json.load(fh)['payload']
    with open(snap / 'field_survey_points.json') as fh:
        field_rows = json.load(fh)
    fails, info = check(R, iaq, contacts, field_rows)
    print(json.dumps(info, indent=1))
    for f in fails:
        print('FAIL', f)
    print(f'{len(fails)} failure(s)')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
