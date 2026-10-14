import test from 'node:test';
import assert from 'node:assert/strict';
import { loadPure, readSource } from './load_pure.mjs';

const H = loadPure(['splitExcludedDuplicates']);
const pt = (lon, lat, properties) => ({ type: 'Feature', geometry: { type: 'Point', coordinates: [lon, lat] }, properties });

test('kept row lists the earlier answer; dates come from superseded_features (6255 Dennison)', () => {
  const kept = pt(-82, 29.78, { response_id: 'R_h6cnt2kXgSK5Bbg', household_responses: 2,
                                superseded_response_ids: ['R_6s0PVusMDUucFQY'] });
  const early = pt(-82, 29.78, { response_id: 'R_6s0PVusMDUucFQY', superseded: true,
                                 superseded_by: 'R_h6cnt2kXgSK5Bbg', recorded_date: '2026-01-29 10:00:00' });
  const solo = pt(-82.01, 29.79, { response_id: 'R_solo' });
  const s = H.splitExcludedDuplicates([kept, solo], [early]);
  assert.deepEqual(s.drawn, [kept, solo]);
  assert.deepEqual(s.excluded, [early]);
  assert.equal(s.redirect.get('R_6s0PVusMDUucFQY'), 'R_h6cnt2kXgSK5Bbg');
  assert.deepEqual(s.earlierByKept.get('R_h6cnt2kXgSK5Bbg'),
    [{ response_id: 'R_6s0PVusMDUucFQY', recorded_date: '2026-01-29 10:00:00' }]);
});

test('a superseded row left in features is still not drawn', () => {
  const s = H.splitExcludedDuplicates([pt(0, 0, { response_id: 'R_e', superseded: true, superseded_by: 'R_k' }),
                                       pt(0, 0, { response_id: 'R_k' })]);
  assert.equal(s.drawn.length, 1);
  assert.equal(s.redirect.get('R_e'), 'R_k');
});

test('no duplicates → nothing changes', () => {
  const f = [pt(0, 0, { response_id: 'R_a' })];
  const s = H.splitExcludedDuplicates(f);
  assert.deepEqual(s.drawn, f);
  assert.equal(s.excluded.length, 0);
});

test('every server load of IAQ points applies the rule', () => {
  const src = readSource('static/js/dashboard.js');
  const re = /\biaqData\s+=\s+([^;]+);/g;
  let m, n = 0;
  while ((m = re.exec(src))) {
    if (m[1].startsWith('null')) continue;
    n++;
    assert.ok(m[1].includes('applyIaqDuplicateRule('), `not wrapped: iaqData = ${m[1]}`);
  }
  assert.equal(n, 3);
  assert.ok(/function resolveMatchedIaqFeature[\s\S]{0,900}_iaqDupRedirect\.get\(/.test(src));
});

test('the IAQ loader reads the server superseded_features list and the popup hides the dedup keys', () => {
  const src = readSource('static/js/dashboard.js');
  assert.ok(src.includes('splitExcludedDuplicates(feats, fc.superseded_features || [])'));
  assert.ok(src.includes("'superseded', 'superseded_by', 'superseded_response_ids', 'household_responses',"));
  assert.ok(!src.includes('dup_excluded'), 'old dup_* names are still read');
});
