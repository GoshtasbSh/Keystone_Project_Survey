// Run the dashboard's own address search (sliced from static/js/dashboard.js)
// over the reviewer checklist addresses and require every one to be found at
// its house.
//
// usage: node scripts/audit/search_check.js "<snapshot dir>" <parcels_api.json> <checklist.json>
//   checklist.json: [[checkId, query, lon, lat], ...]  (53 rows, from scratchpad/email/q2.json)
// Exit 0 = every address returns >= 1 result whose label has the same house
// number and that lies within MAX_M metres of the checklist point.
//
// Offline harness: `eval` runs only the repo's own committed dashboard.js
// source, never input data.
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const MAX_M = 40;     // field pins sit up to 35 m from their parcel centroid
const src = fs.readFileSync(path.join(ROOT, 'static/js/dashboard.js'), 'utf8');
const a = src.indexOf('// ── Address search'), b = src.indexOf('let _searchSelection = null;');
if (a < 0 || b < 0) throw new Error('address-search markers not found in dashboard.js');

const [snap, parcelsPath, listPath] = process.argv.slice(2);
// Globals the sliced search code reads.
const ORPHAN_FALLBACK_ADDR = 'Address not on file';       // eslint-disable-line no-unused-vars
let surveyData = JSON.parse(fs.readFileSync(path.join(snap, 'dd_community_contact.json'))).payload;  // eslint-disable-line prefer-const
let parcelsData = JSON.parse(fs.readFileSync(parcelsPath));                                          // eslint-disable-line prefer-const
let iaqData = JSON.parse(fs.readFileSync(path.join(snap, 'dd_iaq_survey.json'))).payload.geojson;   // eslint-disable-line prefer-const
// eslint-disable-next-line no-eval
eval(src.slice(a, b) + ';globalThis.searchAddresses=searchAddresses;');

const houseNo = (s) => (String(s || '').match(/^\s*(\d+)/) || [])[1];
const rows = JSON.parse(fs.readFileSync(listPath));
const fails = [];
for (const [id, q, lon, lat] of rows) {
  const r = searchAddresses(q);
  const t = r[0];
  const d = t ? Math.hypot((t.coords[0] - lon) * 96000, (t.coords[1] - lat) * 111000) : null;
  if (!t) fails.push(`${id} "${q}": no result`);
  else if (houseNo(t.label) !== houseNo(q)) fails.push(`${id} "${q}": top result "${t.label}"`);
  else if (d > MAX_M) fails.push(`${id} "${q}": top result ${Math.round(d)} m away`);
}
fails.forEach((x) => console.log('FAIL', x));
console.log(`${rows.length - fails.length}/${rows.length} addresses found at their house`);
process.exit(fails.length ? 1 : 0);
