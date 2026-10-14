import test from 'node:test';
import assert from 'node:assert/strict';
import { loadPure, readSource } from './load_pure.mjs';

const H = loadPure(['splitExcludedDuplicates']);
const pt = (lon, lat, properties) => ({ type: 'Feature', geometry: { type: 'Point', coordinates: [lon, lat] }, properties });

test('earlier responses are not drawn and redirect to the kept one (6255 Dennison)', () => {
  const early = pt(-82, 29.78, { response_id: 'R_6s0PVusMDUucFQY', dup_excluded: true, dup_kept_response_id: 'R_h6cnt2kXgSK5Bbg', recorded_date: '2026-01-29' });
  const kept = pt(-82, 29.78, { response_id: 'R_h6cnt2kXgSK5Bbg' });
  const solo = pt(-82.01, 29.79, { response_id: 'R_solo' });
  const s = H.splitExcludedDuplicates([early, kept, solo]);
  assert.deepEqual(s.drawn, [kept, solo]);
  assert.deepEqual(s.excluded, [early]);
  assert.equal(s.redirect.get('R_6s0PVusMDUucFQY'), 'R_h6cnt2kXgSK5Bbg');
  assert.deepEqual(s.earlierByKept.get('R_h6cnt2kXgSK5Bbg'), [{ response_id: 'R_6s0PVusMDUucFQY', recorded_date: '2026-01-29' }]);
});

test('server variant: excluded rows omitted, kept row lists them', () => {
  const s = H.splitExcludedDuplicates([pt(0, 0, { response_id: 'R_k', dup_earlier_response_ids: ['R_e'] })]);
  assert.equal(s.drawn.length, 1);
  assert.equal(s.redirect.get('R_e'), 'R_k');
  assert.equal(s.earlierByKept.get('R_k').length, 1);
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
