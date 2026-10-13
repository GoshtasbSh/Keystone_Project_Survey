// Loads the PURE-HELPERS block of static/js/dashboard.js into node so the
// browser-free helpers can be unit-tested without a DOM, MapLibre or a
// bundler. Evaluated with `new Function` (same realm, so deepStrictEqual
// works on the arrays/Sets it returns). Only our own repo file is evaluated.
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const BEGIN = '// ==== PURE-HELPERS BEGIN';
const END = '// ==== PURE-HELPERS END';

export function readSource(rel) {
  return readFileSync(path.join(ROOT, rel), 'utf8');
}

export function loadPure(names) {
  const src = readSource('static/js/dashboard.js');
  const i = src.indexOf(BEGIN);
  const j = src.indexOf(END);
  if (i < 0 || j < i) throw new Error('PURE-HELPERS markers not found in static/js/dashboard.js');
  const block = src.slice(i, j);
  // eslint-disable-next-line no-new-func
  return new Function(`"use strict";\n${block}\nreturn { ${names.join(', ')} };`)();
}

export function loadJson(p) {
  return JSON.parse(readFileSync(p, 'utf8'));
}
