Local-only test inputs that hold resident data (addresses, coordinates).
Everything here except this README and .gitignore stays out of git.

- census_recorded.json: the US Census geocoder's answers for the addresses the
  test suite geocodes, keyed by SHA-256 of the normalised query. Written by
  `KS_RECORD_CENSUS=1 .venv/bin/python -m pytest tests -q` (needs network);
  read by tests/conftest.py so the normal suite never calls Census.
