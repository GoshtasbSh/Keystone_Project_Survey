# Popup (as rendered on screen) vs the May 4 Qualtrics export

Every "Popup shows" value in this table was read out of the live `-blue` dashboard after clicking the map marker and opening the **Survey Answers** tab — it is what a person sees, not an API value. Screenshots of each popup are in `../screenshots/`.

Rows are joined to a Qualtrics question by the popup's own label, then to a CSV column by that question's `ImportId` (QID) — never by column position.

**Verdicts** — `MATCH`: popup equals the CSV cell. `PLACEHOLDER`: the popup shows Qualtrics placeholder text (`Click to write …`); the respondent did answer, but neither the export nor the dashboard resolves the real label (findings F0/F9). `RECODE`: the CSV holds a numeric code and the popup shows a translated label. `DIFFERENT`: popup disagrees with the CSV. `EMPTY-BOTH`: blank in both — correct. `MISSING`: the CSV has an answer but the popup shows nothing. `NOT-IN-EXPORT`: that QID has no column in this export.

## Verdict totals

| Verdict | Cells | % |
|---|---|---|
| RECODE | 1257 | 69.8% |
| PLACEHOLDER | 417 | 23.1% |
| DIFFERENT | 63 | 3.5% |
| EMPTY-BOTH | 33 | 1.8% |
| MATCH | 30 | 1.7% |
| NOT-IN-EXPORT | 2 | 0.1% |

Total answer cells compared: **1802** across **30** points.

## 1. `R_1E4YReRP6XTeX06` — 6390 Bucknell Ave

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_1E4YReRP6XTeX06.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Seasonally | 3 | 123 | `RespIll` | RECODE |
| 2 | How often does anyone in your home have asthma symptoms? | Seasonally | 3 | 122 | `asthma` | RECODE |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | 5 | 125 | `wheeze` | RECODE |
| 4 | How often does anyone in your home experience headaches? | Rarely or Never | 5 | 120 | `Headache` | RECODE |
| 5 | How often do you feel tired or fatigued in your home? | weekly | 1 | 124 | `Tired` | RECODE |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | yes | 2 | 132 | `Hospital Respiratory` | RECODE |
| 7 | Evidence of mold in any area of the home? | Yes | 10 | 108 | `Mold` | RECODE |
| 8 | Water leakage — Roof | none | 4 | 110 | `Leakage 2_1` | RECODE |
| 9 | Water leakage — Walls | none | 4 | 111 | `Leakage 2_2` | RECODE |
| 10 | Water leakage — Windows | none | 4 | 112 | `Leakage 2_3` | RECODE |
| 11 | Water leakage — Floor | none | 4 | 113 | `Leakage 2_4` | RECODE |
| 12 | Cooling system — Central AC | More than 15 years | 3 | 100 | `Cooling System _1` | RECODE |
| 13 | Cooling system — Window unit | nan | — | 101 | `Cooling System _2` | DIFFERENT |
| 14 | Cooling system — Fan only | less than 10 years | 1 | 102 | `Cooling System _3` | RECODE |
| 15 | Cooling system — No cooling | nan | — | 103 | `Cooling System _4` | DIFFERENT |
| 16 | Cooking fuel / method | electric cooktops | 7 | 106 | `Cooking` | RECODE |
| 17 | When was your house built? | Built 1960–1979 | 2 | 39 | `QID192` | RECODE |
| 18 | What type of house do you live in? | Double Wide Mobile Home | 2 | 40 | `QID128` | RECODE |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Fair- Some repairs needed. | 3 | 55 | `QID141` | RECODE |
| 20 | What is your current housing ownership status? | Owner | 1 | 24 | `Ownership` | RECODE |
| 21 | How long have you lived in High Ridge Estates? (years) | 6 | 6 | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Steel | 3 | 44 | `QID47` | RECODE |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | 1 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Less than 6 months | 1 | 56 | `QID21` | RECODE |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | Click to write Choice 4 | 4 | 57 | `QID194` | PLACEHOLDER |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 4 | 2 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes - Portable (Which Room(s)),Yes- Integrated into central air heating system,Don’t Know | 1,2,4 | 59 | `QID19` | DIFFERENT |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 1 | 1 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 3 | 3 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 3 | 3 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 1 | 1 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 1 | 1 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 2 | 2 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | Click to write Scale Point 1 | 1 | 36 | `QID181_8` | PLACEHOLDER |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Nature reserves and preserves | 7 | 67 | `QID195_1` | RECODE |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Nature reserves and preserves | 7 | 68 | `QID195_2` | RECODE |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Nature reserves and preserves | 7 | 69 | `QID195_3` | RECODE |
| 39 | Intervention — Improve heating/cooling system(s) | Click to write Scale Point 1 | 1 | 70 | `QID195_4` | PLACEHOLDER |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Click to write Scale Point 1 | 1 | 71 | `QID195_5` | PLACEHOLDER |
| 41 | Intervention — Replace well/septic | Click to write Scale Point 1 | 1 | 72 | `QID195_6` | PLACEHOLDER |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Nature reserves and preserves | 7 | 74 | `QID195_8` | RECODE |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Click to write Scale Point 1 | 1 | 75 | `QID195_9` | PLACEHOLDER |
| 45 | Intervention — Trim trees | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 76 | `QID195_10` | RECODE |
| 46 | Intervention — Improved drainage | Nature reserves and preserves | 7 | 77 | `QID195_11` | RECODE |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | 2 | 84 | `QID124_1` | RECODE |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | 2 | 85 | `QID124_2` | RECODE |
| 49 | Experience — Extreme heat in recent years | Weekly | 2 | 86 | `QID124_3` | RECODE |
| 50 | Experience — Changing your kids' school due to moving | Weekly | 2 | 87 | `QID124_4` | RECODE |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Daily | 1 | 88 | `QID124_5` | RECODE |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | 2 | 89 | `QID124_6` | RECODE |
| 53 | Experience — Well drying up | Weekly | 2 | 90 | `QID124_7` | RECODE |
| 54 | Experience — A problem with pests in your home | Daily | 1 | 91 | `QID124_8` | RECODE |
| 55 | Experience — A problem with water leaks | Weekly | 2 | 92 | `QID124_9` | RECODE |
| 56 | Experience — A problem with loose animals | Weekly | 2 | 93 | `QID124_10` | RECODE |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | 1 | 133 | `QID211` | RECODE |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | 2 | 134 | `QID219` | RECODE |
| 59 | What is the highest level of education you have completed? | Vocational/Technical Licensing or Certification | 9 | 142 | `QID178` | RECODE |
| 60 | Which best describes your employment status? | Employed- Full time | 1 | 143 | `QID176` | RECODE |

## 2. `R_23kV7GlWM0LQkKc` — 6176 Harvard Avenue

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_23kV7GlWM0LQkKc.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | weekly | 1 | 123 | `RespIll` | RECODE |
| 2 | How often does anyone in your home have asthma symptoms? | weekly | 1 | 122 | `asthma` | RECODE |
| 3 | How often does anyone in your home wheeze? | Seasonally | 3 | 125 | `wheeze` | RECODE |
| 4 | How often does anyone in your home experience headaches? | weekly | 1 | 120 | `Headache` | RECODE |
| 5 | How often do you feel tired or fatigued in your home? | weekly | 1 | 124 | `Tired` | RECODE |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | yes | 1 | 132 | `Hospital Respiratory` | RECODE |
| 7 | Evidence of mold in any area of the home? | Yes | 7 | 108 | `Mold` | RECODE |
| 8 | Water leakage — Roof | not fixed | 3 | 110 | `Leakage 2_1` | RECODE |
| 9 | Water leakage — Walls | not fixed | 3 | 111 | `Leakage 2_2` | RECODE |
| 10 | Water leakage — Windows | not fixed | 3 | 112 | `Leakage 2_3` | RECODE |
| 11 | Water leakage — Floor | none | 4 | 113 | `Leakage 2_4` | RECODE |
| 12 | Cooling system — Central AC | nan | — | 100 | `Cooling System _1` | DIFFERENT |
| 13 | Cooling system — Window unit | Don't know/Not applicable | 4 | 101 | `Cooling System _2` | RECODE |
| 14 | Cooling system — Fan only | 10 to 15 years | 2 | 102 | `Cooling System _3` | RECODE |
| 15 | Cooling system — No cooling | nan | — | 103 | `Cooling System _4` | DIFFERENT |
| 16 | Cooking fuel / method | electric cooktops | 7 | 106 | `Cooking` | RECODE |
| 17 | When was your house built? | Built 1960–1979 | 2 | 39 | `QID192` | RECODE |
| 18 | What type of house do you live in? | Double Wide Mobile Home | 2 | 40 | `QID128` | RECODE |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Poor- Major repairs needed. | 4 | 55 | `QID141` | RECODE |
| 20 | What is your current housing ownership status? | Owner | 1 | 24 | `Ownership` | RECODE |
| 21 | How long have you lived in High Ridge Estates? (years) | 14 | 14 | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | 4 | 44 | `QID47` | RECODE |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 4 | 2 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Less than 6 months | 1 | 56 | `QID21` | RECODE |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | More than 6 months | 2 | 57 | `QID194` | RECODE |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 3 | 1 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes- Integrated into central air heating system,No,Click to write Choice 6 | 2,3,6 | 59 | `QID19` | PLACEHOLDER |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 1 | 1 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 2 | 2 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 3 | 3 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 3 | 3 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 2 | 2 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 3 | 3 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 67 | `QID195_1` | RECODE |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 68 | `QID195_2` | RECODE |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 69 | `QID195_3` | RECODE |
| 39 | Intervention — Improve heating/cooling system(s) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 70 | `QID195_4` | RECODE |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 71 | `QID195_5` | RECODE |
| 41 | Intervention — Replace well/septic | Click to write Scale Point 1 | 1 | 72 | `QID195_6` | PLACEHOLDER |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Nature reserves and preserves | 7 | 74 | `QID195_8` | RECODE |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Click to write Scale Point 1 | 1 | 75 | `QID195_9` | PLACEHOLDER |
| 45 | Intervention — Trim trees | Click to write Scale Point 1 | 1 | 76 | `QID195_10` | PLACEHOLDER |
| 46 | Intervention — Improved drainage | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 77 | `QID195_11` | RECODE |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | 2 | 84 | `QID124_1` | RECODE |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | 2 | 85 | `QID124_2` | RECODE |
| 49 | Experience — Extreme heat in recent years | Daily | 1 | 86 | `QID124_3` | RECODE |
| 50 | Experience — Changing your kids' school due to moving | Weekly | 2 | 87 | `QID124_4` | RECODE |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Weekly | 2 | 88 | `QID124_5` | RECODE |
| 52 | Experience — Losing home owners insurance due to age of home | Daily | 1 | 89 | `QID124_6` | RECODE |
| 53 | Experience — Well drying up | Weekly | 2 | 90 | `QID124_7` | RECODE |
| 54 | Experience — A problem with pests in your home | Daily | 1 | 91 | `QID124_8` | RECODE |
| 55 | Experience — A problem with water leaks | Daily | 1 | 92 | `QID124_9` | RECODE |
| 56 | Experience — A problem with loose animals | Daily | 1 | 93 | `QID124_10` | RECODE |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | 1 | 133 | `QID211` | RECODE |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | Name the problem | 4 | 134 | `QID219` | RECODE |
| 59 | What is the highest level of education you have completed? | Vocational/Technical Licensing or Certification | 9 | 142 | `QID178` | RECODE |
| 60 | Which best describes your employment status? | Unemployed | 3 | 143 | `QID176` | RECODE |

## 3. `R_378SeCJx2uslNli` — 6369 Dennison

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_378SeCJx2uslNli.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Seasonally | 3 | 123 | `RespIll` | RECODE |
| 2 | How often does anyone in your home have asthma symptoms? | Seasonally | 3 | 122 | `asthma` | RECODE |
| 3 | How often does anyone in your home wheeze? | Seasonally | 3 | 125 | `wheeze` | RECODE |
| 4 | How often does anyone in your home experience headaches? | Monthly | 2 | 120 | `Headache` | RECODE |
| 5 | How often do you feel tired or fatigued in your home? | Seasonally | 3 | 124 | `Tired` | RECODE |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | 4 | 132 | `Hospital Respiratory` | RECODE |
| 7 | Evidence of mold in any area of the home? | Yes | 1,4,7,9 | 108 | `Mold` | DIFFERENT |
| 8 | Water leakage — Roof | more than one week | 2 | 110 | `Leakage 2_1` | RECODE |
| 9 | Water leakage — Walls | less than one week | 1 | 111 | `Leakage 2_2` | RECODE |
| 10 | Water leakage — Windows | none | 4 | 112 | `Leakage 2_3` | RECODE |
| 11 | Water leakage — Floor | more than one week | 2 | 113 | `Leakage 2_4` | RECODE |
| 12 | Cooling system — Central AC | Don't know/Not applicable | 4 | 100 | `Cooling System _1` | RECODE |
| 13 | Cooling system — Window unit | 10 to 15 years | 2 | 101 | `Cooling System _2` | RECODE |
| 14 | Cooling system — Fan only | Don't know/Not applicable | 4 | 102 | `Cooling System _3` | RECODE |
| 15 | Cooling system — No cooling | less than 10 years | 1 | 103 | `Cooling System _4` | RECODE |
| 16 | Cooking fuel / method | electric cooktops | 7 | 106 | `Cooking` | RECODE |
| 17 | When was your house built? | Built 1960–1979 | 2 | 39 | `QID192` | RECODE |
| 18 | What type of house do you live in? | Double Wide Mobile Home | 2 | 40 | `QID128` | RECODE |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Poor- Major repairs needed. | 4 | 55 | `QID141` | RECODE |
| 20 | What is your current housing ownership status? | Owner | 1 | 24 | `Ownership` | RECODE |
| 21 | How long have you lived in High Ridge Estates? (years) | 9 | 9 | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | 4 | 44 | `QID47` | RECODE |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 4 | 2 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Don't know | 3 | 56 | `QID21` | RECODE |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | Don't know | 3 | 57 | `QID194` | RECODE |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 3 | 1 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes- Integrated into central air heating system,Don’t Know,Click to write Choice 6 | 2,4,6 | 59 | `QID19` | PLACEHOLDER |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 4 | 4 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 4 | 4 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 4 | 4 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 3 | 3 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 3 | 3 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 4 | 4 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 3 | 3 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | Click to write Scale Point 1 | 1 | 36 | `QID181_8` | PLACEHOLDER |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 67 | `QID195_1` | RECODE |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 68 | `QID195_2` | RECODE |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 69 | `QID195_3` | RECODE |
| 39 | Intervention — Improve heating/cooling system(s) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 70 | `QID195_4` | RECODE |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 71 | `QID195_5` | RECODE |
| 41 | Intervention — Replace well/septic | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 72 | `QID195_6` | RECODE |
| 42 | Intervention — Connect to city water through CCUA | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 73 | `QID195_7` | RECODE |
| 43 | Intervention — Add a fence for safety | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 74 | `QID195_8` | RECODE |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Click to write Scale Point 1 | 1 | 75 | `QID195_9` | PLACEHOLDER |
| 45 | Intervention — Trim trees | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 76 | `QID195_10` | RECODE |
| 46 | Intervention — Improved drainage | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 77 | `QID195_11` | RECODE |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | 2 | 84 | `QID124_1` | RECODE |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | 2 | 85 | `QID124_2` | RECODE |
| 49 | Experience — Extreme heat in recent years | Daily | 1 | 86 | `QID124_3` | RECODE |
| 50 | Experience — Changing your kids' school due to moving | Weekly | 2 | 87 | `QID124_4` | RECODE |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Weekly | 2 | 88 | `QID124_5` | RECODE |
| 52 | Experience — Losing home owners insurance due to age of home | Daily | 1 | 89 | `QID124_6` | RECODE |
| 53 | Experience — Well drying up | Daily | 1 | 90 | `QID124_7` | RECODE |
| 54 | Experience — A problem with pests in your home | Daily | 1 | 91 | `QID124_8` | RECODE |
| 55 | Experience — A problem with water leaks | Daily | 1 | 92 | `QID124_9` | RECODE |
| 56 | Experience — A problem with loose animals | Daily | 1 | 93 | `QID124_10` | RECODE |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | 1 | 133 | `QID211` | RECODE |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | 2 | 134 | `QID219` | RECODE |
| 59 | What is the highest level of education you have completed? | less than high school | 1 | 142 | `QID178` | RECODE |
| 60 | Which best describes your employment status? | Unemployed | 3 | 143 | `QID176` | RECODE |

## 4. `R_3N0BugWZGh4ufub` — 6348 Baylor Avenue

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_3N0BugWZGh4ufub.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | 5 | 123 | `RespIll` | RECODE |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | 5 | 122 | `asthma` | RECODE |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | 5 | 125 | `wheeze` | RECODE |
| 4 | How often does anyone in your home experience headaches? | Rarely or Never | 5 | 120 | `Headache` | RECODE |
| 5 | How often do you feel tired or fatigued in your home? | Rarely or Never | 5 | 124 | `Tired` | RECODE |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | 4 | 132 | `Hospital Respiratory` | RECODE |
| 7 | Evidence of mold in any area of the home? | No | — | 108 | `Mold` | DIFFERENT |
| 8 | Water leakage — Roof | none | 4 | 110 | `Leakage 2_1` | RECODE |
| 9 | Water leakage — Walls | none | 4 | 111 | `Leakage 2_2` | RECODE |
| 10 | Water leakage — Windows | none | 4 | 112 | `Leakage 2_3` | RECODE |
| 11 | Water leakage — Floor | none | 4 | 113 | `Leakage 2_4` | RECODE |
| 12 | Cooling system — Central AC | nan | — | 100 | `Cooling System _1` | DIFFERENT |
| 13 | Cooling system — Window unit | 10 to 15 years | 2 | 101 | `Cooling System _2` | RECODE |
| 14 | Cooling system — Fan only | nan | — | 102 | `Cooling System _3` | DIFFERENT |
| 15 | Cooling system — No cooling | nan | — | 103 | `Cooling System _4` | DIFFERENT |
| 16 | Cooking fuel / method | electric cooktops | 7 | 106 | `Cooking` | RECODE |
| 17 | When was your house built? | Click to write Choice 5 | 5 | 39 | `QID192` | PLACEHOLDER |
| 18 | What type of house do you live in? | Single Wide Mobile Home | 1 | 40 | `QID128` | RECODE |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Fair- Some repairs needed. | 3 | 55 | `QID141` | RECODE |
| 20 | What is your current housing ownership status? | Owner | 1 | 24 | `Ownership` | RECODE |
| 21 | How long have you lived in High Ridge Estates? (years) | 6yrs | 6yrs | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Concrete | 2 | 44 | `QID47` | RECODE |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | 1 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | More than 6 months | 2 | 56 | `QID21` | RECODE |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | Click to write Choice 4 | 4 | 57 | `QID194` | PLACEHOLDER |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 3 | 1 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes - Portable (Which Room(s)),No,Don’t Know,Click to write Choice 5,Click to write Choice 6 | 1,3,4,5,6 | 59 | `QID19` | PLACEHOLDER |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 3 | 3 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 3 | 3 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 3 | 3 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 3 | 3 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 1 | 1 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 3 | 3 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | Click to write Scale Point 1 | 1 | 36 | `QID181_8` | PLACEHOLDER |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 67 | `QID195_1` | RECODE |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 68 | `QID195_2` | RECODE |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 69 | `QID195_3` | RECODE |
| 39 | Intervention — Improve heating/cooling system(s) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 70 | `QID195_4` | RECODE |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 71 | `QID195_5` | RECODE |
| 41 | Intervention — Replace well/septic | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 72 | `QID195_6` | RECODE |
| 42 | Intervention — Connect to city water through CCUA | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 73 | `QID195_7` | RECODE |
| 43 | Intervention — Add a fence for safety | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 74 | `QID195_8` | RECODE |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 75 | `QID195_9` | RECODE |
| 45 | Intervention — Trim trees | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 76 | `QID195_10` | RECODE |
| 46 | Intervention — Improved drainage | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 77 | `QID195_11` | RECODE |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | 2 | 84 | `QID124_1` | RECODE |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | 2 | 85 | `QID124_2` | RECODE |
| 49 | Experience — Extreme heat in recent years | Weekly | 2 | 86 | `QID124_3` | RECODE |
| 50 | Experience — Changing your kids' school due to moving | Weekly | 2 | 87 | `QID124_4` | RECODE |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Weekly | 2 | 88 | `QID124_5` | RECODE |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | 2 | 89 | `QID124_6` | RECODE |
| 53 | Experience — Well drying up | Weekly | 2 | 90 | `QID124_7` | RECODE |
| 54 | Experience — A problem with pests in your home | Weekly | 2 | 91 | `QID124_8` | RECODE |
| 55 | Experience — A problem with water leaks | Weekly | 2 | 92 | `QID124_9` | RECODE |
| 56 | Experience — A problem with loose animals | Daily | 1 | 93 | `QID124_10` | RECODE |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | 1 | 133 | `QID211` | RECODE |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | 2 | 134 | `QID219` | RECODE |
| 59 | What is the highest level of education you have completed? | High school diploma or equivalent | 5 | 142 | `QID178` | RECODE |
| 60 | Which best describes your employment status? | Unemployed | 3 | 143 | `QID176` | RECODE |

## 5. `R_43YLnrxxRNRA5hW` — 6260 Baylor Avenue

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_43YLnrxxRNRA5hW.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | 5 | 123 | `RespIll` | RECODE |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | 5 | 122 | `asthma` | RECODE |
| 3 | How often does anyone in your home wheeze? | weekly | 1 | 125 | `wheeze` | RECODE |
| 4 | How often does anyone in your home experience headaches? | Rarely or Never | 5 | 120 | `Headache` | RECODE |
| 5 | How often do you feel tired or fatigued in your home? | Rarely or Never | 5 | 124 | `Tired` | RECODE |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | 4 | 132 | `Hospital Respiratory` | RECODE |
| 7 | Evidence of mold in any area of the home? | Yes | 10 | 108 | `Mold` | RECODE |
| 8 | Water leakage — Roof | none | 4 | 110 | `Leakage 2_1` | RECODE |
| 9 | Water leakage — Walls | none | 4 | 111 | `Leakage 2_2` | RECODE |
| 10 | Water leakage — Windows | none | 4 | 112 | `Leakage 2_3` | RECODE |
| 11 | Water leakage — Floor | none | 4 | 113 | `Leakage 2_4` | RECODE |
| 12 | Cooling system — Central AC | More than 15 years | 3 | 100 | `Cooling System _1` | RECODE |
| 13 | Cooling system — Window unit | More than 15 years | 3 | 101 | `Cooling System _2` | RECODE |
| 14 | Cooling system — Fan only | less than 10 years | 1 | 102 | `Cooling System _3` | RECODE |
| 15 | Cooling system — No cooling | Don't know/Not applicable | 4 | 103 | `Cooling System _4` | RECODE |
| 16 | Cooking fuel / method | electric cooktops | 7 | 106 | `Cooking` | RECODE |
| 17 | When was your house built? | Built 1960–1979 | 2 | 39 | `QID192` | RECODE |
| 18 | What type of house do you live in? | Double Wide Mobile Home | 2 | 40 | `QID128` | RECODE |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Good- Minor repairs needed. | 2 | 55 | `QID141` | RECODE |
| 20 | What is your current housing ownership status? | Owner | 1 | 24 | `Ownership` | RECODE |
| 21 | How long have you lived in High Ridge Estates? (years) | 6 years | 6 years | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | 4 | 44 | `QID47` | RECODE |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | 1 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Less than 6 months | 1 | 56 | `QID21` | RECODE |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | Less than 6 months | 1 | 57 | `QID194` | RECODE |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 4 | 2 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes- Integrated into central air heating system | 2 | 59 | `QID19` | RECODE |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 1 | 1 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 4 | 4 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 4 | 4 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 3 | 3 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 3 | 3 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 5 | 5 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Click to write Scale Point 1 | 1 | 67 | `QID195_1` | PLACEHOLDER |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Click to write Scale Point 1 | 1 | 68 | `QID195_2` | PLACEHOLDER |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Click to write Scale Point 1 | 1 | 69 | `QID195_3` | PLACEHOLDER |
| 39 | Intervention — Improve heating/cooling system(s) | Click to write Scale Point 1 | 1 | 70 | `QID195_4` | PLACEHOLDER |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Click to write Scale Point 1 | 1 | 71 | `QID195_5` | PLACEHOLDER |
| 41 | Intervention — Replace well/septic | Click to write Scale Point 1 | 1 | 72 | `QID195_6` | PLACEHOLDER |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 74 | `QID195_8` | RECODE |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Click to write Scale Point 1 | 1 | 75 | `QID195_9` | PLACEHOLDER |
| 45 | Intervention — Trim trees | Click to write Scale Point 1 | 1 | 76 | `QID195_10` | PLACEHOLDER |
| 46 | Intervention — Improved drainage | Click to write Scale Point 1 | 1 | 77 | `QID195_11` | PLACEHOLDER |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | 2 | 84 | `QID124_1` | RECODE |
| 48 | Experience — In case of flooding, received help for cleaning | Biweekly | 3 | 85 | `QID124_2` | RECODE |
| 49 | Experience — Extreme heat in recent years | Daily | 1 | 86 | `QID124_3` | RECODE |
| 50 | Experience — Changing your kids' school due to moving | Biweekly | 3 | 87 | `QID124_4` | RECODE |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Weekly | 2 | 88 | `QID124_5` | RECODE |
| 52 | Experience — Losing home owners insurance due to age of home | Biweekly | 3 | 89 | `QID124_6` | RECODE |
| 53 | Experience — Well drying up | Biweekly | 3 | 90 | `QID124_7` | RECODE |
| 54 | Experience — A problem with pests in your home | Weekly | 2 | 91 | `QID124_8` | RECODE |
| 55 | Experience — A problem with water leaks | Weekly | 2 | 92 | `QID124_9` | RECODE |
| 56 | Experience — A problem with loose animals | Weekly | 2 | 93 | `QID124_10` | RECODE |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | 1 | 133 | `QID211` | RECODE |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | 2 | 134 | `QID219` | RECODE |
| 59 | What is the highest level of education you have completed? | less than high school | 1 | 142 | `QID178` | RECODE |
| 60 | Which best describes your employment status? | Retired | 4 | 143 | `QID176` | RECODE |

## 6. `R_5241irqeSjBwQi1` — 7171 Pembroke Street

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_5241irqeSjBwQi1.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | 5 | 123 | `RespIll` | RECODE |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | 5 | 122 | `asthma` | RECODE |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | 5 | 125 | `wheeze` | RECODE |
| 4 | How often does anyone in your home experience headaches? | Rarely or Never | 5 | 120 | `Headache` | RECODE |
| 5 | How often do you feel tired or fatigued in your home? | Rarely or Never | 5 | 124 | `Tired` | RECODE |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | 4 | 132 | `Hospital Respiratory` | RECODE |
| 7 | Evidence of mold in any area of the home? | Yes | 9,10 | 108 | `Mold` | DIFFERENT |
| 8 | Water leakage — Roof | none | 4 | 110 | `Leakage 2_1` | RECODE |
| 9 | Water leakage — Walls | none | 4 | 111 | `Leakage 2_2` | RECODE |
| 10 | Water leakage — Windows | none | 4 | 112 | `Leakage 2_3` | RECODE |
| 11 | Water leakage — Floor | none | 4 | 113 | `Leakage 2_4` | RECODE |
| 12 | Cooling system — Central AC | Don't know/Not applicable | 4 | 100 | `Cooling System _1` | RECODE |
| 13 | Cooling system — Window unit | less than 10 years | 1 | 101 | `Cooling System _2` | RECODE |
| 14 | Cooling system — Fan only | Don't know/Not applicable | 4 | 102 | `Cooling System _3` | RECODE |
| 15 | Cooling system — No cooling | Don't know/Not applicable | 4 | 103 | `Cooling System _4` | RECODE |
| 16 | Cooking fuel / method | electric cooktops | 7 | 106 | `Cooking` | RECODE |
| 17 | When was your house built? | Built 1980–1999 | 3 | 39 | `QID192` | RECODE |
| 18 | What type of house do you live in? | Single Wide Mobile Home | 1 | 40 | `QID128` | RECODE |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Click to write Choice 5 | 1 | 55 | `QID141` | PLACEHOLDER |
| 20 | What is your current housing ownership status? | Owner | 1 | 24 | `Ownership` | RECODE |
| 21 | How long have you lived in High Ridge Estates? (years) | 15 | 15 | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | 4 | 44 | `QID47` | RECODE |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | 1 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Don't know | 3 | 56 | `QID21` | RECODE |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | Less than 6 months | 1 | 57 | `QID194` | RECODE |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 4 | 2 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes - Portable (Which Room(s)),Yes- Integrated into central air heating system,Click to write Choice 7 | 1,2,7 | 59 | `QID19` | PLACEHOLDER |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 2 | 2 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 5 | 5 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 2 | 2 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 5 | 5 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 1 | 1 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 5 | 5 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 67 | `QID195_1` | RECODE |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 68 | `QID195_2` | RECODE |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Nature reserves and preserves | 7 | 69 | `QID195_3` | RECODE |
| 39 | Intervention — Improve heating/cooling system(s) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 70 | `QID195_4` | RECODE |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Nature reserves and preserves | 7 | 71 | `QID195_5` | RECODE |
| 41 | Intervention — Replace well/septic | Nature reserves and preserves | 7 | 72 | `QID195_6` | RECODE |
| 42 | Intervention — Connect to city water through CCUA | Nature reserves and preserves | 7 | 73 | `QID195_7` | RECODE |
| 43 | Intervention — Add a fence for safety | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 74 | `QID195_8` | RECODE |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Nature reserves and preserves | 7 | 75 | `QID195_9` | RECODE |
| 45 | Intervention — Trim trees | Nature reserves and preserves | 7 | 76 | `QID195_10` | RECODE |
| 46 | Intervention — Improved drainage | Nature reserves and preserves | 7 | 77 | `QID195_11` | RECODE |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | 2 | 84 | `QID124_1` | RECODE |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | 2 | 85 | `QID124_2` | RECODE |
| 49 | Experience — Extreme heat in recent years | Weekly | 2 | 86 | `QID124_3` | RECODE |
| 50 | Experience — Changing your kids' school due to moving | Weekly | 2 | 87 | `QID124_4` | RECODE |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Weekly | 2 | 88 | `QID124_5` | RECODE |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | 2 | 89 | `QID124_6` | RECODE |
| 53 | Experience — Well drying up | Weekly | 2 | 90 | `QID124_7` | RECODE |
| 54 | Experience — A problem with pests in your home | Weekly | 2 | 91 | `QID124_8` | RECODE |
| 55 | Experience — A problem with water leaks | Weekly | 2 | 92 | `QID124_9` | RECODE |
| 56 | Experience — A problem with loose animals | Weekly | 2 | 93 | `QID124_10` | RECODE |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | 1 | 133 | `QID211` | RECODE |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | 2 | 134 | `QID219` | RECODE |
| 59 | What is the highest level of education you have completed? | High school diploma or equivalent | 5 | 142 | `QID178` | RECODE |
| 60 | Which best describes your employment status? | Employed- Full time | 1 | 143 | `QID176` | RECODE |

## 7. `R_53V7a6BGdQkzzSd` — 7160 Pembroke Street

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_53V7a6BGdQkzzSd.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | 5 | 123 | `RespIll` | RECODE |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | 5 | 122 | `asthma` | RECODE |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | 5 | 125 | `wheeze` | RECODE |
| 4 | How often does anyone in your home experience headaches? | Rarely or Never | 5 | 120 | `Headache` | RECODE |
| 5 | How often do you feel tired or fatigued in your home? | Rarely or Never | 5 | 124 | `Tired` | RECODE |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | 4 | 132 | `Hospital Respiratory` | RECODE |
| 7 | Evidence of mold in any area of the home? | Yes | 10 | 108 | `Mold` | RECODE |
| 8 | Water leakage — Roof | none | 4 | 110 | `Leakage 2_1` | RECODE |
| 9 | Water leakage — Walls | none | 4 | 111 | `Leakage 2_2` | RECODE |
| 10 | Water leakage — Windows | none | 4 | 112 | `Leakage 2_3` | RECODE |
| 11 | Water leakage — Floor | none | 4 | 113 | `Leakage 2_4` | RECODE |
| 12 | Cooling system — Central AC | less than 10 years | 1 | 100 | `Cooling System _1` | RECODE |
| 13 | Cooling system — Window unit | nan | — | 101 | `Cooling System _2` | DIFFERENT |
| 14 | Cooling system — Fan only | less than 10 years | 1 | 102 | `Cooling System _3` | RECODE |
| 15 | Cooling system — No cooling | nan | — | 103 | `Cooling System _4` | DIFFERENT |
| 16 | Cooking fuel / method | electric cooktops | 7 | 106 | `Cooking` | RECODE |
| 17 | When was your house built? | Before 1960 | 1 | 39 | `QID192` | RECODE |
| 18 | What type of house do you live in? | Double Wide Mobile Home | 2 | 40 | `QID128` | RECODE |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Click to write Choice 5 | 1 | 55 | `QID141` | PLACEHOLDER |
| 20 | What is your current housing ownership status? | Owner | 1 | 24 | `Ownership` | RECODE |
| 21 | How long have you lived in High Ridge Estates? (years) | 40yrs | 40yrs | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | 4 | 44 | `QID47` | RECODE |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | 1 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Less than 6 months | 1 | 56 | `QID21` | RECODE |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | More than 6 months | 2 | 57 | `QID194` | RECODE |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 3 | 1 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes- Integrated into central air heating system,Click to write Choice 6,Click to write Choice 7 | 2,6,7 | 59 | `QID19` | PLACEHOLDER |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 1 | 1 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 5 | 5 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 5 | 5 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 5 | 5 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 5 | 5 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 5 | 5 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 5 | 5 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Nature reserves and preserves | 7 | 67 | `QID195_1` | RECODE |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Nature reserves and preserves | 7 | 68 | `QID195_2` | RECODE |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Nature reserves and preserves | 7 | 69 | `QID195_3` | RECODE |
| 39 | Intervention — Improve heating/cooling system(s) | Nature reserves and preserves | 7 | 70 | `QID195_4` | RECODE |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Nature reserves and preserves | 7 | 71 | `QID195_5` | RECODE |
| 41 | Intervention — Replace well/septic | Nature reserves and preserves | 7 | 72 | `QID195_6` | RECODE |
| 42 | Intervention — Connect to city water through CCUA | Nature reserves and preserves | 7 | 73 | `QID195_7` | RECODE |
| 43 | Intervention — Add a fence for safety | Nature reserves and preserves | 7 | 74 | `QID195_8` | RECODE |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Nature reserves and preserves | 7 | 75 | `QID195_9` | RECODE |
| 45 | Intervention — Trim trees | Nature reserves and preserves | 7 | 76 | `QID195_10` | RECODE |
| 46 | Intervention — Improved drainage | Nature reserves and preserves | 7 | 77 | `QID195_11` | RECODE |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | 2 | 84 | `QID124_1` | RECODE |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | 2 | 85 | `QID124_2` | RECODE |
| 49 | Experience — Extreme heat in recent years | Weekly | 2 | 86 | `QID124_3` | RECODE |
| 50 | Experience — Changing your kids' school due to moving | Weekly | 2 | 87 | `QID124_4` | RECODE |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Daily | 1 | 88 | `QID124_5` | RECODE |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | 2 | 89 | `QID124_6` | RECODE |
| 53 | Experience — Well drying up | Weekly | 2 | 90 | `QID124_7` | RECODE |
| 54 | Experience — A problem with pests in your home | Weekly | 2 | 91 | `QID124_8` | RECODE |
| 55 | Experience — A problem with water leaks | Weekly | 2 | 92 | `QID124_9` | RECODE |
| 56 | Experience — A problem with loose animals | Daily | 1 | 93 | `QID124_10` | RECODE |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | 1 | 133 | `QID211` | RECODE |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | 2 | 134 | `QID219` | RECODE |
| 59 | What is the highest level of education you have completed? | High school diploma or equivalent | 5 | 142 | `QID178` | RECODE |
| 60 | Which best describes your employment status? | Retired | 4 | 143 | `QID176` | RECODE |

## 8. `R_5BmauNbh58cXIzf` — 6280 Dennison

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_5BmauNbh58cXIzf.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | 5 | 123 | `RespIll` | RECODE |
| 2 | How often does anyone in your home have asthma symptoms? | Seasonally | 3 | 122 | `asthma` | RECODE |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | 5 | 125 | `wheeze` | RECODE |
| 4 | How often does anyone in your home experience headaches? | Seasonally | 3 | 120 | `Headache` | RECODE |
| 5 | How often do you feel tired or fatigued in your home? | weekly | 1 | 124 | `Tired` | RECODE |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | 4 | 132 | `Hospital Respiratory` | RECODE |
| 7 | Evidence of mold in any area of the home? | Yes | 4 | 108 | `Mold` | RECODE |
| 8 | Water leakage — Roof | none | 4 | 110 | `Leakage 2_1` | RECODE |
| 9 | Water leakage — Walls | none | 4 | 111 | `Leakage 2_2` | RECODE |
| 10 | Water leakage — Windows | none | 4 | 112 | `Leakage 2_3` | RECODE |
| 11 | Water leakage — Floor | none | 4 | 113 | `Leakage 2_4` | RECODE |
| 12 | Cooling system — Central AC | Don't know/Not applicable | 4 | 100 | `Cooling System _1` | RECODE |
| 13 | Cooling system — Window unit | less than 10 years | 1 | 101 | `Cooling System _2` | RECODE |
| 14 | Cooling system — Fan only | Don't know/Not applicable | 4 | 102 | `Cooling System _3` | RECODE |
| 15 | Cooling system — No cooling | less than 10 years | 1 | 103 | `Cooling System _4` | RECODE |
| 16 | Cooking fuel / method | electric cooktops | 7 | 106 | `Cooking` | RECODE |
| 17 | When was your house built? | Click to write Choice 5 | 5 | 39 | `QID192` | PLACEHOLDER |
| 18 | What type of house do you live in? | Single Wide Mobile Home | 1 | 40 | `QID128` | RECODE |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Fair- Some repairs needed. | 3 | 55 | `QID141` | RECODE |
| 20 | What is your current housing ownership status? | Renter | 2 | 24 | `Ownership` | RECODE |
| 21 | How long have you lived in High Ridge Estates? (years) | 2months | 2months | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Concrete | 2 | 44 | `QID47` | RECODE |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 4 | 2 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Don't know | 3 | 56 | `QID21` | RECODE |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | Don't know | 3 | 57 | `QID194` | RECODE |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 4 | 2 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes- Integrated into central air heating system,Click to write Choice 5,Click to write Choice 6 | 2,5,6 | 59 | `QID19` | PLACEHOLDER |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 3 | 3 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 3 | 3 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 3 | 3 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 3 | 3 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 1 | 1 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 3 | 3 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 67 | `QID195_1` | RECODE |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 68 | `QID195_2` | RECODE |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Nature reserves and preserves | 7 | 69 | `QID195_3` | RECODE |
| 39 | Intervention — Improve heating/cooling system(s) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 70 | `QID195_4` | RECODE |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 71 | `QID195_5` | RECODE |
| 41 | Intervention — Replace well/septic | Click to write Scale Point 1 | 1 | 72 | `QID195_6` | PLACEHOLDER |
| 42 | Intervention — Connect to city water through CCUA | Nature reserves and preserves | 7 | 73 | `QID195_7` | RECODE |
| 43 | Intervention — Add a fence for safety | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 74 | `QID195_8` | RECODE |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Click to write Scale Point 1 | 1 | 75 | `QID195_9` | PLACEHOLDER |
| 45 | Intervention — Trim trees | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 76 | `QID195_10` | RECODE |
| 46 | Intervention — Improved drainage | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 77 | `QID195_11` | RECODE |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | 2 | 84 | `QID124_1` | RECODE |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | 2 | 85 | `QID124_2` | RECODE |
| 49 | Experience — Extreme heat in recent years | Weekly | 2 | 86 | `QID124_3` | RECODE |
| 50 | Experience — Changing your kids' school due to moving | Biweekly | 3 | 87 | `QID124_4` | RECODE |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Weekly | 2 | 88 | `QID124_5` | RECODE |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | 2 | 89 | `QID124_6` | RECODE |
| 53 | Experience — Well drying up | Weekly | 2 | 90 | `QID124_7` | RECODE |
| 54 | Experience — A problem with pests in your home | Daily | 1 | 91 | `QID124_8` | RECODE |
| 55 | Experience — A problem with water leaks | Weekly | 2 | 92 | `QID124_9` | RECODE |
| 56 | Experience — A problem with loose animals | Daily | 1 | 93 | `QID124_10` | RECODE |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | 1 | 133 | `QID211` | RECODE |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | Not Sure | 3 | 134 | `QID219` | RECODE |
| 59 | What is the highest level of education you have completed? | High school diploma or equivalent | 5 | 142 | `QID178` | RECODE |
| 60 | Which best describes your employment status? | Employed- Full time | 1 | 143 | `QID176` | RECODE |

## 9. `R_5CxQduTse6FT7Z4` — 7156 Duke Street

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_5CxQduTse6FT7Z4.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | 5 | 123 | `RespIll` | RECODE |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | 5 | 122 | `asthma` | RECODE |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | 5 | 125 | `wheeze` | RECODE |
| 4 | How often does anyone in your home experience headaches? | Rarely or Never | 5 | 120 | `Headache` | RECODE |
| 5 | How often do you feel tired or fatigued in your home? | Rarely or Never | 5 | 124 | `Tired` | RECODE |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | 4 | 132 | `Hospital Respiratory` | RECODE |
| 7 | Evidence of mold in any area of the home? | Yes | 10 | 108 | `Mold` | RECODE |
| 8 | Water leakage — Roof | none | 4 | 110 | `Leakage 2_1` | RECODE |
| 9 | Water leakage — Walls | none | 4 | 111 | `Leakage 2_2` | RECODE |
| 10 | Water leakage — Windows | none | 4 | 112 | `Leakage 2_3` | RECODE |
| 11 | Water leakage — Floor | less than one week | 1 | 113 | `Leakage 2_4` | RECODE |
| 12 | Cooling system — Central AC | less than 10 years | 1 | 100 | `Cooling System _1` | RECODE |
| 13 | Cooling system — Window unit | Don't know/Not applicable | 4 | 101 | `Cooling System _2` | RECODE |
| 14 | Cooling system — Fan only | Don't know/Not applicable | 4 | 102 | `Cooling System _3` | RECODE |
| 15 | Cooling system — No cooling | less than 10 years | 1 | 103 | `Cooling System _4` | RECODE |
| 16 | Cooking fuel / method | electric cooktops | 7 | 106 | `Cooking` | RECODE |
| 17 | When was your house built? | Click to write Choice 5 | 5 | 39 | `QID192` | PLACEHOLDER |
| 18 | What type of house do you live in? | House built on site | 3 | 40 | `QID128` | RECODE |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Click to write Choice 5 | 1 | 55 | `QID141` | PLACEHOLDER |
| 20 | What is your current housing ownership status? | Renter | 2 | 24 | `Ownership` | RECODE |
| 21 | How long have you lived in High Ridge Estates? (years) | 0 | 0 | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Concrete | 2 | 44 | `QID47` | RECODE |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 4 | 2 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | More than 6 months | 2 | 56 | `QID21` | RECODE |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | More than 6 months | 2 | 57 | `QID194` | RECODE |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 3 | 1 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes - Portable (Which Room(s)) | 1 | 59 | `QID19` | RECODE |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 1 | 1 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 4 | 4 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 4 | 4 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 5 | 5 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 1 | 1 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 3 | 3 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | Click to write Scale Point 1 | 1 | 36 | `QID181_8` | PLACEHOLDER |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 67 | `QID195_1` | RECODE |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 68 | `QID195_2` | RECODE |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 69 | `QID195_3` | RECODE |
| 39 | Intervention — Improve heating/cooling system(s) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 70 | `QID195_4` | RECODE |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 71 | `QID195_5` | RECODE |
| 41 | Intervention — Replace well/septic | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 72 | `QID195_6` | RECODE |
| 42 | Intervention — Connect to city water through CCUA | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 73 | `QID195_7` | RECODE |
| 43 | Intervention — Add a fence for safety | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 74 | `QID195_8` | RECODE |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Click to write Scale Point 1 | 1 | 75 | `QID195_9` | PLACEHOLDER |
| 45 | Intervention — Trim trees | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 76 | `QID195_10` | RECODE |
| 46 | Intervention — Improved drainage | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 77 | `QID195_11` | RECODE |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | 2 | 84 | `QID124_1` | RECODE |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | 2 | 85 | `QID124_2` | RECODE |
| 49 | Experience — Extreme heat in recent years | Daily | 1 | 86 | `QID124_3` | RECODE |
| 50 | Experience — Changing your kids' school due to moving | Daily | 1 | 87 | `QID124_4` | RECODE |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Weekly | 2 | 88 | `QID124_5` | RECODE |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | 2 | 89 | `QID124_6` | RECODE |
| 53 | Experience — Well drying up | Biweekly | 3 | 90 | `QID124_7` | RECODE |
| 54 | Experience — A problem with pests in your home | Weekly | 2 | 91 | `QID124_8` | RECODE |
| 55 | Experience — A problem with water leaks | Weekly | 2 | 92 | `QID124_9` | RECODE |
| 56 | Experience — A problem with loose animals | Weekly | 2 | 93 | `QID124_10` | RECODE |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | 1 | 133 | `QID211` | RECODE |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | 2 | 134 | `QID219` | RECODE |
| 59 | What is the highest level of education you have completed? | Graduate Degree | 8 | 142 | `QID178` | RECODE |
| 60 | Which best describes your employment status? | Employed- Full time | 1 | 143 | `QID176` | RECODE |

## 10. `R_5TtaBRz99nWhzm1` — 7173 Duke Street

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_5TtaBRz99nWhzm1.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | weekly | 1 | 123 | `RespIll` | RECODE |
| 2 | How often does anyone in your home have asthma symptoms? | Seasonally | 3 | 122 | `asthma` | RECODE |
| 3 | How often does anyone in your home wheeze? | Monthly | 2 | 125 | `wheeze` | RECODE |
| 4 | How often does anyone in your home experience headaches? | Rarely or Never | 5 | 120 | `Headache` | RECODE |
| 5 | How often do you feel tired or fatigued in your home? | weekly | 1 | 124 | `Tired` | RECODE |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | — | 132 | `Hospital Respiratory` | DIFFERENT |
| 7 | Evidence of mold in any area of the home? | No | — | 108 | `Mold` | DIFFERENT |
| 8 | Water leakage — Roof | none | 4 | 110 | `Leakage 2_1` | RECODE |
| 9 | Water leakage — Walls | none | 4 | 111 | `Leakage 2_2` | RECODE |
| 10 | Water leakage — Windows | none | 4 | 112 | `Leakage 2_3` | RECODE |
| 11 | Water leakage — Floor | none | 4 | 113 | `Leakage 2_4` | RECODE |
| 12 | Cooling system — Central AC | less than 10 years | 1 | 100 | `Cooling System _1` | RECODE |
| 13 | Cooling system — Window unit | nan | — | 101 | `Cooling System _2` | DIFFERENT |
| 14 | Cooling system — Fan only | 10 to 15 years | 2 | 102 | `Cooling System _3` | RECODE |
| 15 | Cooling system — No cooling | nan | — | 103 | `Cooling System _4` | DIFFERENT |
| 16 | Cooking fuel / method | electric cooktops | 7 | 106 | `Cooking` | RECODE |
| 17 | When was your house built? | Built 1960–1979 | 2 | 39 | `QID192` | RECODE |
| 18 | What type of house do you live in? | Double Wide Mobile Home | 2 | 40 | `QID128` | RECODE |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Good- Minor repairs needed. | 2 | 55 | `QID141` | RECODE |
| 20 | What is your current housing ownership status? | Owner | 1 | 24 | `Ownership` | RECODE |
| 21 | How long have you lived in High Ridge Estates? (years) | 37 | 37 | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | 4 | 44 | `QID47` | RECODE |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | 1 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Less than 6 months | 1 | 56 | `QID21` | RECODE |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | Don't know | 3 | 57 | `QID194` | RECODE |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 5 | 3 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes- Integrated into central air heating system,Click to write Choice 6,Click to write Choice 7 | 2,6,7 | 59 | `QID19` | PLACEHOLDER |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 4 | 4 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 4 | 4 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 5 | 5 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 3 | 3 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 5 | 5 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 5 | 5 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 67 | `QID195_1` | RECODE |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 68 | `QID195_2` | RECODE |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Click to write Scale Point 1 | 1 | 69 | `QID195_3` | PLACEHOLDER |
| 39 | Intervention — Improve heating/cooling system(s) | Click to write Scale Point 1 | 1 | 70 | `QID195_4` | PLACEHOLDER |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Click to write Scale Point 1 | 1 | 71 | `QID195_5` | PLACEHOLDER |
| 41 | Intervention — Replace well/septic | Click to write Scale Point 1 | 1 | 72 | `QID195_6` | PLACEHOLDER |
| 42 | Intervention — Connect to city water through CCUA | — | — | 73 | `QID195_7` | EMPTY-BOTH |
| 43 | Intervention — Add a fence for safety | Click to write Scale Point 1 | 1 | 74 | `QID195_8` | PLACEHOLDER |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Click to write Scale Point 1 | 1 | 75 | `QID195_9` | PLACEHOLDER |
| 45 | Intervention — Trim trees | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 76 | `QID195_10` | RECODE |
| 46 | Intervention — Improved drainage | Click to write Scale Point 1 | 1 | 77 | `QID195_11` | PLACEHOLDER |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | 2 | 84 | `QID124_1` | RECODE |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | 2 | 85 | `QID124_2` | RECODE |
| 49 | Experience — Extreme heat in recent years | Daily | 1 | 86 | `QID124_3` | RECODE |
| 50 | Experience — Changing your kids' school due to moving | Biweekly | 3 | 87 | `QID124_4` | RECODE |
| 51 | Experience — Calling law enforcement because of problem with neighbors | — | — | 88 | `QID124_5` | EMPTY-BOTH |
| 52 | Experience — Losing home owners insurance due to age of home | Daily | 1 | 89 | `QID124_6` | RECODE |
| 53 | Experience — Well drying up | Weekly | 2 | 90 | `QID124_7` | RECODE |
| 54 | Experience — A problem with pests in your home | Weekly | 2 | 91 | `QID124_8` | RECODE |
| 55 | Experience — A problem with water leaks | Weekly | 2 | 92 | `QID124_9` | RECODE |
| 56 | Experience — A problem with loose animals | Weekly | 2 | 93 | `QID124_10` | RECODE |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | 1 | 133 | `QID211` | RECODE |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | Name the problem | 4 | 134 | `QID219` | RECODE |
| 59 | What is the highest level of education you have completed? | High school diploma or equivalent | 5 | 142 | `QID178` | RECODE |
| 60 | Which best describes your employment status? | Retired | 4 | 143 | `QID176` | RECODE |

## 11. `R_5tJl6j6gNRyLVMe` — 6220 Colgate Rd

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_5tJl6j6gNRyLVMe.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | 5 | 123 | `RespIll` | RECODE |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | 5 | 122 | `asthma` | RECODE |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | 5 | 125 | `wheeze` | RECODE |
| 4 | How often does anyone in your home experience headaches? | Rarely or Never | 5 | 120 | `Headache` | RECODE |
| 5 | How often do you feel tired or fatigued in your home? | Rarely or Never | 5 | 124 | `Tired` | RECODE |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | 4 | 132 | `Hospital Respiratory` | RECODE |
| 7 | Evidence of mold in any area of the home? | Yes | 10 | 108 | `Mold` | RECODE |
| 8 | Water leakage — Roof | none | 4 | 110 | `Leakage 2_1` | RECODE |
| 9 | Water leakage — Walls | none | 4 | 111 | `Leakage 2_2` | RECODE |
| 10 | Water leakage — Windows | none | 4 | 112 | `Leakage 2_3` | RECODE |
| 11 | Water leakage — Floor | less than one week | 1 | 113 | `Leakage 2_4` | RECODE |
| 12 | Cooling system — Central AC | nan | — | 100 | `Cooling System _1` | DIFFERENT |
| 13 | Cooling system — Window unit | less than 10 years | 1 | 101 | `Cooling System _2` | RECODE |
| 14 | Cooling system — Fan only | Don't know/Not applicable | 4 | 102 | `Cooling System _3` | RECODE |
| 15 | Cooling system — No cooling | nan | — | 103 | `Cooling System _4` | DIFFERENT |
| 16 | Cooking fuel / method | electric cooktops | 7 | 106 | `Cooking` | RECODE |
| 17 | When was your house built? | Built 1980–1999 | 3 | 39 | `QID192` | RECODE |
| 18 | What type of house do you live in? | Double Wide Mobile Home | 2 | 40 | `QID128` | RECODE |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Good- Minor repairs needed. | 2 | 55 | `QID141` | RECODE |
| 20 | What is your current housing ownership status? | Other | 4 | 24 | `Ownership` | RECODE |
| 21 | How long have you lived in High Ridge Estates? (years) | 6 mo | 6 mo | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | 4 | 44 | `QID47` | RECODE |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 4 | 2 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Less than 6 months | 1 | 56 | `QID21` | RECODE |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | More than 6 months | 2 | 57 | `QID194` | RECODE |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 3 | 1 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes- Integrated into central air heating system,No | 2,3 | 59 | `QID19` | DIFFERENT |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 3 | 3 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 1 | 1 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 3 | 3 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 3 | 3 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 1 | 1 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 4 | 4 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Click to write Scale Point 1 | 1 | 67 | `QID195_1` | PLACEHOLDER |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Click to write Scale Point 1 | 1 | 68 | `QID195_2` | PLACEHOLDER |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Click to write Scale Point 1 | 1 | 69 | `QID195_3` | PLACEHOLDER |
| 39 | Intervention — Improve heating/cooling system(s) | Click to write Scale Point 1 | 1 | 70 | `QID195_4` | PLACEHOLDER |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Click to write Scale Point 1 | 1 | 71 | `QID195_5` | PLACEHOLDER |
| 41 | Intervention — Replace well/septic | Click to write Scale Point 1 | 1 | 72 | `QID195_6` | PLACEHOLDER |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Click to write Scale Point 1 | 1 | 74 | `QID195_8` | PLACEHOLDER |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Nature reserves and preserves | 7 | 75 | `QID195_9` | RECODE |
| 45 | Intervention — Trim trees | Nature reserves and preserves | 7 | 76 | `QID195_10` | RECODE |
| 46 | Intervention — Improved drainage | Click to write Scale Point 1 | 1 | 77 | `QID195_11` | PLACEHOLDER |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | 2 | 84 | `QID124_1` | RECODE |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | 2 | 85 | `QID124_2` | RECODE |
| 49 | Experience — Extreme heat in recent years | Daily | 1 | 86 | `QID124_3` | RECODE |
| 50 | Experience — Changing your kids' school due to moving | Weekly | 2 | 87 | `QID124_4` | RECODE |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Weekly | 2 | 88 | `QID124_5` | RECODE |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | 2 | 89 | `QID124_6` | RECODE |
| 53 | Experience — Well drying up | Weekly | 2 | 90 | `QID124_7` | RECODE |
| 54 | Experience — A problem with pests in your home | Weekly | 2 | 91 | `QID124_8` | RECODE |
| 55 | Experience — A problem with water leaks | Weekly | 2 | 92 | `QID124_9` | RECODE |
| 56 | Experience — A problem with loose animals | Daily | 1 | 93 | `QID124_10` | RECODE |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | 1 | 133 | `QID211` | RECODE |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | 2 | 134 | `QID219` | RECODE |
| 59 | What is the highest level of education you have completed? | High school diploma or equivalent | 5 | 142 | `QID178` | RECODE |
| 60 | Which best describes your employment status? | Employed - Part time | 2 | 143 | `QID176` | RECODE |

## 12. `R_6SGNzs6svx7pBbb` — Dennison

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_6SGNzs6svx7pBbb.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | 5 | 123 | `RespIll` | RECODE |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | 5 | 122 | `asthma` | RECODE |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | 5 | 125 | `wheeze` | RECODE |
| 4 | How often does anyone in your home experience headaches? | Monthly | 2 | 120 | `Headache` | RECODE |
| 5 | How often do you feel tired or fatigued in your home? | Rarely or Never | 5 | 124 | `Tired` | RECODE |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | 4 | 132 | `Hospital Respiratory` | RECODE |
| 7 | Evidence of mold in any area of the home? | Yes | 10 | 108 | `Mold` | RECODE |
| 8 | Water leakage — Roof | none | 4 | 110 | `Leakage 2_1` | RECODE |
| 9 | Water leakage — Walls | none | 4 | 111 | `Leakage 2_2` | RECODE |
| 10 | Water leakage — Windows | not fixed | 3 | 112 | `Leakage 2_3` | RECODE |
| 11 | Water leakage — Floor | not fixed | 3 | 113 | `Leakage 2_4` | RECODE |
| 12 | Cooling system — Central AC | More than 15 years | 3 | 100 | `Cooling System _1` | RECODE |
| 13 | Cooling system — Window unit | less than 10 years | 1 | 101 | `Cooling System _2` | RECODE |
| 14 | Cooling system — Fan only | less than 10 years | 1 | 102 | `Cooling System _3` | RECODE |
| 15 | Cooling system — No cooling | nan | — | 103 | `Cooling System _4` | DIFFERENT |
| 16 | Cooking fuel / method | electric cooktops | 7 | 106 | `Cooking` | RECODE |
| 17 | When was your house built? | Built 1960–1979 | 2 | 39 | `QID192` | RECODE |
| 18 | What type of house do you live in? | Double Wide Mobile Home | 2 | 40 | `QID128` | RECODE |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Poor- Major repairs needed. | 4 | 55 | `QID141` | RECODE |
| 20 | What is your current housing ownership status? | Owner | 1 | 24 | `Ownership` | RECODE |
| 21 | How long have you lived in High Ridge Estates? (years) | 17 years | 17 years | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | 4 | 44 | `QID47` | RECODE |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | 1 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | More than 6 months | 2 | 56 | `QID21` | RECODE |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | More than 6 months | 2 | 57 | `QID194` | RECODE |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | — | — | 58 | `QID17` | EMPTY-BOTH |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes- Integrated into central air heating system,No,Click to write Choice 6 | 2,3,6 | 59 | `QID19` | PLACEHOLDER |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 4 | 4 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 3 | 3 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 3 | 3 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 3 | 3 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 3 | 3 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 3 | 3 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 67 | `QID195_1` | RECODE |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 68 | `QID195_2` | RECODE |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Nature reserves and preserves | 7 | 69 | `QID195_3` | RECODE |
| 39 | Intervention — Improve heating/cooling system(s) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 70 | `QID195_4` | RECODE |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 71 | `QID195_5` | RECODE |
| 41 | Intervention — Replace well/septic | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 72 | `QID195_6` | RECODE |
| 42 | Intervention — Connect to city water through CCUA | Nature reserves and preserves | 7 | 73 | `QID195_7` | RECODE |
| 43 | Intervention — Add a fence for safety | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 74 | `QID195_8` | RECODE |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 75 | `QID195_9` | RECODE |
| 45 | Intervention — Trim trees | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 76 | `QID195_10` | RECODE |
| 46 | Intervention — Improved drainage | Nature reserves and preserves | 7 | 77 | `QID195_11` | RECODE |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | 2 | 84 | `QID124_1` | RECODE |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | 2 | 85 | `QID124_2` | RECODE |
| 49 | Experience — Extreme heat in recent years | Daily | 1 | 86 | `QID124_3` | RECODE |
| 50 | Experience — Changing your kids' school due to moving | Weekly | 2 | 87 | `QID124_4` | RECODE |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Weekly | 2 | 88 | `QID124_5` | RECODE |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | 2 | 89 | `QID124_6` | RECODE |
| 53 | Experience — Well drying up | Daily | 1 | 90 | `QID124_7` | RECODE |
| 54 | Experience — A problem with pests in your home | Daily | 1 | 91 | `QID124_8` | RECODE |
| 55 | Experience — A problem with water leaks | Weekly | 2 | 92 | `QID124_9` | RECODE |
| 56 | Experience — A problem with loose animals | Weekly | 2 | 93 | `QID124_10` | RECODE |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | 1 | 133 | `QID211` | RECODE |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | 2 | 134 | `QID219` | RECODE |
| 59 | What is the highest level of education you have completed? | High school diploma or equivalent | 5 | 142 | `QID178` | RECODE |
| 60 | Which best describes your employment status? | Retired | 4 | 143 | `QID176` | RECODE |

## 13. `R_6s0PVusMDUucFQY` — Dennison

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_6s0PVusMDUucFQY.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Seasonally | 3 | 123 | `RespIll` | RECODE |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | 5 | 122 | `asthma` | RECODE |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | 5 | 125 | `wheeze` | RECODE |
| 4 | How often does anyone in your home experience headaches? | Monthly | 2 | 120 | `Headache` | RECODE |
| 5 | How often do you feel tired or fatigued in your home? | Rarely or Never | 5 | 124 | `Tired` | RECODE |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | yes | 1 | 132 | `Hospital Respiratory` | RECODE |
| 7 | Evidence of mold in any area of the home? | No | — | 108 | `Mold` | DIFFERENT |
| 8 | Water leakage — Roof | less than one week | 1 | 110 | `Leakage 2_1` | RECODE |
| 9 | Water leakage — Walls | none | 4 | 111 | `Leakage 2_2` | RECODE |
| 10 | Water leakage — Windows | less than one week | 1 | 112 | `Leakage 2_3` | RECODE |
| 11 | Water leakage — Floor | less than one week | 1 | 113 | `Leakage 2_4` | RECODE |
| 12 | Cooling system — Central AC | Don't know/Not applicable | 4 | 100 | `Cooling System _1` | RECODE |
| 13 | Cooling system — Window unit | less than 10 years | 1 | 101 | `Cooling System _2` | RECODE |
| 14 | Cooling system — Fan only | Don't know/Not applicable | 4 | 102 | `Cooling System _3` | RECODE |
| 15 | Cooling system — No cooling | nan | — | 103 | `Cooling System _4` | DIFFERENT |
| 16 | Cooking fuel / method | Other: | 9 | 106 | `Cooking` | RECODE |
| 17 | When was your house built? | Click to write Choice 5 | 5 | 39 | `QID192` | PLACEHOLDER |
| 18 | What type of house do you live in? | Single Wide Mobile Home | 1 | 40 | `QID128` | RECODE |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Poor- Major repairs needed. | 4 | 55 | `QID141` | RECODE |
| 20 | What is your current housing ownership status? | Renter | 2 | 24 | `Ownership` | RECODE |
| 21 | How long have you lived in High Ridge Estates? (years) | 5 years | 5 years | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Don't know | 5 | 44 | `QID47` | RECODE |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | 1 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | More than 6 months | 2 | 56 | `QID21` | RECODE |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | Don't know | 3 | 57 | `QID194` | RECODE |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 3 | 1 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes - Portable (Which Room(s)),Yes- Integrated into central air heating system,Don’t Know | 1,2,4 | 59 | `QID19` | DIFFERENT |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 4 | 4 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 4 | 4 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 4 | 4 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 3 | 3 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 3 | 3 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 3 | 3 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | Click to write Scale Point 1 | 1 | 36 | `QID181_8` | PLACEHOLDER |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Nature reserves and preserves | 7 | 67 | `QID195_1` | RECODE |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Nature reserves and preserves | 7 | 68 | `QID195_2` | RECODE |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Nature reserves and preserves | 7 | 69 | `QID195_3` | RECODE |
| 39 | Intervention — Improve heating/cooling system(s) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 70 | `QID195_4` | RECODE |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 71 | `QID195_5` | RECODE |
| 41 | Intervention — Replace well/septic | Nature reserves and preserves | 7 | 72 | `QID195_6` | RECODE |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 74 | `QID195_8` | RECODE |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 75 | `QID195_9` | RECODE |
| 45 | Intervention — Trim trees | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 76 | `QID195_10` | RECODE |
| 46 | Intervention — Improved drainage | Nature reserves and preserves | 7 | 77 | `QID195_11` | RECODE |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | 2 | 84 | `QID124_1` | RECODE |
| 48 | Experience — In case of flooding, received help for cleaning | — | — | 85 | `QID124_2` | EMPTY-BOTH |
| 49 | Experience — Extreme heat in recent years | Daily | 1 | 86 | `QID124_3` | RECODE |
| 50 | Experience — Changing your kids' school due to moving | Weekly | 2 | 87 | `QID124_4` | RECODE |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Daily | 1 | 88 | `QID124_5` | RECODE |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | 2 | 89 | `QID124_6` | RECODE |
| 53 | Experience — Well drying up | Weekly | 2 | 90 | `QID124_7` | RECODE |
| 54 | Experience — A problem with pests in your home | Biweekly | 3 | 91 | `QID124_8` | RECODE |
| 55 | Experience — A problem with water leaks | Daily | 1 | 92 | `QID124_9` | RECODE |
| 56 | Experience — A problem with loose animals | Daily | 1 | 93 | `QID124_10` | RECODE |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | 1 | 133 | `QID211` | RECODE |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | 2 | 134 | `QID219` | RECODE |
| 59 | What is the highest level of education you have completed? | High school diploma or equivalent | 5 | 142 | `QID178` | RECODE |
| 60 | Which best describes your employment status? | Employed - Part time | 2 | 143 | `QID176` | RECODE |

## 14. `R_6xzTr24XxYm8KC4` — 7276 Temple

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_6xzTr24XxYm8KC4.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | 5 | 123 | `RespIll` | RECODE |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | 5 | 122 | `asthma` | RECODE |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | 5 | 125 | `wheeze` | RECODE |
| 4 | How often does anyone in your home experience headaches? | weekly | 1 | 120 | `Headache` | RECODE |
| 5 | How often do you feel tired or fatigued in your home? | weekly | 1 | 124 | `Tired` | RECODE |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | 4 | 132 | `Hospital Respiratory` | RECODE |
| 7 | Evidence of mold in any area of the home? | Yes | 7,10 | 108 | `Mold` | DIFFERENT |
| 8 | Water leakage — Roof | none | 4 | 110 | `Leakage 2_1` | RECODE |
| 9 | Water leakage — Walls | none | 4 | 111 | `Leakage 2_2` | RECODE |
| 10 | Water leakage — Windows | none | 4 | 112 | `Leakage 2_3` | RECODE |
| 11 | Water leakage — Floor | not fixed | 3 | 113 | `Leakage 2_4` | RECODE |
| 12 | Cooling system — Central AC | More than 15 years | 3 | 100 | `Cooling System _1` | RECODE |
| 13 | Cooling system — Window unit | More than 15 years | 3 | 101 | `Cooling System _2` | RECODE |
| 14 | Cooling system — Fan only | More than 15 years | 3 | 102 | `Cooling System _3` | RECODE |
| 15 | Cooling system — No cooling | Don't know/Not applicable | 4 | 103 | `Cooling System _4` | RECODE |
| 16 | Cooking fuel / method | gas cooktops,Other: | 1,9 | 106 | `Cooking` | DIFFERENT |
| 17 | When was your house built? | Built 2000 or later | 4 | 39 | `QID192` | RECODE |
| 18 | What type of house do you live in? | Single Wide Mobile Home | 1 | 40 | `QID128` | RECODE |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Poor- Major repairs needed. | 4 | 55 | `QID141` | RECODE |
| 20 | What is your current housing ownership status? | Owner | 1 | 24 | `Ownership` | RECODE |
| 21 | How long have you lived in High Ridge Estates? (years) | 1 | 1 | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Don't know | 5 | 44 | `QID47` | RECODE |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 4 | 2 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Don't know | 3 | 56 | `QID21` | RECODE |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | Click to write Choice 5 | 5 | 57 | `QID194` | PLACEHOLDER |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 3 | 1 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Don’t Know,Click to write Choice 6 | 4,6 | 59 | `QID19` | PLACEHOLDER |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 1 | 1 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 5 | 5 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 1 | 1 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 1 | 1 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 1 | 1 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 5 | 5 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | Click to write Scale Point 5 | 5 | 36 | `QID181_8` | PLACEHOLDER |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Nature reserves and preserves | 7 | 67 | `QID195_1` | RECODE |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 68 | `QID195_2` | RECODE |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Click to write Scale Point 1 | 1 | 69 | `QID195_3` | PLACEHOLDER |
| 39 | Intervention — Improve heating/cooling system(s) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 70 | `QID195_4` | RECODE |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 71 | `QID195_5` | RECODE |
| 41 | Intervention — Replace well/septic | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 72 | `QID195_6` | RECODE |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Nature reserves and preserves | 7 | 74 | `QID195_8` | RECODE |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Click to write Scale Point 1 | 1 | 75 | `QID195_9` | PLACEHOLDER |
| 45 | Intervention — Trim trees | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 76 | `QID195_10` | RECODE |
| 46 | Intervention — Improved drainage | Nature reserves and preserves | 7 | 77 | `QID195_11` | RECODE |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | 2 | 84 | `QID124_1` | RECODE |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | 2 | 85 | `QID124_2` | RECODE |
| 49 | Experience — Extreme heat in recent years | Daily | 1 | 86 | `QID124_3` | RECODE |
| 50 | Experience — Changing your kids' school due to moving | Daily | 1 | 87 | `QID124_4` | RECODE |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Daily | 1 | 88 | `QID124_5` | RECODE |
| 52 | Experience — Losing home owners insurance due to age of home | Daily | 1 | 89 | `QID124_6` | RECODE |
| 53 | Experience — Well drying up | Weekly | 2 | 90 | `QID124_7` | RECODE |
| 54 | Experience — A problem with pests in your home | Weekly | 2 | 91 | `QID124_8` | RECODE |
| 55 | Experience — A problem with water leaks | Weekly | 2 | 92 | `QID124_9` | RECODE |
| 56 | Experience — A problem with loose animals | Daily | 1 | 93 | `QID124_10` | RECODE |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | 1 | 133 | `QID211` | RECODE |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | 2 | 134 | `QID219` | RECODE |
| 59 | What is the highest level of education you have completed? | Some college, no degree | 6 | 142 | `QID178` | RECODE |
| 60 | Which best describes your employment status? | Employed- Full time | 1 | 143 | `QID176` | RECODE |

## 15. `R_71LqP7xFx71BPsl` — Baylor Ave

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_71LqP7xFx71BPsl.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | 5 | 123 | `RespIll` | RECODE |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | 5 | 122 | `asthma` | RECODE |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | 5 | 125 | `wheeze` | RECODE |
| 4 | How often does anyone in your home experience headaches? | Rarely or Never | 5 | 120 | `Headache` | RECODE |
| 5 | How often do you feel tired or fatigued in your home? | Rarely or Never | 5 | 124 | `Tired` | RECODE |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | 4 | 132 | `Hospital Respiratory` | RECODE |
| 7 | Evidence of mold in any area of the home? | Yes | 7,8 | 108 | `Mold` | DIFFERENT |
| 8 | Water leakage — Roof | more than one week | 2 | 110 | `Leakage 2_1` | RECODE |
| 9 | Water leakage — Walls | none | 4 | 111 | `Leakage 2_2` | RECODE |
| 10 | Water leakage — Windows | less than one week | 1 | 112 | `Leakage 2_3` | RECODE |
| 11 | Water leakage — Floor | none | 4 | 113 | `Leakage 2_4` | RECODE |
| 12 | Cooling system — Central AC | nan | — | 100 | `Cooling System _1` | DIFFERENT |
| 13 | Cooling system — Window unit | less than 10 years | 1 | 101 | `Cooling System _2` | RECODE |
| 14 | Cooling system — Fan only | nan | — | 102 | `Cooling System _3` | DIFFERENT |
| 15 | Cooling system — No cooling | nan | — | 103 | `Cooling System _4` | DIFFERENT |
| 16 | Cooking fuel / method | Other: | 9 | 106 | `Cooking` | RECODE |
| 17 | When was your house built? | Built 2000 or later | 4 | 39 | `QID192` | RECODE |
| 18 | What type of house do you live in? | Double Wide Mobile Home | 2 | 40 | `QID128` | RECODE |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Fair- Some repairs needed. | 3 | 55 | `QID141` | RECODE |
| 20 | What is your current housing ownership status? | Owner | 1 | 24 | `Ownership` | RECODE |
| 21 | How long have you lived in High Ridge Estates? (years) | 1 | 1 | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | 4 | 44 | `QID47` | RECODE |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 4 | 2 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | More than 6 months | 2 | 56 | `QID21` | RECODE |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | Don't know | 3 | 57 | `QID194` | RECODE |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 4 | 2 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes - Portable (Which Room(s)),Yes- Integrated into central air heating system,Don’t Know | 1,2,4 | 59 | `QID19` | DIFFERENT |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 3 | 3 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 2 | 2 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 3 | 3 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 4 | 4 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 3 | 3 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 3 | 3 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 4 | 4 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | Click to write Scale Point 1 | 1 | 36 | `QID181_8` | PLACEHOLDER |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 67 | `QID195_1` | RECODE |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 68 | `QID195_2` | RECODE |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 69 | `QID195_3` | RECODE |
| 39 | Intervention — Improve heating/cooling system(s) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 70 | `QID195_4` | RECODE |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 71 | `QID195_5` | RECODE |
| 41 | Intervention — Replace well/septic | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 72 | `QID195_6` | RECODE |
| 42 | Intervention — Connect to city water through CCUA | Nature reserves and preserves | 7 | 73 | `QID195_7` | RECODE |
| 43 | Intervention — Add a fence for safety | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 74 | `QID195_8` | RECODE |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 75 | `QID195_9` | RECODE |
| 45 | Intervention — Trim trees | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 76 | `QID195_10` | RECODE |
| 46 | Intervention — Improved drainage | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 77 | `QID195_11` | RECODE |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | 2 | 84 | `QID124_1` | RECODE |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | 2 | 85 | `QID124_2` | RECODE |
| 49 | Experience — Extreme heat in recent years | Weekly | 2 | 86 | `QID124_3` | RECODE |
| 50 | Experience — Changing your kids' school due to moving | Weekly | 2 | 87 | `QID124_4` | RECODE |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Weekly | 2 | 88 | `QID124_5` | RECODE |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | 2 | 89 | `QID124_6` | RECODE |
| 53 | Experience — Well drying up | Weekly | 2 | 90 | `QID124_7` | RECODE |
| 54 | Experience — A problem with pests in your home | Daily | 1 | 91 | `QID124_8` | RECODE |
| 55 | Experience — A problem with water leaks | Daily | 1 | 92 | `QID124_9` | RECODE |
| 56 | Experience — A problem with loose animals | Daily | 1 | 93 | `QID124_10` | RECODE |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | 1 | 133 | `QID211` | RECODE |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | 2 | 134 | `QID219` | RECODE |
| 59 | What is the highest level of education you have completed? | High school diploma or equivalent | 5 | 142 | `QID178` | RECODE |
| 60 | Which best describes your employment status? | Unemployed | 3 | 143 | `QID176` | RECODE |

## 16. `R_78TZ7UtnmZU0jKm` — 7201 Notre Dame St

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_78TZ7UtnmZU0jKm.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | 5 | 123 | `RespIll` | RECODE |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | 5 | 122 | `asthma` | RECODE |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | 5 | 125 | `wheeze` | RECODE |
| 4 | How often does anyone in your home experience headaches? | Rarely or Never | 5 | 120 | `Headache` | RECODE |
| 5 | How often do you feel tired or fatigued in your home? | Rarely or Never | 5 | 124 | `Tired` | RECODE |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | 4 | 132 | `Hospital Respiratory` | RECODE |
| 7 | Evidence of mold in any area of the home? | Yes | 10 | 108 | `Mold` | RECODE |
| 8 | Water leakage — Roof | more than one week | 2 | 110 | `Leakage 2_1` | RECODE |
| 9 | Water leakage — Walls | none | 4 | 111 | `Leakage 2_2` | RECODE |
| 10 | Water leakage — Windows | none | 4 | 112 | `Leakage 2_3` | RECODE |
| 11 | Water leakage — Floor | more than one week | 2 | 113 | `Leakage 2_4` | RECODE |
| 12 | Cooling system — Central AC | less than 10 years | 1 | 100 | `Cooling System _1` | RECODE |
| 13 | Cooling system — Window unit | less than 10 years | 1 | 101 | `Cooling System _2` | RECODE |
| 14 | Cooling system — Fan only | Don't know/Not applicable | 4 | 102 | `Cooling System _3` | RECODE |
| 15 | Cooling system — No cooling | Don't know/Not applicable | 4 | 103 | `Cooling System _4` | RECODE |
| 16 | Cooking fuel / method | electric cooktops | 7 | 106 | `Cooking` | RECODE |
| 17 | When was your house built? | Built 1960–1979 | 2 | 39 | `QID192` | RECODE |
| 18 | What type of house do you live in? | Double Wide Mobile Home | 2 | 40 | `QID128` | RECODE |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Fair- Some repairs needed. | 3 | 55 | `QID141` | RECODE |
| 20 | What is your current housing ownership status? | Owner | 1 | 24 | `Ownership` | RECODE |
| 21 | How long have you lived in High Ridge Estates? (years) | 5 years | 5 years | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Concrete | 2 | 44 | `QID47` | RECODE |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | 1 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Less than 6 months | 1 | 56 | `QID21` | RECODE |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | Less than 6 months | 1 | 57 | `QID194` | RECODE |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 3 | 1 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes- Integrated into central air heating system | 2 | 59 | `QID19` | RECODE |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 1 | 1 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 1 | 1 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 5 | 5 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 1 | 1 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 4 | 4 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 4 | 4 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 67 | `QID195_1` | RECODE |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 68 | `QID195_2` | RECODE |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Click to write Scale Point 1 | 1 | 69 | `QID195_3` | PLACEHOLDER |
| 39 | Intervention — Improve heating/cooling system(s) | Click to write Scale Point 1 | 1 | 70 | `QID195_4` | PLACEHOLDER |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Click to write Scale Point 1 | 1 | 71 | `QID195_5` | PLACEHOLDER |
| 41 | Intervention — Replace well/septic | Click to write Scale Point 1 | 1 | 72 | `QID195_6` | PLACEHOLDER |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Click to write Scale Point 1 | 1 | 74 | `QID195_8` | PLACEHOLDER |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Click to write Scale Point 1 | 1 | 75 | `QID195_9` | PLACEHOLDER |
| 45 | Intervention — Trim trees | Click to write Scale Point 1 | 1 | 76 | `QID195_10` | PLACEHOLDER |
| 46 | Intervention — Improved drainage | Click to write Scale Point 1 | 1 | 77 | `QID195_11` | PLACEHOLDER |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | 2 | 84 | `QID124_1` | RECODE |
| 48 | Experience — In case of flooding, received help for cleaning | Biweekly | 3 | 85 | `QID124_2` | RECODE |
| 49 | Experience — Extreme heat in recent years | Weekly | 2 | 86 | `QID124_3` | RECODE |
| 50 | Experience — Changing your kids' school due to moving | Weekly | 2 | 87 | `QID124_4` | RECODE |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Weekly | 2 | 88 | `QID124_5` | RECODE |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | 2 | 89 | `QID124_6` | RECODE |
| 53 | Experience — Well drying up | Weekly | 2 | 90 | `QID124_7` | RECODE |
| 54 | Experience — A problem with pests in your home | Daily | 1 | 91 | `QID124_8` | RECODE |
| 55 | Experience — A problem with water leaks | Weekly | 2 | 92 | `QID124_9` | RECODE |
| 56 | Experience — A problem with loose animals | Daily | 1 | 93 | `QID124_10` | RECODE |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | 1 | 133 | `QID211` | RECODE |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | 2 | 134 | `QID219` | RECODE |
| 59 | What is the highest level of education you have completed? | High school diploma or equivalent | 5 | 142 | `QID178` | RECODE |
| 60 | Which best describes your employment status? | Retired | 4 | 143 | `QID176` | RECODE |

## 17. `R_87qCLdadYRHhw4P` — 6200 Harvard Avenue

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_87qCLdadYRHhw4P.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Yearly | 4 | 123 | `RespIll` | RECODE |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | 5 | 122 | `asthma` | RECODE |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | 5 | 125 | `wheeze` | RECODE |
| 4 | How often does anyone in your home experience headaches? | weekly | 1 | 120 | `Headache` | RECODE |
| 5 | How often do you feel tired or fatigued in your home? | Rarely or Never | 5 | 124 | `Tired` | RECODE |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | yes | 3 | 132 | `Hospital Respiratory` | RECODE |
| 7 | Evidence of mold in any area of the home? | Yes | 10 | 108 | `Mold` | RECODE |
| 8 | Water leakage — Roof | none | 4 | 110 | `Leakage 2_1` | RECODE |
| 9 | Water leakage — Walls | more than one week | 2 | 111 | `Leakage 2_2` | RECODE |
| 10 | Water leakage — Windows | none | 4 | 112 | `Leakage 2_3` | RECODE |
| 11 | Water leakage — Floor | none | 4 | 113 | `Leakage 2_4` | RECODE |
| 12 | Cooling system — Central AC | less than 10 years | 1 | 100 | `Cooling System _1` | RECODE |
| 13 | Cooling system — Window unit | Don't know/Not applicable | 4 | 101 | `Cooling System _2` | RECODE |
| 14 | Cooling system — Fan only | less than 10 years | 1 | 102 | `Cooling System _3` | RECODE |
| 15 | Cooling system — No cooling | Don't know/Not applicable | 4 | 103 | `Cooling System _4` | RECODE |
| 16 | Cooking fuel / method | electric cooktops | 7 | 106 | `Cooking` | RECODE |
| 17 | When was your house built? | Click to write Choice 5 | 5 | 39 | `QID192` | PLACEHOLDER |
| 18 | What type of house do you live in? | House built on site | 3 | 40 | `QID128` | RECODE |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Good- Minor repairs needed. | 2 | 55 | `QID141` | RECODE |
| 20 | What is your current housing ownership status? | Renter | 2 | 24 | `Ownership` | RECODE |
| 21 | How long have you lived in High Ridge Estates? (years) | 4 years | 4 years | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | 4 | 44 | `QID47` | RECODE |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 4 | 2 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Don't know | 3 | 56 | `QID21` | RECODE |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | More than 6 months | 2 | 57 | `QID194` | RECODE |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 3 | 1 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Click to write Choice 7 | 7 | 59 | `QID19` | PLACEHOLDER |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 1 | 1 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 1 | 1 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 3 | 3 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 1 | 1 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 1 | 1 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 3 | 3 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Click to write Scale Point 1 | 1 | 67 | `QID195_1` | PLACEHOLDER |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Click to write Scale Point 1 | 1 | 68 | `QID195_2` | PLACEHOLDER |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Nature reserves and preserves | 7 | 69 | `QID195_3` | RECODE |
| 39 | Intervention — Improve heating/cooling system(s) | Click to write Scale Point 1 | 1 | 70 | `QID195_4` | PLACEHOLDER |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Click to write Scale Point 1 | 1 | 71 | `QID195_5` | PLACEHOLDER |
| 41 | Intervention — Replace well/septic | Click to write Scale Point 1 | 1 | 72 | `QID195_6` | PLACEHOLDER |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 74 | `QID195_8` | RECODE |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Click to write Scale Point 1 | 1 | 75 | `QID195_9` | PLACEHOLDER |
| 45 | Intervention — Trim trees | Click to write Scale Point 1 | 1 | 76 | `QID195_10` | PLACEHOLDER |
| 46 | Intervention — Improved drainage | Click to write Scale Point 1 | 1 | 77 | `QID195_11` | PLACEHOLDER |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | 2 | 84 | `QID124_1` | RECODE |
| 48 | Experience — In case of flooding, received help for cleaning | Biweekly | 3 | 85 | `QID124_2` | RECODE |
| 49 | Experience — Extreme heat in recent years | Daily | 1 | 86 | `QID124_3` | RECODE |
| 50 | Experience — Changing your kids' school due to moving | Biweekly | 3 | 87 | `QID124_4` | RECODE |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Daily | 1 | 88 | `QID124_5` | RECODE |
| 52 | Experience — Losing home owners insurance due to age of home | Biweekly | 3 | 89 | `QID124_6` | RECODE |
| 53 | Experience — Well drying up | Weekly | 2 | 90 | `QID124_7` | RECODE |
| 54 | Experience — A problem with pests in your home | Daily | 1 | 91 | `QID124_8` | RECODE |
| 55 | Experience — A problem with water leaks | Weekly | 2 | 92 | `QID124_9` | RECODE |
| 56 | Experience — A problem with loose animals | Daily | 1 | 93 | `QID124_10` | RECODE |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | 1 | 133 | `QID211` | RECODE |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | 2 | 134 | `QID219` | RECODE |
| 59 | What is the highest level of education you have completed? | Bachelor's Degree | 7 | 142 | `QID178` | RECODE |
| 60 | Which best describes your employment status? | Employed- Full time | 1 | 143 | `QID176` | RECODE |

## 18. `R_8iSqFy8YDl9Xt1b` — 6397 Cascade Drive

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_8iSqFy8YDl9Xt1b.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | 5 | 123 | `RespIll` | RECODE |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | 5 | 122 | `asthma` | RECODE |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | 5 | 125 | `wheeze` | RECODE |
| 4 | How often does anyone in your home experience headaches? | Rarely or Never | 5 | 120 | `Headache` | RECODE |
| 5 | How often do you feel tired or fatigued in your home? | Rarely or Never | 5 | 124 | `Tired` | RECODE |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | 4 | 132 | `Hospital Respiratory` | RECODE |
| 7 | Evidence of mold in any area of the home? | Yes | 10 | 108 | `Mold` | RECODE |
| 8 | Water leakage — Roof | none | 4 | 110 | `Leakage 2_1` | RECODE |
| 9 | Water leakage — Walls | none | 4 | 111 | `Leakage 2_2` | RECODE |
| 10 | Water leakage — Windows | not fixed | 3 | 112 | `Leakage 2_3` | RECODE |
| 11 | Water leakage — Floor | none | 4 | 113 | `Leakage 2_4` | RECODE |
| 12 | Cooling system — Central AC | 10 to 15 years | 2 | 100 | `Cooling System _1` | RECODE |
| 13 | Cooling system — Window unit | nan | — | 101 | `Cooling System _2` | DIFFERENT |
| 14 | Cooling system — Fan only | nan | — | 102 | `Cooling System _3` | DIFFERENT |
| 15 | Cooling system — No cooling | nan | — | 103 | `Cooling System _4` | DIFFERENT |
| 16 | Cooking fuel / method | gas cooktops | 1 | 106 | `Cooking` | RECODE |
| 17 | When was your house built? | Built 1960–1979 | 2 | 39 | `QID192` | RECODE |
| 18 | What type of house do you live in? | Single Wide Mobile Home | 1 | 40 | `QID128` | RECODE |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Good- Minor repairs needed. | 2 | 55 | `QID141` | RECODE |
| 20 | What is your current housing ownership status? | Owner | 1 | 24 | `Ownership` | RECODE |
| 21 | How long have you lived in High Ridge Estates? (years) | 3 years | 3 years | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | 4 | 44 | `QID47` | RECODE |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | 1 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Less than 6 months | 1 | 56 | `QID21` | RECODE |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | More than 6 months | 2 | 57 | `QID194` | RECODE |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 3 | 1 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes - Portable (Which Room(s)),Yes- Integrated into central air heating system,Click to write Choice 6 | 1,2,6 | 59 | `QID19` | PLACEHOLDER |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 1 | 1 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 4 | 4 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 4 | 4 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 4 | 4 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 4 | 4 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 4 | 4 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 67 | `QID195_1` | RECODE |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 68 | `QID195_2` | RECODE |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 69 | `QID195_3` | RECODE |
| 39 | Intervention — Improve heating/cooling system(s) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 70 | `QID195_4` | RECODE |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 71 | `QID195_5` | RECODE |
| 41 | Intervention — Replace well/septic | Click to write Scale Point 1 | 1 | 72 | `QID195_6` | PLACEHOLDER |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Click to write Scale Point 1 | 1 | 74 | `QID195_8` | PLACEHOLDER |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 75 | `QID195_9` | RECODE |
| 45 | Intervention — Trim trees | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 76 | `QID195_10` | RECODE |
| 46 | Intervention — Improved drainage | Click to write Scale Point 1 | 1 | 77 | `QID195_11` | PLACEHOLDER |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | 2 | 84 | `QID124_1` | RECODE |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | 2 | 85 | `QID124_2` | RECODE |
| 49 | Experience — Extreme heat in recent years | Daily | 1 | 86 | `QID124_3` | RECODE |
| 50 | Experience — Changing your kids' school due to moving | Weekly | 2 | 87 | `QID124_4` | RECODE |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Weekly | 2 | 88 | `QID124_5` | RECODE |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | 2 | 89 | `QID124_6` | RECODE |
| 53 | Experience — Well drying up | Daily | 1 | 90 | `QID124_7` | RECODE |
| 54 | Experience — A problem with pests in your home | Daily | 1 | 91 | `QID124_8` | RECODE |
| 55 | Experience — A problem with water leaks | Daily | 1 | 92 | `QID124_9` | RECODE |
| 56 | Experience — A problem with loose animals | Daily | 1 | 93 | `QID124_10` | RECODE |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | 1 | 133 | `QID211` | RECODE |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | 2 | 134 | `QID219` | RECODE |
| 59 | What is the highest level of education you have completed? | Graduate Degree | 8 | 142 | `QID178` | RECODE |
| 60 | Which best describes your employment status? | Retired | 4 | 143 | `QID176` | RECODE |

## 19. `R_aPZYZkLLHTo3YDR` — 6392 Beloit Avenue

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_aPZYZkLLHTo3YDR.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | 5 | 123 | `RespIll` | RECODE |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | 5 | 122 | `asthma` | RECODE |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | 5 | 125 | `wheeze` | RECODE |
| 4 | How often does anyone in your home experience headaches? | Rarely or Never | 5 | 120 | `Headache` | RECODE |
| 5 | How often do you feel tired or fatigued in your home? | weekly | 1 | 124 | `Tired` | RECODE |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | 4 | 132 | `Hospital Respiratory` | RECODE |
| 7 | Evidence of mold in any area of the home? | No | — | 108 | `Mold` | DIFFERENT |
| 8 | Water leakage — Roof | none | 4 | 110 | `Leakage 2_1` | RECODE |
| 9 | Water leakage — Walls | none | 4 | 111 | `Leakage 2_2` | RECODE |
| 10 | Water leakage — Windows | none | 4 | 112 | `Leakage 2_3` | RECODE |
| 11 | Water leakage — Floor | none | 4 | 113 | `Leakage 2_4` | RECODE |
| 12 | Cooling system — Central AC | nan | — | 100 | `Cooling System _1` | DIFFERENT |
| 13 | Cooling system — Window unit | Don't know/Not applicable | 4 | 101 | `Cooling System _2` | RECODE |
| 14 | Cooling system — Fan only | Don't know/Not applicable | 4 | 102 | `Cooling System _3` | RECODE |
| 15 | Cooling system — No cooling | nan | — | 103 | `Cooling System _4` | DIFFERENT |
| 16 | Cooking fuel / method | electric cooktops | 7 | 106 | `Cooking` | RECODE |
| 17 | When was your house built? | Click to write Choice 5 | 5 | 39 | `QID192` | PLACEHOLDER |
| 18 | What type of house do you live in? | nan | — | 40 | `QID128` | DIFFERENT |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Fair- Some repairs needed. | 3 | 55 | `QID141` | RECODE |
| 20 | What is your current housing ownership status? | Renter | 2 | 24 | `Ownership` | RECODE |
| 21 | How long have you lived in High Ridge Estates? (years) | 7 y | 7 y | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Don't know | 5 | 44 | `QID47` | RECODE |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | 1 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | More than 6 months | 2 | 56 | `QID21` | RECODE |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | More than 6 months | 2 | 57 | `QID194` | RECODE |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 3 | 1 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Don’t Know,Click to write Choice 7 | 4,7 | 59 | `QID19` | PLACEHOLDER |
| 28 | Relocation factor — Employment opportunities nearby | — | — | 29 | `QID181_1` | EMPTY-BOTH |
| 29 | Relocation factor — Affordable housing | — | — | 30 | `QID181_2` | EMPTY-BOTH |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 4 | 4 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | — | — | 32 | `QID181_4` | EMPTY-BOTH |
| 32 | Relocation factor — Retirement | — | — | 33 | `QID181_5` | EMPTY-BOTH |
| 33 | Relocation factor — Environmental quality and access to nature | — | — | 34 | `QID181_6` | EMPTY-BOTH |
| 34 | Relocation factor — Inherited property | — | — | 35 | `QID181_7` | EMPTY-BOTH |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Nature reserves and preserves | 7 | 67 | `QID195_1` | RECODE |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Nature reserves and preserves | 7 | 68 | `QID195_2` | RECODE |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Nature reserves and preserves | 7 | 69 | `QID195_3` | RECODE |
| 39 | Intervention — Improve heating/cooling system(s) | Nature reserves and preserves | 7 | 70 | `QID195_4` | RECODE |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Nature reserves and preserves | 7 | 71 | `QID195_5` | RECODE |
| 41 | Intervention — Replace well/septic | Nature reserves and preserves | 7 | 72 | `QID195_6` | RECODE |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Nature reserves and preserves | 7 | 74 | `QID195_8` | RECODE |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Click to write Scale Point 1 | 1 | 75 | `QID195_9` | PLACEHOLDER |
| 45 | Intervention — Trim trees | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 76 | `QID195_10` | RECODE |
| 46 | Intervention — Improved drainage | Nature reserves and preserves | 7 | 77 | `QID195_11` | RECODE |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | 2 | 84 | `QID124_1` | RECODE |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | 2 | 85 | `QID124_2` | RECODE |
| 49 | Experience — Extreme heat in recent years | Daily | 1 | 86 | `QID124_3` | RECODE |
| 50 | Experience — Changing your kids' school due to moving | Weekly | 2 | 87 | `QID124_4` | RECODE |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Weekly | 2 | 88 | `QID124_5` | RECODE |
| 52 | Experience — Losing home owners insurance due to age of home | Biweekly | 3 | 89 | `QID124_6` | RECODE |
| 53 | Experience — Well drying up | Weekly | 2 | 90 | `QID124_7` | RECODE |
| 54 | Experience — A problem with pests in your home | Daily | 1 | 91 | `QID124_8` | RECODE |
| 55 | Experience — A problem with water leaks | Weekly | 2 | 92 | `QID124_9` | RECODE |
| 56 | Experience — A problem with loose animals | Weekly | 2 | 93 | `QID124_10` | RECODE |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | 1 | 133 | `QID211` | RECODE |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | Not Sure | 3 | 134 | `QID219` | RECODE |
| 59 | What is the highest level of education you have completed? | less than high school | 1 | 142 | `QID178` | RECODE |
| 60 | Which best describes your employment status? | Unemployed | 3 | 143 | `QID176` | RECODE |

## 20. `R_bt9KhSC0xqF2xuS` — Beloit Ave

Read from the **Survey Answers** tab · 66 rows rendered · screenshot: `../screenshots/R_bt9KhSC0xqF2xuS.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | 5 | 123 | `RespIll` | RECODE |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | 5 | 122 | `asthma` | RECODE |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | 5 | 125 | `wheeze` | RECODE |
| 4 | How often does anyone in your home experience headaches? | Rarely or Never | 5 | 120 | `Headache` | RECODE |
| 5 | How often do you feel tired or fatigued in your home? | Rarely or Never | 5 | 124 | `Tired` | RECODE |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | 4 | 132 | `Hospital Respiratory` | RECODE |
| 7 | Evidence of mold in any area of the home? | No | — | 108 | `Mold` | DIFFERENT |
| 8 | Water leakage — Roof | none | 4 | 110 | `Leakage 2_1` | RECODE |
| 9 | Water leakage — Walls | none | 4 | 111 | `Leakage 2_2` | RECODE |
| 10 | Water leakage — Windows | none | 4 | 112 | `Leakage 2_3` | RECODE |
| 11 | Water leakage — Floor | none | 4 | 113 | `Leakage 2_4` | RECODE |
| 12 | Cooling system — Central AC | nan | — | 100 | `Cooling System _1` | DIFFERENT |
| 13 | Cooling system — Window unit | Don't know/Not applicable | 4 | 101 | `Cooling System _2` | RECODE |
| 14 | Cooling system — Fan only | Don't know/Not applicable | 4 | 102 | `Cooling System _3` | RECODE |
| 15 | Cooling system — No cooling | nan | — | 103 | `Cooling System _4` | DIFFERENT |
| 16 | Cooking fuel / method | gas cooktops | 1 | 106 | `Cooking` | RECODE |
| 17 | When was your house built? | Built 1980–1999 | 3 | 39 | `QID192` | RECODE |
| 18 | What type of house do you live in? | Single Wide Mobile Home | 1 | 40 | `QID128` | RECODE |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Good- Minor repairs needed. | 2 | 55 | `QID141` | RECODE |
| 20 | What is your current housing ownership status? | Renter | 2 | 24 | `Ownership` | RECODE |
| 21 | How long have you lived in High Ridge Estates? (years) | 5 | 5 | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | 4 | 44 | `QID47` | RECODE |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | 1 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | More than 6 months | 2 | 56 | `QID21` | RECODE |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | Less than 6 months | 1 | 57 | `QID194` | RECODE |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 3 | 1 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes- Integrated into central air heating system,Click to write Choice 6 | 2,6 | 59 | `QID19` | PLACEHOLDER |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 1 | 1 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 1 | 1 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 1 | 1 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 4 | 4 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 1 | 1 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 1 | 1 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Nature reserves and preserves | 7 | 67 | `QID195_1` | RECODE |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Nature reserves and preserves | 7 | 68 | `QID195_2` | RECODE |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Nature reserves and preserves | 7 | 69 | `QID195_3` | RECODE |
| 39 | Intervention — Improve heating/cooling system(s) | Nature reserves and preserves | 7 | 70 | `QID195_4` | RECODE |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Nature reserves and preserves | 7 | 71 | `QID195_5` | RECODE |
| 41 | Intervention — Replace well/septic | Nature reserves and preserves | 7 | 72 | `QID195_6` | RECODE |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Nature reserves and preserves | 7 | 74 | `QID195_8` | RECODE |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Click to write Scale Point 1 | 1 | 75 | `QID195_9` | PLACEHOLDER |
| 45 | Intervention — Trim trees | Nature reserves and preserves | 7 | 76 | `QID195_10` | RECODE |
| 46 | Intervention — Improved drainage | Nature reserves and preserves | 7 | 77 | `QID195_11` | RECODE |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | 2 | 84 | `QID124_1` | RECODE |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | 2 | 85 | `QID124_2` | RECODE |
| 49 | Experience — Extreme heat in recent years | Daily | 1 | 86 | `QID124_3` | RECODE |
| 50 | Experience — Changing your kids' school due to moving | Weekly | 2 | 87 | `QID124_4` | RECODE |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Weekly | 2 | 88 | `QID124_5` | RECODE |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | 2 | 89 | `QID124_6` | RECODE |
| 53 | Experience — Well drying up | Weekly | 2 | 90 | `QID124_7` | RECODE |
| 54 | Experience — A problem with pests in your home | Weekly | 2 | 91 | `QID124_8` | RECODE |
| 55 | Experience — A problem with water leaks | Weekly | 2 | 92 | `QID124_9` | RECODE |
| 56 | Experience — A problem with loose animals | Weekly | 2 | 93 | `QID124_10` | RECODE |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | 1 | 133 | `QID211` | RECODE |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | Yes | 1 | 134 | `QID219` | RECODE |
| 59 | What is the highest level of education you have completed? | High school diploma or equivalent | 5 | 142 | `QID178` | RECODE |
| 60 | Which best describes your employment status? | Retired | 4 | 143 | `QID176` | RECODE |
| 61 | Orphan | true | — | — | — | NOT-IN-EXPORT |
| 62 | Parcel Address | Address not on file | — | — | — | NOT-IN-EXPORT |

## 21. `R_bxz0eWgFA4AstpB` — 7239 Purdue Street

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_bxz0eWgFA4AstpB.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | weekly | 1 | 123 | `RespIll` | RECODE |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | 5 | 122 | `asthma` | RECODE |
| 3 | How often does anyone in your home wheeze? | weekly | 1 | 125 | `wheeze` | RECODE |
| 4 | How often does anyone in your home experience headaches? | weekly | 1 | 120 | `Headache` | RECODE |
| 5 | How often do you feel tired or fatigued in your home? | Rarely or Never | 5 | 124 | `Tired` | RECODE |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | 4 | 132 | `Hospital Respiratory` | RECODE |
| 7 | Evidence of mold in any area of the home? | Yes | 10 | 108 | `Mold` | RECODE |
| 8 | Water leakage — Roof | none | 4 | 110 | `Leakage 2_1` | RECODE |
| 9 | Water leakage — Walls | none | 4 | 111 | `Leakage 2_2` | RECODE |
| 10 | Water leakage — Windows | less than one week | 1 | 112 | `Leakage 2_3` | RECODE |
| 11 | Water leakage — Floor | none | 4 | 113 | `Leakage 2_4` | RECODE |
| 12 | Cooling system — Central AC | nan | — | 100 | `Cooling System _1` | DIFFERENT |
| 13 | Cooling system — Window unit | less than 10 years | 1 | 101 | `Cooling System _2` | RECODE |
| 14 | Cooling system — Fan only | Don't know/Not applicable | 4 | 102 | `Cooling System _3` | RECODE |
| 15 | Cooling system — No cooling | Don't know/Not applicable | 4 | 103 | `Cooling System _4` | RECODE |
| 16 | Cooking fuel / method | electric cooktops | 7 | 106 | `Cooking` | RECODE |
| 17 | When was your house built? | Click to write Choice 5 | 5 | 39 | `QID192` | PLACEHOLDER |
| 18 | What type of house do you live in? | Double Wide Mobile Home | 2 | 40 | `QID128` | RECODE |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Fair- Some repairs needed. | 3 | 55 | `QID141` | RECODE |
| 20 | What is your current housing ownership status? | Owner | 1 | 24 | `Ownership` | RECODE |
| 21 | How long have you lived in High Ridge Estates? (years) | 20 years | 20 years | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | 4 | 44 | `QID47` | RECODE |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 4 | 2 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Less than 6 months | 1 | 56 | `QID21` | RECODE |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | Less than 6 months | 1 | 57 | `QID194` | RECODE |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 5 | 3 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Click to write Choice 6 | 6 | 59 | `QID19` | PLACEHOLDER |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 1 | 1 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 1 | 1 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 4 | 4 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 4 | 4 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 1 | 1 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 1 | 1 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 67 | `QID195_1` | RECODE |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 68 | `QID195_2` | RECODE |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 69 | `QID195_3` | RECODE |
| 39 | Intervention — Improve heating/cooling system(s) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 70 | `QID195_4` | RECODE |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 71 | `QID195_5` | RECODE |
| 41 | Intervention — Replace well/septic | Click to write Scale Point 1 | 1 | 72 | `QID195_6` | PLACEHOLDER |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Click to write Scale Point 1 | 1 | 74 | `QID195_8` | PLACEHOLDER |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Click to write Scale Point 1 | 1 | 75 | `QID195_9` | PLACEHOLDER |
| 45 | Intervention — Trim trees | Click to write Scale Point 1 | 1 | 76 | `QID195_10` | PLACEHOLDER |
| 46 | Intervention — Improved drainage | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 77 | `QID195_11` | RECODE |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | 2 | 84 | `QID124_1` | RECODE |
| 48 | Experience — In case of flooding, received help for cleaning | Biweekly | 3 | 85 | `QID124_2` | RECODE |
| 49 | Experience — Extreme heat in recent years | Weekly | 2 | 86 | `QID124_3` | RECODE |
| 50 | Experience — Changing your kids' school due to moving | Weekly | 2 | 87 | `QID124_4` | RECODE |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Daily | 1 | 88 | `QID124_5` | RECODE |
| 52 | Experience — Losing home owners insurance due to age of home | Biweekly | 3 | 89 | `QID124_6` | RECODE |
| 53 | Experience — Well drying up | Weekly | 2 | 90 | `QID124_7` | RECODE |
| 54 | Experience — A problem with pests in your home | Weekly | 2 | 91 | `QID124_8` | RECODE |
| 55 | Experience — A problem with water leaks | Daily | 1 | 92 | `QID124_9` | RECODE |
| 56 | Experience — A problem with loose animals | Daily | 1 | 93 | `QID124_10` | RECODE |
| 57 | Do you (or your household) own or have regular access to a car? | No | 2 | 133 | `QID211` | RECODE |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | 2 | 134 | `QID219` | RECODE |
| 59 | What is the highest level of education you have completed? | Vocational/Technical Licensing or Certification | 9 | 142 | `QID178` | RECODE |
| 60 | Which best describes your employment status? | Retired | 4 | 143 | `QID176` | RECODE |

## 22. `R_d4T4ee11cH6ntjW` — 7197 Pembroke Street

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_d4T4ee11cH6ntjW.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Monthly | 2 | 123 | `RespIll` | RECODE |
| 2 | How often does anyone in your home have asthma symptoms? | Monthly | 2 | 122 | `asthma` | RECODE |
| 3 | How often does anyone in your home wheeze? | Monthly | 2 | 125 | `wheeze` | RECODE |
| 4 | How often does anyone in your home experience headaches? | Monthly | 2 | 120 | `Headache` | RECODE |
| 5 | How often do you feel tired or fatigued in your home? | weekly | 1 | 124 | `Tired` | RECODE |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | yes | 1 | 132 | `Hospital Respiratory` | RECODE |
| 7 | Evidence of mold in any area of the home? | Yes | 10 | 108 | `Mold` | RECODE |
| 8 | Water leakage — Roof | none | 4 | 110 | `Leakage 2_1` | RECODE |
| 9 | Water leakage — Walls | none | 4 | 111 | `Leakage 2_2` | RECODE |
| 10 | Water leakage — Windows | none | 4 | 112 | `Leakage 2_3` | RECODE |
| 11 | Water leakage — Floor | none | 4 | 113 | `Leakage 2_4` | RECODE |
| 12 | Cooling system — Central AC | less than 10 years | 1 | 100 | `Cooling System _1` | RECODE |
| 13 | Cooling system — Window unit | nan | — | 101 | `Cooling System _2` | DIFFERENT |
| 14 | Cooling system — Fan only | 10 to 15 years | 2 | 102 | `Cooling System _3` | RECODE |
| 15 | Cooling system — No cooling | nan | — | 103 | `Cooling System _4` | DIFFERENT |
| 16 | Cooking fuel / method | electric cooktops | 7 | 106 | `Cooking` | RECODE |
| 17 | When was your house built? | Before 1960 | 1 | 39 | `QID192` | RECODE |
| 18 | What type of house do you live in? | Single Wide Mobile Home | 1 | 40 | `QID128` | RECODE |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Good- Minor repairs needed. | 2 | 55 | `QID141` | RECODE |
| 20 | What is your current housing ownership status? | Owner | 1 | 24 | `Ownership` | RECODE |
| 21 | How long have you lived in High Ridge Estates? (years) | 20 years | 20 years | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | 4 | 44 | `QID47` | RECODE |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | 1 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Don't know | 3 | 56 | `QID21` | RECODE |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | More than 6 months | 2 | 57 | `QID194` | RECODE |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 3 | 1 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes - Portable (Which Room(s)),Yes- Integrated into central air heating system,No | 1,2,3 | 59 | `QID19` | DIFFERENT |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 1 | 1 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 5 | 5 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 4 | 4 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 1 | 1 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 1 | 1 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 1 | 1 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 67 | `QID195_1` | RECODE |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 68 | `QID195_2` | RECODE |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 69 | `QID195_3` | RECODE |
| 39 | Intervention — Improve heating/cooling system(s) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 70 | `QID195_4` | RECODE |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 71 | `QID195_5` | RECODE |
| 41 | Intervention — Replace well/septic | Nature reserves and preserves | 7 | 72 | `QID195_6` | RECODE |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 74 | `QID195_8` | RECODE |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Nature reserves and preserves | 7 | 75 | `QID195_9` | RECODE |
| 45 | Intervention — Trim trees | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 76 | `QID195_10` | RECODE |
| 46 | Intervention — Improved drainage | Nature reserves and preserves | 7 | 77 | `QID195_11` | RECODE |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | 2 | 84 | `QID124_1` | RECODE |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | 2 | 85 | `QID124_2` | RECODE |
| 49 | Experience — Extreme heat in recent years | Daily | 1 | 86 | `QID124_3` | RECODE |
| 50 | Experience — Changing your kids' school due to moving | Weekly | 2 | 87 | `QID124_4` | RECODE |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Daily | 1 | 88 | `QID124_5` | RECODE |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | 2 | 89 | `QID124_6` | RECODE |
| 53 | Experience — Well drying up | Weekly | 2 | 90 | `QID124_7` | RECODE |
| 54 | Experience — A problem with pests in your home | Daily | 1 | 91 | `QID124_8` | RECODE |
| 55 | Experience — A problem with water leaks | Daily | 1 | 92 | `QID124_9` | RECODE |
| 56 | Experience — A problem with loose animals | Daily | 1 | 93 | `QID124_10` | RECODE |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | 1 | 133 | `QID211` | RECODE |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | Name the problem | 4 | 134 | `QID219` | RECODE |
| 59 | What is the highest level of education you have completed? | High school diploma or equivalent | 5 | 142 | `QID178` | RECODE |
| 60 | Which best describes your employment status? | Unemployed | 3 | 143 | `QID176` | RECODE |

## 23. `R_h0LfcAVvLrGULaj` — 7166 Pembroke Street

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_h0LfcAVvLrGULaj.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | 5 | 123 | `RespIll` | RECODE |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | 5 | 122 | `asthma` | RECODE |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | 5 | 125 | `wheeze` | RECODE |
| 4 | How often does anyone in your home experience headaches? | Rarely or Never | 5 | 120 | `Headache` | RECODE |
| 5 | How often do you feel tired or fatigued in your home? | Rarely or Never | 5 | 124 | `Tired` | RECODE |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | 4 | 132 | `Hospital Respiratory` | RECODE |
| 7 | Evidence of mold in any area of the home? | Yes | 10 | 108 | `Mold` | RECODE |
| 8 | Water leakage — Roof | none | 4 | 110 | `Leakage 2_1` | RECODE |
| 9 | Water leakage — Walls | none | 4 | 111 | `Leakage 2_2` | RECODE |
| 10 | Water leakage — Windows | none | 4 | 112 | `Leakage 2_3` | RECODE |
| 11 | Water leakage — Floor | none | 4 | 113 | `Leakage 2_4` | RECODE |
| 12 | Cooling system — Central AC | nan | — | 100 | `Cooling System _1` | DIFFERENT |
| 13 | Cooling system — Window unit | nan | — | 101 | `Cooling System _2` | DIFFERENT |
| 14 | Cooling system — Fan only | nan | — | 102 | `Cooling System _3` | DIFFERENT |
| 15 | Cooling system — No cooling | less than 10 years | 1 | 103 | `Cooling System _4` | RECODE |
| 16 | Cooking fuel / method | gas cooktops | 1 | 106 | `Cooking` | RECODE |
| 17 | When was your house built? | Built 1980–1999 | 3 | 39 | `QID192` | RECODE |
| 18 | What type of house do you live in? | Single Wide Mobile Home | 1 | 40 | `QID128` | RECODE |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Click to write Choice 5 | 1 | 55 | `QID141` | PLACEHOLDER |
| 20 | What is your current housing ownership status? | Owner | 1 | 24 | `Ownership` | RECODE |
| 21 | How long have you lived in High Ridge Estates? (years) | 40yrs | 40yrs | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | 4 | 44 | `QID47` | RECODE |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | 1 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Click to write Choice 4 | 4 | 56 | `QID21` | PLACEHOLDER |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | Don't know | 3 | 57 | `QID194` | RECODE |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 3 | 1 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes- Integrated into central air heating system,Click to write Choice 6 | 2,6 | 59 | `QID19` | PLACEHOLDER |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 5 | 5 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 5 | 5 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 5 | 5 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 5 | 5 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 5 | 5 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 5 | 5 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 5 | 5 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | Click to write Scale Point 5 | 5 | 36 | `QID181_8` | PLACEHOLDER |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 67 | `QID195_1` | RECODE |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 68 | `QID195_2` | RECODE |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 69 | `QID195_3` | RECODE |
| 39 | Intervention — Improve heating/cooling system(s) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 70 | `QID195_4` | RECODE |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 71 | `QID195_5` | RECODE |
| 41 | Intervention — Replace well/septic | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 72 | `QID195_6` | RECODE |
| 42 | Intervention — Connect to city water through CCUA | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 73 | `QID195_7` | RECODE |
| 43 | Intervention — Add a fence for safety | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 74 | `QID195_8` | RECODE |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 75 | `QID195_9` | RECODE |
| 45 | Intervention — Trim trees | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 76 | `QID195_10` | RECODE |
| 46 | Intervention — Improved drainage | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 77 | `QID195_11` | RECODE |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | 2 | 84 | `QID124_1` | RECODE |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | 2 | 85 | `QID124_2` | RECODE |
| 49 | Experience — Extreme heat in recent years | Daily | 1 | 86 | `QID124_3` | RECODE |
| 50 | Experience — Changing your kids' school due to moving | Weekly | 2 | 87 | `QID124_4` | RECODE |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Daily | 1 | 88 | `QID124_5` | RECODE |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | 2 | 89 | `QID124_6` | RECODE |
| 53 | Experience — Well drying up | Weekly | 2 | 90 | `QID124_7` | RECODE |
| 54 | Experience — A problem with pests in your home | Weekly | 2 | 91 | `QID124_8` | RECODE |
| 55 | Experience — A problem with water leaks | Weekly | 2 | 92 | `QID124_9` | RECODE |
| 56 | Experience — A problem with loose animals | Weekly | 2 | 93 | `QID124_10` | RECODE |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | 1 | 133 | `QID211` | RECODE |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | 2 | 134 | `QID219` | RECODE |
| 59 | What is the highest level of education you have completed? | High school diploma or equivalent | 5 | 142 | `QID178` | RECODE |
| 60 | Which best describes your employment status? | Employed- Full time | 1 | 143 | `QID176` | RECODE |

## 24. `R_iGZqrFKoHdcjKOH` — 6394 Baylor Avenue

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_iGZqrFKoHdcjKOH.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | 5 | 123 | `RespIll` | RECODE |
| 2 | How often does anyone in your home have asthma symptoms? | Seasonally | 3 | 122 | `asthma` | RECODE |
| 3 | How often does anyone in your home wheeze? | weekly | 1 | 125 | `wheeze` | RECODE |
| 4 | How often does anyone in your home experience headaches? | Monthly | 2 | 120 | `Headache` | RECODE |
| 5 | How often do you feel tired or fatigued in your home? | weekly | 1 | 124 | `Tired` | RECODE |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | 4 | 132 | `Hospital Respiratory` | RECODE |
| 7 | Evidence of mold in any area of the home? | Yes | 7 | 108 | `Mold` | RECODE |
| 8 | Water leakage — Roof | nan | — | 110 | `Leakage 2_1` | DIFFERENT |
| 9 | Water leakage — Walls | nan | — | 111 | `Leakage 2_2` | DIFFERENT |
| 10 | Water leakage — Windows | more than one week | 2 | 112 | `Leakage 2_3` | RECODE |
| 11 | Water leakage — Floor | nan | — | 113 | `Leakage 2_4` | DIFFERENT |
| 12 | Cooling system — Central AC | nan | — | 100 | `Cooling System _1` | DIFFERENT |
| 13 | Cooling system — Window unit | less than 10 years | 1 | 101 | `Cooling System _2` | RECODE |
| 14 | Cooling system — Fan only | nan | — | 102 | `Cooling System _3` | DIFFERENT |
| 15 | Cooling system — No cooling | nan | — | 103 | `Cooling System _4` | DIFFERENT |
| 16 | Cooking fuel / method | electric cooktops | 7 | 106 | `Cooking` | RECODE |
| 17 | When was your house built? | Click to write Choice 5 | 5 | 39 | `QID192` | PLACEHOLDER |
| 18 | What type of house do you live in? | Double Wide Mobile Home | 2 | 40 | `QID128` | RECODE |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Good- Minor repairs needed. | 2 | 55 | `QID141` | RECODE |
| 20 | What is your current housing ownership status? | Renter | 2 | 24 | `Ownership` | RECODE |
| 21 | How long have you lived in High Ridge Estates? (years) | 5 | 5 | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Don't know | 5 | 44 | `QID47` | RECODE |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | 1 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | More than 6 months | 2 | 56 | `QID21` | RECODE |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | Click to write Choice 4 | 4 | 57 | `QID194` | PLACEHOLDER |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 3 | 1 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes - Portable (Which Room(s)),Click to write Choice 6 | 1,6 | 59 | `QID19` | PLACEHOLDER |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 3 | 3 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 3 | 3 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 3 | 3 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 3 | 3 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 3 | 3 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 3 | 3 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 67 | `QID195_1` | RECODE |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 68 | `QID195_2` | RECODE |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 69 | `QID195_3` | RECODE |
| 39 | Intervention — Improve heating/cooling system(s) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 70 | `QID195_4` | RECODE |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 71 | `QID195_5` | RECODE |
| 41 | Intervention — Replace well/septic | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 72 | `QID195_6` | RECODE |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 74 | `QID195_8` | RECODE |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 75 | `QID195_9` | RECODE |
| 45 | Intervention — Trim trees | — | — | 76 | `QID195_10` | EMPTY-BOTH |
| 46 | Intervention — Improved drainage | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 77 | `QID195_11` | RECODE |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | 2 | 84 | `QID124_1` | RECODE |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | 2 | 85 | `QID124_2` | RECODE |
| 49 | Experience — Extreme heat in recent years | Daily | 1 | 86 | `QID124_3` | RECODE |
| 50 | Experience — Changing your kids' school due to moving | Weekly | 2 | 87 | `QID124_4` | RECODE |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Weekly | 2 | 88 | `QID124_5` | RECODE |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | 2 | 89 | `QID124_6` | RECODE |
| 53 | Experience — Well drying up | Weekly | 2 | 90 | `QID124_7` | RECODE |
| 54 | Experience — A problem with pests in your home | Weekly | 2 | 91 | `QID124_8` | RECODE |
| 55 | Experience — A problem with water leaks | Weekly | 2 | 92 | `QID124_9` | RECODE |
| 56 | Experience — A problem with loose animals | Weekly | 2 | 93 | `QID124_10` | RECODE |
| 57 | Do you (or your household) own or have regular access to a car? | No | 2 | 133 | `QID211` | RECODE |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | Not Sure | 3 | 134 | `QID219` | RECODE |
| 59 | What is the highest level of education you have completed? | Vocational/Technical Licensing or Certification | 9 | 142 | `QID178` | RECODE |
| 60 | Which best describes your employment status? | Unemployed | 3 | 143 | `QID176` | RECODE |

## 25. `R_jIMWa4XhirJ5WDy` — 6301 Columbia Avenue

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_jIMWa4XhirJ5WDy.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | 5 | 123 | `RespIll` | RECODE |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | 5 | 122 | `asthma` | RECODE |
| 3 | How often does anyone in your home wheeze? | Seasonally | 3 | 125 | `wheeze` | RECODE |
| 4 | How often does anyone in your home experience headaches? | Rarely or Never | 5 | 120 | `Headache` | RECODE |
| 5 | How often do you feel tired or fatigued in your home? | weekly | 1 | 124 | `Tired` | RECODE |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | yes | 2 | 132 | `Hospital Respiratory` | RECODE |
| 7 | Evidence of mold in any area of the home? | Yes | 1,4,5,6 | 108 | `Mold` | DIFFERENT |
| 8 | Water leakage — Roof | none | 4 | 110 | `Leakage 2_1` | RECODE |
| 9 | Water leakage — Walls | none | 4 | 111 | `Leakage 2_2` | RECODE |
| 10 | Water leakage — Windows | not fixed | 3 | 112 | `Leakage 2_3` | RECODE |
| 11 | Water leakage — Floor | none | 4 | 113 | `Leakage 2_4` | RECODE |
| 12 | Cooling system — Central AC | Don't know/Not applicable | 4 | 100 | `Cooling System _1` | RECODE |
| 13 | Cooling system — Window unit | More than 15 years | 3 | 101 | `Cooling System _2` | RECODE |
| 14 | Cooling system — Fan only | Don't know/Not applicable | 4 | 102 | `Cooling System _3` | RECODE |
| 15 | Cooling system — No cooling | Don't know/Not applicable | 4 | 103 | `Cooling System _4` | RECODE |
| 16 | Cooking fuel / method | electric cooktops | 7 | 106 | `Cooking` | RECODE |
| 17 | When was your house built? | Built 1960–1979 | 2 | 39 | `QID192` | RECODE |
| 18 | What type of house do you live in? | Single Wide Mobile Home | 1 | 40 | `QID128` | RECODE |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Fair- Some repairs needed. | 3 | 55 | `QID141` | RECODE |
| 20 | What is your current housing ownership status? | Renter | 2 | 24 | `Ownership` | RECODE |
| 21 | How long have you lived in High Ridge Estates? (years) | 2.5 years | 2.5 years | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | 4 | 44 | `QID47` | RECODE |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | 1 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Don't know | 3 | 56 | `QID21` | RECODE |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | More than 6 months | 2 | 57 | `QID194` | RECODE |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 3 | 1 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes- Integrated into central air heating system | 2 | 59 | `QID19` | RECODE |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 1 | 1 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 1 | 1 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 3 | 3 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 4 | 4 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 4 | 4 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 5 | 5 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 67 | `QID195_1` | RECODE |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 68 | `QID195_2` | RECODE |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 69 | `QID195_3` | RECODE |
| 39 | Intervention — Improve heating/cooling system(s) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 70 | `QID195_4` | RECODE |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Click to write Scale Point 1 | 1 | 71 | `QID195_5` | PLACEHOLDER |
| 41 | Intervention — Replace well/septic | Click to write Scale Point 1 | 1 | 72 | `QID195_6` | PLACEHOLDER |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Click to write Scale Point 1 | 1 | 74 | `QID195_8` | PLACEHOLDER |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Click to write Scale Point 1 | 1 | 75 | `QID195_9` | PLACEHOLDER |
| 45 | Intervention — Trim trees | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 76 | `QID195_10` | RECODE |
| 46 | Intervention — Improved drainage | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 77 | `QID195_11` | RECODE |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Daily | 1 | 84 | `QID124_1` | RECODE |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | 2 | 85 | `QID124_2` | RECODE |
| 49 | Experience — Extreme heat in recent years | Daily | 1 | 86 | `QID124_3` | RECODE |
| 50 | Experience — Changing your kids' school due to moving | Weekly | 2 | 87 | `QID124_4` | RECODE |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Daily | 1 | 88 | `QID124_5` | RECODE |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | 2 | 89 | `QID124_6` | RECODE |
| 53 | Experience — Well drying up | Daily | 1 | 90 | `QID124_7` | RECODE |
| 54 | Experience — A problem with pests in your home | Daily | 1 | 91 | `QID124_8` | RECODE |
| 55 | Experience — A problem with water leaks | Daily | 1 | 92 | `QID124_9` | RECODE |
| 56 | Experience — A problem with loose animals | Weekly | 2 | 93 | `QID124_10` | RECODE |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | 1 | 133 | `QID211` | RECODE |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | Yes | 1 | 134 | `QID219` | RECODE |
| 59 | What is the highest level of education you have completed? | High school diploma or equivalent | 5 | 142 | `QID178` | RECODE |
| 60 | Which best describes your employment status? | Unemployed | 3 | 143 | `QID176` | RECODE |

## 26. `R_kVLcdKScFHPgWVR` — 6308 Bucknell

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_kVLcdKScFHPgWVR.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | weekly | 1 | 123 | `RespIll` | RECODE |
| 2 | How often does anyone in your home have asthma symptoms? | weekly | 1 | 122 | `asthma` | RECODE |
| 3 | How often does anyone in your home wheeze? | weekly | 1 | 125 | `wheeze` | RECODE |
| 4 | How often does anyone in your home experience headaches? | Rarely or Never | 5 | 120 | `Headache` | RECODE |
| 5 | How often do you feel tired or fatigued in your home? | weekly | 1 | 124 | `Tired` | RECODE |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | 4 | 132 | `Hospital Respiratory` | RECODE |
| 7 | Evidence of mold in any area of the home? | Yes | 10 | 108 | `Mold` | RECODE |
| 8 | Water leakage — Roof | none | 4 | 110 | `Leakage 2_1` | RECODE |
| 9 | Water leakage — Walls | none | 4 | 111 | `Leakage 2_2` | RECODE |
| 10 | Water leakage — Windows | none | 4 | 112 | `Leakage 2_3` | RECODE |
| 11 | Water leakage — Floor | none | 4 | 113 | `Leakage 2_4` | RECODE |
| 12 | Cooling system — Central AC | less than 10 years | 1 | 100 | `Cooling System _1` | RECODE |
| 13 | Cooling system — Window unit | nan | — | 101 | `Cooling System _2` | DIFFERENT |
| 14 | Cooling system — Fan only | nan | — | 102 | `Cooling System _3` | DIFFERENT |
| 15 | Cooling system — No cooling | nan | — | 103 | `Cooling System _4` | DIFFERENT |
| 16 | Cooking fuel / method | electric cooktops | 7 | 106 | `Cooking` | RECODE |
| 17 | When was your house built? | Before 1960 | 1 | 39 | `QID192` | RECODE |
| 18 | What type of house do you live in? | Double Wide Mobile Home | 2 | 40 | `QID128` | RECODE |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Click to write Choice 5 | 1 | 55 | `QID141` | PLACEHOLDER |
| 20 | What is your current housing ownership status? | Owner | 1 | 24 | `Ownership` | RECODE |
| 21 | How long have you lived in High Ridge Estates? (years) | 1 | 1 | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | 4 | 44 | `QID47` | RECODE |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | 1 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Less than 6 months | 1 | 56 | `QID21` | RECODE |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | Less than 6 months | 1 | 57 | `QID194` | RECODE |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 5 | 3 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes- Integrated into central air heating system | 2 | 59 | `QID19` | RECODE |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 1 | 1 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 1 | 1 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 1 | 1 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 1 | 1 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 4 | 4 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 4 | 4 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Nature reserves and preserves | 7 | 67 | `QID195_1` | RECODE |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Nature reserves and preserves | 7 | 68 | `QID195_2` | RECODE |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Nature reserves and preserves | 7 | 69 | `QID195_3` | RECODE |
| 39 | Intervention — Improve heating/cooling system(s) | Nature reserves and preserves | 7 | 70 | `QID195_4` | RECODE |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Nature reserves and preserves | 7 | 71 | `QID195_5` | RECODE |
| 41 | Intervention — Replace well/septic | Nature reserves and preserves | 7 | 72 | `QID195_6` | RECODE |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 74 | `QID195_8` | RECODE |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Nature reserves and preserves | 7 | 75 | `QID195_9` | RECODE |
| 45 | Intervention — Trim trees | Nature reserves and preserves | 7 | 76 | `QID195_10` | RECODE |
| 46 | Intervention — Improved drainage | Nature reserves and preserves | 7 | 77 | `QID195_11` | RECODE |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | 2 | 84 | `QID124_1` | RECODE |
| 48 | Experience — In case of flooding, received help for cleaning | Biweekly | 3 | 85 | `QID124_2` | RECODE |
| 49 | Experience — Extreme heat in recent years | Weekly | 2 | 86 | `QID124_3` | RECODE |
| 50 | Experience — Changing your kids' school due to moving | Weekly | 2 | 87 | `QID124_4` | RECODE |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Weekly | 2 | 88 | `QID124_5` | RECODE |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | 2 | 89 | `QID124_6` | RECODE |
| 53 | Experience — Well drying up | Weekly | 2 | 90 | `QID124_7` | RECODE |
| 54 | Experience — A problem with pests in your home | Weekly | 2 | 91 | `QID124_8` | RECODE |
| 55 | Experience — A problem with water leaks | Weekly | 2 | 92 | `QID124_9` | RECODE |
| 56 | Experience — A problem with loose animals | Weekly | 2 | 93 | `QID124_10` | RECODE |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | 1 | 133 | `QID211` | RECODE |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | 2 | 134 | `QID219` | RECODE |
| 59 | What is the highest level of education you have completed? | High school diploma or equivalent | 5 | 142 | `QID178` | RECODE |
| 60 | Which best describes your employment status? | Retired | 4 | 143 | `QID176` | RECODE |

## 27. `R_l1yOBZ0aTpnAxq3` — 7358 Yale St.

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_l1yOBZ0aTpnAxq3.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | 5 | 123 | `RespIll` | RECODE |
| 2 | How often does anyone in your home have asthma symptoms? | Monthly | 2 | 122 | `asthma` | RECODE |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | 5 | 125 | `wheeze` | RECODE |
| 4 | How often does anyone in your home experience headaches? | Rarely or Never | 5 | 120 | `Headache` | RECODE |
| 5 | How often do you feel tired or fatigued in your home? | weekly | 1 | 124 | `Tired` | RECODE |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | yes | 3 | 132 | `Hospital Respiratory` | RECODE |
| 7 | Evidence of mold in any area of the home? | Yes | 10 | 108 | `Mold` | RECODE |
| 8 | Water leakage — Roof | none | 4 | 110 | `Leakage 2_1` | RECODE |
| 9 | Water leakage — Walls | none | 4 | 111 | `Leakage 2_2` | RECODE |
| 10 | Water leakage — Windows | none | 4 | 112 | `Leakage 2_3` | RECODE |
| 11 | Water leakage — Floor | none | 4 | 113 | `Leakage 2_4` | RECODE |
| 12 | Cooling system — Central AC | Don't know/Not applicable | 4 | 100 | `Cooling System _1` | RECODE |
| 13 | Cooling system — Window unit | Don't know/Not applicable | 4 | 101 | `Cooling System _2` | RECODE |
| 14 | Cooling system — Fan only | 10 to 15 years | 2 | 102 | `Cooling System _3` | RECODE |
| 15 | Cooling system — No cooling | Don't know/Not applicable | 4 | 103 | `Cooling System _4` | RECODE |
| 16 | Cooking fuel / method | electric cooktops | 7 | 106 | `Cooking` | RECODE |
| 17 | When was your house built? | Click to write Choice 5 | 5 | 39 | `QID192` | PLACEHOLDER |
| 18 | What type of house do you live in? | Double Wide Mobile Home | 2 | 40 | `QID128` | RECODE |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Fair- Some repairs needed. | 3 | 55 | `QID141` | RECODE |
| 20 | What is your current housing ownership status? | Renter | 2 | 24 | `Ownership` | RECODE |
| 21 | How long have you lived in High Ridge Estates? (years) | 5months | 5months | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Wood | 1 | 44 | `QID47` | RECODE |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | 1 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Less than 6 months | 1 | 56 | `QID21` | RECODE |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | Don't know | 3 | 57 | `QID194` | RECODE |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 3 | 1 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes- Integrated into central air heating system | 2 | 59 | `QID19` | RECODE |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 1 | 1 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 2 | 2 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 2 | 2 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 1 | 1 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 1 | 1 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 3 | 3 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 67 | `QID195_1` | RECODE |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 68 | `QID195_2` | RECODE |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Click to write Scale Point 1 | 1 | 69 | `QID195_3` | PLACEHOLDER |
| 39 | Intervention — Improve heating/cooling system(s) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 70 | `QID195_4` | RECODE |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 71 | `QID195_5` | RECODE |
| 41 | Intervention — Replace well/septic | Click to write Scale Point 1 | 1 | 72 | `QID195_6` | PLACEHOLDER |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 74 | `QID195_8` | RECODE |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Click to write Scale Point 1 | 1 | 75 | `QID195_9` | PLACEHOLDER |
| 45 | Intervention — Trim trees | Click to write Scale Point 1 | 1 | 76 | `QID195_10` | PLACEHOLDER |
| 46 | Intervention — Improved drainage | Click to write Scale Point 1 | 1 | 77 | `QID195_11` | PLACEHOLDER |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | 2 | 84 | `QID124_1` | RECODE |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | 2 | 85 | `QID124_2` | RECODE |
| 49 | Experience — Extreme heat in recent years | Weekly | 2 | 86 | `QID124_3` | RECODE |
| 50 | Experience — Changing your kids' school due to moving | Weekly | 2 | 87 | `QID124_4` | RECODE |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Weekly | 2 | 88 | `QID124_5` | RECODE |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | 2 | 89 | `QID124_6` | RECODE |
| 53 | Experience — Well drying up | Weekly | 2 | 90 | `QID124_7` | RECODE |
| 54 | Experience — A problem with pests in your home | Weekly | 2 | 91 | `QID124_8` | RECODE |
| 55 | Experience — A problem with water leaks | Weekly | 2 | 92 | `QID124_9` | RECODE |
| 56 | Experience — A problem with loose animals | Daily | 1 | 93 | `QID124_10` | RECODE |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | 1 | 133 | `QID211` | RECODE |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | 2 | 134 | `QID219` | RECODE |
| 59 | What is the highest level of education you have completed? | Some college, no degree | 6 | 142 | `QID178` | RECODE |
| 60 | Which best describes your employment status? | Employed- Full time | 1 | 143 | `QID176` | RECODE |

## 28. `R_mhCImQQ64DBmsPH` — 6389 Baylor

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_mhCImQQ64DBmsPH.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | 5 | 123 | `RespIll` | RECODE |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | 5 | 122 | `asthma` | RECODE |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | 5 | 125 | `wheeze` | RECODE |
| 4 | How often does anyone in your home experience headaches? | Rarely or Never | 5 | 120 | `Headache` | RECODE |
| 5 | How often do you feel tired or fatigued in your home? | Monthly | 2 | 124 | `Tired` | RECODE |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | yes | 3 | 132 | `Hospital Respiratory` | RECODE |
| 7 | Evidence of mold in any area of the home? | Yes | 4,6,7 | 108 | `Mold` | DIFFERENT |
| 8 | Water leakage — Roof | more than one week | 2 | 110 | `Leakage 2_1` | RECODE |
| 9 | Water leakage — Walls | none | 4 | 111 | `Leakage 2_2` | RECODE |
| 10 | Water leakage — Windows | none | 4 | 112 | `Leakage 2_3` | RECODE |
| 11 | Water leakage — Floor | none | 4 | 113 | `Leakage 2_4` | RECODE |
| 12 | Cooling system — Central AC | nan | — | 100 | `Cooling System _1` | DIFFERENT |
| 13 | Cooling system — Window unit | less than 10 years | 1 | 101 | `Cooling System _2` | RECODE |
| 14 | Cooling system — Fan only | nan | — | 102 | `Cooling System _3` | DIFFERENT |
| 15 | Cooling system — No cooling | nan | — | 103 | `Cooling System _4` | DIFFERENT |
| 16 | Cooking fuel / method | electric cooktops | 7 | 106 | `Cooking` | RECODE |
| 17 | When was your house built? | Before 1960 | 1 | 39 | `QID192` | RECODE |
| 18 | What type of house do you live in? | Double Wide Mobile Home | 2 | 40 | `QID128` | RECODE |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Poor- Major repairs needed. | 4 | 55 | `QID141` | RECODE |
| 20 | What is your current housing ownership status? | Owner | 1 | 24 | `Ownership` | RECODE |
| 21 | How long have you lived in High Ridge Estates? (years) | 50 yrs family land | 50 yrs family land | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | 4 | 44 | `QID47` | RECODE |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | 1 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Less than 6 months | 1 | 56 | `QID21` | RECODE |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | Don't know | 3 | 57 | `QID194` | RECODE |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 5 | 3 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes- Integrated into central air heating system | 2 | 59 | `QID19` | RECODE |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 1 | 1 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 5 | 5 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 5 | 5 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 5 | 5 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 5 | 5 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 5 | 5 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 5 | 5 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 67 | `QID195_1` | RECODE |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 68 | `QID195_2` | RECODE |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Nature reserves and preserves | 7 | 69 | `QID195_3` | RECODE |
| 39 | Intervention — Improve heating/cooling system(s) | Nature reserves and preserves | 7 | 70 | `QID195_4` | RECODE |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 71 | `QID195_5` | RECODE |
| 41 | Intervention — Replace well/septic | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 72 | `QID195_6` | RECODE |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 74 | `QID195_8` | RECODE |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Click to write Scale Point 1 | 1 | 75 | `QID195_9` | PLACEHOLDER |
| 45 | Intervention — Trim trees | Click to write Scale Point 1 | 1 | 76 | `QID195_10` | PLACEHOLDER |
| 46 | Intervention — Improved drainage | Click to write Scale Point 1 | 1 | 77 | `QID195_11` | PLACEHOLDER |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | 2 | 84 | `QID124_1` | RECODE |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | 2 | 85 | `QID124_2` | RECODE |
| 49 | Experience — Extreme heat in recent years | Weekly | 2 | 86 | `QID124_3` | RECODE |
| 50 | Experience — Changing your kids' school due to moving | Weekly | 2 | 87 | `QID124_4` | RECODE |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Daily | 1 | 88 | `QID124_5` | RECODE |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | 2 | 89 | `QID124_6` | RECODE |
| 53 | Experience — Well drying up | Weekly | 2 | 90 | `QID124_7` | RECODE |
| 54 | Experience — A problem with pests in your home | Weekly | 2 | 91 | `QID124_8` | RECODE |
| 55 | Experience — A problem with water leaks | Daily | 1 | 92 | `QID124_9` | RECODE |
| 56 | Experience — A problem with loose animals | Weekly | 2 | 93 | `QID124_10` | RECODE |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | 1 | 133 | `QID211` | RECODE |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | Yes | 1 | 134 | `QID219` | RECODE |
| 59 | What is the highest level of education you have completed? | High school diploma or equivalent | 5 | 142 | `QID178` | RECODE |
| 60 | Which best describes your employment status? | Retired | 4 | 143 | `QID176` | RECODE |

## 29. `R_oAELLLNZllsvEkJ` — 6413 Bowdoin Ave

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_oAELLLNZllsvEkJ.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | 5 | 123 | `RespIll` | RECODE |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | 5 | 122 | `asthma` | RECODE |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | 5 | 125 | `wheeze` | RECODE |
| 4 | How often does anyone in your home experience headaches? | Seasonally | 3 | 120 | `Headache` | RECODE |
| 5 | How often do you feel tired or fatigued in your home? | weekly | 1 | 124 | `Tired` | RECODE |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | 4 | 132 | `Hospital Respiratory` | RECODE |
| 7 | Evidence of mold in any area of the home? | Yes | 10 | 108 | `Mold` | RECODE |
| 8 | Water leakage — Roof | more than one week | 2 | 110 | `Leakage 2_1` | RECODE |
| 9 | Water leakage — Walls | none | 4 | 111 | `Leakage 2_2` | RECODE |
| 10 | Water leakage — Windows | more than one week | 2 | 112 | `Leakage 2_3` | RECODE |
| 11 | Water leakage — Floor | more than one week | 2 | 113 | `Leakage 2_4` | RECODE |
| 12 | Cooling system — Central AC | less than 10 years | 1 | 100 | `Cooling System _1` | RECODE |
| 13 | Cooling system — Window unit | Don't know/Not applicable | 4 | 101 | `Cooling System _2` | RECODE |
| 14 | Cooling system — Fan only | Don't know/Not applicable | 4 | 102 | `Cooling System _3` | RECODE |
| 15 | Cooling system — No cooling | Don't know/Not applicable | 4 | 103 | `Cooling System _4` | RECODE |
| 16 | Cooking fuel / method | electric cooktops | 7 | 106 | `Cooking` | RECODE |
| 17 | When was your house built? | Built 1980–1999 | 3 | 39 | `QID192` | RECODE |
| 18 | What type of house do you live in? | Single Wide Mobile Home | 1 | 40 | `QID128` | RECODE |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Good- Minor repairs needed. | 2 | 55 | `QID141` | RECODE |
| 20 | What is your current housing ownership status? | Owner | 1 | 24 | `Ownership` | RECODE |
| 21 | How long have you lived in High Ridge Estates? (years) | 9 | 9 | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | 4 | 44 | `QID47` | RECODE |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | 1 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | More than 6 months | 2 | 56 | `QID21` | RECODE |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | More than 6 months | 2 | 57 | `QID194` | RECODE |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 4 | 2 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes- Integrated into central air heating system | 2 | 59 | `QID19` | RECODE |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 2 | 2 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 3 | 3 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 3 | 3 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 2 | 2 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 3 | 3 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 2 | 2 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 2 | 2 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Click to write Scale Point 1 | 1 | 67 | `QID195_1` | PLACEHOLDER |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Click to write Scale Point 1 | 1 | 68 | `QID195_2` | PLACEHOLDER |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Click to write Scale Point 1 | 1 | 69 | `QID195_3` | PLACEHOLDER |
| 39 | Intervention — Improve heating/cooling system(s) | Click to write Scale Point 1 | 1 | 70 | `QID195_4` | PLACEHOLDER |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Click to write Scale Point 1 | 1 | 71 | `QID195_5` | PLACEHOLDER |
| 41 | Intervention — Replace well/septic | Click to write Scale Point 1 | 1 | 72 | `QID195_6` | PLACEHOLDER |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 74 | `QID195_8` | RECODE |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Click to write Scale Point 1 | 1 | 75 | `QID195_9` | PLACEHOLDER |
| 45 | Intervention — Trim trees | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 76 | `QID195_10` | RECODE |
| 46 | Intervention — Improved drainage | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 77 | `QID195_11` | RECODE |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | 2 | 84 | `QID124_1` | RECODE |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | 2 | 85 | `QID124_2` | RECODE |
| 49 | Experience — Extreme heat in recent years | Weekly | 2 | 86 | `QID124_3` | RECODE |
| 50 | Experience — Changing your kids' school due to moving | Weekly | 2 | 87 | `QID124_4` | RECODE |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Daily | 1 | 88 | `QID124_5` | RECODE |
| 52 | Experience — Losing home owners insurance due to age of home | Biweekly | 3 | 89 | `QID124_6` | RECODE |
| 53 | Experience — Well drying up | Biweekly | 3 | 90 | `QID124_7` | RECODE |
| 54 | Experience — A problem with pests in your home | Weekly | 2 | 91 | `QID124_8` | RECODE |
| 55 | Experience — A problem with water leaks | Daily | 1 | 92 | `QID124_9` | RECODE |
| 56 | Experience — A problem with loose animals | Daily | 1 | 93 | `QID124_10` | RECODE |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | 1 | 133 | `QID211` | RECODE |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | 2 | 134 | `QID219` | RECODE |
| 59 | What is the highest level of education you have completed? | Some college, no degree | 6 | 142 | `QID178` | RECODE |
| 60 | Which best describes your employment status? | Retired | 4 | 143 | `QID176` | RECODE |

## 30. `R_orcmMnaQVATvgHJ` — 7183 Duke St

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_orcmMnaQVATvgHJ.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | 5 | 123 | `RespIll` | RECODE |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | 5 | 122 | `asthma` | RECODE |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | 5 | 125 | `wheeze` | RECODE |
| 4 | How often does anyone in your home experience headaches? | Rarely or Never | 5 | 120 | `Headache` | RECODE |
| 5 | How often do you feel tired or fatigued in your home? | Rarely or Never | 5 | 124 | `Tired` | RECODE |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | 4 | 132 | `Hospital Respiratory` | RECODE |
| 7 | Evidence of mold in any area of the home? | Yes | 10 | 108 | `Mold` | RECODE |
| 8 | Water leakage — Roof | less than one week | 1 | 110 | `Leakage 2_1` | RECODE |
| 9 | Water leakage — Walls | less than one week | 1 | 111 | `Leakage 2_2` | RECODE |
| 10 | Water leakage — Windows | less than one week | 1 | 112 | `Leakage 2_3` | RECODE |
| 11 | Water leakage — Floor | less than one week | 1 | 113 | `Leakage 2_4` | RECODE |
| 12 | Cooling system — Central AC | less than 10 years | 1 | 100 | `Cooling System _1` | RECODE |
| 13 | Cooling system — Window unit | Don't know/Not applicable | 4 | 101 | `Cooling System _2` | RECODE |
| 14 | Cooling system — Fan only | less than 10 years | 1 | 102 | `Cooling System _3` | RECODE |
| 15 | Cooling system — No cooling | nan | — | 103 | `Cooling System _4` | DIFFERENT |
| 16 | Cooking fuel / method | electric cooktops | 7 | 106 | `Cooking` | RECODE |
| 17 | When was your house built? | Built 1960–1979 | 2 | 39 | `QID192` | RECODE |
| 18 | What type of house do you live in? | Single Wide Mobile Home | 1 | 40 | `QID128` | RECODE |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Good- Minor repairs needed. | 2 | 55 | `QID141` | RECODE |
| 20 | What is your current housing ownership status? | Owner | 1 | 24 | `Ownership` | RECODE |
| 21 | How long have you lived in High Ridge Estates? (years) | 20 | 20 | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | 4 | 44 | `QID47` | RECODE |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | 1 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Click to write Choice 4 | 4 | 56 | `QID21` | PLACEHOLDER |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | More than 6 months | 2 | 57 | `QID194` | RECODE |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 3 | 1 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes - Portable (Which Room(s)) | 1 | 59 | `QID19` | RECODE |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 1 | 1 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 5 | 5 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 5 | 5 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 2 | 2 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 1 | 1 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 3 | 3 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Click to write Scale Point 1 | 1 | 67 | `QID195_1` | PLACEHOLDER |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 6 | 68 | `QID195_2` | RECODE |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Click to write Scale Point 1 | 1 | 69 | `QID195_3` | PLACEHOLDER |
| 39 | Intervention — Improve heating/cooling system(s) | Click to write Scale Point 1 | 1 | 70 | `QID195_4` | PLACEHOLDER |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Click to write Scale Point 1 | 1 | 71 | `QID195_5` | PLACEHOLDER |
| 41 | Intervention — Replace well/septic | Click to write Scale Point 1 | 1 | 72 | `QID195_6` | PLACEHOLDER |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Click to write Scale Point 1 | 1 | 74 | `QID195_8` | PLACEHOLDER |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Click to write Scale Point 1 | 1 | 75 | `QID195_9` | PLACEHOLDER |
| 45 | Intervention — Trim trees | Click to write Scale Point 1 | 1 | 76 | `QID195_10` | PLACEHOLDER |
| 46 | Intervention — Improved drainage | Click to write Scale Point 1 | 1 | 77 | `QID195_11` | PLACEHOLDER |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | 2 | 84 | `QID124_1` | RECODE |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | 2 | 85 | `QID124_2` | RECODE |
| 49 | Experience — Extreme heat in recent years | Daily | 1 | 86 | `QID124_3` | RECODE |
| 50 | Experience — Changing your kids' school due to moving | Weekly | 2 | 87 | `QID124_4` | RECODE |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Weekly | 2 | 88 | `QID124_5` | RECODE |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | 2 | 89 | `QID124_6` | RECODE |
| 53 | Experience — Well drying up | Weekly | 2 | 90 | `QID124_7` | RECODE |
| 54 | Experience — A problem with pests in your home | Weekly | 2 | 91 | `QID124_8` | RECODE |
| 55 | Experience — A problem with water leaks | Daily | 1 | 92 | `QID124_9` | RECODE |
| 56 | Experience — A problem with loose animals | Daily | 1 | 93 | `QID124_10` | RECODE |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | 1 | 133 | `QID211` | RECODE |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | 2 | 134 | `QID219` | RECODE |
| 59 | What is the highest level of education you have completed? | Vocational/Technical Licensing or Certification | 9 | 142 | `QID178` | RECODE |
| 60 | Which best describes your employment status? | Retired | 4 | 143 | `QID176` | RECODE |

