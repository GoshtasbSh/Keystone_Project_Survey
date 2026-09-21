# Qualtrics ↔ Dashboard Data-Integrity Audit — Final Report

**Date:** 2026-09-20 · **Dashboard audited:** `https://keystone-project-survey-blue.vercel.app/` (live, signed in as admin) · **Method:** 30 map points opened by clicking them, one at a time, and reading the Survey Answers tab on screen.

---

## The short answer

**Your collaborators are right. The addresses are fine; the answers are not.**

Every point I checked is on the correct house. But for a large share of the questions, the text shown as the respondent's answer is not their answer — it is either placeholder text, or wording that belongs to a completely different question. Two of the affected fields feed the risk score, so some households are shown in the wrong risk tier.

None of this is a mistake in how the code reads the spreadsheet. The columns are read correctly. The problem is in what the exported file *contains*, and in a handful of hand-written translation tables.

---

## What is wrong, in plain terms

### 1. The survey's export labels are stale — this is the root cause (F9)

A Qualtrics question stores two sets of labels: what the respondent saw on screen (`Choices.Display`), and an export-label override (`VariableNaming`). The text-format CSV writes the **override**. In this survey the overrides were never updated as the questionnaire was edited, so for 28 questions they now contain leftovers from other questions.

The dashboard is loaded from a text export, so it displays those leftovers. Live right now, across all 110 households:

| The question asked | What the dashboard shows as the answer |
|---|---|
| Do you feel safe from environmental threats? | `Less than 6 months` (61), `More than 6 months` (28), `Don't know` (19) |
| Do you feel safe from social threats? | `Less than 6 months` (42), `Don't know` (29), `More than 6 months` (28) |
| Have you experienced flooding of the house? | **`Weekly` (105 of 110)**, `Daily` (5) |
| Most effective strategy for affordable housing? | `Yes- Integrated into central air heating system` … |

"Less than 6 months" was never an option for "do you feel safe". These are not near-misses; the text comes from other questions entirely.

### 2. 1,441 answers show as "Click to write…" placeholder text (F0)

Where the override was left at its factory default, the export writes the placeholder itself. `mh_skirting` shows placeholder text for **all 110 households**; the relocation-factor and affordability-urgency questions for ~108 each.

The most serious case: **19 households answered that their home is "Critical — Uninhabitable without repairs."** The dashboard shows `Click to write Choice 5`.

### 3. Because of that, six households are shown as low risk when they are not (F0)

The structural score awards +35 for a "critical" condition by matching the word. Placeholder text matches nothing, so those 19 households score **+0 instead of +35**. Recomputed with their real answer:

| Household | Street | Risk now → corrected | Tier |
|---|---|---|---|
| `R_1LOVKbX2iH6Xh3j` | Bucknell Ave | 31 → 41 | **Low → Medium** |
| `R_53V7a6BGdQkzzSd` | Pembroke St | 24 → 34 | **Low → Medium** |
| `R_h0LfcAVvLrGULaj` | Pembroke St | 26 → 36 | **Low → Medium** |
| `R_geSs0TKZpnVhtIz` | Centre Cir | 26 → 37 | **Low → Medium** |
| `R_6EyCCkI0I64KiK6` | Rollins St | 23 → 34 | **Low → Medium** |
| `R_03zxekptX5jBk3d` | Baylor Ave | 28 → 39 | **Low → Medium** |

### 4. House age is reversed (F9)

| The respondent chose | The dashboard shows |
|---|---|
| `2000-now` | `Before 1960` |
| `Before 1960` | `Built 2000 or later` |

Age also feeds the structural score (+30 for pre-1960), so the newest houses are collecting the oldest houses' risk points.

### 5. Smaller, but real

- **`nan` shown as an answer** (F10) — 167 cells live, 45 seen on screen. Mostly the cooling questions, where an unticked box renders as `nan`.
- **The four water-leakage rows are mislabelled** (F11) — "Water leakage — Roof" is actually the *broken/leaky water pipes* column; "— Floor" is actually *well not working*.
- **Two matched households are drawn as "Qualtric only"** (F1) — the sidebar reads 83/27 where the data says 85/25.
- **Eight pairs of responses sit on identical coordinates** (F8) — only one of each pair can ever be clicked.
- **Popup question labels were truncated at 90 characters and paraphrased** (F3, F4) — so they could not be found in Excel. Fixed, see below.

---

## What is actually fine

Worth saying plainly, because it narrows where to look:

- **Addresses are correct.** Of the 30 points clicked: 12 exact matches, 14 matching after normal abbreviation differences, **0 genuine mismatches**. Four popups show only a street name instead of the house number — a display gap, not wrong data.
- **The spreadsheet is read correctly.** All 40 survey fields resolve by their Qualtrics `ImportId`, never by a hardcoded column position. Verified over 10 responses in both exports against an independently written reader: **0 disagreements**.
- **Python and JavaScript do not disagree about indices.** The frontend does not use column positions at all — it looks values up by name. There is no index mismatch to fix.
- **The two exports agree with each other.** Across 134 joined question columns the April and May files are the same data in two encodings — 0 bijection violations, 0 changed `RecordedDate`s.
- **No console errors** on any of the 48 popups opened.

---

## What I changed

Only the label problems, which were safe to fix without touching any data:

| Change | File |
|---|---|
| All 40 question labels replaced with the survey's own verbatim wording | `api/_processing.py` (`SURVEY_QUESTIONS`) |
| All 20 IAQ labels sourced from the column actually read — this also fixes the mislabelled leakage rows | `api/_processing.py` (`IAQ_FEATURE_POPUP_LABELS`) |
| Removed the 90-character truncation so labels are searchable | `static/js/dashboard.js:1638-1649` |
| Frontend fallback labels made verbatim too | `static/js/dashboard.js` (`_RAW_IAQ_LABELS`) |
| Integer recode codes no longer extracted as `6.0` | `api/_processing.py:793-805` |

**58 of 60 popup labels now appear verbatim in the CSV**, so a collaborator can copy one and find it with Excel's Find. (The remaining two differ only by an embedded line break in the export.)

Three tests now guard this: `tests/test_survey_label_verbatim.py` and `tests/test_survey_extraction_provenance.py`. The full suite passes — **118 passed, 1 skipped**.

**I did not change any data, and I did not attempt to fix the placeholder/label corruption itself** — that needs your decision, see below.

---

## What I recommend, in order

1. **Fix `VariableNaming` in the Qualtrics survey and re-export.** This is the root cause and the cleanest fix. Everything in §1, §2 and §4 comes from it.
2. **Meanwhile, switch ingest to the numeric export and resolve labels from the QSF.** Numeric codes are unambiguous and map cleanly to `Choices.Display`. One exception: `QID141` recodes choice 5 onto code 1, colliding with choice 1, so it needs special handling (F5).
3. **Re-run scoring after either fix.** Condition and house age both feed the risk tier; the map's colours will change.
4. **Correct three recode tables before any numeric export is loaded** — `QID141` (inverted), `Hospital Respiratory` (codes 2 and 3 are "Yes", currently "No"), `Ownership` (code 3 is "Live with friends/family", code 4 unmapped). These are harmless today and become live bugs the moment a numeric file is uploaded.
5. **Export the current Qualtrics data into the project folders.** 35 of the 110 live responses (32%) exist in neither CSV here, so anyone checking the dashboard against these files will find rows that appear to be missing (F2).

---

## Caveats

- The sample is **30 of the 66 matched points that can be checked against a CSV**; drawn with seed `20260920` so it can be reproduced exactly. 19 matched points could not be value-checked at all because they are in no CSV (F2).
- My label fixes are **local only — not deployed.** The live dashboard still shows truncated, paraphrased labels.
- The recode-table faults (F5, F6, F7) are **latent**: they do not affect today's display, which runs on a text export. I verified they are wrong against the QSF, not that they are currently visible.
- The cooling questions ask for system type **and age** in one question; the cells hold the age. The scoring only tests whether a box was ticked, so the score is unaffected, but the row labels imply the value is a type.

---

## Evidence

| Path | Contents |
|---|---|
| `screenshots/` | 31 screenshots — the dashboard plus each sampled popup, open on Survey Answers |
| `popups/rendered_reads.json` | The label/value pairs read off the screen for all 30 |
| `popups/*.html` | Raw popup DOM for 48 points |
| `tables/01-address-match.md` | Address agreement across 4 sources |
| `tables/02-value-parity-april.md` | Every rendered answer vs the April export |
| `tables/03-value-parity-may.md` | Same vs the May export |
| `tables/04-april-vs-may.md` | April ↔ May agreement |
| `tables/05-provenance.md` | Line-by-line data path, index answer, 10-response test |
| `tables/06-qsf-recode-verification.md` | Every recode pair vs the QSF |
| `FINDINGS_RUNNING.md` | All 13 findings with evidence and fix directions |

**Read-only confirmed:** feature counts were identical at the start and end of the audit — 110 IAQ responses, 321 contacts, 85 matched.
