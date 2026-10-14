import test from 'node:test';
import assert from 'node:assert/strict';
import { readSource } from './load_pure.mjs';

const src = readSource('static/js/dashboard.js');

test('matching and household internals never render as survey answers', () => {
  const m = src.match(/const _IAQ_NON_ANSWER_FIELDS = new Set\((\[[\s\S]*?\])\);/);
  assert.ok(m, '_IAQ_NON_ANSWER_FIELDS not found');
  const set = new Set(new Function(`return ${m[1]};`)());
  for (const k of ['house_number', 'recorded_date', 'match_review', 'match_review_note',
                   'household_responses', 'superseded_response_ids', 'superseded',
                   'superseded_by', 'restored_from_field_pin']) {
    assert.ok(set.has(k), `${k} would show under "Other exported fields"`);
  }
});

test('a house-number mismatch shows a needs-review note (6306/6318 Amherst, 6376/6378 Antioch)', () => {
  const body = src.slice(src.indexOf('function buildSurveyAnswersTab('), src.indexOf('function buildParcelTab('));
  assert.ok(body.includes("props.match_review === 'house_number_mismatch'"));
  assert.ok(body.includes('escapeHtml(props.match_review_note'));
  assert.ok(body.includes('${reviewNote}'));
});
