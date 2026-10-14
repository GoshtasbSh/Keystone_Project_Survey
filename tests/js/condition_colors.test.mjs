// Home Condition doughnut: colour follows the label, never the key order of
// housing.conditions (first-seen order, and JSONB reorders keys by length).
import test from 'node:test';
import assert from 'node:assert/strict';
import { loadPure, readSource } from './load_pure.mjs';

const { conditionChartSeries, CONDITION_COLORS } = loadPure(['conditionChartSeries', 'CONDITION_COLORS']);

test('October key order (Fair, Good, Poor, Excellent) still gets meaning-based colours', () => {
  const s = conditionChartSeries({ Fair: 31, Good: 37, Poor: 19, Excellent: 19 });
  assert.deepEqual(s.labels, ['Excellent', 'Good', 'Fair', 'Poor']);
  assert.deepEqual(s.data, [19, 37, 31, 19]);
  assert.deepEqual(s.colors, s.labels.map(l => CONDITION_COLORS[l]));
  assert.equal(CONDITION_COLORS.Excellent, '#10b981');   // green
  assert.equal(CONDITION_COLORS.Critical, '#ef4444');    // red
});

test('a 5th and 6th bucket (Critical, Unknown) get their own colours; unknown keys go grey', () => {
  const s = conditionChartSeries({ Unknown: 2, Critical: 1, Good: 3, Weird: 4 });
  assert.deepEqual(s.labels, ['Good', 'Critical', 'Unknown', 'Weird']);
  assert.equal(new Set(s.colors.slice(0, 3)).size, 3);
  assert.ok(s.colors.every(Boolean));
  assert.equal(s.colors[3], CONDITION_COLORS.Unknown);
});

test('empty or missing input gives empty series', () => {
  assert.deepEqual(conditionChartSeries(undefined), { labels: [], data: [], colors: [] });
});

test('the rc-cond chart uses the series, not positional colours', () => {
  const src = readSource('static/js/dashboard.js');
  const i = src.indexOf("mk('rc-cond'");
  assert.ok(i > 0);
  assert.ok(/conditionChartSeries\(/.test(src.slice(i - 300, i + 400)));
});
