import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { loadPure, readSource, ROOT } from './load_pure.mjs';

const H = loadPure(['sharedCodeLabelState']);

// USER DECISION 2026-10-13: the note "must then not show for any field". A
// missing key (analysis not loaded yet, /api/analysis failed, or a blob
// written before the re-upload) is the decided state, not "unverified".
test('key absent or analysis not loaded → no field flagged (decided state)', () => {
  for (const a of [{}, undefined, null, { shared_code_labels: null }]) {
    const st = H.sharedCodeLabelState(a);
    assert.equal(st.verified, true);
    assert.equal(st.unverified.size, 0);
  }
});

test('only an explicit verified=false from the server flags the default fields', () => {
  assert.deepEqual([...H.sharedCodeLabelState({ shared_code_labels: { verified: false } }).unverified].sort(),
    ['afford_urgency', 'condition', 'mh_skirting']);
});

test('the note no longer promises a pending Qualtrics check', () => {
  assert.ok(!/Pending a check in Qualtrics/.test(readSource('static/js/dashboard.js')));
});

test('server field list wins; verified=true hides every note', () => {
  assert.deepEqual([...H.sharedCodeLabelState({ shared_code_labels: { verified: false, fields: ['condition'] } }).unverified], ['condition']);
  const v = H.sharedCodeLabelState({ shared_code_labels: { verified: true, fields: ['condition'] } });
  assert.equal(v.verified, true);
  assert.equal(v.unverified.size, 0);
});

// USER DECISION 2026-10-13: every shared-code question is resolved
// (QID141 code 1 = Excellent, QID100/QID221 1 = Yes / 2 = No / Not applicable,
// QID17 unchanged), so with the status the server ships no field carries a note.
const SHIPPED_STATUS = {
  resolution: { QID100: 'original_choice', QID141: 'original_choice',
                QID17: 'recoded_choice', QID221: 'original_choice' },
  questions: ['QID100', 'QID141', 'QID17', 'QID221'],
  fields: ['condition', 'afford_urgency', 'mh_skirting'],
  verified: true,
};

test('the decided (shipped) status shows no "label unverified" note on any field', () => {
  const st = H.sharedCodeLabelState({ shared_code_labels: SHIPPED_STATUS });
  assert.equal(st.verified, true);
  for (const f of ['condition', 'afford_urgency', 'mh_skirting']) assert.equal(st.unverified.has(f), false, f);
});

test('the server really ships that status (api/survey_logic.shared_code_status)', (t) => {
  const py = path.join(ROOT, '.venv', 'bin', 'python');
  if (!existsSync(py)) { t.skip('project .venv not present'); return; }
  const r = spawnSync(py, ['-I', '-c',
    'import json, sys; sys.path.insert(0, sys.argv[1]); import survey_logic; '
    + 'print(json.dumps(survey_logic.shared_code_status()))', path.join(ROOT, 'api')],
    { encoding: 'utf8', timeout: 60000 });
  assert.equal(r.status, 0, r.stderr);
  const status = JSON.parse(r.stdout.trim().split('\n').pop());
  assert.deepEqual(status, SHIPPED_STATUS);
  assert.equal(H.sharedCodeLabelState({ shared_code_labels: status }).unverified.size, 0);
});

test('popup and analysis both consult the switch state', () => {
  const src = readSource('static/js/dashboard.js');
  assert.ok(/function buildSurveyAnswersTab[\s\S]{0,600}sharedCodeLabelState\(/.test(src));
  assert.ok(/function buildSurveyResultsTab[\s\S]{0,3000}sharedCodeLabelState\(/.test(src));
});
