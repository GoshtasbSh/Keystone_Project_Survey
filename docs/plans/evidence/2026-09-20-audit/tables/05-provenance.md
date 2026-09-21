# Table 05 — Where every survey value comes from, line by line

This answers: *which exact line reads which exact column, does Python use a
different index than the JavaScript, and can the numbers be trusted?*

## 1. The chain, hop by hop

A single answer travels this path from the Qualtrics CSV to the popup row:

| # | Stage | File : line | What happens |
|---|---|---|---|
| 1 | Decode + header detection | `api/_processing.py:1840-1921` | Tries 5 encodings; detects the 3-row Qualtrics header |
| 2 | Skip header rows | `api/_processing.py:1873-1887` | Row 1 (question text) and row 2 (`ImportId`) are skipped from the data frame |
| 3 | Build the QID → column map | `api/_processing.py:1900-1917` | Parses `{"ImportId":"QIDxxx"}` from row 2. **This is the identifier everything else keys off** |
| 4 | Keep only completed responses | `api/_processing.py:1959-1971` | `Finished` in `true`/`1` |
| 5 | Keep all 150 columns | `api/_processing.py:1961-1964` | `df_full` retains blank/duplicate-named columns so positional access stays valid |
| 6 | Detect numeric vs text export | `api/_processing.py:357-404` | Samples `Headache`, `QID195_1`, `QID124_1`, `QID178` |
| 7 | Translate recode codes → labels | `api/_processing.py:407-438` | Applies `_QSF_RECODE_LABELS` (`:228-252`) and `_COLNAME_RECODE_LABELS` (`:~270-301`) |
| 8 | Normalise code keys | `api/_processing.py:304-346` | `6` / `6.0` / `'6'` all become `'6'` |
| 9 | **Extract each field** | `api/_processing.py:846-889` | 3-tier resolution, see §2 |
| 10 | Read the cell | `api/_processing.py:787-805` | `full_row.iloc[col]`, NaN → `''` |
| 11 | Raw IAQ fields read by column NAME | `api/_processing.py:2084-2103` | `Mold`, `Leakage 2_*`, `Cooling System _*`, `Cooking`, `QID141`, … |
| 12 | Scores | `api/_processing.py:2002-2007` | health + IAQ + struct → `risk = 0.35·h + 0.35·i + 0.30·s` |
| 13 | Structural score | `api/survey_logic.py:26-65` | Keyword match on year-built / housing-type / condition text |
| 14 | Symptom frequency → 0–4 | `api/survey_logic.py:68-96` | `weekly`=4 … `annual`=1 |
| 15 | Match to canvass contacts | `api/_processing.py:2112-2126` | Sets `iaq_matched`, then `match_status` |
| 16 | Labels attached for the popup | `api/_processing.py:~168-200`, `:1732-1733` | `IAQ_FEATURE_POPUP_LABELS` + `SURVEY_QUESTIONS` canonical text |
| 17 | Transport to the browser | `api/iaq-points.py:105-121` | `?full=1` + team-member auth returns answers; anonymous is stripped |
| 18 | Render the popup | `static/js/dashboard.js:1633-1694` | `buildSurveyAnswersTab`; labels merged at `:1634`; cells formatted `:1615-1631` |

## 2. The three-tier field resolution (the part that could go wrong)

`_extract_survey_extras`, `api/_processing.py:875-886`:

1. **QID from the CSV's `ImportId` row** — `qmap.get(qid)`
2. **QID embedded in the column header text** — `_build_colname_qid_map`, `:819-843`
3. **Hardcoded column index** — `col = idx` at `:884`, logged to `miss_log` at `:885-886`

Tier 3 is the dangerous one: it is only correct while the export keeps its
historical column order.

### Measured result: tier 3 is never used

`tests/test_survey_extraction_provenance.py::test_no_field_falls_back_to_a_hardcoded_column_index`
runs the real extractor over both exports and asserts `miss_log` is empty.

**It passes for both the April 15 and the May 4 export.** Every one of the 40
`SURVEY_QUESTIONS` fields resolves by `ImportId`. The hardcoded indices in the
table are dead code on these files.

## 3. Does Python use a different index than the JavaScript?

**No — and the frontend has no indices at all.**

- **Python** resolves by `ImportId`, with a positional fallback that is
  currently never taken (§2). The one positional read that does happen,
  `full_row.iloc[orig_idx]` at `api/_processing.py:793`, uses the index that
  tier 1 just resolved from the QID — not a hardcoded one.
- **JavaScript** never indexes by column position. It looks values up by
  **named property** on the GeoJSON feature — `props[k]` at
  `static/js/dashboard.js:1654` and `:1658` — and takes the label for the same
  key from the server's `survey_questions` map (`:1634`).

So there is no Python/JS index to disagree about. The only positional coupling
in the whole chain is the popup's *row order*, which follows `_IAQ_CATEGORIES`
(`static/js/dashboard.js:1525-1595`); that is a display order, not a data
lookup.

## 4. The 10-response extraction test

`tests/test_survey_extraction_provenance.py::test_extractor_matches_independent_reader`
takes the first 10 completed responses from each export and compares **every**
`SURVEY_QUESTIONS` field against `scripts/audit/qualtrics_ground_truth.py`, an
independent reader that does not import any code under test.

| Export | Responses | Fields compared | Disagreements |
|---|---|---|---|
| April 15 | 10 | 400 | **0** |
| May 4 | 10 | 400 | **0** |

Values are compared as values: a numeric export's `6` and `6.0` are the same
answer from the same cell. That representation difference is asserted
separately by `test_numeric_codes_are_not_extracted_as_floats`, which failed on
the May export before this audit and passes after the fix at
`api/_processing.py:793-805` (integral floats now render as `6`, not `6.0`).

**Conclusion for §3 and §4: the extraction layer is sound.** Values come from
the columns they are supposed to come from, in both export formats. The defects
this audit found are *not* wrong-column reads — they are wrong *labels*
(findings F9, F0, F5, F6, F7, F11) and wrong *presentation* (F10, F3, F4).

## 5. Where the numbers do go wrong

The scoring inputs are read correctly but can be interpreted wrongly, because
the text they are matched against is wrong:

| Score input | Read at | Broken by |
|---|---|---|
| `condition` → struct `+35/+25/+15` | `api/survey_logic.py:44-64` | F0 — placeholder text matches no keyword, so `+0` |
| `year_built` → struct `+30/+20/+10` | `api/survey_logic.py:28-33` | F9 — `VariableNaming` reverses the age bands |
| `hospital_visit` → health `+20` | `api/_processing.py:751` | F6 — latent; correct on text exports |
| `Leakage 2_*` → IAQ `+7.5` each | `api/_processing.py:764-767` | F11 — score unaffected, attribution mislabelled |
| `Cooling System _*` → IAQ `+4/+2` | `api/_processing.py:772-781` | Selection detection is sound; the cells hold system **age**, not type |

Both `condition` and `year_built` feed the structural score, and the structural
score is 30% of the headline risk number — so the risk tier shown on the map is
affected. F0 quantifies six households that change tier from `condition` alone.
