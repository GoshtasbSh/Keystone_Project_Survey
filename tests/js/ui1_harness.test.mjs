import test from 'node:test';
import assert from 'node:assert/strict';
import { loadPure, readSource } from './load_pure.mjs';

const H = loadPure(['formatIaqAnswerCell']);

test('formatIaqAnswerCell keeps existing behaviour', () => {
  assert.deepEqual(H.formatIaqAnswerCell('has_mold', true), { text: 'Yes', muted: false });
  assert.deepEqual(H.formatIaqAnswerCell('has_mold', 0), { text: 'No', muted: false });
  assert.deepEqual(H.formatIaqAnswerCell('x', null), { text: '—', muted: true });
  assert.deepEqual(H.formatIaqAnswerCell('x', '  '), { text: '—', muted: true });
  assert.deepEqual(H.formatIaqAnswerCell('x', 'Click to write Choice 5'),
    { text: 'Click to write Choice 5 (Qualtrics placeholder)', muted: true });
  assert.deepEqual(H.formatIaqAnswerCell('x', 'Often'), { text: 'Often', muted: false });
});

test('formatIaqAnswerCell is defined once (moved, not copied)', () => {
  const src = readSource('static/js/dashboard.js');
  assert.equal(src.match(/function formatIaqAnswerCell\(/g).length, 1);
  assert.equal(src.match(/const _IAQ_PLACEHOLDER_RE =/g).length, 1);
});
