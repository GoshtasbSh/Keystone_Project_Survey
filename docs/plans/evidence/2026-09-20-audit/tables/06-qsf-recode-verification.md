# 06 — QSF recode-table verification

Date: 2026-09-20. Read-only audit; no source code was modified.

## Sources

| Role | Path |
|---|---|
| Authoritative survey definition | `/Users/goshtasbshahriari/UF Dropbox/Goshtasb Shahriari Mehr/DTSC_Lab/Keystone_Data/Keystone_Heights_Survey_-_V1 (1).qsf` (212 `SurveyElement`s with `Element == "SQ"`) |
| Hand-written tables under audit | `/Users/goshtasbshahriari/UF Dropbox/Goshtasb Shahriari Mehr/DTSC_Lab/KeyStone_project/api/_processing.py` (`_QSF_RECODE_LABELS` L228–L270, `_COLNAME_RECODE_LABELS` L273–L301) |
| | `/Users/goshtasbshahriari/UF Dropbox/Goshtasb Shahriari Mehr/DTSC_Lab/KeyStone_project/api/survey_logic.py` (`QID141_RECODE_LABELS` L9–L15) |
| Corroborating exports (used only to confirm QSF reading) | `.../Keystone_Data/Keystone Heights Survey - V1_May 4, 2026_16.57.csv` (numeric) and `.../KeyStone_project/data/Keystone Heights Survey - V1_April 15, 2026_13.25.csv` (text) |

## How the QSF was read (and where it differs from the brief's assumptions)

The brief's model is broadly right, with four deviations that materially change the verdicts. All four are stated here because they are the reason several entries are wrong.

1. **`RecodeValues` is PARTIAL in this QSF.** It is a map *choice-key → exported code*, but it only lists the choices whose code was explicitly overridden. Unlisted choices export as their own choice key. Example `QID141`: `RecodeValues == {'5': '1'}` — choices 1–4 export as `1,2,3,4` **and choice 5 also exports as `1`**, so code `1` is ambiguous and, in practice, means choice 5. The May CSV confirms it: `QID141` contains only the values `1,2,3,4` (no `5`), and the April text export contains **zero** "Excellent" responses while showing 11 choice-5 responses versus 15 occurrences of code `1` in May (with 9 extra rows). Same partial-override pattern in `QID17` (`{'3':'1','4':'2','5':'3'}`) and `QID100` (`{'3':'1','4':'2'}`) — the code correctly excludes those two but **not** `QID141`.
2. **For matrix questions, `RecodeValues` recodes the ANSWER (scale) keys, not the choice rows.** Verified on `QID195`/`QID124`/`QID181`, where the `RecodeValues` keys line up 1:1 with `Answers`/`AnswerOrder`, and `AnswerRecodeValues` is `null` throughout the file.
3. **`Payload.VariableNaming` (the "recode label" field) is stale/garbage for many questions, and the April text export wrote THOSE strings, not `Choices[*].Display`.** Example: April `Ownership` cells read `Owner`, `Renter`, `Click to write Choice 3`, `Click to write Choice 4`, exactly `QID134.VariableNaming`. Consequence: for several questions the two exports can never agree, whatever the lookup table says (see "Cross-export divergence" below). `Choices[*].Display` / `Answers[*].Display` is treated as authoritative for MEANING in every verdict below.
4. **`Cooling System` (`QID205`) DOES have an age dimension.** Its `QuestionType` is `Matrix`, `Selector: Likert`, `SubSelector: MultipleAnswer`; text `"What type of cooling system do you use and how old is it? (check all that apply)"`; `Choices` = the four cooling types (rows), `Answers` = `less than 10 years / 10 to 15 years / More than 15 years / Don't know/Not applicable`. Each CSV column `Cooling System _N` is row N (its header line 2 names the type) and the **cell value is the AGE answer code**. The in-code comment "this question has NO age dimension" is factually wrong, and the "correction" it describes inverted a correct mapping.

Verdict key: MATCH / LABEL-DRIFT / WRONG-CODE / NOT-IN-QSF, per the audit brief.

---

# Part 1 — `api/_processing.py` `_QSF_RECODE_LABELS`

## QID195 — matrix, `Answers` scale (`RecodeValues {'1':'1','2':'6','3':'7'}`)

| QID | code | code's label | QSF Display | verdict |
|---|---|---|---|---|
| QID195 | `1` | `"Dislike"` | `"Dislike"` | MATCH |
| QID195 | `6` | `"Like"` | `"Like"` | MATCH |
| QID195 | `7` | `"Not Applicable/Unsure"` | `"Not Applicable/Unsure"` | MATCH |

## QID124 — matrix, `Answers` scale (`RecodeValues {'1':'1','2':'2','3':'3'}`)

| QID | code | code's label | QSF Display | verdict |
|---|---|---|---|---|
| QID124 | `1` | `"Yes"` | `"Yes"` | MATCH |
| QID124 | `2` | `"No"` | `"No"` | MATCH |
| QID124 | `3` | `"Prefer Not Answer"` | `"Prefer Not Answer"` | MATCH |

## QID181 — matrix, `Answers` scale (`RecodeValues` identity 1–5)

| QID | code | code's label | QSF Display | verdict |
|---|---|---|---|---|
| QID181 | `1` | `"Not important"` | `"Not important"` | MATCH |
| QID181 | `2` | `"Slightly important"` | `"Slightly important"` | MATCH |
| QID181 | `3` | `"Important"` | `"Important"` | MATCH |
| QID181 | `4` | `"Very Important"` | `"Very Important"` | MATCH |
| QID181 | `5` | `"One of my key concerns"` | `"One of my key concerns"` | MATCH |

## QID178 — MC SAVR, tag `Degree` (`RecodeValues {'1':'1','2':'5','3':'6','4':'7','5':'8','6':'9'}`)

| QID | code | code's label | QSF Display | verdict |
|---|---|---|---|---|
| QID178 | `1` | `"Less than high school"` | `"less than high school"` | LABEL-DRIFT (leading `L` vs `l`) |
| QID178 | `5` | `"High school diploma or equivalent"` | `"High school diploma or equivalent"` | MATCH |
| QID178 | `6` | `"Some college, no degree"` | `"Some college, no degree"` | MATCH |
| QID178 | `7` | `"Bachelor's Degree"` | `"Bachelor's Degree"` | MATCH |
| QID178 | `8` | `"Graduate Degree"` | `"Graduate Degree"` | MATCH |
| QID178 | `9` | `"Vocational/Technical Licensing or Certification"` | `"Vocational/Technical Licensing or Certification"` | MATCH |

## QID176 — MC SAVR, tag `Employment` (`RecodeValues {'45':'1','48':'2','49':'3','50':'4','51':'5'}`)

| QID | code | code's label | QSF Display | verdict |
|---|---|---|---|---|
| QID176 | `1` | `"Employed- Full time"` | `"Employed- Full time"` | MATCH |
| QID176 | `2` | `"Employed - Part time"` | `"Employed - Part time"` | MATCH |
| QID176 | `3` | `"Unemployed"` | `"Unemployed"` | MATCH |
| QID176 | `4` | `"Retired"` | `"Retired"` | MATCH |
| QID176 | `5` | `"Prefer not to respond"` | `"Prefer not to respond"` | MATCH (note `VariableNaming['51']` is `"Prefer not to respond."` with a trailing period — the April export may carry the period) |

## QID211 — MC SAVR, no `RecodeValues` (codes = choice keys)

| QID | code | code's label | QSF Display | verdict |
|---|---|---|---|---|
| QID211 | `1` | `"Yes"` | `"Yes"` | MATCH |
| QID211 | `2` | `"No"` | `"No"` | MATCH |

## QID219 — MC SAVR, no `RecodeValues`

| QID | code | code's label | QSF Display | verdict |
|---|---|---|---|---|
| QID219 | `1` | `"Yes"` | `"Yes"` | MATCH |
| QID219 | `2` | `"No"` | `"No"` | MATCH |
| QID219 | `3` | `"Not Sure"` | `"Not Sure"` | MATCH |
| QID219 | `4` | `"Other"` | `"Name the problem"` | LABEL-DRIFT (same choice — the free-text branch, `QID219_4_TEXT`; April rows literally contain `"Name the problem"`, so the two exports disagree on this value) |

## QID21 — MC SAVR, environmental safety (`RecodeValues` identity 1–5)

| QID | code | code's label | QSF Display | verdict |
|---|---|---|---|---|
| QID21 | `1` | `"Always feel safe"` | `"Always feel safe"` | MATCH |
| QID21 | `2` | `"Mostly feel safe"` | `"Mostly feel safe"` | MATCH |
| QID21 | `3` | `"Somewhat feel safe"` | `"Somewhat feel safe"` | MATCH |
| QID21 | `4` | `"Rarely feel safe"` | `"Rarely feel safe"` | MATCH |
| QID21 | `5` | `"Never feel safe"` | `"Never feel safe"` | MATCH |

## QID194 — MC SAVR, social safety (`RecodeValues` identity 1–5)

| QID | code | code's label | QSF Display | verdict |
|---|---|---|---|---|
| QID194 | `1` | `"Always feel safe"` | `"Always feel safe"` | MATCH |
| QID194 | `2` | `"Mostly feel safe"` | `"Mostly feel safe"` | MATCH |
| QID194 | `3` | `"Somewhat feel safe"` | `"Somewhat feel safe"` | MATCH |
| QID194 | `4` | `"Rarely feel safe"` | `"Rarely feel safe"` | MATCH |
| QID194 | `5` | `"Never feel safe"` | `"Never feel safe"` | MATCH |

Caveat (not a table defect): `QID21.VariableNaming` and `QID194.VariableNaming` are `{'1':'Less than 6 months','2':'More than 6 months ','3':"Don't know ",…}` and the April export wrote **those** strings, so April safety cells read `"Less than 6 months"` etc. See "Cross-export divergence".

## QID47 — `MC MAHR` (multiple-answer!) (`RecodeValues` identity 1–5)

| QID | code | code's label | QSF Display | verdict |
|---|---|---|---|---|
| QID47 | `1` | `"Less than 1 year"` | `"less than 1 year"` | LABEL-DRIFT (leading `L` vs `l`) |
| QID47 | `2` | `"1-5 years"` | `"1-5 years"` | MATCH |
| QID47 | `3` | `"6-10 years"` | `"6-10 years"` | MATCH |
| QID47 | `4` | `"Indefinitely"` | `"Indefinitely"` | MATCH |
| QID47 | `5` | `"Don't know"` | `"Don't know"` | MATCH |

Caveat: because the selector is `MAHR`, cells can hold comma-joined codes — the May CSV contains `"2,3"` in one row, which no single-code lookup can translate (stays a bare `"2,3"`).

## QID192 — `MC SAHR`, year built (`RecodeValues` identity 1–5)

| QID | code | code's label | QSF Display | verdict |
|---|---|---|---|---|
| QID192 | `1` | `"2000-now"` | `"2000-now"` | MATCH |
| QID192 | `2` | `"1980-1999"` | `"1980-1999"` | MATCH |
| QID192 | `3` | `"1960-1979"` | `"1960-1979"` | MATCH |
| QID192 | `4` | `"Before 1960"` | `"Before 1960"` | MATCH |
| QID192 | `5` | `"I don't know"` | `"I don't know"` | MATCH |

**Loud caveat (highest-impact cross-export issue, not a table-vs-Display defect).** `QID192.VariableNaming` is `{'1':'Before 1960','2':'Built 1960–1979','3':'Built 1980–1999','4':'Built 2000 or later','5':'Click to write Choice 5'}` — i.e. the survey author's recode labels run in the **opposite direction** to the `Display` values, and the April export wrote the recode labels. So one household that picked choice 2 appears as `"1980-1999"` when loaded from the May CSV and as `"Built 1960–1979"` when loaded from the April CSV. `compute_struct_score()` (`api/survey_logic.py`) substring-matches `"before 1960"` / `"1960"` / `"1980"`, so the same household scores differently depending on which export is loaded, and April rows are scored on an inverted age scale. Note the en-dash `–` in `"Built 1960–1979"` versus the hyphen `-` in `"1960-1979"`.

## QID128 — MC SAVR, house type (no `RecodeValues`; codes = choice keys)

| QID | code | code's label | QSF Display | verdict |
|---|---|---|---|---|
| QID128 | `1` | `"Single Wide Mobile Home"` | `"Single Wide Mobile Home"` | MATCH |
| QID128 | `2` | `"Double Wide Mobile Home"` | `"Double Wide Mobile Home"` | MATCH |
| QID128 | `3` | `"House built on site"` | `"House built on site"` | MATCH |
| QID128 | `4` | `"Non-traditional structure (camper, shed, etc.)"` | `"Non-traditional structure (camper, shed, etc.)"` | MATCH |
| QID128 | `5` | `"Other"` | `"Other"` | MATCH |

## QID141 (as embedded in `_QSF_RECODE_LABELS` via `dict(QID141_RECODE_LABELS)`)

`RecodeValues == {'5': '1'}`. Exported codes are therefore `1` (choice 1 **or** choice 5), `2`, `3`, `4`. There is **no code `5`**.

| QID | code | code's label | QSF Display | verdict |
|---|---|---|---|---|
| QID141 | `1` | `"Excellent- No repairs needed."` | `"Critical- Uninhabitable without repairs."` (choice 5, recoded to `1`; choice 1 shares the same code) | **WRONG-CODE** |
| QID141 | `2` | `"Good- Minor repairs needed."` | `"Good- Minor repairs needed."` | MATCH |
| QID141 | `3` | `"Fair- Some repairs needed."` | `"Fair- Some repairs needed."` | MATCH |
| QID141 | `4` | `"Poor- Major repairs needed."` | `"Poor- Major repairs needed."` | MATCH |
| QID141 | `5` | `"Critical- Uninhabitable without repairs."` | no choice exports code `5` | NOT-IN-QSF (dead entry) |

---

# Part 2 — `api/_processing.py` `_COLNAME_RECODE_LABELS`

## Symptom-frequency columns → `QID43` (`Respiratory Symptoms`), matrix `Answers`, `RecodeValues` identity 1–5

Columns `Headache` (QID43_1), `asthma` (QID43_5), `RespIll` (QID43_6), `Tired` (QID43_7), `wheeze` (QID43_8) all carry the same table. One table shown; the verdicts apply identically to all five columns (5 × 5 = 25 pairs).

| QID | code | code's label | QSF Display | verdict |
|---|---|---|---|---|
| QID43 | `1` | `"weekly"` | `"weekly"` | MATCH |
| QID43 | `2` | `"monthly"` | `"Monthly"` | LABEL-DRIFT (`m` vs `M`) |
| QID43 | `3` | `"seasonally"` | `"Seasonally"` | LABEL-DRIFT (`s` vs `S`) |
| QID43 | `4` | `"annually"` | `"Yearly"` | LABEL-DRIFT (different word entirely) |
| QID43 | `5` | `"Never or rarely"` | `"Rarely or Never"` | LABEL-DRIFT (words reversed and re-cased) |

These four drifts are not cosmetic: the April export writes the QSF strings (`"Monthly"`, `"Seasonally"`, `"Yearly"`, `"Rarely or Never"` — confirmed in the April CSV), so after translation the May rows hold `"monthly"/"seasonally"/"annually"/"Never or rarely"` for the exact same answers. Any string comparison, `value_counts()` grouping, or legend built across both exports splits each answer into two categories.

## `Hospital Respiratory` → `QID59` (`RecodeValues {'5':'1','6':'2','7':'3','8':'4'}`)

| QID | code | code's label | QSF Display | verdict |
|---|---|---|---|---|
| QID59 | `1` | `"Yes"` | `"Yes, Doctor visits for allergy."` | LABEL-DRIFT (correct choice, deliberately collapsed to `Yes`) |
| QID59 | `2` | `"No"` | `"Yes, hospitalization/visiting the emergency room for asthma attack."` | **WRONG-CODE — answer meaning inverted (Yes → No)** |
| QID59 | `3` | `"No"` | `"Yes, Others."` | **WRONG-CODE — answer meaning inverted (Yes → No)** |
| QID59 | `4` | `"No"` | `"No"` | MATCH |

Impact: in the May CSV these codes occur `4`×56, `3`×9, `1`×8, `2`×7. Codes `2` and `3` are 16 households who reported an ER/hospitalization or another respiratory visit and are recorded as `"No"`. The in-code comment "binary Yes/No. Any code ≠ '1' treated as No" encodes the bug. `Hospital Respiratory` feeds the Health composite (+20) and the `hospital_pct` chart, so both understate respiratory burden by roughly two thirds of the positive cases.

## `Ownership` → `QID134` (`RecodeValues {'1':'1','2':'2','4':'3','5':'4'}`)

| QID | code | code's label | QSF Display | verdict |
|---|---|---|---|---|
| QID134 | `1` | `"Owner"` | `"Own"` | LABEL-DRIFT (matches `VariableNaming['1'] == "Owner"`, i.e. the April export, but not the `Display`) |
| QID134 | `2` | `"Renter"` | `"Rent"` | LABEL-DRIFT (matches `VariableNaming['2'] == "Renter"`) |
| QID134 | `3` | `"Other"` | `"Live with friends/family"` | **WRONG-CODE** |
| QID134 | `4` | *(no entry)* | `"Other"` | missing — see below |

## `Cooling System _1..4` → `QID205`, matrix **MultipleAnswer**, cells hold the AGE answer

`QID205.Choices` (rows, = the four CSV columns): `1 "Central Air-conditioning"`, `2 "Window/Wall/Portable AC units for just one or two rooms"`, `3 "Ceiling Fans"`, `4 "No Air-conditioning"`. `QID205.Answers` (the scale actually written into the cells): `1 "less than 10 years"`, `2 "10 to 15 years"`, `3 "More than 15 years"`, `4 "Don't know/Not applicable"`. `RecodeValues` is `null`, so codes = answer keys. The April text export confirms it: every `Cooling System _N` column contains only `less than 10 years / 10 to 15 years / More than 15 years / Don't know/Not applicable`.

| QID | code | code's label | QSF Display (for that cell code) | verdict |
|---|---|---|---|---|
| QID205_1 | `1` | `"Central Air-conditioning"` | `"less than 10 years"` | **WRONG-CODE** (the type is the column, not the value) |
| QID205_2 | `2` | `"Window/Wall AC"` | `"10 to 15 years"` | **WRONG-CODE** |
| QID205_2 | `1` | `"Window/Wall AC"` | `"less than 10 years"` | **WRONG-CODE** |
| QID205_3 | `3` | `"Ceiling Fans"` | `"More than 15 years"` | **WRONG-CODE** |
| QID205_3 | `1` | `"Ceiling Fans"` | `"less than 10 years"` | **WRONG-CODE** |
| QID205_4 | `4` | `"No Air-conditioning"` | `"Don't know/Not applicable"` | **WRONG-CODE** |
| QID205_4 | `1` | `"No Air-conditioning"` | `"less than 10 years"` | **WRONG-CODE** |

Secondary note: the row-name drift is also real — the QSF row 2 `Display` is `"Window/Wall/Portable AC units for just one or two rooms"`, not `"Window/Wall AC"`.

Impact. The IAQ arithmetic in `_compute_iaq_score()` happens to survive, because `_cool_sel()` only tests "cell non-empty" and the mislabelling does not change emptiness. What breaks is everything that reads the *value*: for a household whose central-AC is 15+ years old, `Cooling System _1` holds `3` and is displayed as a bare `"3"` (no entry for `3` in the `_1` map), while a household with a <10-year-old central AC is displayed as `"Central Air-conditioning"`. Same question, same column, two incomparable renderings, and the surviving labels assert a type where the respondent answered an age. April rows pass through untranslated (`"less than 10 years"` is not a key), so cooling charts mix age strings, type strings and bare integers in one axis.

---

# Part 3 — `api/survey_logic.py` `QID141_RECODE_LABELS`

Same content as Part 1's QID141 block; audited separately because this is the definition site and it is also imported by `compute_struct_score()`'s callers.

| QID | code | code's label | QSF Display | verdict |
|---|---|---|---|---|
| QID141 | `"1"` | `"Excellent- No repairs needed."` | `"Critical- Uninhabitable without repairs."` (choice 5 recodes to `1`) | **WRONG-CODE** |
| QID141 | `"2"` | `"Good- Minor repairs needed."` | `"Good- Minor repairs needed."` | MATCH |
| QID141 | `"3"` | `"Fair- Some repairs needed."` | `"Fair- Some repairs needed."` | MATCH |
| QID141 | `"4"` | `"Poor- Major repairs needed."` | `"Poor- Major repairs needed."` | MATCH |
| QID141 | `"5"` | `"Critical- Uninhabitable without repairs."` | no choice exports code `5` | NOT-IN-QSF (dead entry) |

Evidence for the code-`1` reading, stated plainly because it inverts the housing-condition scale:

| value | April 15 export (text) | May 4 export (numeric) |
|---|---|---|
| Excellent | 0 rows | — |
| `Click to write Choice 5` (= choice 5, "Critical") | 11 rows | — |
| code `1` | — | 15 rows |
| Good / code `2` | 25 | 26 |
| Fair / code `3` | 19 | 22 |
| Poor / code `4` | 20 | 21 |
| code `5` | — | 0 rows (never appears) |

(April has 83 rows, May 92, so +4 on code `1` is consistent with the 9 new responses.) Nobody in this survey has ever selected "Excellent", yet the dashboard reports 15 households as `"Excellent- No repairs needed."` — those are the 15 worst houses in the dataset.

---

# Summary

## Actionable bugs — WRONG-CODE (12 pairs)

1. **`QID141` code `1` → `"Excellent- No repairs needed."`; the QSF says code `1` is `"Critical- Uninhabitable without repairs."`** Present in BOTH tables (`api/survey_logic.py:10` and, via `dict(QID141_RECODE_LABELS)`, `api/_processing.py:269`). 15 of 92 May households are labelled the best housing condition when they reported the worst. Choice 1 ("Excellent") shares code `1`, so the code is genuinely ambiguous in the export — `QID141` belongs in the same exclusion list as `QID17`/`QID100`, or needs disambiguation from the April text export. `compute_struct_score()` matches on these strings, so the structural score and the `conditions` chart are both affected.
2. **`Hospital Respiratory` (`QID59`) code `2` → `"No"`; the QSF says `"Yes, hospitalization/visiting the emergency room for asthma attack."`** 7 May households.
3. **`Hospital Respiratory` (`QID59`) code `3` → `"No"`; the QSF says `"Yes, Others."`** 9 May households. Together with (2), 16 of the 24 positive respiratory-care responses are inverted to `No`, deflating the Health composite (+20) and `hospital_pct`.
4. **`Ownership` (`QID134`) code `3` → `"Other"`; the QSF says `"Live with friends/family"`.** 4 May households mis-bucketed, and the real `"Other"` (code `4`) has no entry at all.
5. **All seven `Cooling System _1..4` pairs (`QID205`).** The cells hold the AGE answer (`less than 10 years` … `Don't know/Not applicable`), not the cooling type; the type is fixed by the column. The in-code comment asserting `QID205` "has NO age dimension" is contradicted by the question text `"What type of cooling system do you use and how old is it? (check all that apply)"`, by `SubSelector: MultipleAnswer` + the `Answers` block, and by the April text export. Whoever "corrected" the age labels to type labels inverted a correct mapping; the previous "age" labels were not fabricated.

## NOT-IN-QSF (2 pairs)

- `QID141` code `5` → `"Critical- Uninhabitable without repairs."` — unreachable; `RecodeValues {'5':'1'}` means choice 5 exports as `1`, and code `5` never appears in the May CSV. Counted once per table (`_QSF_RECODE_LABELS`, `survey_logic.QID141_RECODE_LABELS`).

No audited QID was absent from the QSF; all 13 QIDs and both custom-named question groups resolved.

## QSF choices with NO entry in the code's tables (dashboard shows a bare number)

| Column / QID | unmapped codes | QSF Display | consequence |
|---|---|---|---|
| `Ownership` / QID134 | `4` | `"Other"` | 2 May rows render as `"4"` |
| `Cooling System _1` / QID205_1 | `2`, `3`, `4` | `"10 to 15 years"`, `"More than 15 years"`, `"Don't know/Not applicable"` | 29 of 55 non-blank May cells render as bare digits |
| `Cooling System _2` | `3`, `4` (and `2` is mislabelled) | as above | 23 of 62 |
| `Cooling System _3` | `2`, `4` | as above | 26 of 57 |
| `Cooling System _4` | `2`, `3` | as above | 2 of 35 |
| `Rash` / QID43_4 (`"Skin Rashes"`) | `1`–`5` | `weekly … Rarely or Never` | the sixth symptom row has no table entry although its five siblings do |
| `Mold` / QID149 | `1,4,5,6,7,8,9,10` | `Kitchen, Bathroom, Living Room, Bedroom, Inner walls/Windows, Outer walls/Windows, Ceiling, Other:` | no table at all; May `Mold` shows bare numbers (`"10"`×41) in popups. `_compute_iaq_score()` only tests non-emptiness so the +30 still fires, but `mold_pct` / `mold_by_street` group on the raw value, so April (`"Other:"`) and May (`"10"`) never aggregate together |
| `Cooking` / QID148 | `1` `"gas cooktops"`, `7` `"electric cooktops"`, `8` `"don't know"`, `9` `"Other:"` | — | no table at all, and `_compute_iaq_score()` tests `'gas' in value.lower()`. For May rows the value is `"1"`, so the **+10 gas-stove IAQ penalty never fires** — 6 households (plus one `"1,9"`) silently lose 10 IAQ points |
| `Leakage 2_1..4` / QID42 | `1` `"less than one week"`, `2` `"more than one week"`, `3` `"not fixed"`, `4` `"none"` | — | no table at all, and `_compute_iaq_score()` adds +7.5 per column unless the value is literally `"none"`. May rows store `"4"` for "none", so **every May respondent is scored as having all four water problems: up to +30 spurious IAQ points** (`Leakage 2_1` alone has 50 `"4"` cells). This is a scoring bug caused by the missing table, not a label bug |
| `Leakage 3_1..5` / QID114 | `1`–`5` | matrix answers | no table; bare numbers in `leakage_*` popup properties |

## LABEL-DRIFT (26 pairs) and the cross-export divergence behind most of them

Drifts: `QID178` `1`; `QID219` `4`; `QID47` `1`; `QID43` codes `2,3,4,5` × 5 symptom columns (20); `QID59` `1`; `QID134` `1`,`2`.

Because these labels are compared as strings downstream, the case and wording differences above (`"monthly"` vs `"Monthly"`, `"annually"` vs `"Yearly"`, `"Never or rarely"` vs `"Rarely or Never"`, `"Owner"` vs `"Own"`) mean a May-loaded household and an April-loaded household with the identical answer end up in different buckets.

Separately — and this is the largest remaining comparability problem, beyond any table entry — **the April 15 text export wrote `Payload.VariableNaming` (the recode labels), not `Choices[*].Display`.** Where the survey's recode labels are stale, the April CSV therefore contains strings that do not describe the answer at all, and no lookup table keyed on codes can reconcile the two exports:

| QID | April cell text (from `VariableNaming`) | actual meaning (`Display`) |
|---|---|---|
| QID192 (year built) | `"Before 1960"`, `"Built 1960–1979"`, `"Built 1980–1999"`, `"Built 2000 or later"`, `"Click to write Choice 5"` | `"2000-now"`, `"1980-1999"`, `"1960-1979"`, `"Before 1960"`, `"I don't know"` — **the recode labels run in the opposite direction** |
| QID21 / QID194 (safety) | `"Less than 6 months"`, `"More than 6 months"`, `"Don't know"`, `"Click to write Choice 4/5"` | `"Always feel safe"` … `"Never feel safe"` |
| QID47 (how long staying) | `"Wood"`, `"Concrete"`, `"Steel"`, `"Others"`, `"Don't know"` | `"less than 1 year"` … `"Don't know"` |
| QID124 (experiences) | `"Daily"`, `"Weekly"`, `"Biweekly"` | `"Yes"`, `"No"`, `"Prefer Not Answer"` |
| QID195 (interventions) | `"Click to write Scale Point 1"`, `"Cultural & Historical sites…"`, `"Nature reserves and preserves"` | `"Dislike"`, `"Like"`, `"Not Applicable/Unsure"` |
| QID181 (relocation factors) | `"Click to write Scale Point 1..5"` | `"Not important"` … `"One of my key concerns"` |
| QID134 (ownership) | `"Owner"`, `"Renter"`, `"Click to write Choice 3"`, `"Click to write Choice 4"` | `"Own"`, `"Rent"`, `"Live with friends/family"`, `"Other"` |
| QID141 (condition) | `"Click to write Choice 5"` for Critical | `"Critical- Uninhabitable without repairs."` |
| QID114 (`Leakage 3`) | `"Click to write Scale Point 4/5"` | matrix answers |

Any household whose row came from the April CSV is being analysed on these strings. `_pct_yes` on `QID124`, the safety charts on `QID21`/`QID194`, `_pct_want` on `QID195`, the relocation-factor analysis on `QID181` and `compute_struct_score()`'s year-built branch all read text that either means nothing or means the opposite. A table-only fix will not close this; the loader needs to translate the April export's variable labels to canonical `Display` values as well.

## Counts

| verdict | pairs |
|---|---|
| MATCH | 62 |
| LABEL-DRIFT | 26 |
| WRONG-CODE | 12 |
| NOT-IN-QSF | 2 |
| **total pairs checked** | **102** |

Per table: `_QSF_RECODE_LABELS` 58 pairs (53 MATCH / 3 LABEL-DRIFT / 1 WRONG-CODE / 1 NOT-IN-QSF); `_COLNAME_RECODE_LABELS` 39 pairs (6 / 23 / 10 / 0); `survey_logic.QID141_RECODE_LABELS` 5 pairs (3 / 0 / 1 / 1).

## Verified-correct decisions in the code

- Excluding `QID17` and `QID100`: confirmed. `QID17.RecodeValues == {'3':'1','4':'2','5':'3'}` collides with choices 1–3, and `QID100.RecodeValues == {'3':'1','4':'2'}` collides with `Yes`/`No`. `QID141` has the identical defect and should have been excluded on the same grounds.
- The ` ` → space normalisation in `_apply_qsf_recode_labels()` (`api/_processing.py:430`): necessary and correct — the real CSV header is `"Cooling System _1"` while the table key uses an ordinary space, and the normaliser bridges them.
- The `qid_key != qid_base and not qid_key.startswith(qid_base + '_')` guard prevents `QID21`'s map from leaking onto `QID211`/`QID219`. Confirmed safe for every QID in the table.
