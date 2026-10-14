// IAQ upload notices: one toast, warnings first, so the "History is
// incomplete" audit-trail warning is never replaced by a later toast. The
// field-pin line says "linked", because linking no longer changes a pin's
// status (the surveyor's status is kept).
import test from 'node:test';
import assert from 'node:assert/strict';
import { loadPure, readSource } from './load_pure.mjs';

const { iaqUploadNotices } = loadPure(['iaqUploadNotices']);

test('audit-trail and missing-column warnings both survive, warnings first, long duration', () => {
  const r = iaqUploadNotices({
    n_upgraded: 2, n_field_upgraded: 9,
    audit_trail: { status: 'partial', detail: 'version row failed' },
    validation: { missing_columns: ['Q1'] },
  });
  assert.equal(r.lines.length, 4);
  assert.match(r.lines[0], /History is incomplete: version row failed/);
  assert.match(r.lines[1], /missing Qualtrics columns/);
  assert.match(r.lines[3], /^9 field survey points linked to a Qualtrics response$/);
  assert.equal(r.durationMs, 12000);
});

test('no warnings: short toast; singular wording; nothing to say gives no lines', () => {
  const r = iaqUploadNotices({ n_field_upgraded: 1, audit_trail: { status: 'full' } });
  assert.deepEqual(r.lines, ['1 field survey point linked to a Qualtrics response']);
  assert.equal(r.durationMs, 5000);
  assert.deepEqual(iaqUploadNotices({}).lines, []);
});

test('the upload success path shows the notices in one toast', () => {
  const src = readSource('static/js/dashboard.js');
  assert.ok(!src.includes('upgraded to Completed'));
  assert.ok(/iaqUploadNotices\(data\)/.test(src));
});
