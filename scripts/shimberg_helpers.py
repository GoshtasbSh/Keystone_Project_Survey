"""Pure helpers for scripts/export_for_shimberg.py (no network, no env)."""
from __future__ import annotations


def superseded_collection(iaq_payload: dict) -> dict | None:
    """Earlier answers of households that answered twice, flagged
    superseded=True, as a FeatureCollection; None when there are none."""
    sup = ((iaq_payload or {}).get('geojson') or {}).get('superseded_features') or []
    if not sup:
        return None
    return {'type': 'FeatureCollection',
            'features': [{**f, 'properties': {**(f.get('properties') or {}), 'superseded': True}}
                         for f in sup]}
