import test from 'node:test';
import assert from 'node:assert/strict';
import { loadPure } from './load_pure.mjs';

const H = loadPure(['formatIaqAnswerCell']);

// R_hW4D1SHXd37YIjC typed "No answer" into the free-text years_in_hre box.
// That is the respondent's own non-answer, not a Qualtrics export placeholder.
test('a typed non-answer is muted but not tagged as a Qualtrics placeholder', () => {
  assert.deepEqual(H.formatIaqAnswerCell('years_in_hre', 'No answer'), { text: 'No answer', muted: true });
  for (const raw of ['no answer', 'N/A', 'n/a', 'NA', '--', '-', 'Skipped', 'skip']) {
    const out = H.formatIaqAnswerCell('years_in_hre', raw);
    assert.equal(out.muted, true, `${raw} should be muted`);
    assert.equal(out.text, raw, `${raw} should be shown as typed`);
    assert.ok(!/placeholder/i.test(out.text), `${raw} must not be called a Qualtrics placeholder`);
  }
});

test('real Qualtrics export placeholders keep the tag', () => {
  for (const raw of ['Click to write Choice 5', 'click to write choice 12', 'Click to write Scale point 3']) {
    assert.deepEqual(H.formatIaqAnswerCell('x', raw), { text: `${raw} (Qualtrics placeholder)`, muted: true });
  }
});

test('ordinary answers stay unmuted and untagged', () => {
  assert.deepEqual(H.formatIaqAnswerCell('years_in_hre', '12'), { text: '12', muted: false });
  assert.deepEqual(H.formatIaqAnswerCell('x', 'None'), { text: 'None', muted: false });
  assert.deepEqual(H.formatIaqAnswerCell('x', 'No answer given by tenant, owner says 5'),
    { text: 'No answer given by tenant, owner says 5', muted: false });
});
