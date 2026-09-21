# Verification rounds — what was found, what it affected, how it was fixed

Every round was run against the **live production dashboard** at
`https://keystone-project-survey-blue.vercel.app/`, signed in as admin, by
filtering the map to *Matched (contact + Qualtric)*, clicking each point one at
a time, opening the **Survey Answers** tab and reading what was painted on
screen. Values were then compared against the **May 4 Qualtrics export**.

**No data was uploaded, replaced or deleted at any point.** Counts were
identical at the start and end of every round: **110 survey responses,
16 field points, 321 community contacts.**

---

## Round 0 — before the rounds began

Fixes made from the initial audit, deployed before round v1:

| # | Problem | Effect | Fix |
|---|---|---|---|
| 0.1 | Export labels (`VariableNaming`) had gone stale; the dashboard showed placeholder text, another question's answers, and a reversed house-age scale | ~1,441 answer cells wrong; 19 households under-scored; 6 shown as Low risk when they are Medium | Generated `api/qsf_labels.py` from the survey definition and resolve every answer back through it, before any hand-written table |
| 0.2 | `QID141` condition scale inverted — code `1` read as "Excellent" | The 15 worst homes displayed as the best, and lost 35 structural risk points each | Corrected to "Critical". Verified empirically: all 11 responses carrying code `1` read "Choice 5" in the text export, and the survey has zero Excellent answers |
| 0.3 | Hospital-visit codes 2 and 3 mapped to "No" | 16 households' respiratory hospital visits recorded as No, suppressing the +20 health penalty | Mapped to their real "Yes, …" variants |
| 0.4 | Popup labels truncated at 90 characters and paraphrased | Could not be found in the export with Excel's Find | Labels are now the survey's own wording, untruncated — 58 of 60 match the CSV byte for byte |
| 0.5 | The four water-leakage rows were attributed to the wrong questions | "Water leakage — Roof" was actually the *broken water pipes* column | Labels now come from the column actually read |
| 0.6 | Integer recode codes extracted as `6.0` | Any question without a label table would display `6.0` as the answer | Integral floats render as integers |

---

## Round v1 — 30 points

**Sample:** all 24 matched points present in the May export that had never been
clicked, plus 6 repeats to reach 30. Seed 1.

### Problems found

**v1-A — the checking tool resolved labels by column name instead of QID**

*Found:* 1,267 of 1,800 answer cells reported as "CSV code unresolvable".

*Cause:* fields such as `respiratory_ill` are read from the CSV by column name
(`RespIll`), and I was looking those names up in the survey-definition map,
which is keyed by question ID. The lookup found nothing.

*Effect:* a verification-tool defect only — **it never affected the dashboard
or the data.** But left unfixed it would have hidden real mismatches behind a
wall of false "unresolvable" results.

*Fix:* take the QID from the export's own `ImportId` header row, which carries
the real question ID for every column. Unresolvable cells fell from 1,267 to 0.

**v1-B — a respondent's real ownership answer was being shown as "Other"**

*Found:* one household (`R_3usRq7RFV77PKWl`) answered "Live with
friends/family" (code 3); the popup showed "Other".

*Effect:* a housing-insecurity signal — relevant to this research — was being
flattened away. My earlier fix had deliberately kept a three-way
Owner/Renter/Other split, which turned out to be too conservative.

*Fix:* keep the respondent's actual answer. Verified safe for every consumer:
the owner/renter counts and map filters test the literal strings `Owner` and
`Renter`, and the "other" bucket is derived as the remainder, so the aggregate
is unchanged at 8 on both exports. Deployed.

**v1-C — the deploy failed**

*Found:* deployment `fsxr98eik` failed in 10 seconds:
`Total bundle size (254.41 MB) exceeds the maximum function size (225 MB)`.

*Cause:* Vercel copies the repository into every serverless function, and
`docs/` had grown to 120 MB — **because of the audit screenshots I had been
saving** — on top of `final review/` (48 MB) and `user_manual/` (27 MB). None
of it is routed or executed.

*Effect:* that one deployment failed. Production kept serving the previous
healthy build throughout; no outage, no data affected.

*Fix:* added those directories to `.vercelignore`. Uploaded files fell from
**405 to 105** and the next deploy completed normally. Verified live afterwards:
`/static`, `/api/iaq-points`, `/api/survey-points`, `/api/field-points` and the
login page all return 200; `/api/analysis` returns 401 unauthenticated, which is
correct because it is admin-gated.

### v1 result, after fixes

| Check | Result |
|---|---|
| Addresses agree (geolocated / popup / Qualtrics) | **30 / 30** — 26 exact, 4 where the popup shows the street only |
| Answer cells compared | 1,800 (30 points × 60 questions) |
| Exactly matching | 504 |
| Same answer, popup shows the export's stale label | 686 |
| Same answer, popup shows placeholder text | 390 |
| Blank in both, or blank ≡ "none" | 178 |
| Deliberate Yes/No summaries (mold, hospital visit) | 41 |
| Old build bucketed ownership as "Other" | 1 |
| **Unexplained differences** | **0** |

---

## Round v2 — 30 different points

**Sample:** 30 matched points present in the May export, **none of them used in
v1**. Seed 2. Run against the redeployed build.

### Problem found

**v2-A — a respondent's typo was reported as an address mismatch**

*Found:* one point (`R_lDNFFIRpCANiFsV`) flagged CHECK. The county parcel says
`6406 BUCKNELL Ave`, the popup says `6406 Bucknell`, and the respondent typed
`6406 bucknelle Ave` — with an extra "e".

*Effect:* a verification-tool false positive. All three refer to the same house;
nothing is wrong with the data.

*Fix:* the address comparison now requires an exact house number but tolerates a
small spelling difference in the street name, and reports the result honestly as
"respondent typed a typo" rather than either hiding it or calling it a mismatch.

### v2 result, after fix

| Check | Result |
|---|---|
| Addresses agree | **30 / 30** — 26 exact, 3 street-only, 1 respondent typo |
| Answer cells compared | 1,800 |
| Exactly matching | 526 |
| Same answer, popup shows the export's stale label | 654 |
| Same answer, popup shows placeholder text | 414 |
| Blank in both, or blank ≡ "none" | 164 |
| Deliberate Yes/No summaries | 41 |
| Old build bucketed ownership as "Other" | 1 |
| **Unexplained differences** | **0** |

---

## What the two rounds together establish

Across **60 points and 3,600 answer comparisons**, on the live dashboard:

1. **Addresses are correct.** 60 of 60 points agree across all three sources —
   the county parcel the marker sits on, the address in the popup header, and
   the address the respondent typed. There is not a single case of a point
   sitting on the wrong house.
2. **Every answer traces to the respondent's real answer.** Zero unexplained
   differences in either round.
3. **The remaining visible wrongness is the stale export labels**, which
   accounts for 1,040 (v1) and 1,068 (v2) cells. That is already corrected in
   the code; those cells turn green the moment the dashboard's stored data is
   reprocessed.

### Two presentation issues worth fixing later

- **7 of 60 popups show only a street name** ("Dennison", "Baylor Ave") instead
  of the house number, because the stored record has no address and the popup
  falls back to the street. The underlying data is correct in every case.
- **2 points open a popup with no address header at all**
  (`R_5LnXMcaezhqW28F`, `R_bt9KhSC0xqF2xuS`) and render 66 rows instead of 64.
  These are the two households flagged earlier as matched in the data but drawn
  as "Qualtric only" on the map — the same defect, seen from the popup side.

---

## The one thing still outstanding

The dashboard draws its answers from a **stored snapshot** built when the data
was last uploaded, not from live computation. All of the fixes above are
deployed in the code, but the snapshot still holds the old values, so the
dashboard will keep showing the stale labels until the survey data is
reprocessed.

Reprocessing needs a **current Qualtrics export** (~110 responses). The April
and May files in the project hold 75 and 84, and the upload guard correctly
refuses anything that would drop responses — which is why nothing was uploaded
during this audit.

**When you have a current export, one upload through the dashboard's Update
Data flow will apply every fix at once**, and the yellow and red cells in the
attached tables should turn green. The `BASELINE_BEFORE_UPLOAD.json` snapshot
and `scripts/audit/verify_no_data_loss.py` are in place to prove nothing is lost
when that happens.
