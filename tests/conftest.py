"""Suite-wide test setup.

1. No test reaches the US Census geocoder. Every copy of the processing
   module (`_processing`, imported with api/ on sys.path, and
   `api._processing`) gets `_census_geocode` replaced by a lookup in a
   recording of the real answers. Any address not in the recording gets
   (None, None, None), the same as a Census miss. A Census outage, a slow
   Census or a change in its answers can therefore never change a test
   result or hang the suite.

   The recording holds respondents' addresses and coordinates, so it is kept
   out of git (tests/private/ ignores everything but its README). Keys are
   SHA-256 hashes of the whitespace-normalised, lower-cased query. To
   re-record (needs network), run once with KS_RECORD_CENSUS=1:

       KS_RECORD_CENSUS=1 .venv/bin/python -m pytest tests -q

2. The October export is processed once per session (`october_iaq`) and
   each module takes its own deep copy, instead of every module re-running
   process_iaq_bytes on the same CSV.
"""
import copy
import hashlib
import json
import os
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
OCTOBER_CSV = pathlib.Path('/Users/goshtasbshahriari/UF Dropbox/Goshtasb Shahriari Mehr/'
                           'DTSC_Lab/Keystone_Data/'
                           'Keystone Heights Survey - V1_October 7, 2026_00.47.csv')
CENSUS_RECORDING = ROOT / 'tests' / 'private' / 'census_recorded.json'
_RECORD = os.environ.get('KS_RECORD_CENSUS') == '1'


def census_key(addr) -> str:
    return hashlib.sha256(' '.join(str(addr or '').split()).lower().encode('utf-8')).hexdigest()


def _load_recording() -> dict:
    try:
        return json.loads(CENSUS_RECORDING.read_text(encoding='utf-8'))
    except FileNotFoundError:
        return {}


_RECORDED = _load_recording()
_NEW = {}


def _offline_census_geocode(addr):
    hit = _RECORDED.get(census_key(addr))
    return tuple(hit) if hit else (None, None, None)


def _recording_census_geocode(real):
    def geocode(addr):
        k = census_key(addr)
        if k not in _NEW:
            _NEW[k] = list(real(addr))
        return tuple(_NEW[k])
    return geocode


_saved_path = list(sys.path)
try:
    sys.path.insert(0, str(ROOT / 'api'))
    sys.path.insert(0, str(ROOT))
    import _processing as _proc_flat        # noqa: E402
    import api._processing as _proc_pkg     # noqa: E402
finally:
    sys.path[:] = _saved_path

for _mod in (_proc_flat, _proc_pkg):
    _mod._census_geocode = (_recording_census_geocode(_mod._census_geocode)
                            if _RECORD else _offline_census_geocode)


def pytest_sessionfinish(session, exitstatus):
    if _RECORD and _NEW:
        CENSUS_RECORDING.parent.mkdir(parents=True, exist_ok=True)
        merged = {**_RECORDED, **{k: v for k, v in _NEW.items() if v[0] is not None}}
        CENSUS_RECORDING.write_text(json.dumps(merged, indent=1, sort_keys=True), encoding='utf-8')


@pytest.fixture(scope='session')
def october_iaq():
    """process_iaq_bytes on the October export, run once per session.
    Consumers must deep-copy it before changing anything."""
    if not OCTOBER_CSV.exists():
        pytest.skip('October export not present')
    if not _RECORD and not _RECORDED:
        pytest.fail(f'{CENSUS_RECORDING.relative_to(ROOT)} is missing: the October figures '
                    'assume the recorded Census answers. Re-record with KS_RECORD_CENSUS=1 '
                    '(see tests/conftest.py).')
    return _proc_flat.process_iaq_bytes(OCTOBER_CSV.read_bytes(), [], _proc_flat.load_parcel_index())


@pytest.fixture(scope='module')
def october_iaq_copy(october_iaq):
    return copy.deepcopy(october_iaq)
