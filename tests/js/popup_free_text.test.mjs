// node --test tests/js/popup_free_text.test.mjs
// Pins the popup side of the 2026-10-13 survey fixes without a browser.
// (Ruling C4: the Hospital Visit summary-row test belongs to UI-2, not here.)
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const src = readFileSync(
  fileURLToPath(new URL('../../static/js/dashboard.js', import.meta.url)), 'utf8');

function categories() {
  const m = src.match(/const _IAQ_CATEGORIES = (\[[\s\S]*?\n\]);/);
  assert.ok(m, '_IAQ_CATEGORIES not found');
  return new Function(`return ${m[1]};`)();
}
function categoryOf(key) {
  return new Map(categories().flatMap(([t, ks]) => ks.map(k => [k, t]))).get(key);
}

test('the specific hospital choice is listed under Health', () => {
  assert.equal(categoryOf('hospital_visit_detail'), 'Health & Symptoms');
});
