# Qualtrics ↔ Dashboard Popup Data-Integrity Audit — Evidence Manifest

**Audit date:** 2026-09-20
**Plan:** `docs/plans/2026-09-20-qualtrics-popup-data-integrity-audit.md`
**Reason:** Collaborators reported that the Qualtrics reading/analysis looked wrong and that some points did not display correctly.

## Target

| Item | Value |
|---|---|
| Dashboard | `https://keystone-project-survey-blue.vercel.app/` (the `-blue` deployment only) |
| Admin account | `test@test.com` (display name `test2`) — pre-existing sanctioned test admin |
| Access level | Team member / admin (so `address` and other PII fields are present in API responses) |
| Sampling seed | `20260920` |

## Source files audited (SHA-256)

| File | SHA-256 |
|---|---|
| `data/Keystone Heights Survey - V1_April 15, 2026_13.25.csv` | `0589eed945864a855f677f1820fd235d8ab4ffe51e8e7b738335d04fefa27a26` |
| `Keystone_Data/Keystone Heights Survey - V1_May 4, 2026_16.57.csv` | `691c60ce275a73aed3b5803d815ef5928af20c254da895d4002272a1fd4d812e` |
| `Keystone_Data/Keystone_Heights_Survey_-_V1 (1).qsf` | `1a2b6da5f2ceddc9115ab5d9bba843635c896d70f9cd518adfd6b58988e19366` |
| `data/Community Survey Contact Data .xlsx` | `d40c19cbff236170944e5475dfafe16415780fe0231e26d4ea5d7d46e1702a93` |

`Keystone_Data` resolves to `/Users/goshtasbshahriari/UF Dropbox/Goshtasb Shahriari Mehr/DTSC_Lab/Keystone_Data`.

## Structural facts measured (not assumed)

Measured with `scripts/audit/qualtrics_ground_truth.py`:

| Export | Columns | QIDs discovered | Data rows | `Finished` rows (what production processes) |
|---|---|---|---|---|
| April 15, 2026 | 150 | 164 | 82 | 75 |
| May 4, 2026 | 150 | 164 | 91 | 84 |

Both exports are structurally identical in shape and `ImportId` sequence. The May export is the later, larger one. Both carry a 3-row header: row 0 = short names, row 1 = verbatim question text, row 2 = `{"ImportId":"QIDxxx"}`.

## Contents

| Path | What it holds |
|---|---|
| `popups/<response_id>.html` | Verbatim popup DOM captured from the live dashboard after a real marker click |
| `screenshots/<response_id>.png` | Screenshot of that same open popup |
| `tables/01-address-match.md` | User task 1 — address agreement across 4 sources |
| `tables/02-value-parity-april.md` | User task 2 — every field, every sampled point, vs April CSV |
| `tables/03-value-parity-may.md` | User task 3a — same vs May CSV (numeric recodes) |
| `tables/04-april-vs-may.md` | User task 3b — April↔May agreement |
| `tables/05-provenance.md` | User task 4 — line-level chain + Python/JS index answer + 10-point trace |
| `FINAL_REPORT.md` | Verdict and defect list for the research team |

## Integrity rules honoured

- Read-only against the database: no uploads, deletes, status changes, or re-processing.
- No invite codes generated; Team modal's "Get today's code" not touched.
- No credentials written to any file in the repo.
- Every table cell traces to a screenshot, a DOM dump, a CSV row+column, or a source line. Unverifiable cells read `UNVERIFIED — <reason>` rather than being inferred.
