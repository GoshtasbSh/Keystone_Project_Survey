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

test('skirting card no longer claims skip-logic (all 114 answered)', () => {
  assert.ok(!src.includes('responses (skip-logic)'));
});

test('every stored free-text field has a place in the popup', () => {
  const expected = {
    mold_locations: 'Indoor Air Quality',
    mold_other: 'Indoor Air Quality',
    cooking_other: 'Indoor Air Quality',
    housing_type_other: 'Structural & Housing Type',
    ownership_other: 'Structural & Housing Type',
    afford_strategy_other: 'Residency & Affordability',
    reloc_factor_oth_text: 'Relocation Factors',
    hurricane_transport_other: 'Well-being & Mobility',
  };
  for (const [k, title] of Object.entries(expected)) {
    assert.equal(categoryOf(k), title, `${k} should render under ${title}`);
  }
});
