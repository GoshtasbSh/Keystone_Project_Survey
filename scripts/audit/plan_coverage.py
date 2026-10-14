"""Every audited bug must be owned by a fix task AND verified by a VER task.

Convention in the assembled plan: each task section ("### Task <PREFIX>-N: ...")
carries one line  `**Fixes:** P5, Q4-03, DEP-6`  (fix tasks) or
`**Verifies:** P5, Q4-03` (VER tasks). An item with no code fix is listed on a
`**No fix (explained):** Q2-140vs119 — reason` line in the VER completeness task.

usage: python scripts/audit/plan_coverage.py docs/plans/2026-10-13-launch-readiness-fixes.md
Exit 0 = every ID is fixed-or-explained and verified.
"""
from __future__ import annotations

import re
import sys

REQUIRED = (
    [f'P{i}' for i in range(1, 24)]
    + ['Q1-F1', 'Q1-F2', 'Q1-F3']
    + ['Q2-F1', 'Q2-F2', 'Q2-F3', 'Q2-F4', 'Q2-F5', 'Q2-F6', 'Q2-F9']
    + ['Q3-F1', 'Q3-F2', 'Q3-F3', 'Q3-F4', 'Q3-F5', 'Q3-F6', 'Q3-I2']
    + [f'Q4-0{i}' for i in range(1, 10)]
)
ID_RE = re.compile(r'\b(P\d{1,2}|Q\d-(?:F\d+|0\d|I\d+|[A-Za-z0-9]+))\b')


def coverage(md: str) -> dict:
    fixed, verified, explained = set(), set(), set()
    task, in_code = None, False
    for line in md.splitlines():
        if line.lstrip().startswith('```'):
            in_code = not in_code          # tags quoted inside code blocks do not count
            continue
        if in_code:
            continue
        m = re.match(r'#{2,4}\s+Task\s+([A-Z]+)-\d+', line)
        if m:
            task = m.group(1)
            continue
        for tag, bucket in (('**Fixes:**', fixed), ('**Verifies:**', verified),
                            ('**No fix (explained):**', explained)):
            if line.strip().startswith(tag):
                ids = set(ID_RE.findall(line.split(tag, 1)[1].split('—')[0]))
                if tag == '**Fixes:**' and task == 'VER':
                    continue          # a verification task cannot be the fix owner
                bucket |= ids
    missing_fix = [i for i in REQUIRED if i not in fixed and i not in explained]
    missing_ver = [i for i in REQUIRED if i not in verified and i not in explained]
    return {'missing_fix': missing_fix, 'missing_verify': missing_ver}


def main(path):
    res = coverage(open(path, encoding='utf-8').read())
    for k, v in res.items():
        print(f'{k}: {v or "none"}')
    return 1 if any(res.values()) else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
