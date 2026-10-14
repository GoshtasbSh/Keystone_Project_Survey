"""popup_audit.js / search_check.js run the dashboard's own code on synthetic snapshots."""
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts' / 'audit'))


NODE = shutil.which('node')


def _feature(rid, coords, **props):
    return {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': coords},
            'properties': {'response_id': rid, **props}}


def _snap(tmp_path, props):
    (tmp_path / 'dd_iaq_survey.json').write_text(json.dumps({'payload': {
        'analysis': {'survey_questions': {}},
        'geojson': {'type': 'FeatureCollection', 'features': [_feature('R_a', [-82.0, 29.7], **props)]}}}))
    (tmp_path / 'dd_community_contact.json').write_text(json.dumps({'payload': {
        'type': 'FeatureCollection', 'features': [
            {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [-82.014265, 29.790102]},
             'properties': {'id': 53, 'address': '6306 Amherst Ave', 'status': 'Completed'}}]}}))
    return tmp_path


@pytest.mark.skipif(NODE is None, reason='node not installed')
def test_popup_audit_catches_nan_and_passes_clean(tmp_path):
    js = str(ROOT / 'scripts' / 'audit' / 'popup_audit.js')
    bad = subprocess.run([NODE, js, str(_snap(tmp_path, {'education': 'nan'}))], capture_output=True, text=True)
    assert bad.returncode == 1 and 'nan' in bad.stdout
    ok = subprocess.run([NODE, js, str(_snap(tmp_path, {'education': 'Graduate Degree'}))],
                        capture_output=True, text=True)
    assert ok.returncode == 0, ok.stdout + ok.stderr


@pytest.mark.skipif(NODE is None, reason='node not installed')
def test_search_check_finds_contact_address(tmp_path):
    snap = _snap(tmp_path, {})
    parcels = tmp_path / 'parcels.json'
    parcels.write_text(json.dumps({'type': 'FeatureCollection', 'features': []}))
    lst = tmp_path / 'q.json'
    lst.write_text(json.dumps([['M-01', '6306 Amherst Ave', -82.014265, 29.790102],
                               ['X-01', '9999 Nowhere St', -82.0, 29.7]]))
    r = subprocess.run([NODE, str(ROOT / 'scripts' / 'audit' / 'search_check.js'), str(snap), str(parcels), str(lst)],
                       capture_output=True, text=True)
    assert r.returncode == 1
    assert '1/2 addresses found' in r.stdout and 'X-01' in r.stdout


# ── GAP-9: the harness loads the PURE-HELPERS block and renders what a member sees ──

def _dup_snap(tmp_path, earlier_date):
    """One household answered twice (MATCH-3 shape): the kept answer is drawn,
    the earlier one sits in geojson.superseded_features."""
    kept = _feature('R_kept', [-82.0, 29.7], education='Graduate Degree',
                    superseded_response_ids=['R_early'])
    early = _feature('R_early', [-82.0, 29.7], education='nan', superseded=True,
                     superseded_by='R_kept', recorded_date=earlier_date)
    (tmp_path / 'dd_iaq_survey.json').write_text(json.dumps({'payload': {
        'analysis': {'survey_questions': {}, 'shared_code_labels': {'verified': True, 'fields': []}},
        'geojson': {'type': 'FeatureCollection', 'features': [kept], 'superseded_features': [early]}}}))
    return tmp_path


@pytest.mark.skipif(NODE is None, reason='node not installed')
def test_popup_audit_renders_the_repeat_household_note_and_skips_the_earlier_answer(tmp_path):
    js = str(ROOT / 'scripts' / 'audit' / 'popup_audit.js')
    r = subprocess.run([NODE, js, str(_dup_snap(tmp_path, '2026-09-02 10:00:00'))], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr          # the earlier 'nan' answer is never drawn
    assert '1 popups rendered, 0 failure(s)' in r.stdout
    assert '1 popup(s) carry the repeat-household note' in r.stdout


@pytest.mark.skipif(NODE is None, reason='node not installed')
def test_popup_audit_checks_the_text_of_the_repeat_household_note(tmp_path):
    # A broken date in the note ("undefined") is visible text and must fail.
    js = str(ROOT / 'scripts' / 'audit' / 'popup_audit.js')
    r = subprocess.run([NODE, js, str(_dup_snap(tmp_path, 'undefined'))], capture_output=True, text=True)
    assert r.returncode == 1 and 'R_kept: popup text matches' in r.stdout, r.stdout + r.stderr
