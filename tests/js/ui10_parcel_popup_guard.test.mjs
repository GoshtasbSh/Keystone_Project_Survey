import test from 'node:test';
import assert from 'node:assert/strict';
import { loadPure, readSource } from './load_pure.mjs';

const H = loadPure(['PARCEL_POPUP_SUPPRESSING_LAYERS']);
const src = readSource('static/js/dashboard.js');

// Every layer id that has a map.on('click', <id>, ...) handler, both the
// literal form and the `[...].forEach(id => map.on('click', id, ...))` form.
function clickableLayerIds(code) {
  const ids = new Set();
  for (const m of code.matchAll(/map\.on\(\s*'click'\s*,\s*'([^']+)'/g)) ids.add(m[1]);
  for (const m of code.matchAll(/\[([^\]]*)\]\.forEach\(\s*(\w+)\s*=>\s*\{([\s\S]*?)\n\s*\}\);/g)) {
    const [, list, v, body] = m;
    if (!new RegExp(`map\\.on\\(\\s*'click'\\s*,\\s*${v}\\b`).test(body)) continue;
    for (const id of list.matchAll(/'([^']+)'/g)) ids.add(id[1]);
  }
  return ids;
}

test('the scan finds the known click layers (guards the scanner itself)', () => {
  const ids = clickableLayerIds(src);
  for (const id of ['parcels-fill', 'survey-points', 'field-points-dots', 'iaq-points', 'iaq-points-g1']) {
    assert.ok(ids.has(id), `scanner missed ${id}`);
  }
});

test('every clickable point layer suppresses the parcel popup underneath it', () => {
  const guard = new Set(H.PARCEL_POPUP_SUPPRESSING_LAYERS);
  const missing = [...clickableLayerIds(src)].filter(id => id !== 'parcels-fill' && !guard.has(id));
  assert.deepEqual(missing, [], `clicking these opens the parcel popup too: ${missing.join(', ')}`);
  assert.ok(guard.has('field-points-dots'), 'clicking a field pin must not open the parcel popup');
  assert.ok(!guard.has('parcels-fill'), 'the parcel layer must not suppress itself');
});

test('onParcelClick checks the named guard list', () => {
  const body = src.slice(src.indexOf('function onParcelClick('), src.indexOf('function onClusterClick('));
  assert.ok(body.length > 0);
  assert.ok(body.includes('PARCEL_POPUP_SUPPRESSING_LAYERS.filter('), 'onParcelClick must use the shared constant');
});
