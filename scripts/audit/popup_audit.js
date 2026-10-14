// Render the member "Survey Answers" popup tab for EVERY drawn survey feature
// with the dashboard's own code (sliced from static/js/dashboard.js) and scan
// the visible text for anything a reader should never see.
//
// usage: node scripts/audit/popup_audit.js "<snapshot dir>"
//   reads <dir>/dd_iaq_survey.json (full member payload). Exit 0 = clean.
//
// Offline harness: `eval` runs only the repo's own committed dashboard.js
// source, never snapshot data.
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const SUPERSEDED_KEY = 'superseded_by';           // keep in sync with reconcile_responses.py
// Respondents whose typed "1" used to become "Year(s)" (audit Q3 item 1).
const YEARS_ONE = ['R_71LqP7xFx71BPsl', 'R_1LOVKbX2iH6Xh3j', 'R_6xzTr24XxYm8KC4', 'R_kVLcdKScFHPgWVR',
  'R_2jh8CoISTKs6UKv', 'R_m7ABYoFMDa7R15C', 'R_l2K5bwgfJ6nwQIN', 'R_eubE9bDo3QIohbh', 'R_iUaZoRCDNkHIsjm'];
const HOSPITAL_BLANK = ['R_5TtaBRz99nWhzm1', 'R_mT2CaA2cdWYOmij'];
const BAD_TEXT = [/\bnan\b/i, /click to write/i, /\bundefined\b/, /\[object Object\]/, /^\s*null\s*$/m];

const src = fs.readFileSync(path.join(ROOT, 'static/js/dashboard.js'), 'utf8');
const sliceFn = (start, end) => {
  const a = src.indexOf(start), b = src.indexOf(end, a);
  if (a < 0 || b < 0) throw new Error(`slice markers not found: ${start} / ${end}`);
  return src.slice(a, b);
};
const escSrc = sliceFn('function escapeHtml(s) {', '\n}\n') + '\n}\n';
const popupSrc = sliceFn('// Internal / non-answer fields stripped', 'function buildParcelTab');

const snap = process.argv[2];
const payload = JSON.parse(fs.readFileSync(path.join(snap, 'dd_iaq_survey.json'))).payload;
// The dashboard's iaqAnalysis is /api/analysis?type=iaq: {loaded, analysis,
// street_stats, validation} with the analysis keys also lifted to the top
// level (api/analysis.py _iaq_analysis_payload). Build the same shape so the
// popup reads survey_questions AND analysis.shared_code_labels as it does live.
const ana = (payload.analysis && typeof payload.analysis === 'object') ? payload.analysis : {};
const iaqAnalysisShape = { loaded: true };
for (const k of ['analysis', 'street_stats', 'validation']) if (k in payload) iaqAnalysisShape[k] = payload[k];
for (const [k, v] of Object.entries(ana)) if (!(k in iaqAnalysisShape)) iaqAnalysisShape[k] = v;

const BEGIN = '// ==== PURE-HELPERS BEGIN', END = '// ==== PURE-HELPERS END';
// UI-1 moved formatIaqAnswerCell (and UI-5/7 helpers) into this block.
const pureSrc = src.includes(BEGIN) ? sliceFn(BEGIN, END) : '';
// Globals buildSurveyAnswersTab reads after UI-7. Empty by default; when the
// pure block has splitExcludedDuplicates (UI-7/GAP-5) they are filled exactly
// as the dashboard's applyIaqDuplicateRule does, so a kept answer's popup
// carries the same "answered N times" note a member sees, and the drawn set
// is the dashboard's own (earlier answers in geojson.superseded_features or
// flagged superseded are never rendered).
const stubs = 'var _iaqDupEarlierByKept = new Map(); var _iaqDupRedirect = new Map();\n';
const fc = payload.geojson || {};
const dupRule = `
if (typeof splitExcludedDuplicates === 'function') {
  const s = splitExcludedDuplicates(fc.features || [], fc.superseded_features || []);
  _iaqDupEarlierByKept = s.earlierByKept; _iaqDupRedirect = s.redirect;
  globalThis.__auditDrawn = s.drawn; globalThis.__auditDupNotes = s.earlierByKept;
}`;
globalThis.iaqAnalysis = iaqAnalysisShape;
// eslint-disable-next-line no-eval
eval(stubs + escSrc + pureSrc + popupSrc + ';globalThis.buildSurveyAnswersTab=buildSurveyAnswersTab;' + dupRule);
const drawn = globalThis.__auditDrawn || (fc.features || []);
const dupNotes = globalThis.__auditDupNotes || new Map();

const text = (html) => html.replace(/<[^>]+>/g, '\n').replace(/&amp;/g, '&').replace(/&#39;/g, "'")
  .replace(/&quot;/g, '"').replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const fails = [];
let n = 0, withNote = 0;
for (const f of drawn) {
  const p = f.properties;
  if (p[SUPERSEDED_KEY]) continue;
  n++;
  if ((dupNotes.get(String(p.response_id || '').trim()) || []).length) withNote++;
  const t = text(buildSurveyAnswersTab(p));
  for (const re of BAD_TEXT) if (re.test(t)) fails.push(`${p.response_id}: popup text matches ${re}`);
  if (YEARS_ONE.includes(p.response_id) && /Year\(s\)/.test(String(p.years_in_hre)))
    fails.push(`${p.response_id}: years_in_hre shows "${p.years_in_hre}"`);
  if (HOSPITAL_BLANK.includes(p.response_id) && /^no$/i.test(String(p.hospital_visit || '')))
    fails.push(`${p.response_id}: blank hospital answer shown as "${p.hospital_visit}"`);
  if (p.response_id === 'R_36hwtQ5ZQOhBucE' && p.has_mold === true)
    fails.push('R_36hwtQ5ZQOhBucE: "no evidence to my knowledge" shown as mold');
}
fails.forEach((x) => console.log('FAIL', x));
console.log(`${withNote} popup(s) carry the repeat-household note`);
console.log(`${n} popups rendered, ${fails.length} failure(s)`);
process.exit(fails.length ? 1 : 0);
