"""access_probe / static_parity / plan_coverage: the gate's own rules."""
from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts' / 'audit'))

import access_probe as AP    # noqa: E402
import plan_coverage as PC   # noqa: E402
import static_parity as SP   # noqa: E402

# Per-respondent answers and free text that must never reach an anonymous caller.
PRIVATE_KEYS = {'education', 'employment', 'exp_law_enf', 'years_in_hre', 'anticipated_stay',
                'afford_urgency', 'notes_text', 'mold_rooms', 'raw_address', 'address', 'email'}


def test_public_allowlists_hold_no_private_answers():
    for path, keys in AP.ANON_ALLOWED.items():
        assert not (keys & PRIVATE_KEYS), path
        assert not any(k.endswith('_text') for k in keys), path


def test_every_private_blob_row_is_probed():
    assert {'iaq_survey', 'community_contact', 'analysis'} <= set(AP.PRIVATE_DATA_TYPES)


def test_static_parity_files_exist_in_git():
    tracked = set(subprocess.run(['git', '-C', str(ROOT), 'ls-files'], capture_output=True,
                                 text=True, check=True).stdout.splitlines())
    for local, _served in SP.FILES:
        assert local in tracked, local


def test_plan_coverage_requires_fix_and_verify():
    md = '\n'.join(['### Task FIX-1: a', '**Fixes:** P1', '### Task VER-1: b', '**Fixes:** P2',
                    '**Verifies:** P1, P2', '**No fix (explained):** Q2-F1 — label only'])
    res = PC.coverage(md)
    assert 'P1' not in res['missing_fix'] and 'P1' not in res['missing_verify']
    assert 'P2' in res['missing_fix']                 # a VER task cannot own a fix
    assert 'Q2-F1' not in res['missing_fix'] and 'Q2-F1' not in res['missing_verify']
    assert 'P23' in res['missing_fix']


def test_plan_coverage_ignores_tags_inside_code_blocks():
    md = "### Task FIX-1: a\n```python\n**Fixes:** P1\n```\n### Task VER-1: b\n**Verifies:** P1\n"
    assert 'P1' in PC.coverage(md)['missing_fix']


def test_required_ids_cover_every_audit_bucket():
    ids = set(PC.REQUIRED)
    assert {f'P{i}' for i in range(1, 24)} <= ids
    assert {'Q2-F3', 'Q2-F5', 'Q3-F2', 'Q3-I2', 'Q4-02', 'Q4-09'} <= ids


# ── GAP-9: the restored canvass contacts are public, so the frozen allowlist must carry their flag ──

def _load_api(modname: str, filename: str):
    import importlib.util
    spec = importlib.util.spec_from_file_location(modname, ROOT / 'api' / filename)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_restored_contact_flag_is_on_both_public_contact_allowlists():
    for path in ('api/community-contacts', 'api/survey-points'):
        assert 'restored_from_field_pin' in AP.ANON_ALLOWED[path], path


def test_public_copy_of_a_restored_contact_stays_within_the_allowlist():
    """UP-11 restores 6386 Baylor / 6393 Cascade from the pins that swallowed
    them. Build that feature with the repo's own code, strip it the way each
    public endpoint does, and require every key to be allowlisted (so the live
    probe cannot fail on a restored contact after R4)."""
    sys.path.insert(0, str(ROOT / 'api'))
    import _field_layer as FL  # noqa: E402
    host = {'geometry': {'type': 'Point', 'coordinates': [-82.0, 29.78]},
            'properties': {'field_point_id': 'b989a847', 'source': 'field'}}
    entry = {'status': 'Completed', 'street_name': 'Baylor Ave', 'notes': 'n',
             'address': '6386 Baylor Ave', 'matched_address': '6386 BAYLOR AVE',
             'collected_at': '2026-09-01T12:00:00Z'}
    feat = FL._restore_swallowed_contact(entry, host, None)
    assert feat['properties']['restored_from_field_pin'] == 'b989a847'
    for path, filename in (('api/community-contacts', 'community-contacts.py'),
                           ('api/survey-points', 'survey-points.py')):
        mod = _load_api(f'_gap9_{filename.split(".")[0].replace("-", "_")}', filename)
        public = mod._strip_pii({'type': 'FeatureCollection', 'features': [feat]})
        keys = set(public['features'][0]['properties'])
        assert keys <= AP.ANON_ALLOWED[path], (path, sorted(keys - AP.ANON_ALLOWED[path]))
