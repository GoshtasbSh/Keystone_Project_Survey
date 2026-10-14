"""Performance gate: the launch fixes must not slow the upload pipeline.

Times process_iaq_bytes on the October CSV for a BASELINE commit and for the
working tree, each in a fresh subprocess, offline (Supabase env removed and
the Census geocoder stubbed to "no match", so network latency cannot hide or
fake a regression). The baseline and working-tree runs are interleaved
(base, new, base, new, ...) so a burst of background load hits both alike.

Fails if the working tree's FASTEST run is more than --tolerance slower than
the baseline's fastest run. Background noise only ever adds time, so the
minimum of --runs is the stable estimate; the October run takes ~0.25-1.5 s
depending on the machine, and on a fast machine the median of 9 identical
trees swings by +/-20 % (measured 2026-10-14), which would make a median gate
a coin flip. The medians are still printed for the record.

usage:
  .venv/bin/python scripts/audit/perf_pipeline.py --baseline a545ce1 \
      --csv "../Keystone_Data/Keystone Heights Survey - V1_October 7, 2026_00.47.csv" \
      --contacts "$GATE/before/dd_community_contact.json" [--runs 9]
"""
from __future__ import annotations

import argparse
import json
import statistics
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CHILD = r'''
import copy, json, os, sys, time
for k in list(os.environ):
    if k.startswith("SUPABASE"):
        del os.environ[k]
sys.path.insert(0, sys.argv[1])
import _processing as P
P._census_geocode = lambda addr: (None, None, None)
csvb = open(sys.argv[2], "rb").read()
contacts = json.load(open(sys.argv[3]))["payload"]["features"]
contacts = [c for c in contacts if (c.get("properties") or {}).get("source") != "field"]
idx = P.load_parcel_index()
t = time.perf_counter()
out = P.process_iaq_bytes(csvb, copy.deepcopy(contacts), idx)
dt = time.perf_counter() - t
print(json.dumps({"seconds": dt, "features": len((out[0] or {}).get("features") or [])}))
'''


def time_once(api_dir: Path, csv: str, contacts: str) -> dict:
    r = subprocess.run([sys.executable, '-c', CHILD, str(api_dir), csv, contacts],
                       capture_output=True, text=True, cwd=str(api_dir.parent), check=True)
    return json.loads(r.stdout.strip().splitlines()[-1])


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--baseline', required=True, help='git commit before the launch fixes')
    ap.add_argument('--csv', required=True)
    ap.add_argument('--contacts', required=True, help='dd_community_contact.json from launch_snapshot')
    ap.add_argument('--runs', type=int, default=9)
    ap.add_argument('--tolerance', type=float, default=0.10)
    a = ap.parse_args(argv)
    csv, contacts = str(Path(a.csv).resolve()), str(Path(a.contacts).resolve())
    base, new = [], []
    with tempfile.TemporaryDirectory(prefix='ks_perf_') as tmp:
        wt = Path(tmp) / 'base'
        subprocess.run(['git', '-C', str(ROOT), 'worktree', 'add', '--detach', str(wt), a.baseline],
                       check=True, capture_output=True)
        try:
            for _ in range(a.runs):
                base.append(time_once(wt / 'api', csv, contacts))
                new.append(time_once(ROOT / 'api', csv, contacts))
        finally:
            subprocess.run(['git', '-C', str(ROOT), 'worktree', 'remove', '--force', str(wt)],
                           capture_output=True)
    bs, ns = [x['seconds'] for x in base], [x['seconds'] for x in new]
    mb, mn = min(bs), min(ns)
    print(f'baseline {a.baseline}: min {mb:.3f}s  median {statistics.median(bs):.3f}s  '
          f'runs {[round(x, 2) for x in bs]}  features {base[0]["features"]}')
    print(f'working tree   : min {mn:.3f}s  median {statistics.median(ns):.3f}s  '
          f'runs {[round(x, 2) for x in ns]}  features {new[0]["features"]}')
    print(f'change (min) {100 * (mn - mb) / mb:+.1f}% (limit +{100 * a.tolerance:.0f}%)')
    return 1 if mn > mb * (1 + a.tolerance) else 0


if __name__ == '__main__':
    sys.exit(main())
