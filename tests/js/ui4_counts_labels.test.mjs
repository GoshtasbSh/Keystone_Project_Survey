import test from 'node:test';
import assert from 'node:assert/strict';
import { loadPure, readSource } from './load_pure.mjs';

const H = loadPure(['responseCountsSummary']);

test('after the dedup rule: 106 households from 114 responses', () => {
  assert.deepEqual(
    H.responseCountsSummary({ n_responses: 106, n_households: 106, n_mapped_responses: 114, n_duplicates_excluded: 8 }, {}),
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
