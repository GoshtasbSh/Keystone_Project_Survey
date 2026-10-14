"""Performance (user rule: never slow the pipeline): street fuzzy matching is
the single largest cost of an IAQ upload (difflib, ~25 % of process_iaq_bytes).

The launch fixes added house-number checks that parse every address again,
which made the October upload slower than a545ce1 (VER-7 2e). Both helpers
are pure, so each distinct street is now fuzzy-matched once: `_street_core`
is memoised, and an upload canonicalises each distinct street name once.
Outputs are byte-identical (checked on the May and October exports).
"""
from __future__ import annotations

import difflib
import pathlib
import re
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'api'))

import _processing as P  # noqa: E402

OCTOBER = pathlib.Path('/Users/goshtasbshahriari/UF Dropbox/Goshtasb Shahriari Mehr/'
                       'DTSC_Lab/Keystone_Data/'
                       'Keystone Heights Survey - V1_October 7, 2026_00.47.csv')


class _Counting(difflib.SequenceMatcher):
    n = 0

    def __init__(self, *a, **kw):
        type(self).n += 1
        super().__init__(*a, **kw)


def test_street_core_fuzzy_matches_a_street_once(monkeypatch):
    monkeypatch.setattr(P.difflib, 'SequenceMatcher', _Counting)
    _Counting.n = 0
    text = 'Lake Geneva Drve test-u15-cache'   # unique: not cached by other tests
    first = P._street_core(text)
    after_first = _Counting.n
    assert after_first > 0                       # the suffix check really ran
    assert P._street_core(text) == first
    assert _Counting.n == after_first            # second call: no fuzzy work


@pytest.mark.parametrize('text', ['6318 Bucknell Ave', '', 'Bucknell', '  BUcknell  Avenue , FL 32656'])
def test_street_core_values_unchanged(text):
    # The pre-memo body of _street_core, verbatim, as the reference.
    s = str(text).strip()
    s = re.sub(r',?\s*(Keystone Heights|KH|FL|Florida|\d{5}).*$', '', s, flags=re.IGNORECASE)
    s = P._SUFFIX_RE.sub('', s)
    s = re.sub(r'\s+', ' ', s).strip().lower()
    words = s.split()
    if len(words) >= 2 and any(difflib.SequenceMatcher(None, words[-1], sfx).ratio() >= 0.70
                               for sfx in P._KNOWN_SUFFIX_CORES):
        s = ' '.join(words[:-1])
    assert P._street_core(text) == s


def test_street_core_keeps_str_semantics_for_non_strings():
    # 1, 1.0 and True hash alike; the memo must not let one answer for another.
    assert P._street_core(1) == '1'
    assert P._street_core(1.0) == '1.0'
    assert P._street_core(True) == 'true'


def test_an_upload_canonicalises_each_street_name_once(monkeypatch):
    if not OCTOBER.exists():
        pytest.skip('October export not present')
    calls = []
    real = P._canonicalize_street

    def spy(name, known, *a, **kw):
        calls.append(name)
        return real(name, known, *a, **kw)

    monkeypatch.setattr(P, '_canonicalize_street', spy)
    P.process_iaq_bytes(OCTOBER.read_bytes(), [], P.load_parcel_index())
    assert calls, 'the upload canonicalises street names'
    assert len(calls) == len(set(calls))
