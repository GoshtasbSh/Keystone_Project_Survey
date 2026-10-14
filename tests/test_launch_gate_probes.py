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
