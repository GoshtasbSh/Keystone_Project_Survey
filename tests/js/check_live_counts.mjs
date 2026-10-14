// Read-only check of the legend numbers against saved API responses.
// Usage:
//   node tests/js/check_live_counts.mjs survey-points.json field-points.json iaq-points.json
// The three files are saved, member-authenticated responses of
// /api/survey-points, /api/field-points and /api/iaq-points?full=1.
// Prints the numbers the sidebar legends will show and exits 1 when an
// invariant is broken. It never writes anything.
import { loadPure, loadJson } from './load_pure.mjs';

const [spPath, fpPath, iaqPath] = process.argv.slice(2);
if (!spPath || !fpPath || !iaqPath) {
  console.error('usage: check_live_counts.mjs survey-points.json field-points.json iaq-points.json');
  process.exit(2);
}
const names = ['partitionFieldCopies', 'countUnifiedStatuses', 'countMatchGroups', 'isFieldCopy'];
let H;
try { H = loadPure([...names, 'splitExcludedDuplicates']); } catch { H = loadPure(names); }
const sp = loadJson(spPath).features;
const fp = loadJson(fpPath).features;
const iaq = loadJson(iaqPath).features;

const liveIds = new Set(fp.map(f => String(f.properties.id)));
const { kept, stale } = H.partitionFieldCopies(sp, [], liveIds);
const { drawn, excluded } = H.splitExcludedDuplicates
  ? H.splitExcludedDuplicates(iaq) : { drawn: iaq, excluded: [] };
const status = H.countUnifiedStatuses(kept, fp, true);
const groups = H.countMatchGroups(kept, drawn);
const total = Object.values(status).reduce((s, n) => s + n, 0);
const csvContacts = kept.filter(f => !H.isFieldCopy(f.properties));
const completedCsv = csvContacts.filter(f => f.properties.status === 'Completed').length;
const iaqMatched = drawn.filter(f => f.properties.match_status === 'matched').length;

console.log(JSON.stringify({
  stale_field_copies_hidden: stale.map(f => f.properties.field_point_id),
  iaq_drawn: drawn.length, iaq_excluded_earlier: excluded.length,
  status_counts: status, status_total: total, match_groups: groups,
}, null, 2));

const errors = [];
if (stale.some(f => liveIds.has(String(f.properties.field_point_id)))) errors.push('a live pin was hidden');
if (groups.matched + groups.contact_only !== completedCsv)
  errors.push(`matched+contact_only (${groups.matched + groups.contact_only}) != Completed CSV contacts (${completedCsv})`);
if (groups.iaq_only + iaqMatched !== drawn.length)
  errors.push(`iaq_only+matched IAQ (${groups.iaq_only + iaqMatched}) != drawn IAQ (${drawn.length})`);
if (total > csvContacts.length + fp.length) errors.push('status total exceeds contacts + live pins');
if (errors.length) { console.error('FAIL:\n  ' + errors.join('\n  ')); process.exit(1); }
console.log('OK: legend invariants hold');
