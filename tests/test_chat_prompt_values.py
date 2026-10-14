"""The chatbot prompt must only offer coord_source values the pipeline writes
(api/_processing.py:720-737, 2300-2312). 'geocoded' alone matched no point."""
import pathlib

SRC = (pathlib.Path(__file__).resolve().parents[1] / 'api' / 'chat.py').read_text()


def test_coord_source_line_lists_real_tiers():
    line = next(l for l in SRC.splitlines() if l.strip().startswith('coord_source'))
    for v in ('address_matched', 'parcel_exact', 'parcel_snapped', 'geocoded'):
        assert v in line, v
    assert 'gps' not in line.lower()
