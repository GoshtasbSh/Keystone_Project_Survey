# What exactly was wrong with the survey data — explained from scratch

Written for the research team. No code knowledge needed.

---

## The one-sentence version

Qualtrics stores **two different names for every answer option**, and the file we exported was written using the *wrong one* — a set of names that had gone stale years into the project — so the dashboard has been showing answer text that either means nothing ("Click to write Choice 5") or belongs to a completely different question ("Less than 6 months" as an answer to "do you feel safe?").

**The respondents' answers were never lost.** Every person's choice is still recorded correctly. Only the *name* printed next to their choice was wrong. That is why this is fully recoverable.

---

## How a Qualtrics answer is actually stored

When you build a question in Qualtrics, each answer option carries two labels:

| Label | What it is | Who sees it |
|---|---|---|
| **Choice Display** | The text you typed into the questionnaire | The respondent, on screen |
| **Variable Naming** | An optional "export label" — a nickname used only in exported data files | Nobody; it only appears in the CSV |

Most projects never touch Variable Naming, and then Qualtrics just exports the Choice Display. This survey *did* have Variable Naming values set.

**The critical fact: when Variable Naming exists, the text-format export writes that instead of what the respondent saw.**

---

## What went wrong

This survey was edited many times over its life — questions reworded, options added, whole questions repurposed. Each time, the **Choice Display was updated but the Variable Naming was not.** They drifted apart.

By the time of the April 15 export, the Variable Naming values for 28 questions were either:

1. **Never filled in** — so Qualtrics exported its own factory placeholder, the literal text `Click to write Choice 5`.
2. **Left over from a previous version of that question** — so the export wrote a label that belonged to a different question entirely.

The dashboard loads the text export, so it faithfully displayed whatever was in the file. The dashboard was not inventing anything; it was being fed bad labels.

---

## The four ways this showed up

### A. Meaningless placeholder text — 1,441 answer cells

`mh_skirting` (skirting intact?) showed placeholder text for **all 110 households**. The relocation-factor and housing-urgency questions, for ~108 each.

The most consequential case: **19 households selected "Critical — Uninhabitable without repairs"** as their home's condition. The dashboard showed `Click to write Choice 5`.

### B. Another question's answers — the most confusing symptom

| The question on screen | What the dashboard printed as the answer |
|---|---|
| Do you feel safe in your house from environmental threats? | `Less than 6 months`, `More than 6 months`, `Don't know` |
| Do you feel safe from social threats? | same duration labels |
| Have you experienced flooding of the house? | **`Weekly` — for 105 of 110 households** |
| What is the most effective strategy to improve affordability? | `Yes- Integrated into central air heating system` |

"Less than 6 months" was never an option for a safety question. Those labels are the answer set of a *different, older* question that still lived in the Variable Naming field.

This is almost certainly what your collaborators noticed first: answers that could not possibly belong to the question being asked.

### C. A scale printed backwards — house age

This one is the most dangerous, because it looks plausible.

| What the respondent clicked | What the export wrote | What the dashboard showed |
|---|---|---|
| `2000-now` (a new house) | `Before 1960` | **Before 1960** |
| `1980-1999` | `Built 1960–1979` | Built 1960–1979 |
| `1960-1979` | `Built 1980–1999` | Built 1980–1999 |
| `Before 1960` (an old house) | `Built 2000 or later` | **Built 2000 or later** |

The order is exactly inverted. Nothing looks broken on screen — every value is a real-looking age band — which is why this could sit unnoticed indefinitely.

### D. A scale collapsed onto itself — house condition

Separate from Variable Naming, this question has a second, independent defect in its **recode values** (the numeric codes written into the numeric-format export).

Choice 5, "Critical — Uninhabitable without repairs", was configured to export as the code **`1`**. But code `1` is already what choice 1, "Excellent — No repairs needed", exports as. **The best and worst answers became the same number.**

In a numeric export, those 15 households are genuinely indistinguishable from "Excellent" on the code alone. We resolved it by cross-checking against the text export, where the two are still distinguishable: all 11 overlapping responses carrying code `1` read "Click to write Choice 5" — i.e. Critical. Not one is Excellent, and the survey has **zero** Excellent responses out of 159.

---

## Why this mattered beyond the text

Two of the affected questions are inputs to the **risk score** shown on the map:

- **House condition** contributes up to +35 points (a "Critical" answer).
- **House age** contributes up to +30 points (a pre-1960 house).

The risk score is `35% health + 35% indoor air quality + 30% structural`, and both of these feed the structural part.

Because "Click to write Choice 5" matches none of the words the scorer looks for, **all 19 of those households scored 0 instead of 35** for condition. Recomputed with their real answer:

**Six households that told us their home is uninhabitable without repairs were displayed on the map as "Low" risk.**

| Household | Street | Risk shown → correct | Tier |
|---|---|---|---|
| `R_1LOVKbX2iH6Xh3j` | Bucknell Ave | 31 → 41 | Low → **Medium** |
| `R_53V7a6BGdQkzzSd` | Pembroke St | 24 → 34 | Low → **Medium** |
| `R_h0LfcAVvLrGULaj` | Pembroke St | 26 → 36 | Low → **Medium** |
| `R_geSs0TKZpnVhtIz` | Centre Cir | 26 → 37 | Low → **Medium** |
| `R_6EyCCkI0I64KiK6` | Rollins St | 23 → 34 | Low → **Medium** |
| `R_03zxekptX5jBk3d` | Baylor Ave | 28 → 39 | Low → **Medium** |

The house-age inversion pushes in the opposite direction: the newest houses were collecting the oldest houses' risk points.

---

## What was *not* wrong

Worth stating plainly, because it narrows the problem and should reassure:

- **No response was lost or altered.** Every respondent's selection is intact in both exports.
- **The addresses are correct.** Across 30 points opened one by one on the live dashboard: 12 exact matches, 14 matching after ordinary abbreviation differences, **0 genuine mismatches**.
- **The software reads the spreadsheet correctly.** All 40 survey fields are located by their permanent Qualtrics question ID, never by counting columns. Verified against an independently written reader over 10 responses in both exports: **0 disagreements**.
- **The two exports agree with each other.** April and May are the same data in two encodings — the same respondents, no edits between them.

The failure is entirely in the **labels**, not in the data pipeline and not in the responses.

---

## How it was fixed

Qualtrics also publishes the questionnaire's full definition (the `.qsf` file), which still contains the **correct** Choice Display text for every option. That gives an unambiguous way to translate back:

```
what the export wrote  ->  which option that was  ->  what the respondent actually saw
```

This works for both export formats — the text export's stale labels and the numeric export's codes both map to the same place. It was applied to every question, and anything genuinely ambiguous is **left untranslated rather than guessed**.

Result, verified on both exports:

- Zero placeholder strings survive.
- House age reads in the correct direction.
- The safety, flooding and affordability questions show their own answers.
- Both formats now produce **identical answers for every shared respondent** — a test that fails the build if it ever stops being true.

---

## What you should still do in Qualtrics

The fix above makes the pipeline robust, but the survey itself is still mis-configured. Two things are worth correcting at the source:

1. **Clear or correct the Variable Naming values** on the 28 affected questions so future exports carry the real choice text. This is the root cause.
2. **Fix the recode values on the house-condition question** so choice 5 exports as `5`, not `1`. Until this is done, a respondent who genuinely answers "Excellent" will be indistinguishable from one who answers "Critical" in a numeric export.

One more, unrelated to labels: the dashboard currently holds **110 responses while the CSVs in the project folders hold only 75 and 84.** Anyone checking the dashboard against those files will find rows that appear to be missing. Keeping a current export alongside the data would prevent that confusion.
