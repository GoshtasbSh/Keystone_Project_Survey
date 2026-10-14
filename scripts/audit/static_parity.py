"""Byte-compare the deployed static files with the local git HEAD.

Usage:
  .venv/bin/python scripts/audit/static_parity.py --base https://keystone-project-survey-blue.vercel.app
Exit 0 = every file identical.
"""
from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
# (repo path, served path)
FILES = [
    ('dashboard/index.html', 'dashboard'),
    ('field/index.html', 'field'),
    ('login/index.html', 'login'),
    ('index.html', ''),
    ('static/index.html', 'static/index.html'),
    ('static/js/dashboard.js', 'static/js/dashboard.js'),
    ('static/js/dashboard.js', 'dashboard/js/dashboard.js'),
    ('keystone_field_web/index.html', 'keystone_field_web'),
    ('keystone_field_web/login.html', 'keystone_field_web/login'),
    ('keystone_field_web/admin.html', 'admin'),
    ('keystone_field_web/reset.html', 'reset'),
    ('keystone_field_web/sw.js', 'sw.js'),
    ('keystone_field_web/manifest.json', 'manifest.json'),
]


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def head_bytes(path: str) -> bytes:
    return subprocess.run(['git', '-C', str(ROOT), 'show', f'HEAD:{path}'],
                          capture_output=True, check=True).stdout


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default='https://keystone-project-survey-blue.vercel.app')
    a = ap.parse_args(argv)
    dirty = subprocess.run(['git', '-C', str(ROOT), 'status', '--porcelain', '--', 'static', 'keystone_field_web', 'api'],
                           capture_output=True, text=True).stdout.strip()
    if dirty:
        print('FAIL working tree has uncommitted deployable changes:\n' + dirty)
        return 1
    bad = 0
    for local, served in FILES:
        want = head_bytes(local)
        req = urllib.request.Request(f"{a.base.rstrip('/')}/{served}", headers={'Cache-Control': 'no-cache'})
        got = urllib.request.urlopen(req, timeout=60).read()
        same = sha(want) == sha(got)
        bad += not same
        print(f"{'OK  ' if same else 'DIFF'} {served:<28} local {len(want):>7} B  served {len(got):>7} B")
    print(f'{len(FILES) - bad}/{len(FILES)} identical')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
