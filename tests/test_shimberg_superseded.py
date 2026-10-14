"""User decision 2026-10-13: earlier answers of a household are kept in the
data. The handover must carry them, flagged, next to the analysed ones."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'scripts'))
from shimberg_helpers import superseded_collection  # noqa: E402


def test_superseded_rows_are_exported_flagged():
    pl = {'geojson': {'features': [{'properties': {'response_id': 'R_k'}}],
                      'superseded_features': [{'type': 'Feature', 'geometry': None,
                                               'properties': {'response_id': 'R_e', 'superseded_by': 'R_k'}}]}}
    fc = superseded_collection(pl)
    assert [f['properties']['response_id'] for f in fc['features']] == ['R_e']
    assert fc['features'][0]['properties']['superseded'] is True
    assert pl['geojson']['superseded_features'][0]['properties'].get('superseded') is None  # input not mutated


def test_no_superseded_rows_gives_none():
    assert superseded_collection({'geojson': {'features': []}}) is None
