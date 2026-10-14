import test from 'node:test';
import assert from 'node:assert/strict';
import { loadPure, readSource } from './load_pure.mjs';

const H = loadPure(['coordSourceBreakdown', 'coordSourceShort']);

test('breakdown adds up to the total (Oct 13 mix: 89 / 23 / 2)', () => {
  const md = [
    ...Array(89).fill({ coord_source: 'address_matched' }),
    ...Array(23).fill({ coord_source: 'parcel_exact' }),
    ...Array(2).fill({ coord_source: 'parcel_snapped' }),
  ];
  const bd = H.coordSourceBreakdown(md);
  assert.equal(bd.total, 114);
  assert.equal(bd.rows.reduce((s, r) => s + r.count, 0), 114);
  assert.deepEqual(bd.rows.map(r => [r.key, r.count]),
    [['address_matched', 89], ['parcel_exact', 23], ['parcel_snapped', 2]]);
  assert.ok(!bd.rows.some(r => /gps/i.test(r.label)));
  assert.equal(H.coordSourceShort(bd), '89 address · 23 parcel · 2 Census→parcel');
});

test('unknown/legacy sources go to Other; excluded duplicates are not counted', () => {
  const bd = H.coordSourceBreakdown([
    { coord_source: 'gps' }, { coord_source: undefined }, { coord_source: 'geocoded' },
    { coord_source: 'parcel_exact', superseded: true, superseded_by: 'R_k' },
  ]);
  assert.equal(bd.total, 3);
  assert.deepEqual(bd.rows.map(r => [r.key, r.count]), [['geocoded', 1], ['other', 2]]);
  assert.equal(H.coordSourceShort({ total: 0, rows: [] }), 'no placement data');
});

test('every tier the server writes has its own row, in a fixed order', () => {
  const bd = H.coordSourceBreakdown([
    { coord_source: 'geocoded' }, { coord_source: 'parcel_fuzzy' }, { coord_source: 'parcel_snapped' },
    { coord_source: 'parcel_exact' }, { coord_source: 'address_matched' }, { coord_source: 'unknown' },
  ]);
  assert.deepEqual(bd.rows.map(r => r.key),
    ['address_matched', 'parcel_exact', 'parcel_fuzzy', 'parcel_snapped', 'geocoded', 'other']);
  assert.equal(bd.total, 6);
  assert.deepEqual(H.coordSourceBreakdown(undefined), { total: 0, rows: [] });
});

test('no GPS wording is left in the UI', () => {
  const src = readSource('static/js/dashboard.js');
  const html = readSource('static/index.html');
  for (const bad of ["coord_source === 'gps'", 'Validating GPS', 'GPS Cross-Validation', ' GPS · ', "labels: ['GPS'", 'GPS (in-field Qualtrics)']) {
    assert.ok(!src.includes(bad), `dashboard.js still contains: ${bad}`);
  }
  for (const bad of ['Validating GPS coordinates', 'housing, GPS coordinates']) {
    assert.ok(!html.includes(bad), `index.html still contains: ${bad}`);
  }
});
