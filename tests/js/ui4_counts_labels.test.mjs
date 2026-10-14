import test from 'node:test';
import assert from 'node:assert/strict';
import { loadPure, readSource } from './load_pure.mjs';

const H = loadPure(['responseCountsSummary']);

test('after the dedup rule: 106 households from 114 responses', () => {
  assert.deepEqual(
    H.responseCountsSummary({ n_responses: 106, n_households: 106, n_responses_mapped: 114 },
                            { repeat_responses_excluded: 8, households_mapped: 106, responses_mapped: 114 }),
    { households: 106, responses: 114, excluded: 8, unit: 'households' });
});

test('old analysis blob (no dedup fields) is labelled as responses', () => {
  assert.deepEqual(H.responseCountsSummary({ n_responses: 114 }, {}),
    { households: 114, responses: 114, excluded: 0, unit: 'responses' });
});

test('labels: no hard-coded "households" sub, no skip-logic caption', () => {
  const src = readSource('static/js/dashboard.js');
  assert.ok(!src.includes('responses (skip-logic)'));
  assert.ok(!src.includes('<div class="sub">households</div>'));
});

test('validation pane lists the repeat responses; Census-placed count includes parcel-snapped', () => {
  const src = readSource('static/js/dashboard.js');
  assert.ok(src.includes('<div class="label">Repeat responses excluded</div>'));
  assert.ok(src.includes("d.coord_source === 'geocoded' || d.coord_source === 'parcel_snapped'"));
  assert.ok(src.includes('Census-placed: ${unmatchedByReason.geocoded}'));
  assert.ok(!src.includes('Address-geocoded'));
});

test('upload summary says households, not responses, once repeats are excluded', () => {
  const src = readSource('static/js/dashboard.js');
  assert.ok(!src.includes('>Responses Placed on Map<'));
  assert.ok(src.includes("${_rc.unit === 'households' ? 'Households' : 'Responses'} Placed on Map"));
});
