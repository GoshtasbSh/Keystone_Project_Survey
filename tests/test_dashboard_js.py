"""Run the node unit tests for the browser-free helpers in static/js/dashboard.js.

The helpers live between the PURE-HELPERS markers; tests/js/load_pure.mjs
loads that block into node. Keeping this inside pytest means the standard
`pytest tests -q` run also guards the dashboard's display logic.
"""
from __future__ import annotations

import pathlib
import shutil
import subprocess

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
JS_TESTS = sorted((ROOT / 'tests' / 'js').glob('*.test.mjs'))


@pytest.mark.skipif(shutil.which('node') is None, reason='node is not installed')
def test_dashboard_pure_helpers():
    assert JS_TESTS, 'no tests/js/*.test.mjs found'
    r = subprocess.run(['node', '--test', *map(str, JS_TESTS)],
                       cwd=ROOT, capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, r.stdout[-6000:] + r.stderr[-2000:]
