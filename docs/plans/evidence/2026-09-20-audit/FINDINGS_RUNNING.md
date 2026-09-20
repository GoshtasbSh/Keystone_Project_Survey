# Running findings log — 2026-09-20 audit

Appended as each finding is confirmed. Severity: **P0** = wrong analysis/risk output, **P1** = wrong data shown to users, **P2** = misleading/unusable presentation, **P3** = process/coverage gap.

---

## F9 (P0) — ROOT CAUSE: the text export writes `VariableNaming`, which in this survey is stale text from *other questions*

Everything in F0, F5, F6 and F7 is a symptom of this one cause. **The answer text in the dashboard is, for many questions, not this question's answer text at all.**

### The mechanism

Each Qualtrics question in the QSF carries two label sets:

- `Choices[n].Display` — **what the respondent actually saw and clicked.** This is the truth.
- `VariableNaming[n]` — an export-label override. **This is what the text-format CSV writes.**

In this survey `VariableNaming` was never kept in step with the questionnaire as it was edited, so for 28 questions it holds either placeholder junk or labels left over from a completely different question. Production runs on a text export, so the dashboard displays `VariableNaming`.

### What that looks like live, right now (110 households)

| Question | What it asks | What the dashboard displays |
|---|---|---|
| `QID21` → `safety_env` | Do you feel safe from environmental threats? | `Less than 6 months` ×61, `More than 6 months` ×28, `Don't know` ×19 |
| `QID194` → `safety_social` | Do you feel safe from social threats? | `Less than 6 months` ×42, `Don't know` ×29, `More than 6 months` ×28 |
| `QID124_1` → `exp_flooding` | Have you experienced flooding of the house? | **`Weekly` ×105**, `Daily` ×5 |
| `QID19` → `afford_strategy` | Most effective strategy to improve affordability? | `Yes- Integrated into central air heating system`, `Yes - Portable (Which Room(s))` … |
| `QID192` → `year_built` | When was your house built? | **reversed** (see below) |
| `QID141` → `condition` | Condition of your house? | `Click to write Choice 5` ×19 (= "Critical- Uninhabitable") |

None of the answer options offered for "do you feel safe" were ever durations. A reader checking the popup against the questionnaire sees answers that cannot possibly belong to the question — which is exactly the report that triggered this audit.

### `QID192` is reversed, and it feeds the risk score

| choice | `Choices.Display` (respondent saw) | `VariableNaming` (exported, displayed) |
|---|---|---|
| 1 | `2000-now` | `Before 1960` |
| 2 | `1980-1999` | `Built 1960–1979` |
| 3 | `1960-1979` | `Built 1980–1999` |
| 4 | `Before 1960` | `Built 2000 or later` |

`compute_struct_score` (`api/survey_logic.py:28-33`) awards `+30` for `before 1960`, `+20` for `1960`, `+10` for `1980`. Because the labels are inverted, **the newest houses receive the oldest-house risk points and vice versa.** Live: 17 households display `Before 1960` (they actually answered *2000-now*) and 3 display `Built 2000 or later` (they actually answered *Before 1960*).

### Scope

- **Category A — `VariableNaming` is placeholder junk:** 32 choices across 22 questions (`QID100`, `QID114`, `QID134`, `QID141`, `QID17`, `QID181`, `QID19`, `QID192`, `QID194`, `QID195`, `QID21`, `QID221`, …). These produce the 1,441 placeholder cells in F0.
- **Category B — `VariableNaming` holds another question's labels:** `QID114`, `QID124`, `QID134`, `QID140`, `QID166`, `QID182`, `QID19`, `QID192`, `QID193`, `QID194`, `QID21`, … These produce confidently-wrong text.

### Why the numeric export is the safe one

The May-style numeric export writes recode **codes**, not `VariableNaming`. Codes map cleanly to `Choices.Display` via the QSF. An independent bijection check across all 134 joined question columns found **0 violations** and **0 changed `RecordedDate`s** between the two exports — the two files are the same data in two encodings, and the disagreements are purely label faults.

### Fix direction

1. Resolve every answer label from the QSF's `Choices[n].Display` / `Answers[n].Display` — **never** from `VariableNaming` and never from the text export's cell text.
2. Prefer the numeric (recode) export as the ingest format, since its codes are unambiguous.
3. Handle `QID141` specially: its `RecodeValues {'5':'1'}` collides choice 5 onto code 1, so it needs the placeholder/QSF path rather than a code lookup (F5).
4. Re-run scoring afterwards — `year_built` and `condition` both feed `compute_struct_score`, so risk tiers will move (F0 lists 6 households that change tier from `condition` alone).

The cleanest correction at the source is to fix `VariableNaming` in the Qualtrics survey itself and re-export; the code-side fix above makes the pipeline robust regardless.

---

## F0 (P0) — 1,441 survey answers display as Qualtrics placeholder text, and the worst-condition households are scored as low risk

**This is the most likely thing the collaborators saw.** It is live in production right now.

### What is displayed

Across the 110 live IAQ responses, **1,441 answer cells contain Qualtrics placeholder strings** such as `Click to write Choice 5` and `Click to write Scale Point 3` instead of a real answer. Worst-affected fields:

| Field | Placeholder cells | of 110 |
|---|---|---|
| `mh_skirting` | 110 | **every household** |
| `reloc_factor_aff` / `_emp` / `_env` | 108 each | ~all |
| `afford_urgency` | 108 | ~all |
| `reloc_factor_fam` / `_qol` / `_ret` / `_inh` | 106–107 | ~all |
| `intv_ccua_water` | 68 | 62% |
| `intv_trees_shade` | 55 | 50% |
| `year_built` | 30 | 27% |
| `condition` | 19 | 17% |

The dashboard detects these strings (`_IAQ_PLACEHOLDER_RE`, `static/js/dashboard.js:1612`) and renders them muted with "(Qualtrics placeholder)" appended — so the popup honestly admits it has no answer, but the answer *does* exist in the survey and is simply not being resolved.

### Why it happens

The text-format CSV export writes the questionnaire's **placeholder** label for any choice whose Display text was left uncustomised in that export, rather than the real choice text. The real text is present in the QSF. For `QID141` the QSF gives:

```
choice 1: 'Excellent- No repairs needed.'
...
choice 5: 'Critical- Uninhabitable without repairs.'
```

So `Click to write Choice 5` on `condition` unambiguously means **"Critical- Uninhabitable without repairs."** — the single worst answer available. Nothing in the pipeline maps the placeholder back to the QSF choice.

### The analysis damage (verified, not estimated)

`compute_struct_score` (`api/survey_logic.py:44-64`) matches the words `critical` / `poor` / `fair` in the condition text. `Click to write Choice 5` matches none of them, the numeric fallback also fails, so the household scores **+0 instead of +35** for condition.

All 19 affected households are under-scored by 35 structural points. Recomputing `risk = 0.35·health + 0.35·iaq + 0.30·struct` with the correct answer:

| ResponseId | Street | struct now → fixed | risk now → fixed | tier now → fixed |
|---|---|---|---|---|
| `R_1LOVKbX2iH6Xh3j` | Bucknell Ave | 45 → 80 | 31 → 41 | **Low → Medium** |
| `R_53V7a6BGdQkzzSd` | Pembroke St | 45 → 80 | 24 → 34 | **Low → Medium** |
| `R_h0LfcAVvLrGULaj` | Pembroke St | 35 → 70 | 26 → 36 | **Low → Medium** |
| `R_geSs0TKZpnVhtIz` | Centre Cir | 50 → 85 | 26 → 37 | **Low → Medium** |
| `R_6EyCCkI0I64KiK6` | Rollins St | 30 → 65 | 23 → 34 | **Low → Medium** |
| `R_03zxekptX5jBk3d` | Baylor Ave | 35 → 70 | 28 → 39 | **Low → Medium** |

**Six households that reported their home is uninhabitable without repairs are currently presented as "Low" risk.** The other 13 keep their tier but are still under-scored.

**Fix direction:** resolve placeholders against the QSF before scoring — parse `Click to write Choice N` / `Scale Point N`, map N through that QID's `Choices`/`Answers` `Display`, and only fall back to the placeholder if the QSF has no entry. This fixes the popup text and the scores in one place. It must happen upstream of `compute_struct_score`, not in the frontend.

---

## F1 (P1) — 2 matched households are drawn and counted as "Qualtric only"

**What:** `R_5LnXMcaezhqW28F` and `R_bt9KhSC0xqF2xuS` carry `iaq_matched: true` but `match_status: "iaq_only"`.

**Why it happens:** `_apply_iaq_to_field_features` matches Qualtrics responses against **live field-survey points** and flips the flag at `api/_processing.py:1436`:

```python
match_iaq['properties']['iaq_matched'] = True
```

Its own comment states the intent is "so the iaq layer can re-classify this dot from 'iaq_only' (yellow rim) to 'matched' (white rim)". That intent is not achieved: it never updates `match_status`. The stamping of `match_status` happens earlier, in `process_iaq_bytes` at `api/_processing.py:2123-2126`, and is never re-run afterwards.

The map layers filter on `match_status`, not on `iaq_matched` — `static/js/dashboard.js:3935-3936`:

```js
'iaq-points-g1': ['==', ['get', 'match_status'], 'matched'],
'iaq-points':    ['==', ['get', 'match_status'], 'iaq_only'],
```

**User-visible impact:** both households render with the purple "Qualtric only (flyer / QR)" symbol — i.e. "this household answered the survey but we have no canvass record" — when in fact they were matched to a surveyed household. The sidebar Match Status panel is also wrong: it shows **83 matched / 27 Qualtric-only** where the data says **85 / 25**.

**Evidence:** sidebar counts in `screenshots/00-admin-dashboard.png`; property values in `live_iaq_points_full.json`.

**Fix direction:** either set `match_status` alongside `iaq_matched` at `:1436` (and at `:1348`), or derive the layer filter from `iaq_matched` so a single flag is authoritative. The second is preferable — two fields encoding one fact is what caused this.

---

## F2 (P3) — 19 matched live responses exist in no CSV in the project

**What:** production serves 110 IAQ responses. Only 75 appear in the May 4 export and 66 in the April 15 export. **35 live responses (32%) are in neither file**; of the 85 *matched* ones, **19** cannot be value-checked against any CSV provided.

**Why it matters:** production was loaded from a Qualtrics export newer than anything in `data/` or `Keystone_Data/`. A collaborator checking the dashboard against their copy of the survey will find rows that "don't exist in the data" — which may be precisely the complaint that triggered this audit. It is not necessarily a dashboard defect; it is a data-provenance gap.

**Consequence for this audit:** the sampling frame was restricted to matched points present in the May 4 export (66 of them) so that every audited point is actually verifiable. This restriction is disclosed rather than hidden, and the 19-response gap is reported here.

**Recommended action:** export the current Qualtrics data and place it alongside the existing files, so the dashboard and the shared CSVs describe the same population.

---

## F3 (P2) — Popup question labels are truncated to 90 characters

**What:** `static/js/dashboard.js:1639`:

```js
const shortQ = qLabel.length > 90 ? qLabel.slice(0, 87) + '…' : qLabel;
```

**Impact:** the requirement is that a collaborator can copy a question out of the popup and find it in the CSV/Excel with Find. A truncated string with a trailing ellipsis will never match. The full text is preserved in the `title` attribute (`:1644`), so it is recoverable on hover but not by selection or search.

---

## F4 (P2) — Popup question labels are paraphrases, not the survey's own wording

**What:** the label shown for each answer comes from `SURVEY_QUESTIONS` canonical text (`api/_processing.py:93-143`) and `_RAW_IAQ_LABELS` (`static/js/dashboard.js:1598-1609`). Both are human-written summaries.

Example — the code says:

> `'Experience — Flooding of house due to any disaster (e.g., hurricane)'`

while row 1 of the CSV (the survey's own text) reads:

> `"Since you've lived in High Ridge Estates, have you experienced... - Flooding of house due to any disaster (e.g., hurricane)"`

**Impact:** same as F3 — the popup text cannot be found in the export. Combined with F3, no long question label in the popup is searchable against the source data.

**Quantification:** pending `tests/test_survey_label_verbatim.py`, which enumerates every non-verbatim label.

---

## F5 (P0, latent) — the housing-condition scale is inverted for numeric exports

**What:** `QID141_RECODE_LABELS` (`api/survey_logic.py:9-15`) maps code `'1'` → `'Excellent- No repairs needed.'`

The QSF says `QID141` has `RecodeValues: {'5': '1'}` — i.e. **choice 5, "Critical- Uninhabitable without repairs.", is exported as code `1`.** Choices 1–4 have no recode entry and so export as 1, 2, 3, 4. Code `1` is therefore genuinely ambiguous in this survey: it means *either* "Excellent" *or* "Critical".

**Empirical proof:** in the May 4 (numeric) export, `QID141` values are `2`×26, `3`×20, `4`×20, `1`×15 — **code `5` never occurs**. In the April (text) export the same 15-ish rows read `Click to write Choice 5` ×11 and there are **zero** "Excellent" responses. The code `1` rows are Critical answers, not Excellent ones.

**Impact if a numeric export is loaded:** 15 households reporting an uninhabitable home would display as *"Excellent — No repairs needed."* — an exact inversion — and would score +0 instead of +35.

**Status:** **latent, not currently active.** Production is running a text-format export (F0 is the active manifestation). This becomes a live data-corruption bug the moment a May-style numeric CSV is uploaded.

**Fix direction:** `QID141` must be added to the exclusion list that already exists for exactly this reason — `api/_processing.py:258-259` notes that "QID17 and QID100 intentionally omitted — their RecodeValues produce duplicate codes across choices". `QID141` has the same defect and was missed. Disambiguate via the QSF placeholder path (F0) instead of by recode code.

---

## F6 (P1, latent) — hospitalisation answers are recoded to "No"

**What:** `_COLNAME_RECODE_LABELS['Hospital Respiratory']` (`api/_processing.py:286`) is `{'1': 'Yes', '2': 'No', '3': 'No', '4': 'No'}`, with the comment "binary Yes/No. Any code ≠ '1' treated as No."

The QSF (`QID59`, `RecodeValues {'5':'1','6':'2','7':'3','8':'4'}`) says:

| code | real meaning |
|---|---|
| 1 | Yes, Doctor visits for allergy. |
| 2 | **Yes**, hospitalization/visiting the emergency room for asthma attack. |
| 3 | **Yes**, Others. |
| 4 | No |

So codes 2 and 3 are *Yes* answers being relabelled **"No"** — and code 2 is the most severe answer in the question.

**Impact if a numeric export is loaded:** in the May export, code `2`×7 and code `3`×9 — **16 households with a positive respiratory-hospitalisation history would be recorded as "No"**, and the `+20` health-score penalty (`api/_processing.py:751`, `if 'yes' in ...`) would never fire for them.

**Status:** **latent.** Production's text export contains the full strings ("Yes, hospitalization/…"), which contain the substring `yes`, so `hospital_visit` is currently correct (live: 33 yes / 77 no). Uploading a numeric export would silently corrupt it.

---

## F7 (P1, latent) — ownership code 3 mislabelled, code 4 unmapped

`_COLNAME_RECODE_LABELS['Ownership']` (`api/_processing.py:288`) is `{'1':'Owner','2':'Renter','3':'Other'}`.

QSF `QID134` `RecodeValues {'1':'1','2':'2','4':'3','5':'4'}`:

| code | real meaning | code says |
|---|---|---|
| 3 | Live with friends/family | "Other" |
| 4 | Other | *unmapped* — renders as a bare `4` |

In the May export code `3`×4 and code `4`×2. "Live with friends/family" is a housing-insecurity signal and should not be collapsed into "Other".

---

## F8 (P2) — 8 pairs of responses share identical coordinates; one of each pair is unclickable

**What:** the 110 IAQ responses occupy only **102 distinct coordinates**. Eight coordinates carry **two responses each** (16 responses total), at a separation of **0.0 m**.

| Coordinate | Street | Responses (risk) |
|---|---|---|
| −82.017583, 29.781232 | Bucknell Ave | `R_1E4YReRP6XTeX06` (43) + `R_0U4XyfXUNDttX9a` (16) |
| −82.018539, 29.780705 | Bucknell | `R_kZXrW8v3LxbbUTV` (34) + `R_hv0cc021NGKRc5M` (35) |
| −82.006994, 29.778603 | Dennison | `R_6s0PVusMDUucFQY` (36) + `R_h6cnt2kXgSK5Bbg` (27) |
| −82.004295, 29.786213 | Harvard Ave | `R_iB2E7Yzs7PSGMlr` (33) + `R_ju3Amx8yBiJ45L0` (38) |
| −82.017165, 29.785504 | Princeton St | `R_2KqXYjOIYV1zFdH` (54) + `R_5oBDIEcTfYUvj8n` (13) |
| −82.012351, 29.779238 | Dennison | `R_mLTilJCf3lIPEoI` (34) + `R_6Nqhz2mzupemk9v` (46) |
| −82.017276, 29.783271 | Baylor | `R_5LnXMcaezhqW28F` (13) + `R_j1xG6QD0Gw1G3uU` (29) |
| −82.010647, 29.788047 | Wesleyan Rd | `R_6pRawZol21jqapc` (47) + `R_3915ZWsZpRAwPi9` (59) |

**Impact:** clicking that dot can only ever open one of the two. The second household's answers are unreachable through the map, and a user comparing the popup against a spreadsheet row for the *other* response will conclude the dashboard is showing wrong data. Risk values differ sharply within a pair (e.g. 54 vs 13), so which one wins is very visible.

**Cause:** both responses geocode to the same parcel representative point (`coord_source` = `address_matched` or `parcel_exact`), i.e. two survey responses for one address — either two households on one parcel, or one household answering twice.

**Fix direction:** detect coincident IAQ responses and either spiderfy them or show a "2 responses at this address" selector in the popup, the way `coincident_contacts` already handles collapsed community contacts (`api/_processing.py:1297-1311`).
