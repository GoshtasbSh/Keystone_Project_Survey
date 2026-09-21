# Popup (as rendered on screen) vs the April 15 Qualtrics export

Every "Popup shows" value in this table was read out of the live `-blue` dashboard after clicking the map marker and opening the **Survey Answers** tab — it is what a person sees, not an API value. Screenshots of each popup are in `../screenshots/`.

Rows are joined to a Qualtrics question by the popup's own label, then to a CSV column by that question's `ImportId` (QID) — never by column position.

**Verdicts** — `MATCH`: popup equals the CSV cell. `PLACEHOLDER`: the popup shows Qualtrics placeholder text (`Click to write …`); the respondent did answer, but neither the export nor the dashboard resolves the real label (findings F0/F9). `RECODE`: the CSV holds a numeric code and the popup shows a translated label. `DIFFERENT`: popup disagrees with the CSV. `EMPTY-BOTH`: blank in both — correct. `MISSING`: the CSV has an answer but the popup shows nothing. `NOT-IN-EXPORT`: that QID has no column in this export.

## Verdict totals

| Verdict | Cells | % |
|---|---|---|
| MATCH | 963 | 69.4% |
| PLACEHOLDER | 329 | 23.7% |
| DIFFERENT | 67 | 4.8% |
| EMPTY-BOTH | 21 | 1.5% |
| UNVERIFIED-NO-ROW | 7 | 0.5% |

Total answer cells compared: **1387** across **30** points.

## 1. `R_1E4YReRP6XTeX06` — 6390 Bucknell Ave

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_1E4YReRP6XTeX06.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Seasonally | Seasonally | 123 | `RespIll` | MATCH |
| 2 | How often does anyone in your home have asthma symptoms? | Seasonally | Seasonally | 122 | `asthma` | MATCH |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | Rarely or Never | 125 | `wheeze` | MATCH |
| 4 | How often does anyone in your home experience headaches? | Rarely or Never | Rarely or Never | 120 | `Headache` | MATCH |
| 5 | How often do you feel tired or fatigued in your home? | weekly | weekly | 124 | `Tired` | MATCH |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | yes | Yes, hospitalization/visiting the emergency room for asthma attack. | 132 | `Hospital Respiratory` | DIFFERENT |
| 7 | Evidence of mold in any area of the home? | Yes | Other: | 108 | `Mold` | DIFFERENT |
| 8 | Water leakage — Roof | none | none | 110 | `Leakage 2_1` | MATCH |
| 9 | Water leakage — Walls | none | none | 111 | `Leakage 2_2` | MATCH |
| 10 | Water leakage — Windows | none | none | 112 | `Leakage 2_3` | MATCH |
| 11 | Water leakage — Floor | none | none | 113 | `Leakage 2_4` | MATCH |
| 12 | Cooling system — Central AC | More than 15 years | More than 15 years | 100 | `Cooling System _1` | MATCH |
| 13 | Cooling system — Window unit | nan | — | 101 | `Cooling System _2` | DIFFERENT |
| 14 | Cooling system — Fan only | less than 10 years | less than 10 years | 102 | `Cooling System _3` | MATCH |
| 15 | Cooling system — No cooling | nan | — | 103 | `Cooling System _4` | DIFFERENT |
| 16 | Cooking fuel / method | electric cooktops | electric cooktops | 106 | `Cooking` | MATCH |
| 17 | When was your house built? | Built 1960–1979 | Built 1960–1979 | 39 | `QID192` | MATCH |
| 18 | What type of house do you live in? | Double Wide Mobile Home | Double Wide Mobile Home | 40 | `QID128` | MATCH |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Fair- Some repairs needed. | Fair- Some repairs needed. | 55 | `QID141` | MATCH |
| 20 | What is your current housing ownership status? | Owner | Owner | 24 | `Ownership` | MATCH |
| 21 | How long have you lived in High Ridge Estates? (years) | 6 | 6 | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Steel | Steel | 44 | `QID47` | MATCH |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | Click to write Choice 3 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Less than 6 months | Less than 6 months | 56 | `QID21` | MATCH |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | Click to write Choice 4 | Click to write Choice 4 | 57 | `QID194` | PLACEHOLDER |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 4 | Click to write Choice 4 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes - Portable (Which Room(s)),Yes- Integrated into central air heating system,Don’t Know | Yes - Portable (Which Room(s)),Yes- Integrated into central air heating system,Don’t Know | 59 | `QID19` | MATCH |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 1 | Click to write Scale Point 1 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 3 | Click to write Scale Point 3 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 3 | Click to write Scale Point 3 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 1 | Click to write Scale Point 1 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 1 | Click to write Scale Point 1 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 2 | Click to write Scale Point 2 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | Click to write Scale Point 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | Click to write Scale Point 1 | Click to write Scale Point 1 | 36 | `QID181_8` | PLACEHOLDER |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Nature reserves and preserves | Nature reserves and preserves | 67 | `QID195_1` | MATCH |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Nature reserves and preserves | Nature reserves and preserves | 68 | `QID195_2` | MATCH |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Nature reserves and preserves | Nature reserves and preserves | 69 | `QID195_3` | MATCH |
| 39 | Intervention — Improve heating/cooling system(s) | Click to write Scale Point 1 | Click to write Scale Point 1 | 70 | `QID195_4` | PLACEHOLDER |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Click to write Scale Point 1 | Click to write Scale Point 1 | 71 | `QID195_5` | PLACEHOLDER |
| 41 | Intervention — Replace well/septic | Click to write Scale Point 1 | Click to write Scale Point 1 | 72 | `QID195_6` | PLACEHOLDER |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | Click to write Scale Point 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Nature reserves and preserves | Nature reserves and preserves | 74 | `QID195_8` | MATCH |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Click to write Scale Point 1 | Click to write Scale Point 1 | 75 | `QID195_9` | PLACEHOLDER |
| 45 | Intervention — Trim trees | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 76 | `QID195_10` | MATCH |
| 46 | Intervention — Improved drainage | Nature reserves and preserves | Nature reserves and preserves | 77 | `QID195_11` | MATCH |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | Weekly | 84 | `QID124_1` | MATCH |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | Weekly | 85 | `QID124_2` | MATCH |
| 49 | Experience — Extreme heat in recent years | Weekly | Weekly | 86 | `QID124_3` | MATCH |
| 50 | Experience — Changing your kids' school due to moving | Weekly | Weekly | 87 | `QID124_4` | MATCH |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Daily | Daily | 88 | `QID124_5` | MATCH |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | Weekly | 89 | `QID124_6` | MATCH |
| 53 | Experience — Well drying up | Weekly | Weekly | 90 | `QID124_7` | MATCH |
| 54 | Experience — A problem with pests in your home | Daily | Daily | 91 | `QID124_8` | MATCH |
| 55 | Experience — A problem with water leaks | Weekly | Weekly | 92 | `QID124_9` | MATCH |
| 56 | Experience — A problem with loose animals | Weekly | Weekly | 93 | `QID124_10` | MATCH |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | Yes | 133 | `QID211` | MATCH |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | No | 134 | `QID219` | MATCH |
| 59 | What is the highest level of education you have completed? | Vocational/Technical Licensing or Certification | Vocational/Technical Licensing or Certification | 142 | `QID178` | MATCH |
| 60 | Which best describes your employment status? | Employed- Full time | Employed- Full time | 143 | `QID176` | MATCH |

## 2. `R_23kV7GlWM0LQkKc` — 6176 Harvard Avenue

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_23kV7GlWM0LQkKc.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | weekly | weekly | 123 | `RespIll` | MATCH |
| 2 | How often does anyone in your home have asthma symptoms? | weekly | weekly | 122 | `asthma` | MATCH |
| 3 | How often does anyone in your home wheeze? | Seasonally | Seasonally | 125 | `wheeze` | MATCH |
| 4 | How often does anyone in your home experience headaches? | weekly | weekly | 120 | `Headache` | MATCH |
| 5 | How often do you feel tired or fatigued in your home? | weekly | weekly | 124 | `Tired` | MATCH |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | yes | Yes, Doctor visits for allergy. | 132 | `Hospital Respiratory` | DIFFERENT |
| 7 | Evidence of mold in any area of the home? | Yes | Inner walls/Windows | 108 | `Mold` | DIFFERENT |
| 8 | Water leakage — Roof | not fixed | not fixed | 110 | `Leakage 2_1` | MATCH |
| 9 | Water leakage — Walls | not fixed | not fixed | 111 | `Leakage 2_2` | MATCH |
| 10 | Water leakage — Windows | not fixed | not fixed | 112 | `Leakage 2_3` | MATCH |
| 11 | Water leakage — Floor | none | none | 113 | `Leakage 2_4` | MATCH |
| 12 | Cooling system — Central AC | nan | — | 100 | `Cooling System _1` | DIFFERENT |
| 13 | Cooling system — Window unit | Don't know/Not applicable | Don't know/Not applicable | 101 | `Cooling System _2` | MATCH |
| 14 | Cooling system — Fan only | 10 to 15 years | 10 to 15 years | 102 | `Cooling System _3` | MATCH |
| 15 | Cooling system — No cooling | nan | — | 103 | `Cooling System _4` | DIFFERENT |
| 16 | Cooking fuel / method | electric cooktops | electric cooktops | 106 | `Cooking` | MATCH |
| 17 | When was your house built? | Built 1960–1979 | Built 1960–1979 | 39 | `QID192` | MATCH |
| 18 | What type of house do you live in? | Double Wide Mobile Home | Double Wide Mobile Home | 40 | `QID128` | MATCH |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Poor- Major repairs needed. | Poor- Major repairs needed. | 55 | `QID141` | MATCH |
| 20 | What is your current housing ownership status? | Owner | Owner | 24 | `Ownership` | MATCH |
| 21 | How long have you lived in High Ridge Estates? (years) | 14 | 14 | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | Others | 44 | `QID47` | MATCH |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 4 | Click to write Choice 4 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Less than 6 months | Less than 6 months | 56 | `QID21` | MATCH |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | More than 6 months | More than 6 months | 57 | `QID194` | MATCH |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 3 | Click to write Choice 3 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes- Integrated into central air heating system,No,Click to write Choice 6 | Yes- Integrated into central air heating system,No,Click to write Choice 6 | 59 | `QID19` | PLACEHOLDER |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 1 | Click to write Scale Point 1 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 2 | Click to write Scale Point 2 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 3 | Click to write Scale Point 3 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 3 | Click to write Scale Point 3 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 2 | Click to write Scale Point 2 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 3 | Click to write Scale Point 3 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | Click to write Scale Point 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 67 | `QID195_1` | MATCH |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 68 | `QID195_2` | MATCH |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 69 | `QID195_3` | MATCH |
| 39 | Intervention — Improve heating/cooling system(s) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 70 | `QID195_4` | MATCH |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 71 | `QID195_5` | MATCH |
| 41 | Intervention — Replace well/septic | Click to write Scale Point 1 | Click to write Scale Point 1 | 72 | `QID195_6` | PLACEHOLDER |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | Click to write Scale Point 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Nature reserves and preserves | Nature reserves and preserves | 74 | `QID195_8` | MATCH |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Click to write Scale Point 1 | Click to write Scale Point 1 | 75 | `QID195_9` | PLACEHOLDER |
| 45 | Intervention — Trim trees | Click to write Scale Point 1 | Click to write Scale Point 1 | 76 | `QID195_10` | PLACEHOLDER |
| 46 | Intervention — Improved drainage | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 77 | `QID195_11` | MATCH |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | Weekly | 84 | `QID124_1` | MATCH |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | Weekly | 85 | `QID124_2` | MATCH |
| 49 | Experience — Extreme heat in recent years | Daily | Daily | 86 | `QID124_3` | MATCH |
| 50 | Experience — Changing your kids' school due to moving | Weekly | Weekly | 87 | `QID124_4` | MATCH |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Weekly | Weekly | 88 | `QID124_5` | MATCH |
| 52 | Experience — Losing home owners insurance due to age of home | Daily | Daily | 89 | `QID124_6` | MATCH |
| 53 | Experience — Well drying up | Weekly | Weekly | 90 | `QID124_7` | MATCH |
| 54 | Experience — A problem with pests in your home | Daily | Daily | 91 | `QID124_8` | MATCH |
| 55 | Experience — A problem with water leaks | Daily | Daily | 92 | `QID124_9` | MATCH |
| 56 | Experience — A problem with loose animals | Daily | Daily | 93 | `QID124_10` | MATCH |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | Yes | 133 | `QID211` | MATCH |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | Name the problem | Name the problem | 134 | `QID219` | MATCH |
| 59 | What is the highest level of education you have completed? | Vocational/Technical Licensing or Certification | Vocational/Technical Licensing or Certification | 142 | `QID178` | MATCH |
| 60 | Which best describes your employment status? | Unemployed | Unemployed | 143 | `QID176` | MATCH |

## 3. `R_378SeCJx2uslNli` — 6369 Dennison

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_378SeCJx2uslNli.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Seasonally | Seasonally | 123 | `RespIll` | MATCH |
| 2 | How often does anyone in your home have asthma symptoms? | Seasonally | Seasonally | 122 | `asthma` | MATCH |
| 3 | How often does anyone in your home wheeze? | Seasonally | Seasonally | 125 | `wheeze` | MATCH |
| 4 | How often does anyone in your home experience headaches? | Monthly | Monthly | 120 | `Headache` | MATCH |
| 5 | How often do you feel tired or fatigued in your home? | Seasonally | Seasonally | 124 | `Tired` | MATCH |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | No | 132 | `Hospital Respiratory` | MATCH |
| 7 | Evidence of mold in any area of the home? | Yes | Kitchen,Bathroom,Inner walls/Windows,Ceiling | 108 | `Mold` | DIFFERENT |
| 8 | Water leakage — Roof | more than one week | more than one week | 110 | `Leakage 2_1` | MATCH |
| 9 | Water leakage — Walls | less than one week | less than one week | 111 | `Leakage 2_2` | MATCH |
| 10 | Water leakage — Windows | none | none | 112 | `Leakage 2_3` | MATCH |
| 11 | Water leakage — Floor | more than one week | more than one week | 113 | `Leakage 2_4` | MATCH |
| 12 | Cooling system — Central AC | Don't know/Not applicable | Don't know/Not applicable | 100 | `Cooling System _1` | MATCH |
| 13 | Cooling system — Window unit | 10 to 15 years | 10 to 15 years | 101 | `Cooling System _2` | MATCH |
| 14 | Cooling system — Fan only | Don't know/Not applicable | Don't know/Not applicable | 102 | `Cooling System _3` | MATCH |
| 15 | Cooling system — No cooling | less than 10 years | less than 10 years | 103 | `Cooling System _4` | MATCH |
| 16 | Cooking fuel / method | electric cooktops | electric cooktops | 106 | `Cooking` | MATCH |
| 17 | When was your house built? | Built 1960–1979 | Built 1960–1979 | 39 | `QID192` | MATCH |
| 18 | What type of house do you live in? | Double Wide Mobile Home | Double Wide Mobile Home | 40 | `QID128` | MATCH |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Poor- Major repairs needed. | Poor- Major repairs needed. | 55 | `QID141` | MATCH |
| 20 | What is your current housing ownership status? | Owner | Owner | 24 | `Ownership` | MATCH |
| 21 | How long have you lived in High Ridge Estates? (years) | 9 | 9 | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | Others | 44 | `QID47` | MATCH |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 4 | Click to write Choice 4 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Don't know | Don't know | 56 | `QID21` | MATCH |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | Don't know | Don't know | 57 | `QID194` | MATCH |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 3 | Click to write Choice 3 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes- Integrated into central air heating system,Don’t Know,Click to write Choice 6 | Yes- Integrated into central air heating system,Don’t Know,Click to write Choice 6 | 59 | `QID19` | PLACEHOLDER |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 4 | Click to write Scale Point 4 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 4 | Click to write Scale Point 4 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 4 | Click to write Scale Point 4 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 3 | Click to write Scale Point 3 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 3 | Click to write Scale Point 3 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 4 | Click to write Scale Point 4 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 3 | Click to write Scale Point 3 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | Click to write Scale Point 1 | Click to write Scale Point 1 | 36 | `QID181_8` | PLACEHOLDER |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 67 | `QID195_1` | MATCH |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 68 | `QID195_2` | MATCH |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 69 | `QID195_3` | MATCH |
| 39 | Intervention — Improve heating/cooling system(s) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 70 | `QID195_4` | MATCH |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 71 | `QID195_5` | MATCH |
| 41 | Intervention — Replace well/septic | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 72 | `QID195_6` | MATCH |
| 42 | Intervention — Connect to city water through CCUA | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 73 | `QID195_7` | MATCH |
| 43 | Intervention — Add a fence for safety | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 74 | `QID195_8` | MATCH |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Click to write Scale Point 1 | Click to write Scale Point 1 | 75 | `QID195_9` | PLACEHOLDER |
| 45 | Intervention — Trim trees | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 76 | `QID195_10` | MATCH |
| 46 | Intervention — Improved drainage | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 77 | `QID195_11` | MATCH |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | Weekly | 84 | `QID124_1` | MATCH |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | Weekly | 85 | `QID124_2` | MATCH |
| 49 | Experience — Extreme heat in recent years | Daily | Daily | 86 | `QID124_3` | MATCH |
| 50 | Experience — Changing your kids' school due to moving | Weekly | Weekly | 87 | `QID124_4` | MATCH |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Weekly | Weekly | 88 | `QID124_5` | MATCH |
| 52 | Experience — Losing home owners insurance due to age of home | Daily | Daily | 89 | `QID124_6` | MATCH |
| 53 | Experience — Well drying up | Daily | Daily | 90 | `QID124_7` | MATCH |
| 54 | Experience — A problem with pests in your home | Daily | Daily | 91 | `QID124_8` | MATCH |
| 55 | Experience — A problem with water leaks | Daily | Daily | 92 | `QID124_9` | MATCH |
| 56 | Experience — A problem with loose animals | Daily | Daily | 93 | `QID124_10` | MATCH |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | Yes | 133 | `QID211` | MATCH |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | No | 134 | `QID219` | MATCH |
| 59 | What is the highest level of education you have completed? | less than high school | less than high school | 142 | `QID178` | MATCH |
| 60 | Which best describes your employment status? | Unemployed | Unemployed | 143 | `QID176` | MATCH |

## 4. `R_3N0BugWZGh4ufub` — 6348 Baylor Avenue

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_3N0BugWZGh4ufub.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | Rarely or Never | 123 | `RespIll` | MATCH |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | Rarely or Never | 122 | `asthma` | MATCH |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | Rarely or Never | 125 | `wheeze` | MATCH |
| 4 | How often does anyone in your home experience headaches? | Rarely or Never | Rarely or Never | 120 | `Headache` | MATCH |
| 5 | How often do you feel tired or fatigued in your home? | Rarely or Never | Rarely or Never | 124 | `Tired` | MATCH |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | No | 132 | `Hospital Respiratory` | MATCH |
| 7 | Evidence of mold in any area of the home? | No | — | 108 | `Mold` | DIFFERENT |
| 8 | Water leakage — Roof | none | none | 110 | `Leakage 2_1` | MATCH |
| 9 | Water leakage — Walls | none | none | 111 | `Leakage 2_2` | MATCH |
| 10 | Water leakage — Windows | none | none | 112 | `Leakage 2_3` | MATCH |
| 11 | Water leakage — Floor | none | none | 113 | `Leakage 2_4` | MATCH |
| 12 | Cooling system — Central AC | nan | — | 100 | `Cooling System _1` | DIFFERENT |
| 13 | Cooling system — Window unit | 10 to 15 years | 10 to 15 years | 101 | `Cooling System _2` | MATCH |
| 14 | Cooling system — Fan only | nan | — | 102 | `Cooling System _3` | DIFFERENT |
| 15 | Cooling system — No cooling | nan | — | 103 | `Cooling System _4` | DIFFERENT |
| 16 | Cooking fuel / method | electric cooktops | electric cooktops | 106 | `Cooking` | MATCH |
| 17 | When was your house built? | Click to write Choice 5 | Click to write Choice 5 | 39 | `QID192` | PLACEHOLDER |
| 18 | What type of house do you live in? | Single Wide Mobile Home | Single Wide Mobile Home | 40 | `QID128` | MATCH |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Fair- Some repairs needed. | Fair- Some repairs needed. | 55 | `QID141` | MATCH |
| 20 | What is your current housing ownership status? | Owner | Owner | 24 | `Ownership` | MATCH |
| 21 | How long have you lived in High Ridge Estates? (years) | 6yrs | 6yrs | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Concrete | Concrete | 44 | `QID47` | MATCH |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | Click to write Choice 3 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | More than 6 months | More than 6 months | 56 | `QID21` | MATCH |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | Click to write Choice 4 | Click to write Choice 4 | 57 | `QID194` | PLACEHOLDER |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 3 | Click to write Choice 3 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes - Portable (Which Room(s)),No,Don’t Know,Click to write Choice 5,Click to write Choice 6 | Yes - Portable (Which Room(s)),No,Don’t Know,Click to write Choice 5,Click to write Choice 6 | 59 | `QID19` | PLACEHOLDER |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 3 | Click to write Scale Point 3 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 3 | Click to write Scale Point 3 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 3 | Click to write Scale Point 3 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 3 | Click to write Scale Point 3 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 1 | Click to write Scale Point 1 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 3 | Click to write Scale Point 3 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | Click to write Scale Point 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | Click to write Scale Point 1 | Click to write Scale Point 1 | 36 | `QID181_8` | PLACEHOLDER |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 67 | `QID195_1` | MATCH |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 68 | `QID195_2` | MATCH |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 69 | `QID195_3` | MATCH |
| 39 | Intervention — Improve heating/cooling system(s) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 70 | `QID195_4` | MATCH |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 71 | `QID195_5` | MATCH |
| 41 | Intervention — Replace well/septic | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 72 | `QID195_6` | MATCH |
| 42 | Intervention — Connect to city water through CCUA | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 73 | `QID195_7` | MATCH |
| 43 | Intervention — Add a fence for safety | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 74 | `QID195_8` | MATCH |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 75 | `QID195_9` | MATCH |
| 45 | Intervention — Trim trees | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 76 | `QID195_10` | MATCH |
| 46 | Intervention — Improved drainage | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 77 | `QID195_11` | MATCH |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | Weekly | 84 | `QID124_1` | MATCH |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | Weekly | 85 | `QID124_2` | MATCH |
| 49 | Experience — Extreme heat in recent years | Weekly | Weekly | 86 | `QID124_3` | MATCH |
| 50 | Experience — Changing your kids' school due to moving | Weekly | Weekly | 87 | `QID124_4` | MATCH |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Weekly | Weekly | 88 | `QID124_5` | MATCH |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | Weekly | 89 | `QID124_6` | MATCH |
| 53 | Experience — Well drying up | Weekly | Weekly | 90 | `QID124_7` | MATCH |
| 54 | Experience — A problem with pests in your home | Weekly | Weekly | 91 | `QID124_8` | MATCH |
| 55 | Experience — A problem with water leaks | Weekly | Weekly | 92 | `QID124_9` | MATCH |
| 56 | Experience — A problem with loose animals | Daily | Daily | 93 | `QID124_10` | MATCH |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | Yes | 133 | `QID211` | MATCH |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | No | 134 | `QID219` | MATCH |
| 59 | What is the highest level of education you have completed? | High school diploma or equivalent | High school diploma or equivalent | 142 | `QID178` | MATCH |
| 60 | Which best describes your employment status? | Unemployed | Unemployed | 143 | `QID176` | MATCH |

## 5. `R_43YLnrxxRNRA5hW` — 6260 Baylor Avenue

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_43YLnrxxRNRA5hW.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | Rarely or Never | 123 | `RespIll` | MATCH |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | Rarely or Never | 122 | `asthma` | MATCH |
| 3 | How often does anyone in your home wheeze? | weekly | weekly | 125 | `wheeze` | MATCH |
| 4 | How often does anyone in your home experience headaches? | Rarely or Never | Rarely or Never | 120 | `Headache` | MATCH |
| 5 | How often do you feel tired or fatigued in your home? | Rarely or Never | Rarely or Never | 124 | `Tired` | MATCH |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | No | 132 | `Hospital Respiratory` | MATCH |
| 7 | Evidence of mold in any area of the home? | Yes | Other: | 108 | `Mold` | DIFFERENT |
| 8 | Water leakage — Roof | none | none | 110 | `Leakage 2_1` | MATCH |
| 9 | Water leakage — Walls | none | none | 111 | `Leakage 2_2` | MATCH |
| 10 | Water leakage — Windows | none | none | 112 | `Leakage 2_3` | MATCH |
| 11 | Water leakage — Floor | none | none | 113 | `Leakage 2_4` | MATCH |
| 12 | Cooling system — Central AC | More than 15 years | More than 15 years | 100 | `Cooling System _1` | MATCH |
| 13 | Cooling system — Window unit | More than 15 years | More than 15 years | 101 | `Cooling System _2` | MATCH |
| 14 | Cooling system — Fan only | less than 10 years | less than 10 years | 102 | `Cooling System _3` | MATCH |
| 15 | Cooling system — No cooling | Don't know/Not applicable | Don't know/Not applicable | 103 | `Cooling System _4` | MATCH |
| 16 | Cooking fuel / method | electric cooktops | electric cooktops | 106 | `Cooking` | MATCH |
| 17 | When was your house built? | Built 1960–1979 | Built 1960–1979 | 39 | `QID192` | MATCH |
| 18 | What type of house do you live in? | Double Wide Mobile Home | Double Wide Mobile Home | 40 | `QID128` | MATCH |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Good- Minor repairs needed. | Good- Minor repairs needed. | 55 | `QID141` | MATCH |
| 20 | What is your current housing ownership status? | Owner | Owner | 24 | `Ownership` | MATCH |
| 21 | How long have you lived in High Ridge Estates? (years) | 6 years | 6 years | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | Others | 44 | `QID47` | MATCH |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | Click to write Choice 3 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Less than 6 months | Less than 6 months | 56 | `QID21` | MATCH |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | Less than 6 months | Less than 6 months | 57 | `QID194` | MATCH |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 4 | Click to write Choice 4 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes- Integrated into central air heating system | Yes- Integrated into central air heating system | 59 | `QID19` | MATCH |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 1 | Click to write Scale Point 1 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 4 | Click to write Scale Point 4 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 4 | Click to write Scale Point 4 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 3 | Click to write Scale Point 3 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 3 | Click to write Scale Point 3 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 5 | Click to write Scale Point 5 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | Click to write Scale Point 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Click to write Scale Point 1 | Click to write Scale Point 1 | 67 | `QID195_1` | PLACEHOLDER |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Click to write Scale Point 1 | Click to write Scale Point 1 | 68 | `QID195_2` | PLACEHOLDER |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Click to write Scale Point 1 | Click to write Scale Point 1 | 69 | `QID195_3` | PLACEHOLDER |
| 39 | Intervention — Improve heating/cooling system(s) | Click to write Scale Point 1 | Click to write Scale Point 1 | 70 | `QID195_4` | PLACEHOLDER |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Click to write Scale Point 1 | Click to write Scale Point 1 | 71 | `QID195_5` | PLACEHOLDER |
| 41 | Intervention — Replace well/septic | Click to write Scale Point 1 | Click to write Scale Point 1 | 72 | `QID195_6` | PLACEHOLDER |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | Click to write Scale Point 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 74 | `QID195_8` | MATCH |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Click to write Scale Point 1 | Click to write Scale Point 1 | 75 | `QID195_9` | PLACEHOLDER |
| 45 | Intervention — Trim trees | Click to write Scale Point 1 | Click to write Scale Point 1 | 76 | `QID195_10` | PLACEHOLDER |
| 46 | Intervention — Improved drainage | Click to write Scale Point 1 | Click to write Scale Point 1 | 77 | `QID195_11` | PLACEHOLDER |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | Weekly | 84 | `QID124_1` | MATCH |
| 48 | Experience — In case of flooding, received help for cleaning | Biweekly | Biweekly | 85 | `QID124_2` | MATCH |
| 49 | Experience — Extreme heat in recent years | Daily | Daily | 86 | `QID124_3` | MATCH |
| 50 | Experience — Changing your kids' school due to moving | Biweekly | Biweekly | 87 | `QID124_4` | MATCH |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Weekly | Weekly | 88 | `QID124_5` | MATCH |
| 52 | Experience — Losing home owners insurance due to age of home | Biweekly | Biweekly | 89 | `QID124_6` | MATCH |
| 53 | Experience — Well drying up | Biweekly | Biweekly | 90 | `QID124_7` | MATCH |
| 54 | Experience — A problem with pests in your home | Weekly | Weekly | 91 | `QID124_8` | MATCH |
| 55 | Experience — A problem with water leaks | Weekly | Weekly | 92 | `QID124_9` | MATCH |
| 56 | Experience — A problem with loose animals | Weekly | Weekly | 93 | `QID124_10` | MATCH |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | Yes | 133 | `QID211` | MATCH |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | No | 134 | `QID219` | MATCH |
| 59 | What is the highest level of education you have completed? | less than high school | less than high school | 142 | `QID178` | MATCH |
| 60 | Which best describes your employment status? | Retired | Retired | 143 | `QID176` | MATCH |

## 6. `R_5241irqeSjBwQi1` — 7171 Pembroke Street

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_5241irqeSjBwQi1.png`

> **UNVERIFIED** — no row for this ResponseId in the April 15 export (see finding F2, coverage gap).

## 7. `R_53V7a6BGdQkzzSd` — 7160 Pembroke Street

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_53V7a6BGdQkzzSd.png`

> **UNVERIFIED** — no row for this ResponseId in the April 15 export (see finding F2, coverage gap).

## 8. `R_5BmauNbh58cXIzf` — 6280 Dennison

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_5BmauNbh58cXIzf.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | Rarely or Never | 123 | `RespIll` | MATCH |
| 2 | How often does anyone in your home have asthma symptoms? | Seasonally | Seasonally | 122 | `asthma` | MATCH |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | Rarely or Never | 125 | `wheeze` | MATCH |
| 4 | How often does anyone in your home experience headaches? | Seasonally | Seasonally | 120 | `Headache` | MATCH |
| 5 | How often do you feel tired or fatigued in your home? | weekly | weekly | 124 | `Tired` | MATCH |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | No | 132 | `Hospital Respiratory` | MATCH |
| 7 | Evidence of mold in any area of the home? | Yes | Bathroom | 108 | `Mold` | DIFFERENT |
| 8 | Water leakage — Roof | none | none | 110 | `Leakage 2_1` | MATCH |
| 9 | Water leakage — Walls | none | none | 111 | `Leakage 2_2` | MATCH |
| 10 | Water leakage — Windows | none | none | 112 | `Leakage 2_3` | MATCH |
| 11 | Water leakage — Floor | none | none | 113 | `Leakage 2_4` | MATCH |
| 12 | Cooling system — Central AC | Don't know/Not applicable | Don't know/Not applicable | 100 | `Cooling System _1` | MATCH |
| 13 | Cooling system — Window unit | less than 10 years | less than 10 years | 101 | `Cooling System _2` | MATCH |
| 14 | Cooling system — Fan only | Don't know/Not applicable | Don't know/Not applicable | 102 | `Cooling System _3` | MATCH |
| 15 | Cooling system — No cooling | less than 10 years | less than 10 years | 103 | `Cooling System _4` | MATCH |
| 16 | Cooking fuel / method | electric cooktops | electric cooktops | 106 | `Cooking` | MATCH |
| 17 | When was your house built? | Click to write Choice 5 | Click to write Choice 5 | 39 | `QID192` | PLACEHOLDER |
| 18 | What type of house do you live in? | Single Wide Mobile Home | Single Wide Mobile Home | 40 | `QID128` | MATCH |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Fair- Some repairs needed. | Fair- Some repairs needed. | 55 | `QID141` | MATCH |
| 20 | What is your current housing ownership status? | Renter | Renter | 24 | `Ownership` | MATCH |
| 21 | How long have you lived in High Ridge Estates? (years) | 2months | 2months | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Concrete | Concrete | 44 | `QID47` | MATCH |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 4 | Click to write Choice 4 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Don't know | Don't know | 56 | `QID21` | MATCH |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | Don't know | Don't know | 57 | `QID194` | MATCH |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 4 | Click to write Choice 4 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes- Integrated into central air heating system,Click to write Choice 5,Click to write Choice 6 | Yes- Integrated into central air heating system,Click to write Choice 5,Click to write Choice 6 | 59 | `QID19` | PLACEHOLDER |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 3 | Click to write Scale Point 3 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 3 | Click to write Scale Point 3 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 3 | Click to write Scale Point 3 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 3 | Click to write Scale Point 3 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 1 | Click to write Scale Point 1 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 3 | Click to write Scale Point 3 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | Click to write Scale Point 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 67 | `QID195_1` | MATCH |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 68 | `QID195_2` | MATCH |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Nature reserves and preserves | Nature reserves and preserves | 69 | `QID195_3` | MATCH |
| 39 | Intervention — Improve heating/cooling system(s) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 70 | `QID195_4` | MATCH |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 71 | `QID195_5` | MATCH |
| 41 | Intervention — Replace well/septic | Click to write Scale Point 1 | Click to write Scale Point 1 | 72 | `QID195_6` | PLACEHOLDER |
| 42 | Intervention — Connect to city water through CCUA | Nature reserves and preserves | Nature reserves and preserves | 73 | `QID195_7` | MATCH |
| 43 | Intervention — Add a fence for safety | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 74 | `QID195_8` | MATCH |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Click to write Scale Point 1 | Click to write Scale Point 1 | 75 | `QID195_9` | PLACEHOLDER |
| 45 | Intervention — Trim trees | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 76 | `QID195_10` | MATCH |
| 46 | Intervention — Improved drainage | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 77 | `QID195_11` | MATCH |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | Weekly | 84 | `QID124_1` | MATCH |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | Weekly | 85 | `QID124_2` | MATCH |
| 49 | Experience — Extreme heat in recent years | Weekly | Weekly | 86 | `QID124_3` | MATCH |
| 50 | Experience — Changing your kids' school due to moving | Biweekly | Biweekly | 87 | `QID124_4` | MATCH |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Weekly | Weekly | 88 | `QID124_5` | MATCH |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | Weekly | 89 | `QID124_6` | MATCH |
| 53 | Experience — Well drying up | Weekly | Weekly | 90 | `QID124_7` | MATCH |
| 54 | Experience — A problem with pests in your home | Daily | Daily | 91 | `QID124_8` | MATCH |
| 55 | Experience — A problem with water leaks | Weekly | Weekly | 92 | `QID124_9` | MATCH |
| 56 | Experience — A problem with loose animals | Daily | Daily | 93 | `QID124_10` | MATCH |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | Yes | 133 | `QID211` | MATCH |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | Not Sure | Not Sure | 134 | `QID219` | MATCH |
| 59 | What is the highest level of education you have completed? | High school diploma or equivalent | High school diploma or equivalent | 142 | `QID178` | MATCH |
| 60 | Which best describes your employment status? | Employed- Full time | Employed- Full time | 143 | `QID176` | MATCH |

## 9. `R_5CxQduTse6FT7Z4` — 7156 Duke Street

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_5CxQduTse6FT7Z4.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | Rarely or Never | 123 | `RespIll` | MATCH |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | Rarely or Never | 122 | `asthma` | MATCH |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | Rarely or Never | 125 | `wheeze` | MATCH |
| 4 | How often does anyone in your home experience headaches? | Rarely or Never | Rarely or Never | 120 | `Headache` | MATCH |
| 5 | How often do you feel tired or fatigued in your home? | Rarely or Never | Rarely or Never | 124 | `Tired` | MATCH |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | No | 132 | `Hospital Respiratory` | MATCH |
| 7 | Evidence of mold in any area of the home? | Yes | Other: | 108 | `Mold` | DIFFERENT |
| 8 | Water leakage — Roof | none | none | 110 | `Leakage 2_1` | MATCH |
| 9 | Water leakage — Walls | none | none | 111 | `Leakage 2_2` | MATCH |
| 10 | Water leakage — Windows | none | none | 112 | `Leakage 2_3` | MATCH |
| 11 | Water leakage — Floor | less than one week | less than one week | 113 | `Leakage 2_4` | MATCH |
| 12 | Cooling system — Central AC | less than 10 years | less than 10 years | 100 | `Cooling System _1` | MATCH |
| 13 | Cooling system — Window unit | Don't know/Not applicable | Don't know/Not applicable | 101 | `Cooling System _2` | MATCH |
| 14 | Cooling system — Fan only | Don't know/Not applicable | Don't know/Not applicable | 102 | `Cooling System _3` | MATCH |
| 15 | Cooling system — No cooling | less than 10 years | less than 10 years | 103 | `Cooling System _4` | MATCH |
| 16 | Cooking fuel / method | electric cooktops | electric cooktops | 106 | `Cooking` | MATCH |
| 17 | When was your house built? | Click to write Choice 5 | Click to write Choice 5 | 39 | `QID192` | PLACEHOLDER |
| 18 | What type of house do you live in? | House built on site | House built on site | 40 | `QID128` | MATCH |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Click to write Choice 5 | Click to write Choice 5 | 55 | `QID141` | PLACEHOLDER |
| 20 | What is your current housing ownership status? | Renter | Renter | 24 | `Ownership` | MATCH |
| 21 | How long have you lived in High Ridge Estates? (years) | 0 | 0 | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Concrete | Concrete | 44 | `QID47` | MATCH |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 4 | Click to write Choice 4 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | More than 6 months | More than 6 months | 56 | `QID21` | MATCH |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | More than 6 months | More than 6 months | 57 | `QID194` | MATCH |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 3 | Click to write Choice 3 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes - Portable (Which Room(s)) | Yes - Portable (Which Room(s)) | 59 | `QID19` | MATCH |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 1 | Click to write Scale Point 1 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 4 | Click to write Scale Point 4 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 4 | Click to write Scale Point 4 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 5 | Click to write Scale Point 5 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 1 | Click to write Scale Point 1 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 3 | Click to write Scale Point 3 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | Click to write Scale Point 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | Click to write Scale Point 1 | Click to write Scale Point 1 | 36 | `QID181_8` | PLACEHOLDER |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 67 | `QID195_1` | MATCH |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 68 | `QID195_2` | MATCH |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 69 | `QID195_3` | MATCH |
| 39 | Intervention — Improve heating/cooling system(s) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 70 | `QID195_4` | MATCH |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 71 | `QID195_5` | MATCH |
| 41 | Intervention — Replace well/septic | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 72 | `QID195_6` | MATCH |
| 42 | Intervention — Connect to city water through CCUA | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 73 | `QID195_7` | MATCH |
| 43 | Intervention — Add a fence for safety | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 74 | `QID195_8` | MATCH |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Click to write Scale Point 1 | Click to write Scale Point 1 | 75 | `QID195_9` | PLACEHOLDER |
| 45 | Intervention — Trim trees | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 76 | `QID195_10` | MATCH |
| 46 | Intervention — Improved drainage | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 77 | `QID195_11` | MATCH |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | Weekly | 84 | `QID124_1` | MATCH |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | Weekly | 85 | `QID124_2` | MATCH |
| 49 | Experience — Extreme heat in recent years | Daily | Daily | 86 | `QID124_3` | MATCH |
| 50 | Experience — Changing your kids' school due to moving | Daily | Daily | 87 | `QID124_4` | MATCH |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Weekly | Weekly | 88 | `QID124_5` | MATCH |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | Weekly | 89 | `QID124_6` | MATCH |
| 53 | Experience — Well drying up | Biweekly | Biweekly | 90 | `QID124_7` | MATCH |
| 54 | Experience — A problem with pests in your home | Weekly | Weekly | 91 | `QID124_8` | MATCH |
| 55 | Experience — A problem with water leaks | Weekly | Weekly | 92 | `QID124_9` | MATCH |
| 56 | Experience — A problem with loose animals | Weekly | Weekly | 93 | `QID124_10` | MATCH |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | Yes | 133 | `QID211` | MATCH |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | No | 134 | `QID219` | MATCH |
| 59 | What is the highest level of education you have completed? | Graduate Degree | Graduate Degree | 142 | `QID178` | MATCH |
| 60 | Which best describes your employment status? | Employed- Full time | Employed- Full time | 143 | `QID176` | MATCH |

## 10. `R_5TtaBRz99nWhzm1` — 7173 Duke Street

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_5TtaBRz99nWhzm1.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | weekly | weekly | 123 | `RespIll` | MATCH |
| 2 | How often does anyone in your home have asthma symptoms? | Seasonally | Seasonally | 122 | `asthma` | MATCH |
| 3 | How often does anyone in your home wheeze? | Monthly | Monthly | 125 | `wheeze` | MATCH |
| 4 | How often does anyone in your home experience headaches? | Rarely or Never | Rarely or Never | 120 | `Headache` | MATCH |
| 5 | How often do you feel tired or fatigued in your home? | weekly | weekly | 124 | `Tired` | MATCH |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | — | 132 | `Hospital Respiratory` | DIFFERENT |
| 7 | Evidence of mold in any area of the home? | No | — | 108 | `Mold` | DIFFERENT |
| 8 | Water leakage — Roof | none | none | 110 | `Leakage 2_1` | MATCH |
| 9 | Water leakage — Walls | none | none | 111 | `Leakage 2_2` | MATCH |
| 10 | Water leakage — Windows | none | none | 112 | `Leakage 2_3` | MATCH |
| 11 | Water leakage — Floor | none | none | 113 | `Leakage 2_4` | MATCH |
| 12 | Cooling system — Central AC | less than 10 years | less than 10 years | 100 | `Cooling System _1` | MATCH |
| 13 | Cooling system — Window unit | nan | — | 101 | `Cooling System _2` | DIFFERENT |
| 14 | Cooling system — Fan only | 10 to 15 years | 10 to 15 years | 102 | `Cooling System _3` | MATCH |
| 15 | Cooling system — No cooling | nan | — | 103 | `Cooling System _4` | DIFFERENT |
| 16 | Cooking fuel / method | electric cooktops | electric cooktops | 106 | `Cooking` | MATCH |
| 17 | When was your house built? | Built 1960–1979 | Built 1960–1979 | 39 | `QID192` | MATCH |
| 18 | What type of house do you live in? | Double Wide Mobile Home | Double Wide Mobile Home | 40 | `QID128` | MATCH |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Good- Minor repairs needed. | Good- Minor repairs needed. | 55 | `QID141` | MATCH |
| 20 | What is your current housing ownership status? | Owner | Owner | 24 | `Ownership` | MATCH |
| 21 | How long have you lived in High Ridge Estates? (years) | 37 | 37 | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | Others | 44 | `QID47` | MATCH |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | Click to write Choice 3 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Less than 6 months | Less than 6 months | 56 | `QID21` | MATCH |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | Don't know | Don't know | 57 | `QID194` | MATCH |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 5 | Click to write Choice 5 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes- Integrated into central air heating system,Click to write Choice 6,Click to write Choice 7 | Yes- Integrated into central air heating system,Click to write Choice 6,Click to write Choice 7 | 59 | `QID19` | PLACEHOLDER |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 4 | Click to write Scale Point 4 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 4 | Click to write Scale Point 4 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 5 | Click to write Scale Point 5 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 3 | Click to write Scale Point 3 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 5 | Click to write Scale Point 5 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 5 | Click to write Scale Point 5 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | Click to write Scale Point 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 67 | `QID195_1` | MATCH |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 68 | `QID195_2` | MATCH |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Click to write Scale Point 1 | Click to write Scale Point 1 | 69 | `QID195_3` | PLACEHOLDER |
| 39 | Intervention — Improve heating/cooling system(s) | Click to write Scale Point 1 | Click to write Scale Point 1 | 70 | `QID195_4` | PLACEHOLDER |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Click to write Scale Point 1 | Click to write Scale Point 1 | 71 | `QID195_5` | PLACEHOLDER |
| 41 | Intervention — Replace well/septic | Click to write Scale Point 1 | Click to write Scale Point 1 | 72 | `QID195_6` | PLACEHOLDER |
| 42 | Intervention — Connect to city water through CCUA | — | — | 73 | `QID195_7` | EMPTY-BOTH |
| 43 | Intervention — Add a fence for safety | Click to write Scale Point 1 | Click to write Scale Point 1 | 74 | `QID195_8` | PLACEHOLDER |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Click to write Scale Point 1 | Click to write Scale Point 1 | 75 | `QID195_9` | PLACEHOLDER |
| 45 | Intervention — Trim trees | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 76 | `QID195_10` | MATCH |
| 46 | Intervention — Improved drainage | Click to write Scale Point 1 | Click to write Scale Point 1 | 77 | `QID195_11` | PLACEHOLDER |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | Weekly | 84 | `QID124_1` | MATCH |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | Weekly | 85 | `QID124_2` | MATCH |
| 49 | Experience — Extreme heat in recent years | Daily | Daily | 86 | `QID124_3` | MATCH |
| 50 | Experience — Changing your kids' school due to moving | Biweekly | Biweekly | 87 | `QID124_4` | MATCH |
| 51 | Experience — Calling law enforcement because of problem with neighbors | — | — | 88 | `QID124_5` | EMPTY-BOTH |
| 52 | Experience — Losing home owners insurance due to age of home | Daily | Daily | 89 | `QID124_6` | MATCH |
| 53 | Experience — Well drying up | Weekly | Weekly | 90 | `QID124_7` | MATCH |
| 54 | Experience — A problem with pests in your home | Weekly | Weekly | 91 | `QID124_8` | MATCH |
| 55 | Experience — A problem with water leaks | Weekly | Weekly | 92 | `QID124_9` | MATCH |
| 56 | Experience — A problem with loose animals | Weekly | Weekly | 93 | `QID124_10` | MATCH |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | Yes | 133 | `QID211` | MATCH |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | Name the problem | Name the problem | 134 | `QID219` | MATCH |
| 59 | What is the highest level of education you have completed? | High school diploma or equivalent | High school diploma or equivalent | 142 | `QID178` | MATCH |
| 60 | Which best describes your employment status? | Retired | Retired | 143 | `QID176` | MATCH |

## 11. `R_5tJl6j6gNRyLVMe` — 6220 Colgate Rd

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_5tJl6j6gNRyLVMe.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | Rarely or Never | 123 | `RespIll` | MATCH |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | Rarely or Never | 122 | `asthma` | MATCH |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | Rarely or Never | 125 | `wheeze` | MATCH |
| 4 | How often does anyone in your home experience headaches? | Rarely or Never | Rarely or Never | 120 | `Headache` | MATCH |
| 5 | How often do you feel tired or fatigued in your home? | Rarely or Never | Rarely or Never | 124 | `Tired` | MATCH |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | No | 132 | `Hospital Respiratory` | MATCH |
| 7 | Evidence of mold in any area of the home? | Yes | Other: | 108 | `Mold` | DIFFERENT |
| 8 | Water leakage — Roof | none | none | 110 | `Leakage 2_1` | MATCH |
| 9 | Water leakage — Walls | none | none | 111 | `Leakage 2_2` | MATCH |
| 10 | Water leakage — Windows | none | none | 112 | `Leakage 2_3` | MATCH |
| 11 | Water leakage — Floor | less than one week | less than one week | 113 | `Leakage 2_4` | MATCH |
| 12 | Cooling system — Central AC | nan | — | 100 | `Cooling System _1` | DIFFERENT |
| 13 | Cooling system — Window unit | less than 10 years | less than 10 years | 101 | `Cooling System _2` | MATCH |
| 14 | Cooling system — Fan only | Don't know/Not applicable | Don't know/Not applicable | 102 | `Cooling System _3` | MATCH |
| 15 | Cooling system — No cooling | nan | — | 103 | `Cooling System _4` | DIFFERENT |
| 16 | Cooking fuel / method | electric cooktops | electric cooktops | 106 | `Cooking` | MATCH |
| 17 | When was your house built? | Built 1980–1999 | Built 1980–1999 | 39 | `QID192` | MATCH |
| 18 | What type of house do you live in? | Double Wide Mobile Home | Double Wide Mobile Home | 40 | `QID128` | MATCH |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Good- Minor repairs needed. | Good- Minor repairs needed. | 55 | `QID141` | MATCH |
| 20 | What is your current housing ownership status? | Other | Click to write Choice 4 | 24 | `Ownership` | DIFFERENT |
| 21 | How long have you lived in High Ridge Estates? (years) | 6 mo | 6 mo | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | Others | 44 | `QID47` | MATCH |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 4 | Click to write Choice 4 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Less than 6 months | Less than 6 months | 56 | `QID21` | MATCH |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | More than 6 months | More than 6 months | 57 | `QID194` | MATCH |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 3 | Click to write Choice 3 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes- Integrated into central air heating system,No | Yes- Integrated into central air heating system,No | 59 | `QID19` | MATCH |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 3 | Click to write Scale Point 3 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 1 | Click to write Scale Point 1 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 3 | Click to write Scale Point 3 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 3 | Click to write Scale Point 3 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 1 | Click to write Scale Point 1 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 4 | Click to write Scale Point 4 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | Click to write Scale Point 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Click to write Scale Point 1 | Click to write Scale Point 1 | 67 | `QID195_1` | PLACEHOLDER |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Click to write Scale Point 1 | Click to write Scale Point 1 | 68 | `QID195_2` | PLACEHOLDER |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Click to write Scale Point 1 | Click to write Scale Point 1 | 69 | `QID195_3` | PLACEHOLDER |
| 39 | Intervention — Improve heating/cooling system(s) | Click to write Scale Point 1 | Click to write Scale Point 1 | 70 | `QID195_4` | PLACEHOLDER |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Click to write Scale Point 1 | Click to write Scale Point 1 | 71 | `QID195_5` | PLACEHOLDER |
| 41 | Intervention — Replace well/septic | Click to write Scale Point 1 | Click to write Scale Point 1 | 72 | `QID195_6` | PLACEHOLDER |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | Click to write Scale Point 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Click to write Scale Point 1 | Click to write Scale Point 1 | 74 | `QID195_8` | PLACEHOLDER |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Nature reserves and preserves | Nature reserves and preserves | 75 | `QID195_9` | MATCH |
| 45 | Intervention — Trim trees | Nature reserves and preserves | Nature reserves and preserves | 76 | `QID195_10` | MATCH |
| 46 | Intervention — Improved drainage | Click to write Scale Point 1 | Click to write Scale Point 1 | 77 | `QID195_11` | PLACEHOLDER |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | Weekly | 84 | `QID124_1` | MATCH |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | Weekly | 85 | `QID124_2` | MATCH |
| 49 | Experience — Extreme heat in recent years | Daily | Daily | 86 | `QID124_3` | MATCH |
| 50 | Experience — Changing your kids' school due to moving | Weekly | Weekly | 87 | `QID124_4` | MATCH |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Weekly | Weekly | 88 | `QID124_5` | MATCH |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | Weekly | 89 | `QID124_6` | MATCH |
| 53 | Experience — Well drying up | Weekly | Weekly | 90 | `QID124_7` | MATCH |
| 54 | Experience — A problem with pests in your home | Weekly | Weekly | 91 | `QID124_8` | MATCH |
| 55 | Experience — A problem with water leaks | Weekly | Weekly | 92 | `QID124_9` | MATCH |
| 56 | Experience — A problem with loose animals | Daily | Daily | 93 | `QID124_10` | MATCH |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | Yes | 133 | `QID211` | MATCH |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | No | 134 | `QID219` | MATCH |
| 59 | What is the highest level of education you have completed? | High school diploma or equivalent | High school diploma or equivalent | 142 | `QID178` | MATCH |
| 60 | Which best describes your employment status? | Employed - Part time | Employed - Part time | 143 | `QID176` | MATCH |

## 12. `R_6SGNzs6svx7pBbb` — Dennison

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_6SGNzs6svx7pBbb.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | Rarely or Never | 123 | `RespIll` | MATCH |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | Rarely or Never | 122 | `asthma` | MATCH |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | Rarely or Never | 125 | `wheeze` | MATCH |
| 4 | How often does anyone in your home experience headaches? | Monthly | Monthly | 120 | `Headache` | MATCH |
| 5 | How often do you feel tired or fatigued in your home? | Rarely or Never | Rarely or Never | 124 | `Tired` | MATCH |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | No | 132 | `Hospital Respiratory` | MATCH |
| 7 | Evidence of mold in any area of the home? | Yes | Other: | 108 | `Mold` | DIFFERENT |
| 8 | Water leakage — Roof | none | none | 110 | `Leakage 2_1` | MATCH |
| 9 | Water leakage — Walls | none | none | 111 | `Leakage 2_2` | MATCH |
| 10 | Water leakage — Windows | not fixed | not fixed | 112 | `Leakage 2_3` | MATCH |
| 11 | Water leakage — Floor | not fixed | not fixed | 113 | `Leakage 2_4` | MATCH |
| 12 | Cooling system — Central AC | More than 15 years | More than 15 years | 100 | `Cooling System _1` | MATCH |
| 13 | Cooling system — Window unit | less than 10 years | less than 10 years | 101 | `Cooling System _2` | MATCH |
| 14 | Cooling system — Fan only | less than 10 years | less than 10 years | 102 | `Cooling System _3` | MATCH |
| 15 | Cooling system — No cooling | nan | — | 103 | `Cooling System _4` | DIFFERENT |
| 16 | Cooking fuel / method | electric cooktops | electric cooktops | 106 | `Cooking` | MATCH |
| 17 | When was your house built? | Built 1960–1979 | Built 1960–1979 | 39 | `QID192` | MATCH |
| 18 | What type of house do you live in? | Double Wide Mobile Home | Double Wide Mobile Home | 40 | `QID128` | MATCH |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Poor- Major repairs needed. | Poor- Major repairs needed. | 55 | `QID141` | MATCH |
| 20 | What is your current housing ownership status? | Owner | Owner | 24 | `Ownership` | MATCH |
| 21 | How long have you lived in High Ridge Estates? (years) | 17 years | 17 years | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | Others | 44 | `QID47` | MATCH |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | Click to write Choice 3 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | More than 6 months | More than 6 months | 56 | `QID21` | MATCH |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | More than 6 months | More than 6 months | 57 | `QID194` | MATCH |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | — | — | 58 | `QID17` | EMPTY-BOTH |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes- Integrated into central air heating system,No,Click to write Choice 6 | Yes- Integrated into central air heating system,No,Click to write Choice 6 | 59 | `QID19` | PLACEHOLDER |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 4 | Click to write Scale Point 4 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 3 | Click to write Scale Point 3 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 3 | Click to write Scale Point 3 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 3 | Click to write Scale Point 3 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 3 | Click to write Scale Point 3 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 3 | Click to write Scale Point 3 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | Click to write Scale Point 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 67 | `QID195_1` | MATCH |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 68 | `QID195_2` | MATCH |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Nature reserves and preserves | Nature reserves and preserves | 69 | `QID195_3` | MATCH |
| 39 | Intervention — Improve heating/cooling system(s) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 70 | `QID195_4` | MATCH |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 71 | `QID195_5` | MATCH |
| 41 | Intervention — Replace well/septic | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 72 | `QID195_6` | MATCH |
| 42 | Intervention — Connect to city water through CCUA | Nature reserves and preserves | Nature reserves and preserves | 73 | `QID195_7` | MATCH |
| 43 | Intervention — Add a fence for safety | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 74 | `QID195_8` | MATCH |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 75 | `QID195_9` | MATCH |
| 45 | Intervention — Trim trees | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 76 | `QID195_10` | MATCH |
| 46 | Intervention — Improved drainage | Nature reserves and preserves | Nature reserves and preserves | 77 | `QID195_11` | MATCH |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | Weekly | 84 | `QID124_1` | MATCH |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | Weekly | 85 | `QID124_2` | MATCH |
| 49 | Experience — Extreme heat in recent years | Daily | Daily | 86 | `QID124_3` | MATCH |
| 50 | Experience — Changing your kids' school due to moving | Weekly | Weekly | 87 | `QID124_4` | MATCH |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Weekly | Weekly | 88 | `QID124_5` | MATCH |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | Weekly | 89 | `QID124_6` | MATCH |
| 53 | Experience — Well drying up | Daily | Daily | 90 | `QID124_7` | MATCH |
| 54 | Experience — A problem with pests in your home | Daily | Daily | 91 | `QID124_8` | MATCH |
| 55 | Experience — A problem with water leaks | Weekly | Weekly | 92 | `QID124_9` | MATCH |
| 56 | Experience — A problem with loose animals | Weekly | Weekly | 93 | `QID124_10` | MATCH |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | Yes | 133 | `QID211` | MATCH |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | No | 134 | `QID219` | MATCH |
| 59 | What is the highest level of education you have completed? | High school diploma or equivalent | High school diploma or equivalent | 142 | `QID178` | MATCH |
| 60 | Which best describes your employment status? | Retired | Retired | 143 | `QID176` | MATCH |

## 13. `R_6s0PVusMDUucFQY` — Dennison

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_6s0PVusMDUucFQY.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Seasonally | Seasonally | 123 | `RespIll` | MATCH |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | Rarely or Never | 122 | `asthma` | MATCH |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | Rarely or Never | 125 | `wheeze` | MATCH |
| 4 | How often does anyone in your home experience headaches? | Monthly | Monthly | 120 | `Headache` | MATCH |
| 5 | How often do you feel tired or fatigued in your home? | Rarely or Never | Rarely or Never | 124 | `Tired` | MATCH |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | yes | Yes, Doctor visits for allergy. | 132 | `Hospital Respiratory` | DIFFERENT |
| 7 | Evidence of mold in any area of the home? | No | — | 108 | `Mold` | DIFFERENT |
| 8 | Water leakage — Roof | less than one week | less than one week | 110 | `Leakage 2_1` | MATCH |
| 9 | Water leakage — Walls | none | none | 111 | `Leakage 2_2` | MATCH |
| 10 | Water leakage — Windows | less than one week | less than one week | 112 | `Leakage 2_3` | MATCH |
| 11 | Water leakage — Floor | less than one week | less than one week | 113 | `Leakage 2_4` | MATCH |
| 12 | Cooling system — Central AC | Don't know/Not applicable | Don't know/Not applicable | 100 | `Cooling System _1` | MATCH |
| 13 | Cooling system — Window unit | less than 10 years | less than 10 years | 101 | `Cooling System _2` | MATCH |
| 14 | Cooling system — Fan only | Don't know/Not applicable | Don't know/Not applicable | 102 | `Cooling System _3` | MATCH |
| 15 | Cooling system — No cooling | nan | — | 103 | `Cooling System _4` | DIFFERENT |
| 16 | Cooking fuel / method | Other: | Other: | 106 | `Cooking` | MATCH |
| 17 | When was your house built? | Click to write Choice 5 | Click to write Choice 5 | 39 | `QID192` | PLACEHOLDER |
| 18 | What type of house do you live in? | Single Wide Mobile Home | Single Wide Mobile Home | 40 | `QID128` | MATCH |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Poor- Major repairs needed. | Poor- Major repairs needed. | 55 | `QID141` | MATCH |
| 20 | What is your current housing ownership status? | Renter | Renter | 24 | `Ownership` | MATCH |
| 21 | How long have you lived in High Ridge Estates? (years) | 5 years | 5 years | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Don't know | Don't know | 44 | `QID47` | MATCH |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | Click to write Choice 3 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | More than 6 months | More than 6 months | 56 | `QID21` | MATCH |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | Don't know | Don't know | 57 | `QID194` | MATCH |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 3 | Click to write Choice 3 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes - Portable (Which Room(s)),Yes- Integrated into central air heating system,Don’t Know | Yes - Portable (Which Room(s)),Yes- Integrated into central air heating system,Don’t Know | 59 | `QID19` | MATCH |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 4 | Click to write Scale Point 4 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 4 | Click to write Scale Point 4 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 4 | Click to write Scale Point 4 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 3 | Click to write Scale Point 3 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 3 | Click to write Scale Point 3 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 3 | Click to write Scale Point 3 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | Click to write Scale Point 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | Click to write Scale Point 1 | Click to write Scale Point 1 | 36 | `QID181_8` | PLACEHOLDER |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Nature reserves and preserves | Nature reserves and preserves | 67 | `QID195_1` | MATCH |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Nature reserves and preserves | Nature reserves and preserves | 68 | `QID195_2` | MATCH |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Nature reserves and preserves | Nature reserves and preserves | 69 | `QID195_3` | MATCH |
| 39 | Intervention — Improve heating/cooling system(s) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 70 | `QID195_4` | MATCH |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 71 | `QID195_5` | MATCH |
| 41 | Intervention — Replace well/septic | Nature reserves and preserves | Nature reserves and preserves | 72 | `QID195_6` | MATCH |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | Click to write Scale Point 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 74 | `QID195_8` | MATCH |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 75 | `QID195_9` | MATCH |
| 45 | Intervention — Trim trees | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 76 | `QID195_10` | MATCH |
| 46 | Intervention — Improved drainage | Nature reserves and preserves | Nature reserves and preserves | 77 | `QID195_11` | MATCH |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | Weekly | 84 | `QID124_1` | MATCH |
| 48 | Experience — In case of flooding, received help for cleaning | — | — | 85 | `QID124_2` | EMPTY-BOTH |
| 49 | Experience — Extreme heat in recent years | Daily | Daily | 86 | `QID124_3` | MATCH |
| 50 | Experience — Changing your kids' school due to moving | Weekly | Weekly | 87 | `QID124_4` | MATCH |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Daily | Daily | 88 | `QID124_5` | MATCH |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | Weekly | 89 | `QID124_6` | MATCH |
| 53 | Experience — Well drying up | Weekly | Weekly | 90 | `QID124_7` | MATCH |
| 54 | Experience — A problem with pests in your home | Biweekly | Biweekly | 91 | `QID124_8` | MATCH |
| 55 | Experience — A problem with water leaks | Daily | Daily | 92 | `QID124_9` | MATCH |
| 56 | Experience — A problem with loose animals | Daily | Daily | 93 | `QID124_10` | MATCH |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | Yes | 133 | `QID211` | MATCH |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | No | 134 | `QID219` | MATCH |
| 59 | What is the highest level of education you have completed? | High school diploma or equivalent | High school diploma or equivalent | 142 | `QID178` | MATCH |
| 60 | Which best describes your employment status? | Employed - Part time | Employed - Part time | 143 | `QID176` | MATCH |

## 14. `R_6xzTr24XxYm8KC4` — 7276 Temple

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_6xzTr24XxYm8KC4.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | Rarely or Never | 123 | `RespIll` | MATCH |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | Rarely or Never | 122 | `asthma` | MATCH |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | Rarely or Never | 125 | `wheeze` | MATCH |
| 4 | How often does anyone in your home experience headaches? | weekly | weekly | 120 | `Headache` | MATCH |
| 5 | How often do you feel tired or fatigued in your home? | weekly | weekly | 124 | `Tired` | MATCH |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | No | 132 | `Hospital Respiratory` | MATCH |
| 7 | Evidence of mold in any area of the home? | Yes | Inner walls/Windows,Other: | 108 | `Mold` | DIFFERENT |
| 8 | Water leakage — Roof | none | none | 110 | `Leakage 2_1` | MATCH |
| 9 | Water leakage — Walls | none | none | 111 | `Leakage 2_2` | MATCH |
| 10 | Water leakage — Windows | none | none | 112 | `Leakage 2_3` | MATCH |
| 11 | Water leakage — Floor | not fixed | not fixed | 113 | `Leakage 2_4` | MATCH |
| 12 | Cooling system — Central AC | More than 15 years | More than 15 years | 100 | `Cooling System _1` | MATCH |
| 13 | Cooling system — Window unit | More than 15 years | More than 15 years | 101 | `Cooling System _2` | MATCH |
| 14 | Cooling system — Fan only | More than 15 years | More than 15 years | 102 | `Cooling System _3` | MATCH |
| 15 | Cooling system — No cooling | Don't know/Not applicable | Don't know/Not applicable | 103 | `Cooling System _4` | MATCH |
| 16 | Cooking fuel / method | gas cooktops,Other: | gas cooktops,Other: | 106 | `Cooking` | MATCH |
| 17 | When was your house built? | Built 2000 or later | Built 2000 or later | 39 | `QID192` | MATCH |
| 18 | What type of house do you live in? | Single Wide Mobile Home | Single Wide Mobile Home | 40 | `QID128` | MATCH |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Poor- Major repairs needed. | Poor- Major repairs needed. | 55 | `QID141` | MATCH |
| 20 | What is your current housing ownership status? | Owner | Owner | 24 | `Ownership` | MATCH |
| 21 | How long have you lived in High Ridge Estates? (years) | 1 | 1 | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Don't know | Don't know | 44 | `QID47` | MATCH |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 4 | Click to write Choice 4 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Don't know | Don't know | 56 | `QID21` | MATCH |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | Click to write Choice 5 | Click to write Choice 5 | 57 | `QID194` | PLACEHOLDER |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 3 | Click to write Choice 3 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Don’t Know,Click to write Choice 6 | Don’t Know,Click to write Choice 6 | 59 | `QID19` | PLACEHOLDER |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 1 | Click to write Scale Point 1 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 5 | Click to write Scale Point 5 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 1 | Click to write Scale Point 1 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 1 | Click to write Scale Point 1 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 1 | Click to write Scale Point 1 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 5 | Click to write Scale Point 5 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | Click to write Scale Point 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | Click to write Scale Point 5 | Click to write Scale Point 5 | 36 | `QID181_8` | PLACEHOLDER |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Nature reserves and preserves | Nature reserves and preserves | 67 | `QID195_1` | MATCH |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 68 | `QID195_2` | MATCH |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Click to write Scale Point 1 | Click to write Scale Point 1 | 69 | `QID195_3` | PLACEHOLDER |
| 39 | Intervention — Improve heating/cooling system(s) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 70 | `QID195_4` | MATCH |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 71 | `QID195_5` | MATCH |
| 41 | Intervention — Replace well/septic | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 72 | `QID195_6` | MATCH |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | Click to write Scale Point 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Nature reserves and preserves | Nature reserves and preserves | 74 | `QID195_8` | MATCH |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Click to write Scale Point 1 | Click to write Scale Point 1 | 75 | `QID195_9` | PLACEHOLDER |
| 45 | Intervention — Trim trees | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 76 | `QID195_10` | MATCH |
| 46 | Intervention — Improved drainage | Nature reserves and preserves | Nature reserves and preserves | 77 | `QID195_11` | MATCH |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | Weekly | 84 | `QID124_1` | MATCH |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | Weekly | 85 | `QID124_2` | MATCH |
| 49 | Experience — Extreme heat in recent years | Daily | Daily | 86 | `QID124_3` | MATCH |
| 50 | Experience — Changing your kids' school due to moving | Daily | Daily | 87 | `QID124_4` | MATCH |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Daily | Daily | 88 | `QID124_5` | MATCH |
| 52 | Experience — Losing home owners insurance due to age of home | Daily | Daily | 89 | `QID124_6` | MATCH |
| 53 | Experience — Well drying up | Weekly | Weekly | 90 | `QID124_7` | MATCH |
| 54 | Experience — A problem with pests in your home | Weekly | Weekly | 91 | `QID124_8` | MATCH |
| 55 | Experience — A problem with water leaks | Weekly | Weekly | 92 | `QID124_9` | MATCH |
| 56 | Experience — A problem with loose animals | Daily | Daily | 93 | `QID124_10` | MATCH |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | Yes | 133 | `QID211` | MATCH |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | No | 134 | `QID219` | MATCH |
| 59 | What is the highest level of education you have completed? | Some college, no degree | Some college, no degree | 142 | `QID178` | MATCH |
| 60 | Which best describes your employment status? | Employed- Full time | Employed- Full time | 143 | `QID176` | MATCH |

## 15. `R_71LqP7xFx71BPsl` — Baylor Ave

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_71LqP7xFx71BPsl.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | Rarely or Never | 123 | `RespIll` | MATCH |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | Rarely or Never | 122 | `asthma` | MATCH |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | Rarely or Never | 125 | `wheeze` | MATCH |
| 4 | How often does anyone in your home experience headaches? | Rarely or Never | Rarely or Never | 120 | `Headache` | MATCH |
| 5 | How often do you feel tired or fatigued in your home? | Rarely or Never | Rarely or Never | 124 | `Tired` | MATCH |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | No | 132 | `Hospital Respiratory` | MATCH |
| 7 | Evidence of mold in any area of the home? | Yes | Inner walls/Windows,Outer walls/Windows | 108 | `Mold` | DIFFERENT |
| 8 | Water leakage — Roof | more than one week | more than one week | 110 | `Leakage 2_1` | MATCH |
| 9 | Water leakage — Walls | none | none | 111 | `Leakage 2_2` | MATCH |
| 10 | Water leakage — Windows | less than one week | less than one week | 112 | `Leakage 2_3` | MATCH |
| 11 | Water leakage — Floor | none | none | 113 | `Leakage 2_4` | MATCH |
| 12 | Cooling system — Central AC | nan | — | 100 | `Cooling System _1` | DIFFERENT |
| 13 | Cooling system — Window unit | less than 10 years | less than 10 years | 101 | `Cooling System _2` | MATCH |
| 14 | Cooling system — Fan only | nan | — | 102 | `Cooling System _3` | DIFFERENT |
| 15 | Cooling system — No cooling | nan | — | 103 | `Cooling System _4` | DIFFERENT |
| 16 | Cooking fuel / method | Other: | Other: | 106 | `Cooking` | MATCH |
| 17 | When was your house built? | Built 2000 or later | Built 2000 or later | 39 | `QID192` | MATCH |
| 18 | What type of house do you live in? | Double Wide Mobile Home | Double Wide Mobile Home | 40 | `QID128` | MATCH |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Fair- Some repairs needed. | Fair- Some repairs needed. | 55 | `QID141` | MATCH |
| 20 | What is your current housing ownership status? | Owner | Owner | 24 | `Ownership` | MATCH |
| 21 | How long have you lived in High Ridge Estates? (years) | 1 | 1 | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | Others | 44 | `QID47` | MATCH |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 4 | Click to write Choice 4 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | More than 6 months | More than 6 months | 56 | `QID21` | MATCH |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | Don't know | Don't know | 57 | `QID194` | MATCH |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 4 | Click to write Choice 4 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes - Portable (Which Room(s)),Yes- Integrated into central air heating system,Don’t Know | Yes - Portable (Which Room(s)),Yes- Integrated into central air heating system,Don’t Know | 59 | `QID19` | MATCH |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 3 | Click to write Scale Point 3 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 2 | Click to write Scale Point 2 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 3 | Click to write Scale Point 3 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 4 | Click to write Scale Point 4 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 3 | Click to write Scale Point 3 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 3 | Click to write Scale Point 3 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 4 | Click to write Scale Point 4 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | Click to write Scale Point 1 | Click to write Scale Point 1 | 36 | `QID181_8` | PLACEHOLDER |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 67 | `QID195_1` | MATCH |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 68 | `QID195_2` | MATCH |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 69 | `QID195_3` | MATCH |
| 39 | Intervention — Improve heating/cooling system(s) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 70 | `QID195_4` | MATCH |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 71 | `QID195_5` | MATCH |
| 41 | Intervention — Replace well/septic | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 72 | `QID195_6` | MATCH |
| 42 | Intervention — Connect to city water through CCUA | Nature reserves and preserves | Nature reserves and preserves | 73 | `QID195_7` | MATCH |
| 43 | Intervention — Add a fence for safety | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 74 | `QID195_8` | MATCH |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 75 | `QID195_9` | MATCH |
| 45 | Intervention — Trim trees | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 76 | `QID195_10` | MATCH |
| 46 | Intervention — Improved drainage | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 77 | `QID195_11` | MATCH |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | Weekly | 84 | `QID124_1` | MATCH |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | Weekly | 85 | `QID124_2` | MATCH |
| 49 | Experience — Extreme heat in recent years | Weekly | Weekly | 86 | `QID124_3` | MATCH |
| 50 | Experience — Changing your kids' school due to moving | Weekly | Weekly | 87 | `QID124_4` | MATCH |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Weekly | Weekly | 88 | `QID124_5` | MATCH |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | Weekly | 89 | `QID124_6` | MATCH |
| 53 | Experience — Well drying up | Weekly | Weekly | 90 | `QID124_7` | MATCH |
| 54 | Experience — A problem with pests in your home | Daily | Daily | 91 | `QID124_8` | MATCH |
| 55 | Experience — A problem with water leaks | Daily | Daily | 92 | `QID124_9` | MATCH |
| 56 | Experience — A problem with loose animals | Daily | Daily | 93 | `QID124_10` | MATCH |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | Yes | 133 | `QID211` | MATCH |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | No | 134 | `QID219` | MATCH |
| 59 | What is the highest level of education you have completed? | High school diploma or equivalent | High school diploma or equivalent | 142 | `QID178` | MATCH |
| 60 | Which best describes your employment status? | Unemployed | Unemployed | 143 | `QID176` | MATCH |

## 16. `R_78TZ7UtnmZU0jKm` — 7201 Notre Dame St

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_78TZ7UtnmZU0jKm.png`

> **UNVERIFIED** — no row for this ResponseId in the April 15 export (see finding F2, coverage gap).

## 17. `R_87qCLdadYRHhw4P` — 6200 Harvard Avenue

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_87qCLdadYRHhw4P.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Yearly | Yearly | 123 | `RespIll` | MATCH |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | Rarely or Never | 122 | `asthma` | MATCH |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | Rarely or Never | 125 | `wheeze` | MATCH |
| 4 | How often does anyone in your home experience headaches? | weekly | weekly | 120 | `Headache` | MATCH |
| 5 | How often do you feel tired or fatigued in your home? | Rarely or Never | Rarely or Never | 124 | `Tired` | MATCH |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | yes | Yes, Others. | 132 | `Hospital Respiratory` | DIFFERENT |
| 7 | Evidence of mold in any area of the home? | Yes | Other: | 108 | `Mold` | DIFFERENT |
| 8 | Water leakage — Roof | none | none | 110 | `Leakage 2_1` | MATCH |
| 9 | Water leakage — Walls | more than one week | more than one week | 111 | `Leakage 2_2` | MATCH |
| 10 | Water leakage — Windows | none | none | 112 | `Leakage 2_3` | MATCH |
| 11 | Water leakage — Floor | none | none | 113 | `Leakage 2_4` | MATCH |
| 12 | Cooling system — Central AC | less than 10 years | less than 10 years | 100 | `Cooling System _1` | MATCH |
| 13 | Cooling system — Window unit | Don't know/Not applicable | Don't know/Not applicable | 101 | `Cooling System _2` | MATCH |
| 14 | Cooling system — Fan only | less than 10 years | less than 10 years | 102 | `Cooling System _3` | MATCH |
| 15 | Cooling system — No cooling | Don't know/Not applicable | Don't know/Not applicable | 103 | `Cooling System _4` | MATCH |
| 16 | Cooking fuel / method | electric cooktops | electric cooktops | 106 | `Cooking` | MATCH |
| 17 | When was your house built? | Click to write Choice 5 | Click to write Choice 5 | 39 | `QID192` | PLACEHOLDER |
| 18 | What type of house do you live in? | House built on site | House built on site | 40 | `QID128` | MATCH |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Good- Minor repairs needed. | Good- Minor repairs needed. | 55 | `QID141` | MATCH |
| 20 | What is your current housing ownership status? | Renter | Renter | 24 | `Ownership` | MATCH |
| 21 | How long have you lived in High Ridge Estates? (years) | 4 years | 4 years | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | Others | 44 | `QID47` | MATCH |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 4 | Click to write Choice 4 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Don't know | Don't know | 56 | `QID21` | MATCH |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | More than 6 months | More than 6 months | 57 | `QID194` | MATCH |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 3 | Click to write Choice 3 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Click to write Choice 7 | Click to write Choice 7 | 59 | `QID19` | PLACEHOLDER |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 1 | Click to write Scale Point 1 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 1 | Click to write Scale Point 1 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 3 | Click to write Scale Point 3 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 1 | Click to write Scale Point 1 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 1 | Click to write Scale Point 1 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 3 | Click to write Scale Point 3 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | Click to write Scale Point 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Click to write Scale Point 1 | Click to write Scale Point 1 | 67 | `QID195_1` | PLACEHOLDER |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Click to write Scale Point 1 | Click to write Scale Point 1 | 68 | `QID195_2` | PLACEHOLDER |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Nature reserves and preserves | Nature reserves and preserves | 69 | `QID195_3` | MATCH |
| 39 | Intervention — Improve heating/cooling system(s) | Click to write Scale Point 1 | Click to write Scale Point 1 | 70 | `QID195_4` | PLACEHOLDER |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Click to write Scale Point 1 | Click to write Scale Point 1 | 71 | `QID195_5` | PLACEHOLDER |
| 41 | Intervention — Replace well/septic | Click to write Scale Point 1 | Click to write Scale Point 1 | 72 | `QID195_6` | PLACEHOLDER |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | Click to write Scale Point 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 74 | `QID195_8` | MATCH |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Click to write Scale Point 1 | Click to write Scale Point 1 | 75 | `QID195_9` | PLACEHOLDER |
| 45 | Intervention — Trim trees | Click to write Scale Point 1 | Click to write Scale Point 1 | 76 | `QID195_10` | PLACEHOLDER |
| 46 | Intervention — Improved drainage | Click to write Scale Point 1 | Click to write Scale Point 1 | 77 | `QID195_11` | PLACEHOLDER |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | Weekly | 84 | `QID124_1` | MATCH |
| 48 | Experience — In case of flooding, received help for cleaning | Biweekly | Biweekly | 85 | `QID124_2` | MATCH |
| 49 | Experience — Extreme heat in recent years | Daily | Daily | 86 | `QID124_3` | MATCH |
| 50 | Experience — Changing your kids' school due to moving | Biweekly | Biweekly | 87 | `QID124_4` | MATCH |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Daily | Daily | 88 | `QID124_5` | MATCH |
| 52 | Experience — Losing home owners insurance due to age of home | Biweekly | Biweekly | 89 | `QID124_6` | MATCH |
| 53 | Experience — Well drying up | Weekly | Weekly | 90 | `QID124_7` | MATCH |
| 54 | Experience — A problem with pests in your home | Daily | Daily | 91 | `QID124_8` | MATCH |
| 55 | Experience — A problem with water leaks | Weekly | Weekly | 92 | `QID124_9` | MATCH |
| 56 | Experience — A problem with loose animals | Daily | Daily | 93 | `QID124_10` | MATCH |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | Yes | 133 | `QID211` | MATCH |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | No | 134 | `QID219` | MATCH |
| 59 | What is the highest level of education you have completed? | Bachelor's Degree | Bachelor's Degree | 142 | `QID178` | MATCH |
| 60 | Which best describes your employment status? | Employed- Full time | Employed- Full time | 143 | `QID176` | MATCH |

## 18. `R_8iSqFy8YDl9Xt1b` — 6397 Cascade Drive

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_8iSqFy8YDl9Xt1b.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | Rarely or Never | 123 | `RespIll` | MATCH |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | Rarely or Never | 122 | `asthma` | MATCH |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | Rarely or Never | 125 | `wheeze` | MATCH |
| 4 | How often does anyone in your home experience headaches? | Rarely or Never | Rarely or Never | 120 | `Headache` | MATCH |
| 5 | How often do you feel tired or fatigued in your home? | Rarely or Never | Rarely or Never | 124 | `Tired` | MATCH |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | No | 132 | `Hospital Respiratory` | MATCH |
| 7 | Evidence of mold in any area of the home? | Yes | Other: | 108 | `Mold` | DIFFERENT |
| 8 | Water leakage — Roof | none | none | 110 | `Leakage 2_1` | MATCH |
| 9 | Water leakage — Walls | none | none | 111 | `Leakage 2_2` | MATCH |
| 10 | Water leakage — Windows | not fixed | not fixed | 112 | `Leakage 2_3` | MATCH |
| 11 | Water leakage — Floor | none | none | 113 | `Leakage 2_4` | MATCH |
| 12 | Cooling system — Central AC | 10 to 15 years | 10 to 15 years | 100 | `Cooling System _1` | MATCH |
| 13 | Cooling system — Window unit | nan | — | 101 | `Cooling System _2` | DIFFERENT |
| 14 | Cooling system — Fan only | nan | — | 102 | `Cooling System _3` | DIFFERENT |
| 15 | Cooling system — No cooling | nan | — | 103 | `Cooling System _4` | DIFFERENT |
| 16 | Cooking fuel / method | gas cooktops | gas cooktops | 106 | `Cooking` | MATCH |
| 17 | When was your house built? | Built 1960–1979 | Built 1960–1979 | 39 | `QID192` | MATCH |
| 18 | What type of house do you live in? | Single Wide Mobile Home | Single Wide Mobile Home | 40 | `QID128` | MATCH |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Good- Minor repairs needed. | Good- Minor repairs needed. | 55 | `QID141` | MATCH |
| 20 | What is your current housing ownership status? | Owner | Owner | 24 | `Ownership` | MATCH |
| 21 | How long have you lived in High Ridge Estates? (years) | 3 years | 3 years | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | Others | 44 | `QID47` | MATCH |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | Click to write Choice 3 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Less than 6 months | Less than 6 months | 56 | `QID21` | MATCH |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | More than 6 months | More than 6 months | 57 | `QID194` | MATCH |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 3 | Click to write Choice 3 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes - Portable (Which Room(s)),Yes- Integrated into central air heating system,Click to write Choice 6 | Yes - Portable (Which Room(s)),Yes- Integrated into central air heating system,Click to write Choice 6 | 59 | `QID19` | PLACEHOLDER |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 1 | Click to write Scale Point 1 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 4 | Click to write Scale Point 4 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 4 | Click to write Scale Point 4 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 4 | Click to write Scale Point 4 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 4 | Click to write Scale Point 4 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 4 | Click to write Scale Point 4 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | Click to write Scale Point 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 67 | `QID195_1` | MATCH |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 68 | `QID195_2` | MATCH |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 69 | `QID195_3` | MATCH |
| 39 | Intervention — Improve heating/cooling system(s) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 70 | `QID195_4` | MATCH |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 71 | `QID195_5` | MATCH |
| 41 | Intervention — Replace well/septic | Click to write Scale Point 1 | Click to write Scale Point 1 | 72 | `QID195_6` | PLACEHOLDER |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | Click to write Scale Point 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Click to write Scale Point 1 | Click to write Scale Point 1 | 74 | `QID195_8` | PLACEHOLDER |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 75 | `QID195_9` | MATCH |
| 45 | Intervention — Trim trees | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 76 | `QID195_10` | MATCH |
| 46 | Intervention — Improved drainage | Click to write Scale Point 1 | Click to write Scale Point 1 | 77 | `QID195_11` | PLACEHOLDER |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | Weekly | 84 | `QID124_1` | MATCH |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | Weekly | 85 | `QID124_2` | MATCH |
| 49 | Experience — Extreme heat in recent years | Daily | Daily | 86 | `QID124_3` | MATCH |
| 50 | Experience — Changing your kids' school due to moving | Weekly | Weekly | 87 | `QID124_4` | MATCH |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Weekly | Weekly | 88 | `QID124_5` | MATCH |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | Weekly | 89 | `QID124_6` | MATCH |
| 53 | Experience — Well drying up | Daily | Daily | 90 | `QID124_7` | MATCH |
| 54 | Experience — A problem with pests in your home | Daily | Daily | 91 | `QID124_8` | MATCH |
| 55 | Experience — A problem with water leaks | Daily | Daily | 92 | `QID124_9` | MATCH |
| 56 | Experience — A problem with loose animals | Daily | Daily | 93 | `QID124_10` | MATCH |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | Yes | 133 | `QID211` | MATCH |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | No | 134 | `QID219` | MATCH |
| 59 | What is the highest level of education you have completed? | Graduate Degree | Graduate Degree | 142 | `QID178` | MATCH |
| 60 | Which best describes your employment status? | Retired | Retired | 143 | `QID176` | MATCH |

## 19. `R_aPZYZkLLHTo3YDR` — 6392 Beloit Avenue

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_aPZYZkLLHTo3YDR.png`

> **UNVERIFIED** — no row for this ResponseId in the April 15 export (see finding F2, coverage gap).

## 20. `R_bt9KhSC0xqF2xuS` — Beloit Ave

Read from the **Survey Answers** tab · 66 rows rendered · screenshot: `../screenshots/R_bt9KhSC0xqF2xuS.png`

> **UNVERIFIED** — no row for this ResponseId in the April 15 export (see finding F2, coverage gap).

## 21. `R_bxz0eWgFA4AstpB` — 7239 Purdue Street

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_bxz0eWgFA4AstpB.png`

> **UNVERIFIED** — no row for this ResponseId in the April 15 export (see finding F2, coverage gap).

## 22. `R_d4T4ee11cH6ntjW` — 7197 Pembroke Street

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_d4T4ee11cH6ntjW.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Monthly | Monthly | 123 | `RespIll` | MATCH |
| 2 | How often does anyone in your home have asthma symptoms? | Monthly | Monthly | 122 | `asthma` | MATCH |
| 3 | How often does anyone in your home wheeze? | Monthly | Monthly | 125 | `wheeze` | MATCH |
| 4 | How often does anyone in your home experience headaches? | Monthly | Monthly | 120 | `Headache` | MATCH |
| 5 | How often do you feel tired or fatigued in your home? | weekly | weekly | 124 | `Tired` | MATCH |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | yes | Yes, Doctor visits for allergy. | 132 | `Hospital Respiratory` | DIFFERENT |
| 7 | Evidence of mold in any area of the home? | Yes | Other: | 108 | `Mold` | DIFFERENT |
| 8 | Water leakage — Roof | none | none | 110 | `Leakage 2_1` | MATCH |
| 9 | Water leakage — Walls | none | none | 111 | `Leakage 2_2` | MATCH |
| 10 | Water leakage — Windows | none | none | 112 | `Leakage 2_3` | MATCH |
| 11 | Water leakage — Floor | none | none | 113 | `Leakage 2_4` | MATCH |
| 12 | Cooling system — Central AC | less than 10 years | less than 10 years | 100 | `Cooling System _1` | MATCH |
| 13 | Cooling system — Window unit | nan | — | 101 | `Cooling System _2` | DIFFERENT |
| 14 | Cooling system — Fan only | 10 to 15 years | 10 to 15 years | 102 | `Cooling System _3` | MATCH |
| 15 | Cooling system — No cooling | nan | — | 103 | `Cooling System _4` | DIFFERENT |
| 16 | Cooking fuel / method | electric cooktops | electric cooktops | 106 | `Cooking` | MATCH |
| 17 | When was your house built? | Before 1960 | Before 1960 | 39 | `QID192` | MATCH |
| 18 | What type of house do you live in? | Single Wide Mobile Home | Single Wide Mobile Home | 40 | `QID128` | MATCH |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Good- Minor repairs needed. | Good- Minor repairs needed. | 55 | `QID141` | MATCH |
| 20 | What is your current housing ownership status? | Owner | Owner | 24 | `Ownership` | MATCH |
| 21 | How long have you lived in High Ridge Estates? (years) | 20 years | 20 years | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | Others | 44 | `QID47` | MATCH |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | Click to write Choice 3 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Don't know | Don't know | 56 | `QID21` | MATCH |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | More than 6 months | More than 6 months | 57 | `QID194` | MATCH |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 3 | Click to write Choice 3 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes - Portable (Which Room(s)),Yes- Integrated into central air heating system,No | Yes - Portable (Which Room(s)),Yes- Integrated into central air heating system,No | 59 | `QID19` | MATCH |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 1 | Click to write Scale Point 1 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 5 | Click to write Scale Point 5 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 4 | Click to write Scale Point 4 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 1 | Click to write Scale Point 1 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 1 | Click to write Scale Point 1 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 1 | Click to write Scale Point 1 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | Click to write Scale Point 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 67 | `QID195_1` | MATCH |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 68 | `QID195_2` | MATCH |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 69 | `QID195_3` | MATCH |
| 39 | Intervention — Improve heating/cooling system(s) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 70 | `QID195_4` | MATCH |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 71 | `QID195_5` | MATCH |
| 41 | Intervention — Replace well/septic | Nature reserves and preserves | Nature reserves and preserves | 72 | `QID195_6` | MATCH |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | Click to write Scale Point 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 74 | `QID195_8` | MATCH |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Nature reserves and preserves | Nature reserves and preserves | 75 | `QID195_9` | MATCH |
| 45 | Intervention — Trim trees | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 76 | `QID195_10` | MATCH |
| 46 | Intervention — Improved drainage | Nature reserves and preserves | Nature reserves and preserves | 77 | `QID195_11` | MATCH |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | Weekly | 84 | `QID124_1` | MATCH |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | Weekly | 85 | `QID124_2` | MATCH |
| 49 | Experience — Extreme heat in recent years | Daily | Daily | 86 | `QID124_3` | MATCH |
| 50 | Experience — Changing your kids' school due to moving | Weekly | Weekly | 87 | `QID124_4` | MATCH |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Daily | Daily | 88 | `QID124_5` | MATCH |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | Weekly | 89 | `QID124_6` | MATCH |
| 53 | Experience — Well drying up | Weekly | Weekly | 90 | `QID124_7` | MATCH |
| 54 | Experience — A problem with pests in your home | Daily | Daily | 91 | `QID124_8` | MATCH |
| 55 | Experience — A problem with water leaks | Daily | Daily | 92 | `QID124_9` | MATCH |
| 56 | Experience — A problem with loose animals | Daily | Daily | 93 | `QID124_10` | MATCH |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | Yes | 133 | `QID211` | MATCH |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | Name the problem | Name the problem | 134 | `QID219` | MATCH |
| 59 | What is the highest level of education you have completed? | High school diploma or equivalent | High school diploma or equivalent | 142 | `QID178` | MATCH |
| 60 | Which best describes your employment status? | Unemployed | Unemployed | 143 | `QID176` | MATCH |

## 23. `R_h0LfcAVvLrGULaj` — 7166 Pembroke Street

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_h0LfcAVvLrGULaj.png`

> **UNVERIFIED** — no row for this ResponseId in the April 15 export (see finding F2, coverage gap).

## 24. `R_iGZqrFKoHdcjKOH` — 6394 Baylor Avenue

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_iGZqrFKoHdcjKOH.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | Rarely or Never | 123 | `RespIll` | MATCH |
| 2 | How often does anyone in your home have asthma symptoms? | Seasonally | Seasonally | 122 | `asthma` | MATCH |
| 3 | How often does anyone in your home wheeze? | weekly | weekly | 125 | `wheeze` | MATCH |
| 4 | How often does anyone in your home experience headaches? | Monthly | Monthly | 120 | `Headache` | MATCH |
| 5 | How often do you feel tired or fatigued in your home? | weekly | weekly | 124 | `Tired` | MATCH |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | No | 132 | `Hospital Respiratory` | MATCH |
| 7 | Evidence of mold in any area of the home? | Yes | Inner walls/Windows | 108 | `Mold` | DIFFERENT |
| 8 | Water leakage — Roof | nan | — | 110 | `Leakage 2_1` | DIFFERENT |
| 9 | Water leakage — Walls | nan | — | 111 | `Leakage 2_2` | DIFFERENT |
| 10 | Water leakage — Windows | more than one week | more than one week | 112 | `Leakage 2_3` | MATCH |
| 11 | Water leakage — Floor | nan | — | 113 | `Leakage 2_4` | DIFFERENT |
| 12 | Cooling system — Central AC | nan | — | 100 | `Cooling System _1` | DIFFERENT |
| 13 | Cooling system — Window unit | less than 10 years | less than 10 years | 101 | `Cooling System _2` | MATCH |
| 14 | Cooling system — Fan only | nan | — | 102 | `Cooling System _3` | DIFFERENT |
| 15 | Cooling system — No cooling | nan | — | 103 | `Cooling System _4` | DIFFERENT |
| 16 | Cooking fuel / method | electric cooktops | electric cooktops | 106 | `Cooking` | MATCH |
| 17 | When was your house built? | Click to write Choice 5 | Click to write Choice 5 | 39 | `QID192` | PLACEHOLDER |
| 18 | What type of house do you live in? | Double Wide Mobile Home | Double Wide Mobile Home | 40 | `QID128` | MATCH |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Good- Minor repairs needed. | Good- Minor repairs needed. | 55 | `QID141` | MATCH |
| 20 | What is your current housing ownership status? | Renter | Renter | 24 | `Ownership` | MATCH |
| 21 | How long have you lived in High Ridge Estates? (years) | 5 | 5 | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Don't know | Don't know | 44 | `QID47` | MATCH |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | Click to write Choice 3 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | More than 6 months | More than 6 months | 56 | `QID21` | MATCH |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | Click to write Choice 4 | Click to write Choice 4 | 57 | `QID194` | PLACEHOLDER |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 3 | Click to write Choice 3 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes - Portable (Which Room(s)),Click to write Choice 6 | Yes - Portable (Which Room(s)),Click to write Choice 6 | 59 | `QID19` | PLACEHOLDER |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 3 | Click to write Scale Point 3 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 3 | Click to write Scale Point 3 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 3 | Click to write Scale Point 3 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 3 | Click to write Scale Point 3 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 3 | Click to write Scale Point 3 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 3 | Click to write Scale Point 3 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | Click to write Scale Point 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 67 | `QID195_1` | MATCH |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 68 | `QID195_2` | MATCH |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 69 | `QID195_3` | MATCH |
| 39 | Intervention — Improve heating/cooling system(s) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 70 | `QID195_4` | MATCH |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 71 | `QID195_5` | MATCH |
| 41 | Intervention — Replace well/septic | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 72 | `QID195_6` | MATCH |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | Click to write Scale Point 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 74 | `QID195_8` | MATCH |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 75 | `QID195_9` | MATCH |
| 45 | Intervention — Trim trees | — | — | 76 | `QID195_10` | EMPTY-BOTH |
| 46 | Intervention — Improved drainage | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 77 | `QID195_11` | MATCH |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | Weekly | 84 | `QID124_1` | MATCH |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | Weekly | 85 | `QID124_2` | MATCH |
| 49 | Experience — Extreme heat in recent years | Daily | Daily | 86 | `QID124_3` | MATCH |
| 50 | Experience — Changing your kids' school due to moving | Weekly | Weekly | 87 | `QID124_4` | MATCH |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Weekly | Weekly | 88 | `QID124_5` | MATCH |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | Weekly | 89 | `QID124_6` | MATCH |
| 53 | Experience — Well drying up | Weekly | Weekly | 90 | `QID124_7` | MATCH |
| 54 | Experience — A problem with pests in your home | Weekly | Weekly | 91 | `QID124_8` | MATCH |
| 55 | Experience — A problem with water leaks | Weekly | Weekly | 92 | `QID124_9` | MATCH |
| 56 | Experience — A problem with loose animals | Weekly | Weekly | 93 | `QID124_10` | MATCH |
| 57 | Do you (or your household) own or have regular access to a car? | No | No | 133 | `QID211` | MATCH |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | Not Sure | Not Sure | 134 | `QID219` | MATCH |
| 59 | What is the highest level of education you have completed? | Vocational/Technical Licensing or Certification | Vocational/Technical Licensing or Certification | 142 | `QID178` | MATCH |
| 60 | Which best describes your employment status? | Unemployed | Unemployed | 143 | `QID176` | MATCH |

## 25. `R_jIMWa4XhirJ5WDy` — 6301 Columbia Avenue

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_jIMWa4XhirJ5WDy.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | Rarely or Never | 123 | `RespIll` | MATCH |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | Rarely or Never | 122 | `asthma` | MATCH |
| 3 | How often does anyone in your home wheeze? | Seasonally | Seasonally | 125 | `wheeze` | MATCH |
| 4 | How often does anyone in your home experience headaches? | Rarely or Never | Rarely or Never | 120 | `Headache` | MATCH |
| 5 | How often do you feel tired or fatigued in your home? | weekly | weekly | 124 | `Tired` | MATCH |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | yes | Yes, hospitalization/visiting the emergency room for asthma attack. | 132 | `Hospital Respiratory` | DIFFERENT |
| 7 | Evidence of mold in any area of the home? | Yes | Kitchen,Bathroom,Living Room,Bedroom | 108 | `Mold` | DIFFERENT |
| 8 | Water leakage — Roof | none | none | 110 | `Leakage 2_1` | MATCH |
| 9 | Water leakage — Walls | none | none | 111 | `Leakage 2_2` | MATCH |
| 10 | Water leakage — Windows | not fixed | not fixed | 112 | `Leakage 2_3` | MATCH |
| 11 | Water leakage — Floor | none | none | 113 | `Leakage 2_4` | MATCH |
| 12 | Cooling system — Central AC | Don't know/Not applicable | Don't know/Not applicable | 100 | `Cooling System _1` | MATCH |
| 13 | Cooling system — Window unit | More than 15 years | More than 15 years | 101 | `Cooling System _2` | MATCH |
| 14 | Cooling system — Fan only | Don't know/Not applicable | Don't know/Not applicable | 102 | `Cooling System _3` | MATCH |
| 15 | Cooling system — No cooling | Don't know/Not applicable | Don't know/Not applicable | 103 | `Cooling System _4` | MATCH |
| 16 | Cooking fuel / method | electric cooktops | electric cooktops | 106 | `Cooking` | MATCH |
| 17 | When was your house built? | Built 1960–1979 | Built 1960–1979 | 39 | `QID192` | MATCH |
| 18 | What type of house do you live in? | Single Wide Mobile Home | Single Wide Mobile Home | 40 | `QID128` | MATCH |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Fair- Some repairs needed. | Fair- Some repairs needed. | 55 | `QID141` | MATCH |
| 20 | What is your current housing ownership status? | Renter | Renter | 24 | `Ownership` | MATCH |
| 21 | How long have you lived in High Ridge Estates? (years) | 2.5 years | 2.5 years | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | Others | 44 | `QID47` | MATCH |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | Click to write Choice 3 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Don't know | Don't know | 56 | `QID21` | MATCH |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | More than 6 months | More than 6 months | 57 | `QID194` | MATCH |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 3 | Click to write Choice 3 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes- Integrated into central air heating system | Yes- Integrated into central air heating system | 59 | `QID19` | MATCH |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 1 | Click to write Scale Point 1 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 1 | Click to write Scale Point 1 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 3 | Click to write Scale Point 3 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 4 | Click to write Scale Point 4 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 4 | Click to write Scale Point 4 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 5 | Click to write Scale Point 5 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | Click to write Scale Point 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 67 | `QID195_1` | MATCH |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 68 | `QID195_2` | MATCH |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 69 | `QID195_3` | MATCH |
| 39 | Intervention — Improve heating/cooling system(s) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 70 | `QID195_4` | MATCH |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Click to write Scale Point 1 | Click to write Scale Point 1 | 71 | `QID195_5` | PLACEHOLDER |
| 41 | Intervention — Replace well/septic | Click to write Scale Point 1 | Click to write Scale Point 1 | 72 | `QID195_6` | PLACEHOLDER |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | Click to write Scale Point 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Click to write Scale Point 1 | Click to write Scale Point 1 | 74 | `QID195_8` | PLACEHOLDER |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Click to write Scale Point 1 | Click to write Scale Point 1 | 75 | `QID195_9` | PLACEHOLDER |
| 45 | Intervention — Trim trees | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 76 | `QID195_10` | MATCH |
| 46 | Intervention — Improved drainage | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 77 | `QID195_11` | MATCH |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Daily | Daily | 84 | `QID124_1` | MATCH |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | Weekly | 85 | `QID124_2` | MATCH |
| 49 | Experience — Extreme heat in recent years | Daily | Daily | 86 | `QID124_3` | MATCH |
| 50 | Experience — Changing your kids' school due to moving | Weekly | Weekly | 87 | `QID124_4` | MATCH |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Daily | Daily | 88 | `QID124_5` | MATCH |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | Weekly | 89 | `QID124_6` | MATCH |
| 53 | Experience — Well drying up | Daily | Daily | 90 | `QID124_7` | MATCH |
| 54 | Experience — A problem with pests in your home | Daily | Daily | 91 | `QID124_8` | MATCH |
| 55 | Experience — A problem with water leaks | Daily | Daily | 92 | `QID124_9` | MATCH |
| 56 | Experience — A problem with loose animals | Weekly | Weekly | 93 | `QID124_10` | MATCH |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | Yes | 133 | `QID211` | MATCH |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | Yes | Yes | 134 | `QID219` | MATCH |
| 59 | What is the highest level of education you have completed? | High school diploma or equivalent | High school diploma or equivalent | 142 | `QID178` | MATCH |
| 60 | Which best describes your employment status? | Unemployed | Unemployed | 143 | `QID176` | MATCH |

## 26. `R_kVLcdKScFHPgWVR` — 6308 Bucknell

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_kVLcdKScFHPgWVR.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | weekly | weekly | 123 | `RespIll` | MATCH |
| 2 | How often does anyone in your home have asthma symptoms? | weekly | weekly | 122 | `asthma` | MATCH |
| 3 | How often does anyone in your home wheeze? | weekly | weekly | 125 | `wheeze` | MATCH |
| 4 | How often does anyone in your home experience headaches? | Rarely or Never | Rarely or Never | 120 | `Headache` | MATCH |
| 5 | How often do you feel tired or fatigued in your home? | weekly | weekly | 124 | `Tired` | MATCH |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | No | 132 | `Hospital Respiratory` | MATCH |
| 7 | Evidence of mold in any area of the home? | Yes | Other: | 108 | `Mold` | DIFFERENT |
| 8 | Water leakage — Roof | none | none | 110 | `Leakage 2_1` | MATCH |
| 9 | Water leakage — Walls | none | none | 111 | `Leakage 2_2` | MATCH |
| 10 | Water leakage — Windows | none | none | 112 | `Leakage 2_3` | MATCH |
| 11 | Water leakage — Floor | none | none | 113 | `Leakage 2_4` | MATCH |
| 12 | Cooling system — Central AC | less than 10 years | less than 10 years | 100 | `Cooling System _1` | MATCH |
| 13 | Cooling system — Window unit | nan | — | 101 | `Cooling System _2` | DIFFERENT |
| 14 | Cooling system — Fan only | nan | — | 102 | `Cooling System _3` | DIFFERENT |
| 15 | Cooling system — No cooling | nan | — | 103 | `Cooling System _4` | DIFFERENT |
| 16 | Cooking fuel / method | electric cooktops | electric cooktops | 106 | `Cooking` | MATCH |
| 17 | When was your house built? | Before 1960 | Before 1960 | 39 | `QID192` | MATCH |
| 18 | What type of house do you live in? | Double Wide Mobile Home | Double Wide Mobile Home | 40 | `QID128` | MATCH |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Click to write Choice 5 | Click to write Choice 5 | 55 | `QID141` | PLACEHOLDER |
| 20 | What is your current housing ownership status? | Owner | Owner | 24 | `Ownership` | MATCH |
| 21 | How long have you lived in High Ridge Estates? (years) | 1 | 1 | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | Others | 44 | `QID47` | MATCH |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | Click to write Choice 3 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Less than 6 months | Less than 6 months | 56 | `QID21` | MATCH |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | Less than 6 months | Less than 6 months | 57 | `QID194` | MATCH |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 5 | Click to write Choice 5 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes- Integrated into central air heating system | Yes- Integrated into central air heating system | 59 | `QID19` | MATCH |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 1 | Click to write Scale Point 1 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 1 | Click to write Scale Point 1 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 1 | Click to write Scale Point 1 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 1 | Click to write Scale Point 1 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 4 | Click to write Scale Point 4 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 4 | Click to write Scale Point 4 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | Click to write Scale Point 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Nature reserves and preserves | Nature reserves and preserves | 67 | `QID195_1` | MATCH |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Nature reserves and preserves | Nature reserves and preserves | 68 | `QID195_2` | MATCH |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Nature reserves and preserves | Nature reserves and preserves | 69 | `QID195_3` | MATCH |
| 39 | Intervention — Improve heating/cooling system(s) | Nature reserves and preserves | Nature reserves and preserves | 70 | `QID195_4` | MATCH |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Nature reserves and preserves | Nature reserves and preserves | 71 | `QID195_5` | MATCH |
| 41 | Intervention — Replace well/septic | Nature reserves and preserves | Nature reserves and preserves | 72 | `QID195_6` | MATCH |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | Click to write Scale Point 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 74 | `QID195_8` | MATCH |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Nature reserves and preserves | Nature reserves and preserves | 75 | `QID195_9` | MATCH |
| 45 | Intervention — Trim trees | Nature reserves and preserves | Nature reserves and preserves | 76 | `QID195_10` | MATCH |
| 46 | Intervention — Improved drainage | Nature reserves and preserves | Nature reserves and preserves | 77 | `QID195_11` | MATCH |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | Weekly | 84 | `QID124_1` | MATCH |
| 48 | Experience — In case of flooding, received help for cleaning | Biweekly | Biweekly | 85 | `QID124_2` | MATCH |
| 49 | Experience — Extreme heat in recent years | Weekly | Weekly | 86 | `QID124_3` | MATCH |
| 50 | Experience — Changing your kids' school due to moving | Weekly | Weekly | 87 | `QID124_4` | MATCH |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Weekly | Weekly | 88 | `QID124_5` | MATCH |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | Weekly | 89 | `QID124_6` | MATCH |
| 53 | Experience — Well drying up | Weekly | Weekly | 90 | `QID124_7` | MATCH |
| 54 | Experience — A problem with pests in your home | Weekly | Weekly | 91 | `QID124_8` | MATCH |
| 55 | Experience — A problem with water leaks | Weekly | Weekly | 92 | `QID124_9` | MATCH |
| 56 | Experience — A problem with loose animals | Weekly | Weekly | 93 | `QID124_10` | MATCH |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | Yes | 133 | `QID211` | MATCH |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | No | 134 | `QID219` | MATCH |
| 59 | What is the highest level of education you have completed? | High school diploma or equivalent | High school diploma or equivalent | 142 | `QID178` | MATCH |
| 60 | Which best describes your employment status? | Retired | Retired | 143 | `QID176` | MATCH |

## 27. `R_l1yOBZ0aTpnAxq3` — 7358 Yale St.

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_l1yOBZ0aTpnAxq3.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | Rarely or Never | 123 | `RespIll` | MATCH |
| 2 | How often does anyone in your home have asthma symptoms? | Monthly | Monthly | 122 | `asthma` | MATCH |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | Rarely or Never | 125 | `wheeze` | MATCH |
| 4 | How often does anyone in your home experience headaches? | Rarely or Never | Rarely or Never | 120 | `Headache` | MATCH |
| 5 | How often do you feel tired or fatigued in your home? | weekly | weekly | 124 | `Tired` | MATCH |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | yes | Yes, Others. | 132 | `Hospital Respiratory` | DIFFERENT |
| 7 | Evidence of mold in any area of the home? | Yes | Other: | 108 | `Mold` | DIFFERENT |
| 8 | Water leakage — Roof | none | none | 110 | `Leakage 2_1` | MATCH |
| 9 | Water leakage — Walls | none | none | 111 | `Leakage 2_2` | MATCH |
| 10 | Water leakage — Windows | none | none | 112 | `Leakage 2_3` | MATCH |
| 11 | Water leakage — Floor | none | none | 113 | `Leakage 2_4` | MATCH |
| 12 | Cooling system — Central AC | Don't know/Not applicable | Don't know/Not applicable | 100 | `Cooling System _1` | MATCH |
| 13 | Cooling system — Window unit | Don't know/Not applicable | Don't know/Not applicable | 101 | `Cooling System _2` | MATCH |
| 14 | Cooling system — Fan only | 10 to 15 years | 10 to 15 years | 102 | `Cooling System _3` | MATCH |
| 15 | Cooling system — No cooling | Don't know/Not applicable | Don't know/Not applicable | 103 | `Cooling System _4` | MATCH |
| 16 | Cooking fuel / method | electric cooktops | electric cooktops | 106 | `Cooking` | MATCH |
| 17 | When was your house built? | Click to write Choice 5 | Click to write Choice 5 | 39 | `QID192` | PLACEHOLDER |
| 18 | What type of house do you live in? | Double Wide Mobile Home | Double Wide Mobile Home | 40 | `QID128` | MATCH |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Fair- Some repairs needed. | Fair- Some repairs needed. | 55 | `QID141` | MATCH |
| 20 | What is your current housing ownership status? | Renter | Renter | 24 | `Ownership` | MATCH |
| 21 | How long have you lived in High Ridge Estates? (years) | 5months | 5months | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Wood | Wood | 44 | `QID47` | MATCH |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | Click to write Choice 3 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Less than 6 months | Less than 6 months | 56 | `QID21` | MATCH |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | Don't know | Don't know | 57 | `QID194` | MATCH |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 3 | Click to write Choice 3 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes- Integrated into central air heating system | Yes- Integrated into central air heating system | 59 | `QID19` | MATCH |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 1 | Click to write Scale Point 1 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 2 | Click to write Scale Point 2 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 2 | Click to write Scale Point 2 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 1 | Click to write Scale Point 1 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 1 | Click to write Scale Point 1 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 3 | Click to write Scale Point 3 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | Click to write Scale Point 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 67 | `QID195_1` | MATCH |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 68 | `QID195_2` | MATCH |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Click to write Scale Point 1 | Click to write Scale Point 1 | 69 | `QID195_3` | PLACEHOLDER |
| 39 | Intervention — Improve heating/cooling system(s) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 70 | `QID195_4` | MATCH |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 71 | `QID195_5` | MATCH |
| 41 | Intervention — Replace well/septic | Click to write Scale Point 1 | Click to write Scale Point 1 | 72 | `QID195_6` | PLACEHOLDER |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | Click to write Scale Point 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 74 | `QID195_8` | MATCH |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Click to write Scale Point 1 | Click to write Scale Point 1 | 75 | `QID195_9` | PLACEHOLDER |
| 45 | Intervention — Trim trees | Click to write Scale Point 1 | Click to write Scale Point 1 | 76 | `QID195_10` | PLACEHOLDER |
| 46 | Intervention — Improved drainage | Click to write Scale Point 1 | Click to write Scale Point 1 | 77 | `QID195_11` | PLACEHOLDER |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | Weekly | 84 | `QID124_1` | MATCH |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | Weekly | 85 | `QID124_2` | MATCH |
| 49 | Experience — Extreme heat in recent years | Weekly | Weekly | 86 | `QID124_3` | MATCH |
| 50 | Experience — Changing your kids' school due to moving | Weekly | Weekly | 87 | `QID124_4` | MATCH |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Weekly | Weekly | 88 | `QID124_5` | MATCH |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | Weekly | 89 | `QID124_6` | MATCH |
| 53 | Experience — Well drying up | Weekly | Weekly | 90 | `QID124_7` | MATCH |
| 54 | Experience — A problem with pests in your home | Weekly | Weekly | 91 | `QID124_8` | MATCH |
| 55 | Experience — A problem with water leaks | Weekly | Weekly | 92 | `QID124_9` | MATCH |
| 56 | Experience — A problem with loose animals | Daily | Daily | 93 | `QID124_10` | MATCH |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | Yes | 133 | `QID211` | MATCH |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | No | 134 | `QID219` | MATCH |
| 59 | What is the highest level of education you have completed? | Some college, no degree | Some college, no degree | 142 | `QID178` | MATCH |
| 60 | Which best describes your employment status? | Employed- Full time | Employed- Full time | 143 | `QID176` | MATCH |

## 28. `R_mhCImQQ64DBmsPH` — 6389 Baylor

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_mhCImQQ64DBmsPH.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | Rarely or Never | 123 | `RespIll` | MATCH |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | Rarely or Never | 122 | `asthma` | MATCH |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | Rarely or Never | 125 | `wheeze` | MATCH |
| 4 | How often does anyone in your home experience headaches? | Rarely or Never | Rarely or Never | 120 | `Headache` | MATCH |
| 5 | How often do you feel tired or fatigued in your home? | Monthly | Monthly | 124 | `Tired` | MATCH |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | yes | Yes, Others. | 132 | `Hospital Respiratory` | DIFFERENT |
| 7 | Evidence of mold in any area of the home? | Yes | Bathroom,Bedroom,Inner walls/Windows | 108 | `Mold` | DIFFERENT |
| 8 | Water leakage — Roof | more than one week | more than one week | 110 | `Leakage 2_1` | MATCH |
| 9 | Water leakage — Walls | none | none | 111 | `Leakage 2_2` | MATCH |
| 10 | Water leakage — Windows | none | none | 112 | `Leakage 2_3` | MATCH |
| 11 | Water leakage — Floor | none | none | 113 | `Leakage 2_4` | MATCH |
| 12 | Cooling system — Central AC | nan | — | 100 | `Cooling System _1` | DIFFERENT |
| 13 | Cooling system — Window unit | less than 10 years | less than 10 years | 101 | `Cooling System _2` | MATCH |
| 14 | Cooling system — Fan only | nan | — | 102 | `Cooling System _3` | DIFFERENT |
| 15 | Cooling system — No cooling | nan | — | 103 | `Cooling System _4` | DIFFERENT |
| 16 | Cooking fuel / method | electric cooktops | electric cooktops | 106 | `Cooking` | MATCH |
| 17 | When was your house built? | Before 1960 | Before 1960 | 39 | `QID192` | MATCH |
| 18 | What type of house do you live in? | Double Wide Mobile Home | Double Wide Mobile Home | 40 | `QID128` | MATCH |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Poor- Major repairs needed. | Poor- Major repairs needed. | 55 | `QID141` | MATCH |
| 20 | What is your current housing ownership status? | Owner | Owner | 24 | `Ownership` | MATCH |
| 21 | How long have you lived in High Ridge Estates? (years) | 50 yrs family land | 50 yrs family land | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | Others | 44 | `QID47` | MATCH |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | Click to write Choice 3 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Less than 6 months | Less than 6 months | 56 | `QID21` | MATCH |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | Don't know | Don't know | 57 | `QID194` | MATCH |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 5 | Click to write Choice 5 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes- Integrated into central air heating system | Yes- Integrated into central air heating system | 59 | `QID19` | MATCH |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 1 | Click to write Scale Point 1 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 5 | Click to write Scale Point 5 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 5 | Click to write Scale Point 5 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 5 | Click to write Scale Point 5 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 5 | Click to write Scale Point 5 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 5 | Click to write Scale Point 5 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 5 | Click to write Scale Point 5 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 67 | `QID195_1` | MATCH |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 68 | `QID195_2` | MATCH |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Nature reserves and preserves | Nature reserves and preserves | 69 | `QID195_3` | MATCH |
| 39 | Intervention — Improve heating/cooling system(s) | Nature reserves and preserves | Nature reserves and preserves | 70 | `QID195_4` | MATCH |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 71 | `QID195_5` | MATCH |
| 41 | Intervention — Replace well/septic | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 72 | `QID195_6` | MATCH |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | Click to write Scale Point 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 74 | `QID195_8` | MATCH |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Click to write Scale Point 1 | Click to write Scale Point 1 | 75 | `QID195_9` | PLACEHOLDER |
| 45 | Intervention — Trim trees | Click to write Scale Point 1 | Click to write Scale Point 1 | 76 | `QID195_10` | PLACEHOLDER |
| 46 | Intervention — Improved drainage | Click to write Scale Point 1 | Click to write Scale Point 1 | 77 | `QID195_11` | PLACEHOLDER |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | Weekly | 84 | `QID124_1` | MATCH |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | Weekly | 85 | `QID124_2` | MATCH |
| 49 | Experience — Extreme heat in recent years | Weekly | Weekly | 86 | `QID124_3` | MATCH |
| 50 | Experience — Changing your kids' school due to moving | Weekly | Weekly | 87 | `QID124_4` | MATCH |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Daily | Daily | 88 | `QID124_5` | MATCH |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | Weekly | 89 | `QID124_6` | MATCH |
| 53 | Experience — Well drying up | Weekly | Weekly | 90 | `QID124_7` | MATCH |
| 54 | Experience — A problem with pests in your home | Weekly | Weekly | 91 | `QID124_8` | MATCH |
| 55 | Experience — A problem with water leaks | Daily | Daily | 92 | `QID124_9` | MATCH |
| 56 | Experience — A problem with loose animals | Weekly | Weekly | 93 | `QID124_10` | MATCH |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | Yes | 133 | `QID211` | MATCH |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | Yes | Yes | 134 | `QID219` | MATCH |
| 59 | What is the highest level of education you have completed? | High school diploma or equivalent | High school diploma or equivalent | 142 | `QID178` | MATCH |
| 60 | Which best describes your employment status? | Retired | Retired | 143 | `QID176` | MATCH |

## 29. `R_oAELLLNZllsvEkJ` — 6413 Bowdoin Ave

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_oAELLLNZllsvEkJ.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | Rarely or Never | 123 | `RespIll` | MATCH |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | Rarely or Never | 122 | `asthma` | MATCH |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | Rarely or Never | 125 | `wheeze` | MATCH |
| 4 | How often does anyone in your home experience headaches? | Seasonally | Seasonally | 120 | `Headache` | MATCH |
| 5 | How often do you feel tired or fatigued in your home? | weekly | weekly | 124 | `Tired` | MATCH |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | No | 132 | `Hospital Respiratory` | MATCH |
| 7 | Evidence of mold in any area of the home? | Yes | Other: | 108 | `Mold` | DIFFERENT |
| 8 | Water leakage — Roof | more than one week | more than one week | 110 | `Leakage 2_1` | MATCH |
| 9 | Water leakage — Walls | none | none | 111 | `Leakage 2_2` | MATCH |
| 10 | Water leakage — Windows | more than one week | more than one week | 112 | `Leakage 2_3` | MATCH |
| 11 | Water leakage — Floor | more than one week | more than one week | 113 | `Leakage 2_4` | MATCH |
| 12 | Cooling system — Central AC | less than 10 years | less than 10 years | 100 | `Cooling System _1` | MATCH |
| 13 | Cooling system — Window unit | Don't know/Not applicable | Don't know/Not applicable | 101 | `Cooling System _2` | MATCH |
| 14 | Cooling system — Fan only | Don't know/Not applicable | Don't know/Not applicable | 102 | `Cooling System _3` | MATCH |
| 15 | Cooling system — No cooling | Don't know/Not applicable | Don't know/Not applicable | 103 | `Cooling System _4` | MATCH |
| 16 | Cooking fuel / method | electric cooktops | electric cooktops | 106 | `Cooking` | MATCH |
| 17 | When was your house built? | Built 1980–1999 | Built 1980–1999 | 39 | `QID192` | MATCH |
| 18 | What type of house do you live in? | Single Wide Mobile Home | Single Wide Mobile Home | 40 | `QID128` | MATCH |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Good- Minor repairs needed. | Good- Minor repairs needed. | 55 | `QID141` | MATCH |
| 20 | What is your current housing ownership status? | Owner | Owner | 24 | `Ownership` | MATCH |
| 21 | How long have you lived in High Ridge Estates? (years) | 9 | 9 | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | Others | 44 | `QID47` | MATCH |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | Click to write Choice 3 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | More than 6 months | More than 6 months | 56 | `QID21` | MATCH |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | More than 6 months | More than 6 months | 57 | `QID194` | MATCH |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 4 | Click to write Choice 4 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes- Integrated into central air heating system | Yes- Integrated into central air heating system | 59 | `QID19` | MATCH |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 2 | Click to write Scale Point 2 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 3 | Click to write Scale Point 3 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 3 | Click to write Scale Point 3 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 2 | Click to write Scale Point 2 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 3 | Click to write Scale Point 3 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 2 | Click to write Scale Point 2 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 2 | Click to write Scale Point 2 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Click to write Scale Point 1 | Click to write Scale Point 1 | 67 | `QID195_1` | PLACEHOLDER |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Click to write Scale Point 1 | Click to write Scale Point 1 | 68 | `QID195_2` | PLACEHOLDER |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Click to write Scale Point 1 | Click to write Scale Point 1 | 69 | `QID195_3` | PLACEHOLDER |
| 39 | Intervention — Improve heating/cooling system(s) | Click to write Scale Point 1 | Click to write Scale Point 1 | 70 | `QID195_4` | PLACEHOLDER |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Click to write Scale Point 1 | Click to write Scale Point 1 | 71 | `QID195_5` | PLACEHOLDER |
| 41 | Intervention — Replace well/septic | Click to write Scale Point 1 | Click to write Scale Point 1 | 72 | `QID195_6` | PLACEHOLDER |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | Click to write Scale Point 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 74 | `QID195_8` | MATCH |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Click to write Scale Point 1 | Click to write Scale Point 1 | 75 | `QID195_9` | PLACEHOLDER |
| 45 | Intervention — Trim trees | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 76 | `QID195_10` | MATCH |
| 46 | Intervention — Improved drainage | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 77 | `QID195_11` | MATCH |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | Weekly | 84 | `QID124_1` | MATCH |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | Weekly | 85 | `QID124_2` | MATCH |
| 49 | Experience — Extreme heat in recent years | Weekly | Weekly | 86 | `QID124_3` | MATCH |
| 50 | Experience — Changing your kids' school due to moving | Weekly | Weekly | 87 | `QID124_4` | MATCH |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Daily | Daily | 88 | `QID124_5` | MATCH |
| 52 | Experience — Losing home owners insurance due to age of home | Biweekly | Biweekly | 89 | `QID124_6` | MATCH |
| 53 | Experience — Well drying up | Biweekly | Biweekly | 90 | `QID124_7` | MATCH |
| 54 | Experience — A problem with pests in your home | Weekly | Weekly | 91 | `QID124_8` | MATCH |
| 55 | Experience — A problem with water leaks | Daily | Daily | 92 | `QID124_9` | MATCH |
| 56 | Experience — A problem with loose animals | Daily | Daily | 93 | `QID124_10` | MATCH |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | Yes | 133 | `QID211` | MATCH |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | No | 134 | `QID219` | MATCH |
| 59 | What is the highest level of education you have completed? | Some college, no degree | Some college, no degree | 142 | `QID178` | MATCH |
| 60 | Which best describes your employment status? | Retired | Retired | 143 | `QID176` | MATCH |

## 30. `R_orcmMnaQVATvgHJ` — 7183 Duke St

Read from the **Survey Answers** tab · 64 rows rendered · screenshot: `../screenshots/R_orcmMnaQVATvgHJ.png`

| # | Question as shown in the popup | Popup shows | CSV cell | CSV col | QID | Verdict |
|---|---|---|---|---|---|---|
| 1 | How often does anyone in your home have respiratory illness symptoms? | Rarely or Never | Rarely or Never | 123 | `RespIll` | MATCH |
| 2 | How often does anyone in your home have asthma symptoms? | Rarely or Never | Rarely or Never | 122 | `asthma` | MATCH |
| 3 | How often does anyone in your home wheeze? | Rarely or Never | Rarely or Never | 125 | `wheeze` | MATCH |
| 4 | How often does anyone in your home experience headaches? | Rarely or Never | Rarely or Never | 120 | `Headache` | MATCH |
| 5 | How often do you feel tired or fatigued in your home? | Rarely or Never | Rarely or Never | 124 | `Tired` | MATCH |
| 6 | Has anyone in your home visited a hospital for respiratory issues? | no | No | 132 | `Hospital Respiratory` | MATCH |
| 7 | Evidence of mold in any area of the home? | Yes | Other: | 108 | `Mold` | DIFFERENT |
| 8 | Water leakage — Roof | less than one week | less than one week | 110 | `Leakage 2_1` | MATCH |
| 9 | Water leakage — Walls | less than one week | less than one week | 111 | `Leakage 2_2` | MATCH |
| 10 | Water leakage — Windows | less than one week | less than one week | 112 | `Leakage 2_3` | MATCH |
| 11 | Water leakage — Floor | less than one week | less than one week | 113 | `Leakage 2_4` | MATCH |
| 12 | Cooling system — Central AC | less than 10 years | less than 10 years | 100 | `Cooling System _1` | MATCH |
| 13 | Cooling system — Window unit | Don't know/Not applicable | Don't know/Not applicable | 101 | `Cooling System _2` | MATCH |
| 14 | Cooling system — Fan only | less than 10 years | less than 10 years | 102 | `Cooling System _3` | MATCH |
| 15 | Cooling system — No cooling | nan | — | 103 | `Cooling System _4` | DIFFERENT |
| 16 | Cooking fuel / method | electric cooktops | electric cooktops | 106 | `Cooking` | MATCH |
| 17 | When was your house built? | Built 1960–1979 | Built 1960–1979 | 39 | `QID192` | MATCH |
| 18 | What type of house do you live in? | Single Wide Mobile Home | Single Wide Mobile Home | 40 | `QID128` | MATCH |
| 19 | How would you describe the condition of your current house in terms of maintenance and repair? | Good- Minor repairs needed. | Good- Minor repairs needed. | 55 | `QID141` | MATCH |
| 20 | What is your current housing ownership status? | Owner | Owner | 24 | `Ownership` | MATCH |
| 21 | How long have you lived in High Ridge Estates? (years) | 20 | 20 | 27 | `QID12_TEXT` | MATCH |
| 22 | How long do you anticipate continuing to live in your current house? | Others | Others | 44 | `QID47` | MATCH |
| 23 | If you live in a mobile home, does your home have its skirting intact? | Click to write Choice 3 | Click to write Choice 3 | 42 | `QID100` | PLACEHOLDER |
| 24 | Do you feel safe in your house in terms of environmental threats (flooding, heatwaves, heavy rain/wind)? | Click to write Choice 4 | Click to write Choice 4 | 56 | `QID21` | PLACEHOLDER |
| 25 | Do you feel safe in your house in terms of social threats (loose pets, concerns about neighbors, etc.)? | More than 6 months | More than 6 months | 57 | `QID194` | MATCH |
| 26 | How would you rate the urgency of having affordable housing in High Ridge Estates? | Click to write Choice 3 | Click to write Choice 3 | 58 | `QID17` | PLACEHOLDER |
| 27 | In your opinion, what is the most effective strategy to improve housing affordability in HRE? | Yes - Portable (Which Room(s)) | Yes - Portable (Which Room(s)) | 59 | `QID19` | MATCH |
| 28 | Relocation factor — Employment opportunities nearby | Click to write Scale Point 1 | Click to write Scale Point 1 | 29 | `QID181_1` | PLACEHOLDER |
| 29 | Relocation factor — Affordable housing | Click to write Scale Point 5 | Click to write Scale Point 5 | 30 | `QID181_2` | PLACEHOLDER |
| 30 | Relocation factor — Quality of Life | Click to write Scale Point 5 | Click to write Scale Point 5 | 31 | `QID181_3` | PLACEHOLDER |
| 31 | Relocation factor — Proximity to family and friends | Click to write Scale Point 2 | Click to write Scale Point 2 | 32 | `QID181_4` | PLACEHOLDER |
| 32 | Relocation factor — Retirement | Click to write Scale Point 1 | Click to write Scale Point 1 | 33 | `QID181_5` | PLACEHOLDER |
| 33 | Relocation factor — Environmental quality and access to nature | Click to write Scale Point 3 | Click to write Scale Point 3 | 34 | `QID181_6` | PLACEHOLDER |
| 34 | Relocation factor — Inherited property | Click to write Scale Point 1 | Click to write Scale Point 1 | 35 | `QID181_7` | PLACEHOLDER |
| 35 | Relocation factor — Other | — | — | 36 | `QID181_8` | EMPTY-BOTH |
| 36 | Intervention — Strengthen the roof and walls against severe weather | Click to write Scale Point 1 | Click to write Scale Point 1 | 67 | `QID195_1` | PLACEHOLDER |
| 37 | Intervention — Upgrade windows and doors to be more energy-efficient | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | 68 | `QID195_2` | MATCH |
| 38 | Intervention — Install rain gardens to manage stormwater on my property | Click to write Scale Point 1 | Click to write Scale Point 1 | 69 | `QID195_3` | PLACEHOLDER |
| 39 | Intervention — Improve heating/cooling system(s) | Click to write Scale Point 1 | Click to write Scale Point 1 | 70 | `QID195_4` | PLACEHOLDER |
| 40 | Intervention — Improve plumbing or electrical systems for reliability | Click to write Scale Point 1 | Click to write Scale Point 1 | 71 | `QID195_5` | PLACEHOLDER |
| 41 | Intervention — Replace well/septic | Click to write Scale Point 1 | Click to write Scale Point 1 | 72 | `QID195_6` | PLACEHOLDER |
| 42 | Intervention — Connect to city water through CCUA | Click to write Scale Point 1 | Click to write Scale Point 1 | 73 | `QID195_7` | PLACEHOLDER |
| 43 | Intervention — Add a fence for safety | Click to write Scale Point 1 | Click to write Scale Point 1 | 74 | `QID195_8` | PLACEHOLDER |
| 44 | Intervention — Plant more trees around my home for shade and cooling | Click to write Scale Point 1 | Click to write Scale Point 1 | 75 | `QID195_9` | PLACEHOLDER |
| 45 | Intervention — Trim trees | Click to write Scale Point 1 | Click to write Scale Point 1 | 76 | `QID195_10` | PLACEHOLDER |
| 46 | Intervention — Improved drainage | Click to write Scale Point 1 | Click to write Scale Point 1 | 77 | `QID195_11` | PLACEHOLDER |
| 47 | Experience — Flooding of house due to any disaster (e.g., hurricane) | Weekly | Weekly | 84 | `QID124_1` | MATCH |
| 48 | Experience — In case of flooding, received help for cleaning | Weekly | Weekly | 85 | `QID124_2` | MATCH |
| 49 | Experience — Extreme heat in recent years | Daily | Daily | 86 | `QID124_3` | MATCH |
| 50 | Experience — Changing your kids' school due to moving | Weekly | Weekly | 87 | `QID124_4` | MATCH |
| 51 | Experience — Calling law enforcement because of problem with neighbors | Weekly | Weekly | 88 | `QID124_5` | MATCH |
| 52 | Experience — Losing home owners insurance due to age of home | Weekly | Weekly | 89 | `QID124_6` | MATCH |
| 53 | Experience — Well drying up | Weekly | Weekly | 90 | `QID124_7` | MATCH |
| 54 | Experience — A problem with pests in your home | Weekly | Weekly | 91 | `QID124_8` | MATCH |
| 55 | Experience — A problem with water leaks | Daily | Daily | 92 | `QID124_9` | MATCH |
| 56 | Experience — A problem with loose animals | Daily | Daily | 93 | `QID124_10` | MATCH |
| 57 | Do you (or your household) own or have regular access to a car? | Yes | Yes | 133 | `QID211` | MATCH |
| 58 | During hurricanes/disasters, have you experienced transportation problems (e.g., difficulty evacuating)? | No | No | 134 | `QID219` | MATCH |
| 59 | What is the highest level of education you have completed? | Vocational/Technical Licensing or Certification | Vocational/Technical Licensing or Certification | 142 | `QID178` | MATCH |
| 60 | Which best describes your employment status? | Retired | Retired | 143 | `QID176` | MATCH |

