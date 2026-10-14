import test from 'node:test';
import assert from 'node:assert/strict';
import { loadPure, readSource } from './load_pure.mjs';

const H = loadPure(['isFieldCopy', 'partitionFieldCopies', 'countUnifiedStatuses', 'countMatchGroups']);
const pt = (lon, lat, properties) => ({ type: 'Feature', geometry: { type: 'Point', coordinates: [lon, lat] }, properties });

test('field copies whose pin is gone are never kept (deleted test pins)', () => {
  const contact = pt(-82, 29.78, { status: 'Completed', address: '1 A St' });
  const live = pt(-82.001, 29.781, { source: 'field', field_point_id: 'live-1', status: 'Completed' });
  const dead = pt(-82.3, 29.65, { source: 'field', field_point_id: 'b989a847-test', status: 'Completed', has_iaq_survey: true });
  const r = H.partitionFieldCopies([contact, live, dead], [], new Set(['live-1']));
  assert.deepEqual(r.kept, [contact, live]);
  assert.deepEqual(r.stale, [dead]);
  assert.equal(r.changed, true);
  assert.equal(H.partitionFieldCopies([contact, live], [], new Set(['live-1'])).changed, false);
});

test('a parked copy comes back once its pin appears, without duplicating', () => {
  const late = pt(-82, 29.78, { source: 'field', field_point_id: 'new-9' });
  const r1 = H.partitionFieldCopies([late], [], new Set());
  assert.deepEqual(r1.kept, []);
  const r2 = H.partitionFieldCopies([], r1.stale, new Set(['new-9']));
  assert.deepEqual(r2.kept, [late]);
  assert.equal(r2.changed, true);
  assert.equal(H.partitionFieldCopies([late], [late], new Set(['new-9'])).kept.length, 1);
});

test('unified status counts: a field copy never double-counts its own pin', () => {
  const pin = pt(-82.0000, 29.7800, { id: 'p1', status: 'Completed' });
  const csv = pt(-82.0001, 29.7800, { status: 'Left Info' });          // ~10 m away, grabs the pin first
  const copy = pt(-82.0000, 29.7800, { source: 'field', field_point_id: 'p1', status: 'Completed' });
  assert.deepEqual(H.countUnifiedStatuses([csv, copy], [pin], true), { Completed: 1 });
  // Before the live list has loaded, the copy stands in for the pin.
  assert.deepEqual(H.countUnifiedStatuses([csv, copy], [], false), { 'Left Info': 1, Completed: 1 });
});

test('match legend ignores field copies and excluded duplicates', () => {
  const c = H.countMatchGroups(
    [pt(0, 0, { match_status: 'matched' }), pt(0, 0, { match_status: 'contact_only' }),
     pt(0, 0, { source: 'field', field_point_id: 'x', match_status: 'contact_only' })],
    [pt(0, 0, { match_status: 'iaq_only' }), pt(0, 0, { match_status: 'iaq_only', superseded: true, superseded_by: 'R_k' }),
     pt(0, 0, { match_status: 'matched' })]);
  assert.deepEqual(c, { matched: 1, contact_only: 1, iaq_only: 1 });
});

test('every server load of contacts is pruned before it is drawn', () => {
  const src = readSource('static/js/dashboard.js');
  const re = /surveyData\s*=\s*(await\s+(_safeJson|safe)\(ptsRes|pts;)/g;
  let m, n = 0;
  while ((m = re.exec(src))) {
    n++;
    assert.ok(src.slice(m.index, m.index + 200).includes('pruneStaleFieldCopies()'),
      `no prune right after: ${src.slice(m.index, m.index + 60)}`);
  }
  assert.equal(n, 4);
  assert.ok(/function stampCoincidentContacts\(\)\s*\{\s*const pruned = pruneStaleFieldCopies\(\);/.test(src));
  assert.ok(src.includes('return countUnifiedStatuses(surveyData?.features, fieldPointsData?.features, _fieldPointsAuthoritative);'));
});
