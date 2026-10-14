import test from 'node:test';
import assert from 'node:assert/strict';
import { loadPure, readSource } from './load_pure.mjs';

const H = loadPure(['findFieldLinkedCopy']);
const pt = (lon, lat, properties) => ({ type: 'Feature', geometry: { type: 'Point', coordinates: [lon, lat] }, properties });

test('findFieldLinkedCopy returns the linked blob copy of a pin', () => {
  const copy = pt(-82, 29.78, { source: 'field', field_point_id: '589923fa-x', has_iaq_survey: true, iaq_response_id: 'R_6s0PVusMDUucFQY' });
  const unlinked = pt(-82, 29.78, { source: 'field', field_point_id: 'zzz', has_iaq_survey: false });
  const contact = pt(-82, 29.78, { has_iaq_survey: true, iaq_response_id: 'R_x' });
  assert.equal(H.findFieldLinkedCopy([contact, unlinked, copy], '589923fa-x'), copy);
  assert.equal(H.findFieldLinkedCopy([contact, unlinked, copy], 'zzz'), null);
  assert.equal(H.findFieldLinkedCopy([contact, unlinked, copy], ''), null);
  assert.equal(H.findFieldLinkedCopy(undefined, 'a'), null);
});

test('onFieldPointClick builds a Survey Answers tab, gated to members', () => {
  const src = readSource('static/js/dashboard.js');
  const body = src.slice(src.indexOf('async function onFieldPointClick('), src.indexOf('async function initFieldPoints('));
  assert.ok(body.length > 0, 'onFieldPointClick must be async (awaits refreshMyRole)');
  assert.ok(body.includes("_myRole === 'admin' || _myRole === 'member'"));
  assert.ok(body.includes('findFieldLinkedCopy(surveyData?.features, p.id)'));
  assert.ok(body.includes('resolveMatchedIaqFeature('));
  assert.ok(body.includes("label: 'Survey Answers', content: buildSurveyAnswersTab("));
  assert.ok(body.includes('escapeHtml(p.notes)'), 'notes must stay escaped');
});
