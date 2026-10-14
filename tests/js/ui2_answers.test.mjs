import test from 'node:test';
import assert from 'node:assert/strict';
import { loadPure, readSource } from './load_pure.mjs';

const H = loadPure(['formatIaqAnswerCell', 'formatHospitalVisit']);

test('"none" is an answer, shown as None (QID42 water matrix, 323 cells)', () => {
  for (const raw of ['none', 'None', ' NONE ']) {
    assert.deepEqual(H.formatIaqAnswerCell('leakage_roof', raw), { text: 'None', muted: false });
  }
});

test('hospital blank is No answer, never No (R_5TtaBRz99nWhzm1, R_mT2CaA2cdWYOmij)', () => {
  assert.deepEqual(H.formatHospitalVisit(''), { text: 'No answer', tone: 'blank' });
  assert.deepEqual(H.formatHospitalVisit(null), { text: 'No answer', tone: 'blank' });
  assert.deepEqual(H.formatHospitalVisit('yes'), { text: 'Yes', tone: 'yes' });
  assert.deepEqual(H.formatHospitalVisit('no'), { text: 'No', tone: 'no' });
  assert.deepEqual(H.formatHospitalVisit('Yes, emergency room'), { text: 'Yes, emergency room', tone: 'yes' });
  assert.deepEqual(H.formatIaqAnswerCell('hospital_visit', ''), { text: 'No answer', muted: true });
  assert.deepEqual(H.formatIaqAnswerCell('hospital_visit', 'no'), { text: 'No', muted: false });
});

test('summary tab no longer maps every non-yes hospital answer to No', () => {
  const src = readSource('static/js/dashboard.js');
  assert.ok(!src.includes(`p.hospital_visit === 'yes' ? '<span style="color:var(--red)">Yes</span>' : 'No'`));
  assert.ok(src.includes('formatHospitalVisit(p.hospital_visit)'));
});
