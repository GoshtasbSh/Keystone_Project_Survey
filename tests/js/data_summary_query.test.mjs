// DB-6: the Update Data modal (renderDataSummary) must fetch only the three
// blobs it displays, not every keystone_dashboard_data row (analysis,
// survey_points, integrity_metrics are never shown there). Runs the real
// function from static/js/dashboard.js against a fake Supabase client and a
// stub DOM, so the counts it renders are checked too.
import test from 'node:test';
import assert from 'node:assert/strict';
import { loadPure, readSource } from './load_pure.mjs';

function sliceRenderDataSummary() {
  const src = readSource('static/js/dashboard.js');
  const i = src.indexOf('async function renderDataSummary()');
  assert.ok(i >= 0, 'renderDataSummary not found');
  const j = src.indexOf('\n}\n', i);
  return src.slice(i, j + 2);
}

const ROWS = [
  { data_type: 'community_contact', payload: { features: [1, 2, 3], source_filename: 'c.csv' }, updated_at: '2026-10-01T00:00:00Z' },
  { data_type: 'iaq_survey', payload: { geojson: { features: [1, 2] }, source_filename: 'i.csv' }, updated_at: '2026-10-01T00:00:00Z' },
  { data_type: 'parcels', payload: { features: [1, 2, 3, 4] }, updated_at: '2026-10-01T00:00:00Z' },
  { data_type: 'analysis', payload: { big: 'x'.repeat(1000) }, updated_at: '2026-10-01T00:00:00Z' },
  { data_type: 'survey_points', payload: { features: [] }, updated_at: '2026-10-01T00:00:00Z' },
  { data_type: 'integrity_metrics', payload: {}, updated_at: '2026-10-01T00:00:00Z' },
];

function fakeClient(calls) {
  return {
    from(table) {
      calls.push(['from', table]);
      let filter = null;
      const result = () => ({
        data: ROWS.filter(r => !filter || filter.includes(r.data_type)),
        error: null,
      });
      const builder = {
        select(cols) { calls.push(['select', cols]); return builder; },
        in(col, vals) { calls.push(['in', col, [...vals]]); filter = vals; return builder; },
        then(resolve, reject) { return Promise.resolve(result()).then(resolve, reject); },
      };
      return builder;
    },
  };
}

function stubDom() {
  const els = {};
  const el = () => ({ textContent: '', classList: { add() {}, remove() {} } });
  return {
    els,
    document: {
      getElementById(id) { return (els[id] ||= el()); },
      querySelector() { return el(); },
    },
  };
}

test('Update Data modal fetches only community_contact, iaq_survey and parcels', async () => {
  const calls = [];
  const { els, document } = stubDom();
  // eslint-disable-next-line no-new-func
  const render = makeRender(fakeClient(calls), document, {}, false);
  await render();

  const inCalls = calls.filter(c => c[0] === 'in');
  assert.equal(inCalls.length, 1, `expected one .in() filter, got ${JSON.stringify(calls)}`);
  assert.equal(inCalls[0][1], 'data_type');
  assert.deepEqual([...inCalls[0][2]].sort(), ['community_contact', 'iaq_survey', 'parcels']);
  assert.deepEqual(calls.find(c => c[0] === 'select'), ['select', 'data_type, payload, updated_at']);

  // Same counts as before the filter.
  assert.equal(els['ds-community-count'].textContent, (3).toLocaleString());
  assert.equal(els['ds-iaq-count'].textContent, (2).toLocaleString());
  assert.equal(els['ds-parcels-count'].textContent, (4).toLocaleString());
  assert.equal(els['ds-iaq-file'].textContent, 'i.csv');
});

const { communityCardCount } = loadPure(['communityCardCount']);

// Runs the real renderDataSummary with the live unified counts and the
// "live field points + blob loaded" flag supplied by the test.
function makeRender(client, document, liveCounts, liveReady) {
  // eslint-disable-next-line no-new-func
  return new Function('sbClient', 'document', 'computeUnifiedStatusCounts', '_fmtRelative',
    'communityCardCount', 'unifiedCountsReady',
    `"use strict";\n${sliceRenderDataSummary()}\nreturn renderDataSummary;`)(
    client, document, () => liveCounts, () => 'recently', communityCardCount, () => liveReady);
}

test('Update Data → Community card equals the legend total once the live pins have loaded', async () => {
  // The blob holds 3 features (CSV contacts + field copies, possibly of deleted
  // pins). The legend's unified total (copies pruned, each visit once) is 2.
  const { els, document } = stubDom();
  await makeRender(fakeClient([]), document, { Completed: 1, 'Not Home': 1 }, true)();
  assert.equal(els['ds-community-count'].textContent, (2).toLocaleString());
});

test('before the live pins load, the card keeps the larger of blob and live counts', async () => {
  let d = stubDom();
  await makeRender(fakeClient([]), d.document, { Completed: 1 }, false)();
  assert.equal(d.els['ds-community-count'].textContent, (3).toLocaleString());
  d = stubDom();
  await makeRender(fakeClient([]), d.document, { Completed: 5 }, false)();
  assert.equal(d.els['ds-community-count'].textContent, (5).toLocaleString());
});

test('communityCardCount', () => {
  assert.equal(communityCardCount(295, 283, true), 283);
  assert.equal(communityCardCount(295, 283, false), 295);
  assert.equal(communityCardCount(10, 12, false), 12);
});
