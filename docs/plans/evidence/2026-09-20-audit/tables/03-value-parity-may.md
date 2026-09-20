# Table — popup value vs May 4 export, every field, every sampled point

Joined on QID (never on column position). `CSV col` is the real column index resolved from the export's `ImportId` header row. `Verbatim question` is row 1 of the CSV — the survey's own wording.

Verdicts: `MATCH` popup equals the CSV cell · `PLACEHOLDER` the CSV cell is Qualtrics placeholder junk and the popup faithfully shows it (a source-data defect, see F0/F9) · `RECODE` popup shows a label translated from a numeric code · `DIFFERENT` popup disagrees with the CSV · `EMPTY-BOTH` blank in both (correct) · `MISSING` CSV has an answer but the popup shows nothing · `NOT-IN-EXPORT` this QID has no column in this export.
## Verdict totals

| Verdict | Cells |
|---|---|
| RECODE | 729 |
| PLACEHOLDER | 389 |
| EMPTY-BOTH | 33 |
| MATCH | 30 |
| DIFFERENT | 19 |


## 1. `R_1E4YReRP6XTeX06` — 6390 Bucknell Ave

| Field | QID | CSV col | Verbatim question (CSV row 1) | CSV cell | Popup / payload shows | Verdict |
|---|---|---|---|---|---|---|
| `years_in_hre` | `QID12_TEXT` | 27 | How long have you lived in High Ridge Estates? (years) | 6 | 6 | MATCH |
| `reloc_factor_emp` | `QID181_1` | 29 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_aff` | `QID181_2` | 30 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_qol` | `QID181_3` | 31 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_fam` | `QID181_4` | 32 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_ret` | `QID181_5` | 33 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_env` | `QID181_6` | 34 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 2 | Click to write Scale Point 2 | PLACEHOLDER |
| `reloc_factor_inh` | `QID181_7` | 35 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_oth` | `QID181_8` | 36 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `mh_skirting` | `QID100` | 42 | If you live in a mobile home, does your home have its skirting intact? | 1 | Click to write Choice 3 | PLACEHOLDER |
| `anticipated_stay` | `QID47` | 44 | How long do you anticipate continuing to live in your current house? (select the most applicable choice) | 3 | Steel | RECODE |
| `safety_env` | `QID21` | 56 | Do you feel safe in your house in terms of environmental threats (e.g., flooding, heatwaves, heavy rain or win | 1 | Less than 6 months | RECODE |
| `safety_social` | `QID194` | 57 | Do you feel safe in your house in terms of social threats (e.g., loose pets, concern about neighbor's behavior | 4 | Click to write Choice 4 | PLACEHOLDER |
| `afford_urgency` | `QID17` | 58 | How would you rate the urgency of having affordable housing in High Ridge Estates? (select the most applicable | 2 | Click to write Choice 4 | PLACEHOLDER |
| `afford_strategy` | `QID19` | 59 | In your opinion, what is the most effective strategy to improve housing affordability in High Ridge Estates? ( | 1,2,4 | Yes - Portable (Which Room(s)),Yes- Integrated into central air heating system,Don’t Know | DIFFERENT |
| `intv_roof_walls` | `QID195_1` | 67 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_windows_doors` | `QID195_2` | 68 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_rain_gardens` | `QID195_3` | 69 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_hvac` | `QID195_4` | 70 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_plumbing_elec` | `QID195_5` | 71 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_well_septic` | `QID195_6` | 72 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_ccua_water` | `QID195_7` | 73 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_fence` | `QID195_8` | 74 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_trees_shade` | `QID195_9` | 75 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_trim_trees` | `QID195_10` | 76 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_drainage` | `QID195_11` | 77 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `exp_flooding` | `QID124_1` | 84 | Since you've lived in High Ridge Estates, have you experienced... - Flooding of house due to any disaster such | 2 | Weekly | RECODE |
| `exp_flood_help` | `QID124_2` | 85 | Since you've lived in High Ridge Estates, have you experienced... - In case of flooding experience, have you r | 2 | Weekly | RECODE |
| `exp_extreme_heat` | `QID124_3` | 86 | Since you've lived in High Ridge Estates, have you experienced... - Extreme heat in recent years? | 2 | Weekly | RECODE |
| `exp_school_change` | `QID124_4` | 87 | Since you've lived in High Ridge Estates, have you experienced... - Changing your kids' school due to moving? | 2 | Weekly | RECODE |
| `exp_law_enf` | `QID124_5` | 88 | Since you've lived in High Ridge Estates, have you experienced... - Calling law enforcement because of problem | 1 | Daily | RECODE |
| `exp_insurance_loss` | `QID124_6` | 89 | Since you've lived in High Ridge Estates, have you experienced... - Losing home owners insurance due to age of | 2 | Weekly | RECODE |
| `exp_well_dry` | `QID124_7` | 90 | Since you've lived in High Ridge Estates, have you experienced... - Well drying up? | 2 | Weekly | RECODE |
| `exp_pests` | `QID124_8` | 91 | Since you've lived in High Ridge Estates, have you experienced... - A problem with pests in your home? | 1 | Daily | RECODE |
| `exp_water_leaks` | `QID124_9` | 92 | Since you've lived in High Ridge Estates, have you experienced... - A problem with water leaks? | 2 | Weekly | RECODE |
| `exp_loose_animals` | `QID124_10` | 93 | Since you've lived in High Ridge Estates, have you experienced... - A problem with loose animals? | 2 | Weekly | RECODE |
| `car_access` | `QID211` | 133 | Do you (or your household) own or have regular access to a car? | 1 | Yes | RECODE |
| `hurricane_transport` | `QID219` | 134 | During disasters such as hurricanes, have you experienced transportation problems (for example, difficulty eva | 2 | No | RECODE |
| `education` | `QID178` | 142 | What is the highest level of education you have completed? (select the most applicable choice) | 9 | Vocational/Technical Licensing or Certification | RECODE |
| `employment` | `QID176` | 143 | Which best describes your employment status? | 1 | Employed- Full time | RECODE |

## 2. `R_23kV7GlWM0LQkKc` — 6176 Harvard Avenue

| Field | QID | CSV col | Verbatim question (CSV row 1) | CSV cell | Popup / payload shows | Verdict |
|---|---|---|---|---|---|---|
| `years_in_hre` | `QID12_TEXT` | 27 | How long have you lived in High Ridge Estates? (years) | 14 | 14 | MATCH |
| `reloc_factor_emp` | `QID181_1` | 29 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_aff` | `QID181_2` | 30 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 2 | Click to write Scale Point 2 | PLACEHOLDER |
| `reloc_factor_qol` | `QID181_3` | 31 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_fam` | `QID181_4` | 32 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_ret` | `QID181_5` | 33 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 2 | Click to write Scale Point 2 | PLACEHOLDER |
| `reloc_factor_env` | `QID181_6` | 34 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_inh` | `QID181_7` | 35 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_oth` | `QID181_8` | 36 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | — | — | EMPTY-BOTH |
| `mh_skirting` | `QID100` | 42 | If you live in a mobile home, does your home have its skirting intact? | 2 | Click to write Choice 4 | PLACEHOLDER |
| `anticipated_stay` | `QID47` | 44 | How long do you anticipate continuing to live in your current house? (select the most applicable choice) | 4 | Others | RECODE |
| `safety_env` | `QID21` | 56 | Do you feel safe in your house in terms of environmental threats (e.g., flooding, heatwaves, heavy rain or win | 1 | Less than 6 months | RECODE |
| `safety_social` | `QID194` | 57 | Do you feel safe in your house in terms of social threats (e.g., loose pets, concern about neighbor's behavior | 2 | More than 6 months | RECODE |
| `afford_urgency` | `QID17` | 58 | How would you rate the urgency of having affordable housing in High Ridge Estates? (select the most applicable | 1 | Click to write Choice 3 | PLACEHOLDER |
| `afford_strategy` | `QID19` | 59 | In your opinion, what is the most effective strategy to improve housing affordability in High Ridge Estates? ( | 2,3,6 | Yes- Integrated into central air heating system,No,Click to write Choice 6 | DIFFERENT |
| `intv_roof_walls` | `QID195_1` | 67 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_windows_doors` | `QID195_2` | 68 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_rain_gardens` | `QID195_3` | 69 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_hvac` | `QID195_4` | 70 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_plumbing_elec` | `QID195_5` | 71 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_well_septic` | `QID195_6` | 72 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_ccua_water` | `QID195_7` | 73 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_fence` | `QID195_8` | 74 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_trees_shade` | `QID195_9` | 75 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_trim_trees` | `QID195_10` | 76 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_drainage` | `QID195_11` | 77 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `exp_flooding` | `QID124_1` | 84 | Since you've lived in High Ridge Estates, have you experienced... - Flooding of house due to any disaster such | 2 | Weekly | RECODE |
| `exp_flood_help` | `QID124_2` | 85 | Since you've lived in High Ridge Estates, have you experienced... - In case of flooding experience, have you r | 2 | Weekly | RECODE |
| `exp_extreme_heat` | `QID124_3` | 86 | Since you've lived in High Ridge Estates, have you experienced... - Extreme heat in recent years? | 1 | Daily | RECODE |
| `exp_school_change` | `QID124_4` | 87 | Since you've lived in High Ridge Estates, have you experienced... - Changing your kids' school due to moving? | 2 | Weekly | RECODE |
| `exp_law_enf` | `QID124_5` | 88 | Since you've lived in High Ridge Estates, have you experienced... - Calling law enforcement because of problem | 2 | Weekly | RECODE |
| `exp_insurance_loss` | `QID124_6` | 89 | Since you've lived in High Ridge Estates, have you experienced... - Losing home owners insurance due to age of | 1 | Daily | RECODE |
| `exp_well_dry` | `QID124_7` | 90 | Since you've lived in High Ridge Estates, have you experienced... - Well drying up? | 2 | Weekly | RECODE |
| `exp_pests` | `QID124_8` | 91 | Since you've lived in High Ridge Estates, have you experienced... - A problem with pests in your home? | 1 | Daily | RECODE |
| `exp_water_leaks` | `QID124_9` | 92 | Since you've lived in High Ridge Estates, have you experienced... - A problem with water leaks? | 1 | Daily | RECODE |
| `exp_loose_animals` | `QID124_10` | 93 | Since you've lived in High Ridge Estates, have you experienced... - A problem with loose animals? | 1 | Daily | RECODE |
| `car_access` | `QID211` | 133 | Do you (or your household) own or have regular access to a car? | 1 | Yes | RECODE |
| `hurricane_transport` | `QID219` | 134 | During disasters such as hurricanes, have you experienced transportation problems (for example, difficulty eva | 4 | Name the problem | RECODE |
| `education` | `QID178` | 142 | What is the highest level of education you have completed? (select the most applicable choice) | 9 | Vocational/Technical Licensing or Certification | RECODE |
| `employment` | `QID176` | 143 | Which best describes your employment status? | 3 | Unemployed | RECODE |

## 3. `R_378SeCJx2uslNli` — 6369 Dennison

| Field | QID | CSV col | Verbatim question (CSV row 1) | CSV cell | Popup / payload shows | Verdict |
|---|---|---|---|---|---|---|
| `years_in_hre` | `QID12_TEXT` | 27 | How long have you lived in High Ridge Estates? (years) | 9 | 9 | MATCH |
| `reloc_factor_emp` | `QID181_1` | 29 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 4 | Click to write Scale Point 4 | PLACEHOLDER |
| `reloc_factor_aff` | `QID181_2` | 30 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 4 | Click to write Scale Point 4 | PLACEHOLDER |
| `reloc_factor_qol` | `QID181_3` | 31 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 4 | Click to write Scale Point 4 | PLACEHOLDER |
| `reloc_factor_fam` | `QID181_4` | 32 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_ret` | `QID181_5` | 33 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_env` | `QID181_6` | 34 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 4 | Click to write Scale Point 4 | PLACEHOLDER |
| `reloc_factor_inh` | `QID181_7` | 35 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_oth` | `QID181_8` | 36 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `mh_skirting` | `QID100` | 42 | If you live in a mobile home, does your home have its skirting intact? | 2 | Click to write Choice 4 | PLACEHOLDER |
| `anticipated_stay` | `QID47` | 44 | How long do you anticipate continuing to live in your current house? (select the most applicable choice) | 4 | Others | RECODE |
| `safety_env` | `QID21` | 56 | Do you feel safe in your house in terms of environmental threats (e.g., flooding, heatwaves, heavy rain or win | 3 | Don't know | RECODE |
| `safety_social` | `QID194` | 57 | Do you feel safe in your house in terms of social threats (e.g., loose pets, concern about neighbor's behavior | 3 | Don't know | RECODE |
| `afford_urgency` | `QID17` | 58 | How would you rate the urgency of having affordable housing in High Ridge Estates? (select the most applicable | 1 | Click to write Choice 3 | PLACEHOLDER |
| `afford_strategy` | `QID19` | 59 | In your opinion, what is the most effective strategy to improve housing affordability in High Ridge Estates? ( | 2,4,6 | Yes- Integrated into central air heating system,Don’t Know,Click to write Choice 6 | DIFFERENT |
| `intv_roof_walls` | `QID195_1` | 67 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_windows_doors` | `QID195_2` | 68 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_rain_gardens` | `QID195_3` | 69 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_hvac` | `QID195_4` | 70 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_plumbing_elec` | `QID195_5` | 71 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_well_septic` | `QID195_6` | 72 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_ccua_water` | `QID195_7` | 73 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_fence` | `QID195_8` | 74 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_trees_shade` | `QID195_9` | 75 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_trim_trees` | `QID195_10` | 76 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_drainage` | `QID195_11` | 77 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `exp_flooding` | `QID124_1` | 84 | Since you've lived in High Ridge Estates, have you experienced... - Flooding of house due to any disaster such | 2 | Weekly | RECODE |
| `exp_flood_help` | `QID124_2` | 85 | Since you've lived in High Ridge Estates, have you experienced... - In case of flooding experience, have you r | 2 | Weekly | RECODE |
| `exp_extreme_heat` | `QID124_3` | 86 | Since you've lived in High Ridge Estates, have you experienced... - Extreme heat in recent years? | 1 | Daily | RECODE |
| `exp_school_change` | `QID124_4` | 87 | Since you've lived in High Ridge Estates, have you experienced... - Changing your kids' school due to moving? | 2 | Weekly | RECODE |
| `exp_law_enf` | `QID124_5` | 88 | Since you've lived in High Ridge Estates, have you experienced... - Calling law enforcement because of problem | 2 | Weekly | RECODE |
| `exp_insurance_loss` | `QID124_6` | 89 | Since you've lived in High Ridge Estates, have you experienced... - Losing home owners insurance due to age of | 1 | Daily | RECODE |
| `exp_well_dry` | `QID124_7` | 90 | Since you've lived in High Ridge Estates, have you experienced... - Well drying up? | 1 | Daily | RECODE |
| `exp_pests` | `QID124_8` | 91 | Since you've lived in High Ridge Estates, have you experienced... - A problem with pests in your home? | 1 | Daily | RECODE |
| `exp_water_leaks` | `QID124_9` | 92 | Since you've lived in High Ridge Estates, have you experienced... - A problem with water leaks? | 1 | Daily | RECODE |
| `exp_loose_animals` | `QID124_10` | 93 | Since you've lived in High Ridge Estates, have you experienced... - A problem with loose animals? | 1 | Daily | RECODE |
| `car_access` | `QID211` | 133 | Do you (or your household) own or have regular access to a car? | 1 | Yes | RECODE |
| `hurricane_transport` | `QID219` | 134 | During disasters such as hurricanes, have you experienced transportation problems (for example, difficulty eva | 2 | No | RECODE |
| `education` | `QID178` | 142 | What is the highest level of education you have completed? (select the most applicable choice) | 1 | less than high school | RECODE |
| `employment` | `QID176` | 143 | Which best describes your employment status? | 3 | Unemployed | RECODE |

## 4. `R_3N0BugWZGh4ufub` — 6348 Baylor Avenue

| Field | QID | CSV col | Verbatim question (CSV row 1) | CSV cell | Popup / payload shows | Verdict |
|---|---|---|---|---|---|---|
| `years_in_hre` | `QID12_TEXT` | 27 | How long have you lived in High Ridge Estates? (years) | 6yrs | 6yrs | MATCH |
| `reloc_factor_emp` | `QID181_1` | 29 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_aff` | `QID181_2` | 30 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_qol` | `QID181_3` | 31 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_fam` | `QID181_4` | 32 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_ret` | `QID181_5` | 33 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_env` | `QID181_6` | 34 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_inh` | `QID181_7` | 35 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_oth` | `QID181_8` | 36 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `mh_skirting` | `QID100` | 42 | If you live in a mobile home, does your home have its skirting intact? | 1 | Click to write Choice 3 | PLACEHOLDER |
| `anticipated_stay` | `QID47` | 44 | How long do you anticipate continuing to live in your current house? (select the most applicable choice) | 2 | Concrete | RECODE |
| `safety_env` | `QID21` | 56 | Do you feel safe in your house in terms of environmental threats (e.g., flooding, heatwaves, heavy rain or win | 2 | More than 6 months | RECODE |
| `safety_social` | `QID194` | 57 | Do you feel safe in your house in terms of social threats (e.g., loose pets, concern about neighbor's behavior | 4 | Click to write Choice 4 | PLACEHOLDER |
| `afford_urgency` | `QID17` | 58 | How would you rate the urgency of having affordable housing in High Ridge Estates? (select the most applicable | 1 | Click to write Choice 3 | PLACEHOLDER |
| `afford_strategy` | `QID19` | 59 | In your opinion, what is the most effective strategy to improve housing affordability in High Ridge Estates? ( | 1,3,4,5,6 | Yes - Portable (Which Room(s)),No,Don’t Know,Click to write Choice 5,Click to write Choice 6 | DIFFERENT |
| `intv_roof_walls` | `QID195_1` | 67 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_windows_doors` | `QID195_2` | 68 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_rain_gardens` | `QID195_3` | 69 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_hvac` | `QID195_4` | 70 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_plumbing_elec` | `QID195_5` | 71 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_well_septic` | `QID195_6` | 72 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_ccua_water` | `QID195_7` | 73 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_fence` | `QID195_8` | 74 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_trees_shade` | `QID195_9` | 75 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_trim_trees` | `QID195_10` | 76 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_drainage` | `QID195_11` | 77 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `exp_flooding` | `QID124_1` | 84 | Since you've lived in High Ridge Estates, have you experienced... - Flooding of house due to any disaster such | 2 | Weekly | RECODE |
| `exp_flood_help` | `QID124_2` | 85 | Since you've lived in High Ridge Estates, have you experienced... - In case of flooding experience, have you r | 2 | Weekly | RECODE |
| `exp_extreme_heat` | `QID124_3` | 86 | Since you've lived in High Ridge Estates, have you experienced... - Extreme heat in recent years? | 2 | Weekly | RECODE |
| `exp_school_change` | `QID124_4` | 87 | Since you've lived in High Ridge Estates, have you experienced... - Changing your kids' school due to moving? | 2 | Weekly | RECODE |
| `exp_law_enf` | `QID124_5` | 88 | Since you've lived in High Ridge Estates, have you experienced... - Calling law enforcement because of problem | 2 | Weekly | RECODE |
| `exp_insurance_loss` | `QID124_6` | 89 | Since you've lived in High Ridge Estates, have you experienced... - Losing home owners insurance due to age of | 2 | Weekly | RECODE |
| `exp_well_dry` | `QID124_7` | 90 | Since you've lived in High Ridge Estates, have you experienced... - Well drying up? | 2 | Weekly | RECODE |
| `exp_pests` | `QID124_8` | 91 | Since you've lived in High Ridge Estates, have you experienced... - A problem with pests in your home? | 2 | Weekly | RECODE |
| `exp_water_leaks` | `QID124_9` | 92 | Since you've lived in High Ridge Estates, have you experienced... - A problem with water leaks? | 2 | Weekly | RECODE |
| `exp_loose_animals` | `QID124_10` | 93 | Since you've lived in High Ridge Estates, have you experienced... - A problem with loose animals? | 1 | Daily | RECODE |
| `car_access` | `QID211` | 133 | Do you (or your household) own or have regular access to a car? | 1 | Yes | RECODE |
| `hurricane_transport` | `QID219` | 134 | During disasters such as hurricanes, have you experienced transportation problems (for example, difficulty eva | 2 | No | RECODE |
| `education` | `QID178` | 142 | What is the highest level of education you have completed? (select the most applicable choice) | 5 | High school diploma or equivalent | RECODE |
| `employment` | `QID176` | 143 | Which best describes your employment status? | 3 | Unemployed | RECODE |

## 5. `R_43YLnrxxRNRA5hW` — 6260 Baylor Avenue

| Field | QID | CSV col | Verbatim question (CSV row 1) | CSV cell | Popup / payload shows | Verdict |
|---|---|---|---|---|---|---|
| `years_in_hre` | `QID12_TEXT` | 27 | How long have you lived in High Ridge Estates? (years) | 6 years | 6 years | MATCH |
| `reloc_factor_emp` | `QID181_1` | 29 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_aff` | `QID181_2` | 30 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 4 | Click to write Scale Point 4 | PLACEHOLDER |
| `reloc_factor_qol` | `QID181_3` | 31 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 4 | Click to write Scale Point 4 | PLACEHOLDER |
| `reloc_factor_fam` | `QID181_4` | 32 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_ret` | `QID181_5` | 33 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_env` | `QID181_6` | 34 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `reloc_factor_inh` | `QID181_7` | 35 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_oth` | `QID181_8` | 36 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | — | — | EMPTY-BOTH |
| `mh_skirting` | `QID100` | 42 | If you live in a mobile home, does your home have its skirting intact? | 1 | Click to write Choice 3 | PLACEHOLDER |
| `anticipated_stay` | `QID47` | 44 | How long do you anticipate continuing to live in your current house? (select the most applicable choice) | 4 | Others | RECODE |
| `safety_env` | `QID21` | 56 | Do you feel safe in your house in terms of environmental threats (e.g., flooding, heatwaves, heavy rain or win | 1 | Less than 6 months | RECODE |
| `safety_social` | `QID194` | 57 | Do you feel safe in your house in terms of social threats (e.g., loose pets, concern about neighbor's behavior | 1 | Less than 6 months | RECODE |
| `afford_urgency` | `QID17` | 58 | How would you rate the urgency of having affordable housing in High Ridge Estates? (select the most applicable | 2 | Click to write Choice 4 | PLACEHOLDER |
| `afford_strategy` | `QID19` | 59 | In your opinion, what is the most effective strategy to improve housing affordability in High Ridge Estates? ( | 2 | Yes- Integrated into central air heating system | RECODE |
| `intv_roof_walls` | `QID195_1` | 67 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_windows_doors` | `QID195_2` | 68 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_rain_gardens` | `QID195_3` | 69 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_hvac` | `QID195_4` | 70 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_plumbing_elec` | `QID195_5` | 71 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_well_septic` | `QID195_6` | 72 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_ccua_water` | `QID195_7` | 73 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_fence` | `QID195_8` | 74 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_trees_shade` | `QID195_9` | 75 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_trim_trees` | `QID195_10` | 76 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_drainage` | `QID195_11` | 77 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `exp_flooding` | `QID124_1` | 84 | Since you've lived in High Ridge Estates, have you experienced... - Flooding of house due to any disaster such | 2 | Weekly | RECODE |
| `exp_flood_help` | `QID124_2` | 85 | Since you've lived in High Ridge Estates, have you experienced... - In case of flooding experience, have you r | 3 | Biweekly | RECODE |
| `exp_extreme_heat` | `QID124_3` | 86 | Since you've lived in High Ridge Estates, have you experienced... - Extreme heat in recent years? | 1 | Daily | RECODE |
| `exp_school_change` | `QID124_4` | 87 | Since you've lived in High Ridge Estates, have you experienced... - Changing your kids' school due to moving? | 3 | Biweekly | RECODE |
| `exp_law_enf` | `QID124_5` | 88 | Since you've lived in High Ridge Estates, have you experienced... - Calling law enforcement because of problem | 2 | Weekly | RECODE |
| `exp_insurance_loss` | `QID124_6` | 89 | Since you've lived in High Ridge Estates, have you experienced... - Losing home owners insurance due to age of | 3 | Biweekly | RECODE |
| `exp_well_dry` | `QID124_7` | 90 | Since you've lived in High Ridge Estates, have you experienced... - Well drying up? | 3 | Biweekly | RECODE |
| `exp_pests` | `QID124_8` | 91 | Since you've lived in High Ridge Estates, have you experienced... - A problem with pests in your home? | 2 | Weekly | RECODE |
| `exp_water_leaks` | `QID124_9` | 92 | Since you've lived in High Ridge Estates, have you experienced... - A problem with water leaks? | 2 | Weekly | RECODE |
| `exp_loose_animals` | `QID124_10` | 93 | Since you've lived in High Ridge Estates, have you experienced... - A problem with loose animals? | 2 | Weekly | RECODE |
| `car_access` | `QID211` | 133 | Do you (or your household) own or have regular access to a car? | 1 | Yes | RECODE |
| `hurricane_transport` | `QID219` | 134 | During disasters such as hurricanes, have you experienced transportation problems (for example, difficulty eva | 2 | No | RECODE |
| `education` | `QID178` | 142 | What is the highest level of education you have completed? (select the most applicable choice) | 1 | less than high school | RECODE |
| `employment` | `QID176` | 143 | Which best describes your employment status? | 4 | Retired | RECODE |

## 6. `R_5241irqeSjBwQi1` — 7171 Pembroke Street

| Field | QID | CSV col | Verbatim question (CSV row 1) | CSV cell | Popup / payload shows | Verdict |
|---|---|---|---|---|---|---|
| `years_in_hre` | `QID12_TEXT` | 27 | How long have you lived in High Ridge Estates? (years) | 15 | 15 | MATCH |
| `reloc_factor_emp` | `QID181_1` | 29 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 2 | Click to write Scale Point 2 | PLACEHOLDER |
| `reloc_factor_aff` | `QID181_2` | 30 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `reloc_factor_qol` | `QID181_3` | 31 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 2 | Click to write Scale Point 2 | PLACEHOLDER |
| `reloc_factor_fam` | `QID181_4` | 32 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `reloc_factor_ret` | `QID181_5` | 33 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_env` | `QID181_6` | 34 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `reloc_factor_inh` | `QID181_7` | 35 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_oth` | `QID181_8` | 36 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | — | — | EMPTY-BOTH |
| `mh_skirting` | `QID100` | 42 | If you live in a mobile home, does your home have its skirting intact? | 1 | Click to write Choice 3 | PLACEHOLDER |
| `anticipated_stay` | `QID47` | 44 | How long do you anticipate continuing to live in your current house? (select the most applicable choice) | 4 | Others | RECODE |
| `safety_env` | `QID21` | 56 | Do you feel safe in your house in terms of environmental threats (e.g., flooding, heatwaves, heavy rain or win | 3 | Don't know | RECODE |
| `safety_social` | `QID194` | 57 | Do you feel safe in your house in terms of social threats (e.g., loose pets, concern about neighbor's behavior | 1 | Less than 6 months | RECODE |
| `afford_urgency` | `QID17` | 58 | How would you rate the urgency of having affordable housing in High Ridge Estates? (select the most applicable | 2 | Click to write Choice 4 | PLACEHOLDER |
| `afford_strategy` | `QID19` | 59 | In your opinion, what is the most effective strategy to improve housing affordability in High Ridge Estates? ( | 1,2,7 | Yes - Portable (Which Room(s)),Yes- Integrated into central air heating system,Click to write Choice 7 | DIFFERENT |
| `intv_roof_walls` | `QID195_1` | 67 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_windows_doors` | `QID195_2` | 68 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_rain_gardens` | `QID195_3` | 69 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_hvac` | `QID195_4` | 70 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_plumbing_elec` | `QID195_5` | 71 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_well_septic` | `QID195_6` | 72 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_ccua_water` | `QID195_7` | 73 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_fence` | `QID195_8` | 74 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_trees_shade` | `QID195_9` | 75 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_trim_trees` | `QID195_10` | 76 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_drainage` | `QID195_11` | 77 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `exp_flooding` | `QID124_1` | 84 | Since you've lived in High Ridge Estates, have you experienced... - Flooding of house due to any disaster such | 2 | Weekly | RECODE |
| `exp_flood_help` | `QID124_2` | 85 | Since you've lived in High Ridge Estates, have you experienced... - In case of flooding experience, have you r | 2 | Weekly | RECODE |
| `exp_extreme_heat` | `QID124_3` | 86 | Since you've lived in High Ridge Estates, have you experienced... - Extreme heat in recent years? | 2 | Weekly | RECODE |
| `exp_school_change` | `QID124_4` | 87 | Since you've lived in High Ridge Estates, have you experienced... - Changing your kids' school due to moving? | 2 | Weekly | RECODE |
| `exp_law_enf` | `QID124_5` | 88 | Since you've lived in High Ridge Estates, have you experienced... - Calling law enforcement because of problem | 2 | Weekly | RECODE |
| `exp_insurance_loss` | `QID124_6` | 89 | Since you've lived in High Ridge Estates, have you experienced... - Losing home owners insurance due to age of | 2 | Weekly | RECODE |
| `exp_well_dry` | `QID124_7` | 90 | Since you've lived in High Ridge Estates, have you experienced... - Well drying up? | 2 | Weekly | RECODE |
| `exp_pests` | `QID124_8` | 91 | Since you've lived in High Ridge Estates, have you experienced... - A problem with pests in your home? | 2 | Weekly | RECODE |
| `exp_water_leaks` | `QID124_9` | 92 | Since you've lived in High Ridge Estates, have you experienced... - A problem with water leaks? | 2 | Weekly | RECODE |
| `exp_loose_animals` | `QID124_10` | 93 | Since you've lived in High Ridge Estates, have you experienced... - A problem with loose animals? | 2 | Weekly | RECODE |
| `car_access` | `QID211` | 133 | Do you (or your household) own or have regular access to a car? | 1 | Yes | RECODE |
| `hurricane_transport` | `QID219` | 134 | During disasters such as hurricanes, have you experienced transportation problems (for example, difficulty eva | 2 | No | RECODE |
| `education` | `QID178` | 142 | What is the highest level of education you have completed? (select the most applicable choice) | 5 | High school diploma or equivalent | RECODE |
| `employment` | `QID176` | 143 | Which best describes your employment status? | 1 | Employed- Full time | RECODE |

## 7. `R_53V7a6BGdQkzzSd` — 7160 Pembroke Street

| Field | QID | CSV col | Verbatim question (CSV row 1) | CSV cell | Popup / payload shows | Verdict |
|---|---|---|---|---|---|---|
| `years_in_hre` | `QID12_TEXT` | 27 | How long have you lived in High Ridge Estates? (years) | 40yrs | 40yrs | MATCH |
| `reloc_factor_emp` | `QID181_1` | 29 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_aff` | `QID181_2` | 30 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `reloc_factor_qol` | `QID181_3` | 31 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `reloc_factor_fam` | `QID181_4` | 32 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `reloc_factor_ret` | `QID181_5` | 33 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `reloc_factor_env` | `QID181_6` | 34 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `reloc_factor_inh` | `QID181_7` | 35 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `reloc_factor_oth` | `QID181_8` | 36 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | — | — | EMPTY-BOTH |
| `mh_skirting` | `QID100` | 42 | If you live in a mobile home, does your home have its skirting intact? | 1 | Click to write Choice 3 | PLACEHOLDER |
| `anticipated_stay` | `QID47` | 44 | How long do you anticipate continuing to live in your current house? (select the most applicable choice) | 4 | Others | RECODE |
| `safety_env` | `QID21` | 56 | Do you feel safe in your house in terms of environmental threats (e.g., flooding, heatwaves, heavy rain or win | 1 | Less than 6 months | RECODE |
| `safety_social` | `QID194` | 57 | Do you feel safe in your house in terms of social threats (e.g., loose pets, concern about neighbor's behavior | 2 | More than 6 months | RECODE |
| `afford_urgency` | `QID17` | 58 | How would you rate the urgency of having affordable housing in High Ridge Estates? (select the most applicable | 1 | Click to write Choice 3 | PLACEHOLDER |
| `afford_strategy` | `QID19` | 59 | In your opinion, what is the most effective strategy to improve housing affordability in High Ridge Estates? ( | 2,6,7 | Yes- Integrated into central air heating system,Click to write Choice 6,Click to write Choice 7 | DIFFERENT |
| `intv_roof_walls` | `QID195_1` | 67 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_windows_doors` | `QID195_2` | 68 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_rain_gardens` | `QID195_3` | 69 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_hvac` | `QID195_4` | 70 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_plumbing_elec` | `QID195_5` | 71 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_well_septic` | `QID195_6` | 72 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_ccua_water` | `QID195_7` | 73 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_fence` | `QID195_8` | 74 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_trees_shade` | `QID195_9` | 75 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_trim_trees` | `QID195_10` | 76 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_drainage` | `QID195_11` | 77 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `exp_flooding` | `QID124_1` | 84 | Since you've lived in High Ridge Estates, have you experienced... - Flooding of house due to any disaster such | 2 | Weekly | RECODE |
| `exp_flood_help` | `QID124_2` | 85 | Since you've lived in High Ridge Estates, have you experienced... - In case of flooding experience, have you r | 2 | Weekly | RECODE |
| `exp_extreme_heat` | `QID124_3` | 86 | Since you've lived in High Ridge Estates, have you experienced... - Extreme heat in recent years? | 2 | Weekly | RECODE |
| `exp_school_change` | `QID124_4` | 87 | Since you've lived in High Ridge Estates, have you experienced... - Changing your kids' school due to moving? | 2 | Weekly | RECODE |
| `exp_law_enf` | `QID124_5` | 88 | Since you've lived in High Ridge Estates, have you experienced... - Calling law enforcement because of problem | 1 | Daily | RECODE |
| `exp_insurance_loss` | `QID124_6` | 89 | Since you've lived in High Ridge Estates, have you experienced... - Losing home owners insurance due to age of | 2 | Weekly | RECODE |
| `exp_well_dry` | `QID124_7` | 90 | Since you've lived in High Ridge Estates, have you experienced... - Well drying up? | 2 | Weekly | RECODE |
| `exp_pests` | `QID124_8` | 91 | Since you've lived in High Ridge Estates, have you experienced... - A problem with pests in your home? | 2 | Weekly | RECODE |
| `exp_water_leaks` | `QID124_9` | 92 | Since you've lived in High Ridge Estates, have you experienced... - A problem with water leaks? | 2 | Weekly | RECODE |
| `exp_loose_animals` | `QID124_10` | 93 | Since you've lived in High Ridge Estates, have you experienced... - A problem with loose animals? | 1 | Daily | RECODE |
| `car_access` | `QID211` | 133 | Do you (or your household) own or have regular access to a car? | 1 | Yes | RECODE |
| `hurricane_transport` | `QID219` | 134 | During disasters such as hurricanes, have you experienced transportation problems (for example, difficulty eva | 2 | No | RECODE |
| `education` | `QID178` | 142 | What is the highest level of education you have completed? (select the most applicable choice) | 5 | High school diploma or equivalent | RECODE |
| `employment` | `QID176` | 143 | Which best describes your employment status? | 4 | Retired | RECODE |

## 8. `R_5BmauNbh58cXIzf` — 6280 Dennison

| Field | QID | CSV col | Verbatim question (CSV row 1) | CSV cell | Popup / payload shows | Verdict |
|---|---|---|---|---|---|---|
| `years_in_hre` | `QID12_TEXT` | 27 | How long have you lived in High Ridge Estates? (years) | 2months | 2months | MATCH |
| `reloc_factor_emp` | `QID181_1` | 29 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_aff` | `QID181_2` | 30 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_qol` | `QID181_3` | 31 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_fam` | `QID181_4` | 32 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_ret` | `QID181_5` | 33 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_env` | `QID181_6` | 34 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_inh` | `QID181_7` | 35 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_oth` | `QID181_8` | 36 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | — | — | EMPTY-BOTH |
| `mh_skirting` | `QID100` | 42 | If you live in a mobile home, does your home have its skirting intact? | 2 | Click to write Choice 4 | PLACEHOLDER |
| `anticipated_stay` | `QID47` | 44 | How long do you anticipate continuing to live in your current house? (select the most applicable choice) | 2 | Concrete | RECODE |
| `safety_env` | `QID21` | 56 | Do you feel safe in your house in terms of environmental threats (e.g., flooding, heatwaves, heavy rain or win | 3 | Don't know | RECODE |
| `safety_social` | `QID194` | 57 | Do you feel safe in your house in terms of social threats (e.g., loose pets, concern about neighbor's behavior | 3 | Don't know | RECODE |
| `afford_urgency` | `QID17` | 58 | How would you rate the urgency of having affordable housing in High Ridge Estates? (select the most applicable | 2 | Click to write Choice 4 | PLACEHOLDER |
| `afford_strategy` | `QID19` | 59 | In your opinion, what is the most effective strategy to improve housing affordability in High Ridge Estates? ( | 2,5,6 | Yes- Integrated into central air heating system,Click to write Choice 5,Click to write Choice 6 | DIFFERENT |
| `intv_roof_walls` | `QID195_1` | 67 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_windows_doors` | `QID195_2` | 68 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_rain_gardens` | `QID195_3` | 69 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_hvac` | `QID195_4` | 70 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_plumbing_elec` | `QID195_5` | 71 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_well_septic` | `QID195_6` | 72 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_ccua_water` | `QID195_7` | 73 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_fence` | `QID195_8` | 74 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_trees_shade` | `QID195_9` | 75 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_trim_trees` | `QID195_10` | 76 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_drainage` | `QID195_11` | 77 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `exp_flooding` | `QID124_1` | 84 | Since you've lived in High Ridge Estates, have you experienced... - Flooding of house due to any disaster such | 2 | Weekly | RECODE |
| `exp_flood_help` | `QID124_2` | 85 | Since you've lived in High Ridge Estates, have you experienced... - In case of flooding experience, have you r | 2 | Weekly | RECODE |
| `exp_extreme_heat` | `QID124_3` | 86 | Since you've lived in High Ridge Estates, have you experienced... - Extreme heat in recent years? | 2 | Weekly | RECODE |
| `exp_school_change` | `QID124_4` | 87 | Since you've lived in High Ridge Estates, have you experienced... - Changing your kids' school due to moving? | 3 | Biweekly | RECODE |
| `exp_law_enf` | `QID124_5` | 88 | Since you've lived in High Ridge Estates, have you experienced... - Calling law enforcement because of problem | 2 | Weekly | RECODE |
| `exp_insurance_loss` | `QID124_6` | 89 | Since you've lived in High Ridge Estates, have you experienced... - Losing home owners insurance due to age of | 2 | Weekly | RECODE |
| `exp_well_dry` | `QID124_7` | 90 | Since you've lived in High Ridge Estates, have you experienced... - Well drying up? | 2 | Weekly | RECODE |
| `exp_pests` | `QID124_8` | 91 | Since you've lived in High Ridge Estates, have you experienced... - A problem with pests in your home? | 1 | Daily | RECODE |
| `exp_water_leaks` | `QID124_9` | 92 | Since you've lived in High Ridge Estates, have you experienced... - A problem with water leaks? | 2 | Weekly | RECODE |
| `exp_loose_animals` | `QID124_10` | 93 | Since you've lived in High Ridge Estates, have you experienced... - A problem with loose animals? | 1 | Daily | RECODE |
| `car_access` | `QID211` | 133 | Do you (or your household) own or have regular access to a car? | 1 | Yes | RECODE |
| `hurricane_transport` | `QID219` | 134 | During disasters such as hurricanes, have you experienced transportation problems (for example, difficulty eva | 3 | Not Sure | RECODE |
| `education` | `QID178` | 142 | What is the highest level of education you have completed? (select the most applicable choice) | 5 | High school diploma or equivalent | RECODE |
| `employment` | `QID176` | 143 | Which best describes your employment status? | 1 | Employed- Full time | RECODE |

## 9. `R_5CxQduTse6FT7Z4` — 7156 Duke Street

| Field | QID | CSV col | Verbatim question (CSV row 1) | CSV cell | Popup / payload shows | Verdict |
|---|---|---|---|---|---|---|
| `years_in_hre` | `QID12_TEXT` | 27 | How long have you lived in High Ridge Estates? (years) | 0 | 0 | MATCH |
| `reloc_factor_emp` | `QID181_1` | 29 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_aff` | `QID181_2` | 30 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 4 | Click to write Scale Point 4 | PLACEHOLDER |
| `reloc_factor_qol` | `QID181_3` | 31 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 4 | Click to write Scale Point 4 | PLACEHOLDER |
| `reloc_factor_fam` | `QID181_4` | 32 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `reloc_factor_ret` | `QID181_5` | 33 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_env` | `QID181_6` | 34 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_inh` | `QID181_7` | 35 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_oth` | `QID181_8` | 36 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `mh_skirting` | `QID100` | 42 | If you live in a mobile home, does your home have its skirting intact? | 2 | Click to write Choice 4 | PLACEHOLDER |
| `anticipated_stay` | `QID47` | 44 | How long do you anticipate continuing to live in your current house? (select the most applicable choice) | 2 | Concrete | RECODE |
| `safety_env` | `QID21` | 56 | Do you feel safe in your house in terms of environmental threats (e.g., flooding, heatwaves, heavy rain or win | 2 | More than 6 months | RECODE |
| `safety_social` | `QID194` | 57 | Do you feel safe in your house in terms of social threats (e.g., loose pets, concern about neighbor's behavior | 2 | More than 6 months | RECODE |
| `afford_urgency` | `QID17` | 58 | How would you rate the urgency of having affordable housing in High Ridge Estates? (select the most applicable | 1 | Click to write Choice 3 | PLACEHOLDER |
| `afford_strategy` | `QID19` | 59 | In your opinion, what is the most effective strategy to improve housing affordability in High Ridge Estates? ( | 1 | Yes - Portable (Which Room(s)) | RECODE |
| `intv_roof_walls` | `QID195_1` | 67 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_windows_doors` | `QID195_2` | 68 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_rain_gardens` | `QID195_3` | 69 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_hvac` | `QID195_4` | 70 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_plumbing_elec` | `QID195_5` | 71 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_well_septic` | `QID195_6` | 72 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_ccua_water` | `QID195_7` | 73 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_fence` | `QID195_8` | 74 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_trees_shade` | `QID195_9` | 75 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_trim_trees` | `QID195_10` | 76 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_drainage` | `QID195_11` | 77 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `exp_flooding` | `QID124_1` | 84 | Since you've lived in High Ridge Estates, have you experienced... - Flooding of house due to any disaster such | 2 | Weekly | RECODE |
| `exp_flood_help` | `QID124_2` | 85 | Since you've lived in High Ridge Estates, have you experienced... - In case of flooding experience, have you r | 2 | Weekly | RECODE |
| `exp_extreme_heat` | `QID124_3` | 86 | Since you've lived in High Ridge Estates, have you experienced... - Extreme heat in recent years? | 1 | Daily | RECODE |
| `exp_school_change` | `QID124_4` | 87 | Since you've lived in High Ridge Estates, have you experienced... - Changing your kids' school due to moving? | 1 | Daily | RECODE |
| `exp_law_enf` | `QID124_5` | 88 | Since you've lived in High Ridge Estates, have you experienced... - Calling law enforcement because of problem | 2 | Weekly | RECODE |
| `exp_insurance_loss` | `QID124_6` | 89 | Since you've lived in High Ridge Estates, have you experienced... - Losing home owners insurance due to age of | 2 | Weekly | RECODE |
| `exp_well_dry` | `QID124_7` | 90 | Since you've lived in High Ridge Estates, have you experienced... - Well drying up? | 3 | Biweekly | RECODE |
| `exp_pests` | `QID124_8` | 91 | Since you've lived in High Ridge Estates, have you experienced... - A problem with pests in your home? | 2 | Weekly | RECODE |
| `exp_water_leaks` | `QID124_9` | 92 | Since you've lived in High Ridge Estates, have you experienced... - A problem with water leaks? | 2 | Weekly | RECODE |
| `exp_loose_animals` | `QID124_10` | 93 | Since you've lived in High Ridge Estates, have you experienced... - A problem with loose animals? | 2 | Weekly | RECODE |
| `car_access` | `QID211` | 133 | Do you (or your household) own or have regular access to a car? | 1 | Yes | RECODE |
| `hurricane_transport` | `QID219` | 134 | During disasters such as hurricanes, have you experienced transportation problems (for example, difficulty eva | 2 | No | RECODE |
| `education` | `QID178` | 142 | What is the highest level of education you have completed? (select the most applicable choice) | 8 | Graduate Degree | RECODE |
| `employment` | `QID176` | 143 | Which best describes your employment status? | 1 | Employed- Full time | RECODE |

## 10. `R_5TtaBRz99nWhzm1` — 7173 Duke Street

| Field | QID | CSV col | Verbatim question (CSV row 1) | CSV cell | Popup / payload shows | Verdict |
|---|---|---|---|---|---|---|
| `years_in_hre` | `QID12_TEXT` | 27 | How long have you lived in High Ridge Estates? (years) | 37 | 37 | MATCH |
| `reloc_factor_emp` | `QID181_1` | 29 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 4 | Click to write Scale Point 4 | PLACEHOLDER |
| `reloc_factor_aff` | `QID181_2` | 30 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 4 | Click to write Scale Point 4 | PLACEHOLDER |
| `reloc_factor_qol` | `QID181_3` | 31 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `reloc_factor_fam` | `QID181_4` | 32 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_ret` | `QID181_5` | 33 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `reloc_factor_env` | `QID181_6` | 34 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `reloc_factor_inh` | `QID181_7` | 35 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_oth` | `QID181_8` | 36 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | — | — | EMPTY-BOTH |
| `mh_skirting` | `QID100` | 42 | If you live in a mobile home, does your home have its skirting intact? | 1 | Click to write Choice 3 | PLACEHOLDER |
| `anticipated_stay` | `QID47` | 44 | How long do you anticipate continuing to live in your current house? (select the most applicable choice) | 4 | Others | RECODE |
| `safety_env` | `QID21` | 56 | Do you feel safe in your house in terms of environmental threats (e.g., flooding, heatwaves, heavy rain or win | 1 | Less than 6 months | RECODE |
| `safety_social` | `QID194` | 57 | Do you feel safe in your house in terms of social threats (e.g., loose pets, concern about neighbor's behavior | 3 | Don't know | RECODE |
| `afford_urgency` | `QID17` | 58 | How would you rate the urgency of having affordable housing in High Ridge Estates? (select the most applicable | 3 | Click to write Choice 5 | PLACEHOLDER |
| `afford_strategy` | `QID19` | 59 | In your opinion, what is the most effective strategy to improve housing affordability in High Ridge Estates? ( | 2,6,7 | Yes- Integrated into central air heating system,Click to write Choice 6,Click to write Choice 7 | DIFFERENT |
| `intv_roof_walls` | `QID195_1` | 67 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_windows_doors` | `QID195_2` | 68 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_rain_gardens` | `QID195_3` | 69 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_hvac` | `QID195_4` | 70 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_plumbing_elec` | `QID195_5` | 71 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_well_septic` | `QID195_6` | 72 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_ccua_water` | `QID195_7` | 73 | Please indicate whether you would like or would not like to have the following interventions to improve your h | — | — | EMPTY-BOTH |
| `intv_fence` | `QID195_8` | 74 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_trees_shade` | `QID195_9` | 75 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_trim_trees` | `QID195_10` | 76 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_drainage` | `QID195_11` | 77 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `exp_flooding` | `QID124_1` | 84 | Since you've lived in High Ridge Estates, have you experienced... - Flooding of house due to any disaster such | 2 | Weekly | RECODE |
| `exp_flood_help` | `QID124_2` | 85 | Since you've lived in High Ridge Estates, have you experienced... - In case of flooding experience, have you r | 2 | Weekly | RECODE |
| `exp_extreme_heat` | `QID124_3` | 86 | Since you've lived in High Ridge Estates, have you experienced... - Extreme heat in recent years? | 1 | Daily | RECODE |
| `exp_school_change` | `QID124_4` | 87 | Since you've lived in High Ridge Estates, have you experienced... - Changing your kids' school due to moving? | 3 | Biweekly | RECODE |
| `exp_law_enf` | `QID124_5` | 88 | Since you've lived in High Ridge Estates, have you experienced... - Calling law enforcement because of problem | — | — | EMPTY-BOTH |
| `exp_insurance_loss` | `QID124_6` | 89 | Since you've lived in High Ridge Estates, have you experienced... - Losing home owners insurance due to age of | 1 | Daily | RECODE |
| `exp_well_dry` | `QID124_7` | 90 | Since you've lived in High Ridge Estates, have you experienced... - Well drying up? | 2 | Weekly | RECODE |
| `exp_pests` | `QID124_8` | 91 | Since you've lived in High Ridge Estates, have you experienced... - A problem with pests in your home? | 2 | Weekly | RECODE |
| `exp_water_leaks` | `QID124_9` | 92 | Since you've lived in High Ridge Estates, have you experienced... - A problem with water leaks? | 2 | Weekly | RECODE |
| `exp_loose_animals` | `QID124_10` | 93 | Since you've lived in High Ridge Estates, have you experienced... - A problem with loose animals? | 2 | Weekly | RECODE |
| `car_access` | `QID211` | 133 | Do you (or your household) own or have regular access to a car? | 1 | Yes | RECODE |
| `hurricane_transport` | `QID219` | 134 | During disasters such as hurricanes, have you experienced transportation problems (for example, difficulty eva | 4 | Name the problem | RECODE |
| `education` | `QID178` | 142 | What is the highest level of education you have completed? (select the most applicable choice) | 5 | High school diploma or equivalent | RECODE |
| `employment` | `QID176` | 143 | Which best describes your employment status? | 4 | Retired | RECODE |

## 11. `R_5tJl6j6gNRyLVMe` — 6220 Colgate Rd

| Field | QID | CSV col | Verbatim question (CSV row 1) | CSV cell | Popup / payload shows | Verdict |
|---|---|---|---|---|---|---|
| `years_in_hre` | `QID12_TEXT` | 27 | How long have you lived in High Ridge Estates? (years) | 6 mo | 6 mo | MATCH |
| `reloc_factor_emp` | `QID181_1` | 29 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_aff` | `QID181_2` | 30 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_qol` | `QID181_3` | 31 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_fam` | `QID181_4` | 32 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_ret` | `QID181_5` | 33 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_env` | `QID181_6` | 34 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 4 | Click to write Scale Point 4 | PLACEHOLDER |
| `reloc_factor_inh` | `QID181_7` | 35 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_oth` | `QID181_8` | 36 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | — | — | EMPTY-BOTH |
| `mh_skirting` | `QID100` | 42 | If you live in a mobile home, does your home have its skirting intact? | 2 | Click to write Choice 4 | PLACEHOLDER |
| `anticipated_stay` | `QID47` | 44 | How long do you anticipate continuing to live in your current house? (select the most applicable choice) | 4 | Others | RECODE |
| `safety_env` | `QID21` | 56 | Do you feel safe in your house in terms of environmental threats (e.g., flooding, heatwaves, heavy rain or win | 1 | Less than 6 months | RECODE |
| `safety_social` | `QID194` | 57 | Do you feel safe in your house in terms of social threats (e.g., loose pets, concern about neighbor's behavior | 2 | More than 6 months | RECODE |
| `afford_urgency` | `QID17` | 58 | How would you rate the urgency of having affordable housing in High Ridge Estates? (select the most applicable | 1 | Click to write Choice 3 | PLACEHOLDER |
| `afford_strategy` | `QID19` | 59 | In your opinion, what is the most effective strategy to improve housing affordability in High Ridge Estates? ( | 2,3 | Yes- Integrated into central air heating system,No | DIFFERENT |
| `intv_roof_walls` | `QID195_1` | 67 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_windows_doors` | `QID195_2` | 68 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_rain_gardens` | `QID195_3` | 69 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_hvac` | `QID195_4` | 70 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_plumbing_elec` | `QID195_5` | 71 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_well_septic` | `QID195_6` | 72 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_ccua_water` | `QID195_7` | 73 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_fence` | `QID195_8` | 74 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_trees_shade` | `QID195_9` | 75 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_trim_trees` | `QID195_10` | 76 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_drainage` | `QID195_11` | 77 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `exp_flooding` | `QID124_1` | 84 | Since you've lived in High Ridge Estates, have you experienced... - Flooding of house due to any disaster such | 2 | Weekly | RECODE |
| `exp_flood_help` | `QID124_2` | 85 | Since you've lived in High Ridge Estates, have you experienced... - In case of flooding experience, have you r | 2 | Weekly | RECODE |
| `exp_extreme_heat` | `QID124_3` | 86 | Since you've lived in High Ridge Estates, have you experienced... - Extreme heat in recent years? | 1 | Daily | RECODE |
| `exp_school_change` | `QID124_4` | 87 | Since you've lived in High Ridge Estates, have you experienced... - Changing your kids' school due to moving? | 2 | Weekly | RECODE |
| `exp_law_enf` | `QID124_5` | 88 | Since you've lived in High Ridge Estates, have you experienced... - Calling law enforcement because of problem | 2 | Weekly | RECODE |
| `exp_insurance_loss` | `QID124_6` | 89 | Since you've lived in High Ridge Estates, have you experienced... - Losing home owners insurance due to age of | 2 | Weekly | RECODE |
| `exp_well_dry` | `QID124_7` | 90 | Since you've lived in High Ridge Estates, have you experienced... - Well drying up? | 2 | Weekly | RECODE |
| `exp_pests` | `QID124_8` | 91 | Since you've lived in High Ridge Estates, have you experienced... - A problem with pests in your home? | 2 | Weekly | RECODE |
| `exp_water_leaks` | `QID124_9` | 92 | Since you've lived in High Ridge Estates, have you experienced... - A problem with water leaks? | 2 | Weekly | RECODE |
| `exp_loose_animals` | `QID124_10` | 93 | Since you've lived in High Ridge Estates, have you experienced... - A problem with loose animals? | 1 | Daily | RECODE |
| `car_access` | `QID211` | 133 | Do you (or your household) own or have regular access to a car? | 1 | Yes | RECODE |
| `hurricane_transport` | `QID219` | 134 | During disasters such as hurricanes, have you experienced transportation problems (for example, difficulty eva | 2 | No | RECODE |
| `education` | `QID178` | 142 | What is the highest level of education you have completed? (select the most applicable choice) | 5 | High school diploma or equivalent | RECODE |
| `employment` | `QID176` | 143 | Which best describes your employment status? | 2 | Employed - Part time | RECODE |

## 12. `R_6SGNzs6svx7pBbb` — Dennison

| Field | QID | CSV col | Verbatim question (CSV row 1) | CSV cell | Popup / payload shows | Verdict |
|---|---|---|---|---|---|---|
| `years_in_hre` | `QID12_TEXT` | 27 | How long have you lived in High Ridge Estates? (years) | 17 years | 17 years | MATCH |
| `reloc_factor_emp` | `QID181_1` | 29 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 4 | Click to write Scale Point 4 | PLACEHOLDER |
| `reloc_factor_aff` | `QID181_2` | 30 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_qol` | `QID181_3` | 31 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_fam` | `QID181_4` | 32 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_ret` | `QID181_5` | 33 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_env` | `QID181_6` | 34 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_inh` | `QID181_7` | 35 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_oth` | `QID181_8` | 36 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | — | — | EMPTY-BOTH |
| `mh_skirting` | `QID100` | 42 | If you live in a mobile home, does your home have its skirting intact? | 1 | Click to write Choice 3 | PLACEHOLDER |
| `anticipated_stay` | `QID47` | 44 | How long do you anticipate continuing to live in your current house? (select the most applicable choice) | 4 | Others | RECODE |
| `safety_env` | `QID21` | 56 | Do you feel safe in your house in terms of environmental threats (e.g., flooding, heatwaves, heavy rain or win | 2 | More than 6 months | RECODE |
| `safety_social` | `QID194` | 57 | Do you feel safe in your house in terms of social threats (e.g., loose pets, concern about neighbor's behavior | 2 | More than 6 months | RECODE |
| `afford_urgency` | `QID17` | 58 | How would you rate the urgency of having affordable housing in High Ridge Estates? (select the most applicable | — | — | EMPTY-BOTH |
| `afford_strategy` | `QID19` | 59 | In your opinion, what is the most effective strategy to improve housing affordability in High Ridge Estates? ( | 2,3,6 | Yes- Integrated into central air heating system,No,Click to write Choice 6 | DIFFERENT |
| `intv_roof_walls` | `QID195_1` | 67 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_windows_doors` | `QID195_2` | 68 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_rain_gardens` | `QID195_3` | 69 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_hvac` | `QID195_4` | 70 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_plumbing_elec` | `QID195_5` | 71 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_well_septic` | `QID195_6` | 72 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_ccua_water` | `QID195_7` | 73 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_fence` | `QID195_8` | 74 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_trees_shade` | `QID195_9` | 75 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_trim_trees` | `QID195_10` | 76 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_drainage` | `QID195_11` | 77 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `exp_flooding` | `QID124_1` | 84 | Since you've lived in High Ridge Estates, have you experienced... - Flooding of house due to any disaster such | 2 | Weekly | RECODE |
| `exp_flood_help` | `QID124_2` | 85 | Since you've lived in High Ridge Estates, have you experienced... - In case of flooding experience, have you r | 2 | Weekly | RECODE |
| `exp_extreme_heat` | `QID124_3` | 86 | Since you've lived in High Ridge Estates, have you experienced... - Extreme heat in recent years? | 1 | Daily | RECODE |
| `exp_school_change` | `QID124_4` | 87 | Since you've lived in High Ridge Estates, have you experienced... - Changing your kids' school due to moving? | 2 | Weekly | RECODE |
| `exp_law_enf` | `QID124_5` | 88 | Since you've lived in High Ridge Estates, have you experienced... - Calling law enforcement because of problem | 2 | Weekly | RECODE |
| `exp_insurance_loss` | `QID124_6` | 89 | Since you've lived in High Ridge Estates, have you experienced... - Losing home owners insurance due to age of | 2 | Weekly | RECODE |
| `exp_well_dry` | `QID124_7` | 90 | Since you've lived in High Ridge Estates, have you experienced... - Well drying up? | 1 | Daily | RECODE |
| `exp_pests` | `QID124_8` | 91 | Since you've lived in High Ridge Estates, have you experienced... - A problem with pests in your home? | 1 | Daily | RECODE |
| `exp_water_leaks` | `QID124_9` | 92 | Since you've lived in High Ridge Estates, have you experienced... - A problem with water leaks? | 2 | Weekly | RECODE |
| `exp_loose_animals` | `QID124_10` | 93 | Since you've lived in High Ridge Estates, have you experienced... - A problem with loose animals? | 2 | Weekly | RECODE |
| `car_access` | `QID211` | 133 | Do you (or your household) own or have regular access to a car? | 1 | Yes | RECODE |
| `hurricane_transport` | `QID219` | 134 | During disasters such as hurricanes, have you experienced transportation problems (for example, difficulty eva | 2 | No | RECODE |
| `education` | `QID178` | 142 | What is the highest level of education you have completed? (select the most applicable choice) | 5 | High school diploma or equivalent | RECODE |
| `employment` | `QID176` | 143 | Which best describes your employment status? | 4 | Retired | RECODE |

## 13. `R_6s0PVusMDUucFQY` — Dennison

| Field | QID | CSV col | Verbatim question (CSV row 1) | CSV cell | Popup / payload shows | Verdict |
|---|---|---|---|---|---|---|
| `years_in_hre` | `QID12_TEXT` | 27 | How long have you lived in High Ridge Estates? (years) | 5 years | 5 years | MATCH |
| `reloc_factor_emp` | `QID181_1` | 29 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 4 | Click to write Scale Point 4 | PLACEHOLDER |
| `reloc_factor_aff` | `QID181_2` | 30 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 4 | Click to write Scale Point 4 | PLACEHOLDER |
| `reloc_factor_qol` | `QID181_3` | 31 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 4 | Click to write Scale Point 4 | PLACEHOLDER |
| `reloc_factor_fam` | `QID181_4` | 32 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_ret` | `QID181_5` | 33 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_env` | `QID181_6` | 34 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_inh` | `QID181_7` | 35 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_oth` | `QID181_8` | 36 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `mh_skirting` | `QID100` | 42 | If you live in a mobile home, does your home have its skirting intact? | 1 | Click to write Choice 3 | PLACEHOLDER |
| `anticipated_stay` | `QID47` | 44 | How long do you anticipate continuing to live in your current house? (select the most applicable choice) | 5 | Don't know | RECODE |
| `safety_env` | `QID21` | 56 | Do you feel safe in your house in terms of environmental threats (e.g., flooding, heatwaves, heavy rain or win | 2 | More than 6 months | RECODE |
| `safety_social` | `QID194` | 57 | Do you feel safe in your house in terms of social threats (e.g., loose pets, concern about neighbor's behavior | 3 | Don't know | RECODE |
| `afford_urgency` | `QID17` | 58 | How would you rate the urgency of having affordable housing in High Ridge Estates? (select the most applicable | 1 | Click to write Choice 3 | PLACEHOLDER |
| `afford_strategy` | `QID19` | 59 | In your opinion, what is the most effective strategy to improve housing affordability in High Ridge Estates? ( | 1,2,4 | Yes - Portable (Which Room(s)),Yes- Integrated into central air heating system,Don’t Know | DIFFERENT |
| `intv_roof_walls` | `QID195_1` | 67 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_windows_doors` | `QID195_2` | 68 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_rain_gardens` | `QID195_3` | 69 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_hvac` | `QID195_4` | 70 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_plumbing_elec` | `QID195_5` | 71 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_well_septic` | `QID195_6` | 72 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_ccua_water` | `QID195_7` | 73 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_fence` | `QID195_8` | 74 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_trees_shade` | `QID195_9` | 75 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_trim_trees` | `QID195_10` | 76 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_drainage` | `QID195_11` | 77 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `exp_flooding` | `QID124_1` | 84 | Since you've lived in High Ridge Estates, have you experienced... - Flooding of house due to any disaster such | 2 | Weekly | RECODE |
| `exp_flood_help` | `QID124_2` | 85 | Since you've lived in High Ridge Estates, have you experienced... - In case of flooding experience, have you r | — | — | EMPTY-BOTH |
| `exp_extreme_heat` | `QID124_3` | 86 | Since you've lived in High Ridge Estates, have you experienced... - Extreme heat in recent years? | 1 | Daily | RECODE |
| `exp_school_change` | `QID124_4` | 87 | Since you've lived in High Ridge Estates, have you experienced... - Changing your kids' school due to moving? | 2 | Weekly | RECODE |
| `exp_law_enf` | `QID124_5` | 88 | Since you've lived in High Ridge Estates, have you experienced... - Calling law enforcement because of problem | 1 | Daily | RECODE |
| `exp_insurance_loss` | `QID124_6` | 89 | Since you've lived in High Ridge Estates, have you experienced... - Losing home owners insurance due to age of | 2 | Weekly | RECODE |
| `exp_well_dry` | `QID124_7` | 90 | Since you've lived in High Ridge Estates, have you experienced... - Well drying up? | 2 | Weekly | RECODE |
| `exp_pests` | `QID124_8` | 91 | Since you've lived in High Ridge Estates, have you experienced... - A problem with pests in your home? | 3 | Biweekly | RECODE |
| `exp_water_leaks` | `QID124_9` | 92 | Since you've lived in High Ridge Estates, have you experienced... - A problem with water leaks? | 1 | Daily | RECODE |
| `exp_loose_animals` | `QID124_10` | 93 | Since you've lived in High Ridge Estates, have you experienced... - A problem with loose animals? | 1 | Daily | RECODE |
| `car_access` | `QID211` | 133 | Do you (or your household) own or have regular access to a car? | 1 | Yes | RECODE |
| `hurricane_transport` | `QID219` | 134 | During disasters such as hurricanes, have you experienced transportation problems (for example, difficulty eva | 2 | No | RECODE |
| `education` | `QID178` | 142 | What is the highest level of education you have completed? (select the most applicable choice) | 5 | High school diploma or equivalent | RECODE |
| `employment` | `QID176` | 143 | Which best describes your employment status? | 2 | Employed - Part time | RECODE |

## 14. `R_6xzTr24XxYm8KC4` — 7276 Temple

| Field | QID | CSV col | Verbatim question (CSV row 1) | CSV cell | Popup / payload shows | Verdict |
|---|---|---|---|---|---|---|
| `years_in_hre` | `QID12_TEXT` | 27 | How long have you lived in High Ridge Estates? (years) | 1 | 1 | MATCH |
| `reloc_factor_emp` | `QID181_1` | 29 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_aff` | `QID181_2` | 30 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `reloc_factor_qol` | `QID181_3` | 31 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_fam` | `QID181_4` | 32 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_ret` | `QID181_5` | 33 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_env` | `QID181_6` | 34 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `reloc_factor_inh` | `QID181_7` | 35 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_oth` | `QID181_8` | 36 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `mh_skirting` | `QID100` | 42 | If you live in a mobile home, does your home have its skirting intact? | 2 | Click to write Choice 4 | PLACEHOLDER |
| `anticipated_stay` | `QID47` | 44 | How long do you anticipate continuing to live in your current house? (select the most applicable choice) | 5 | Don't know | RECODE |
| `safety_env` | `QID21` | 56 | Do you feel safe in your house in terms of environmental threats (e.g., flooding, heatwaves, heavy rain or win | 3 | Don't know | RECODE |
| `safety_social` | `QID194` | 57 | Do you feel safe in your house in terms of social threats (e.g., loose pets, concern about neighbor's behavior | 5 | Click to write Choice 5 | PLACEHOLDER |
| `afford_urgency` | `QID17` | 58 | How would you rate the urgency of having affordable housing in High Ridge Estates? (select the most applicable | 1 | Click to write Choice 3 | PLACEHOLDER |
| `afford_strategy` | `QID19` | 59 | In your opinion, what is the most effective strategy to improve housing affordability in High Ridge Estates? ( | 4,6 | Don’t Know,Click to write Choice 6 | DIFFERENT |
| `intv_roof_walls` | `QID195_1` | 67 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_windows_doors` | `QID195_2` | 68 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_rain_gardens` | `QID195_3` | 69 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_hvac` | `QID195_4` | 70 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_plumbing_elec` | `QID195_5` | 71 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_well_septic` | `QID195_6` | 72 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_ccua_water` | `QID195_7` | 73 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_fence` | `QID195_8` | 74 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_trees_shade` | `QID195_9` | 75 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_trim_trees` | `QID195_10` | 76 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_drainage` | `QID195_11` | 77 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `exp_flooding` | `QID124_1` | 84 | Since you've lived in High Ridge Estates, have you experienced... - Flooding of house due to any disaster such | 2 | Weekly | RECODE |
| `exp_flood_help` | `QID124_2` | 85 | Since you've lived in High Ridge Estates, have you experienced... - In case of flooding experience, have you r | 2 | Weekly | RECODE |
| `exp_extreme_heat` | `QID124_3` | 86 | Since you've lived in High Ridge Estates, have you experienced... - Extreme heat in recent years? | 1 | Daily | RECODE |
| `exp_school_change` | `QID124_4` | 87 | Since you've lived in High Ridge Estates, have you experienced... - Changing your kids' school due to moving? | 1 | Daily | RECODE |
| `exp_law_enf` | `QID124_5` | 88 | Since you've lived in High Ridge Estates, have you experienced... - Calling law enforcement because of problem | 1 | Daily | RECODE |
| `exp_insurance_loss` | `QID124_6` | 89 | Since you've lived in High Ridge Estates, have you experienced... - Losing home owners insurance due to age of | 1 | Daily | RECODE |
| `exp_well_dry` | `QID124_7` | 90 | Since you've lived in High Ridge Estates, have you experienced... - Well drying up? | 2 | Weekly | RECODE |
| `exp_pests` | `QID124_8` | 91 | Since you've lived in High Ridge Estates, have you experienced... - A problem with pests in your home? | 2 | Weekly | RECODE |
| `exp_water_leaks` | `QID124_9` | 92 | Since you've lived in High Ridge Estates, have you experienced... - A problem with water leaks? | 2 | Weekly | RECODE |
| `exp_loose_animals` | `QID124_10` | 93 | Since you've lived in High Ridge Estates, have you experienced... - A problem with loose animals? | 1 | Daily | RECODE |
| `car_access` | `QID211` | 133 | Do you (or your household) own or have regular access to a car? | 1 | Yes | RECODE |
| `hurricane_transport` | `QID219` | 134 | During disasters such as hurricanes, have you experienced transportation problems (for example, difficulty eva | 2 | No | RECODE |
| `education` | `QID178` | 142 | What is the highest level of education you have completed? (select the most applicable choice) | 6 | Some college, no degree | RECODE |
| `employment` | `QID176` | 143 | Which best describes your employment status? | 1 | Employed- Full time | RECODE |

## 15. `R_71LqP7xFx71BPsl` — Baylor Ave

| Field | QID | CSV col | Verbatim question (CSV row 1) | CSV cell | Popup / payload shows | Verdict |
|---|---|---|---|---|---|---|
| `years_in_hre` | `QID12_TEXT` | 27 | How long have you lived in High Ridge Estates? (years) | 1 | 1 | MATCH |
| `reloc_factor_emp` | `QID181_1` | 29 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_aff` | `QID181_2` | 30 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 2 | Click to write Scale Point 2 | PLACEHOLDER |
| `reloc_factor_qol` | `QID181_3` | 31 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_fam` | `QID181_4` | 32 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 4 | Click to write Scale Point 4 | PLACEHOLDER |
| `reloc_factor_ret` | `QID181_5` | 33 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_env` | `QID181_6` | 34 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_inh` | `QID181_7` | 35 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 4 | Click to write Scale Point 4 | PLACEHOLDER |
| `reloc_factor_oth` | `QID181_8` | 36 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `mh_skirting` | `QID100` | 42 | If you live in a mobile home, does your home have its skirting intact? | 2 | Click to write Choice 4 | PLACEHOLDER |
| `anticipated_stay` | `QID47` | 44 | How long do you anticipate continuing to live in your current house? (select the most applicable choice) | 4 | Others | RECODE |
| `safety_env` | `QID21` | 56 | Do you feel safe in your house in terms of environmental threats (e.g., flooding, heatwaves, heavy rain or win | 2 | More than 6 months | RECODE |
| `safety_social` | `QID194` | 57 | Do you feel safe in your house in terms of social threats (e.g., loose pets, concern about neighbor's behavior | 3 | Don't know | RECODE |
| `afford_urgency` | `QID17` | 58 | How would you rate the urgency of having affordable housing in High Ridge Estates? (select the most applicable | 2 | Click to write Choice 4 | PLACEHOLDER |
| `afford_strategy` | `QID19` | 59 | In your opinion, what is the most effective strategy to improve housing affordability in High Ridge Estates? ( | 1,2,4 | Yes - Portable (Which Room(s)),Yes- Integrated into central air heating system,Don’t Know | DIFFERENT |
| `intv_roof_walls` | `QID195_1` | 67 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_windows_doors` | `QID195_2` | 68 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_rain_gardens` | `QID195_3` | 69 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_hvac` | `QID195_4` | 70 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_plumbing_elec` | `QID195_5` | 71 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_well_septic` | `QID195_6` | 72 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_ccua_water` | `QID195_7` | 73 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_fence` | `QID195_8` | 74 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_trees_shade` | `QID195_9` | 75 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_trim_trees` | `QID195_10` | 76 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_drainage` | `QID195_11` | 77 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `exp_flooding` | `QID124_1` | 84 | Since you've lived in High Ridge Estates, have you experienced... - Flooding of house due to any disaster such | 2 | Weekly | RECODE |
| `exp_flood_help` | `QID124_2` | 85 | Since you've lived in High Ridge Estates, have you experienced... - In case of flooding experience, have you r | 2 | Weekly | RECODE |
| `exp_extreme_heat` | `QID124_3` | 86 | Since you've lived in High Ridge Estates, have you experienced... - Extreme heat in recent years? | 2 | Weekly | RECODE |
| `exp_school_change` | `QID124_4` | 87 | Since you've lived in High Ridge Estates, have you experienced... - Changing your kids' school due to moving? | 2 | Weekly | RECODE |
| `exp_law_enf` | `QID124_5` | 88 | Since you've lived in High Ridge Estates, have you experienced... - Calling law enforcement because of problem | 2 | Weekly | RECODE |
| `exp_insurance_loss` | `QID124_6` | 89 | Since you've lived in High Ridge Estates, have you experienced... - Losing home owners insurance due to age of | 2 | Weekly | RECODE |
| `exp_well_dry` | `QID124_7` | 90 | Since you've lived in High Ridge Estates, have you experienced... - Well drying up? | 2 | Weekly | RECODE |
| `exp_pests` | `QID124_8` | 91 | Since you've lived in High Ridge Estates, have you experienced... - A problem with pests in your home? | 1 | Daily | RECODE |
| `exp_water_leaks` | `QID124_9` | 92 | Since you've lived in High Ridge Estates, have you experienced... - A problem with water leaks? | 1 | Daily | RECODE |
| `exp_loose_animals` | `QID124_10` | 93 | Since you've lived in High Ridge Estates, have you experienced... - A problem with loose animals? | 1 | Daily | RECODE |
| `car_access` | `QID211` | 133 | Do you (or your household) own or have regular access to a car? | 1 | Yes | RECODE |
| `hurricane_transport` | `QID219` | 134 | During disasters such as hurricanes, have you experienced transportation problems (for example, difficulty eva | 2 | No | RECODE |
| `education` | `QID178` | 142 | What is the highest level of education you have completed? (select the most applicable choice) | 5 | High school diploma or equivalent | RECODE |
| `employment` | `QID176` | 143 | Which best describes your employment status? | 3 | Unemployed | RECODE |

## 16. `R_78TZ7UtnmZU0jKm` — 7201 Notre Dame St

| Field | QID | CSV col | Verbatim question (CSV row 1) | CSV cell | Popup / payload shows | Verdict |
|---|---|---|---|---|---|---|
| `years_in_hre` | `QID12_TEXT` | 27 | How long have you lived in High Ridge Estates? (years) | 5 years | 5 years | MATCH |
| `reloc_factor_emp` | `QID181_1` | 29 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_aff` | `QID181_2` | 30 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_qol` | `QID181_3` | 31 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `reloc_factor_fam` | `QID181_4` | 32 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_ret` | `QID181_5` | 33 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 4 | Click to write Scale Point 4 | PLACEHOLDER |
| `reloc_factor_env` | `QID181_6` | 34 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 4 | Click to write Scale Point 4 | PLACEHOLDER |
| `reloc_factor_inh` | `QID181_7` | 35 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_oth` | `QID181_8` | 36 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | — | — | EMPTY-BOTH |
| `mh_skirting` | `QID100` | 42 | If you live in a mobile home, does your home have its skirting intact? | 1 | Click to write Choice 3 | PLACEHOLDER |
| `anticipated_stay` | `QID47` | 44 | How long do you anticipate continuing to live in your current house? (select the most applicable choice) | 2 | Concrete | RECODE |
| `safety_env` | `QID21` | 56 | Do you feel safe in your house in terms of environmental threats (e.g., flooding, heatwaves, heavy rain or win | 1 | Less than 6 months | RECODE |
| `safety_social` | `QID194` | 57 | Do you feel safe in your house in terms of social threats (e.g., loose pets, concern about neighbor's behavior | 1 | Less than 6 months | RECODE |
| `afford_urgency` | `QID17` | 58 | How would you rate the urgency of having affordable housing in High Ridge Estates? (select the most applicable | 1 | Click to write Choice 3 | PLACEHOLDER |
| `afford_strategy` | `QID19` | 59 | In your opinion, what is the most effective strategy to improve housing affordability in High Ridge Estates? ( | 2 | Yes- Integrated into central air heating system | RECODE |
| `intv_roof_walls` | `QID195_1` | 67 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_windows_doors` | `QID195_2` | 68 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_rain_gardens` | `QID195_3` | 69 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_hvac` | `QID195_4` | 70 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_plumbing_elec` | `QID195_5` | 71 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_well_septic` | `QID195_6` | 72 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_ccua_water` | `QID195_7` | 73 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_fence` | `QID195_8` | 74 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_trees_shade` | `QID195_9` | 75 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_trim_trees` | `QID195_10` | 76 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_drainage` | `QID195_11` | 77 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `exp_flooding` | `QID124_1` | 84 | Since you've lived in High Ridge Estates, have you experienced... - Flooding of house due to any disaster such | 2 | Weekly | RECODE |
| `exp_flood_help` | `QID124_2` | 85 | Since you've lived in High Ridge Estates, have you experienced... - In case of flooding experience, have you r | 3 | Biweekly | RECODE |
| `exp_extreme_heat` | `QID124_3` | 86 | Since you've lived in High Ridge Estates, have you experienced... - Extreme heat in recent years? | 2 | Weekly | RECODE |
| `exp_school_change` | `QID124_4` | 87 | Since you've lived in High Ridge Estates, have you experienced... - Changing your kids' school due to moving? | 2 | Weekly | RECODE |
| `exp_law_enf` | `QID124_5` | 88 | Since you've lived in High Ridge Estates, have you experienced... - Calling law enforcement because of problem | 2 | Weekly | RECODE |
| `exp_insurance_loss` | `QID124_6` | 89 | Since you've lived in High Ridge Estates, have you experienced... - Losing home owners insurance due to age of | 2 | Weekly | RECODE |
| `exp_well_dry` | `QID124_7` | 90 | Since you've lived in High Ridge Estates, have you experienced... - Well drying up? | 2 | Weekly | RECODE |
| `exp_pests` | `QID124_8` | 91 | Since you've lived in High Ridge Estates, have you experienced... - A problem with pests in your home? | 1 | Daily | RECODE |
| `exp_water_leaks` | `QID124_9` | 92 | Since you've lived in High Ridge Estates, have you experienced... - A problem with water leaks? | 2 | Weekly | RECODE |
| `exp_loose_animals` | `QID124_10` | 93 | Since you've lived in High Ridge Estates, have you experienced... - A problem with loose animals? | 1 | Daily | RECODE |
| `car_access` | `QID211` | 133 | Do you (or your household) own or have regular access to a car? | 1 | Yes | RECODE |
| `hurricane_transport` | `QID219` | 134 | During disasters such as hurricanes, have you experienced transportation problems (for example, difficulty eva | 2 | No | RECODE |
| `education` | `QID178` | 142 | What is the highest level of education you have completed? (select the most applicable choice) | 5 | High school diploma or equivalent | RECODE |
| `employment` | `QID176` | 143 | Which best describes your employment status? | 4 | Retired | RECODE |

## 17. `R_87qCLdadYRHhw4P` — 6200 Harvard Avenue

| Field | QID | CSV col | Verbatim question (CSV row 1) | CSV cell | Popup / payload shows | Verdict |
|---|---|---|---|---|---|---|
| `years_in_hre` | `QID12_TEXT` | 27 | How long have you lived in High Ridge Estates? (years) | 4 years | 4 years | MATCH |
| `reloc_factor_emp` | `QID181_1` | 29 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_aff` | `QID181_2` | 30 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_qol` | `QID181_3` | 31 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_fam` | `QID181_4` | 32 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_ret` | `QID181_5` | 33 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_env` | `QID181_6` | 34 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_inh` | `QID181_7` | 35 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_oth` | `QID181_8` | 36 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | — | — | EMPTY-BOTH |
| `mh_skirting` | `QID100` | 42 | If you live in a mobile home, does your home have its skirting intact? | 2 | Click to write Choice 4 | PLACEHOLDER |
| `anticipated_stay` | `QID47` | 44 | How long do you anticipate continuing to live in your current house? (select the most applicable choice) | 4 | Others | RECODE |
| `safety_env` | `QID21` | 56 | Do you feel safe in your house in terms of environmental threats (e.g., flooding, heatwaves, heavy rain or win | 3 | Don't know | RECODE |
| `safety_social` | `QID194` | 57 | Do you feel safe in your house in terms of social threats (e.g., loose pets, concern about neighbor's behavior | 2 | More than 6 months | RECODE |
| `afford_urgency` | `QID17` | 58 | How would you rate the urgency of having affordable housing in High Ridge Estates? (select the most applicable | 1 | Click to write Choice 3 | PLACEHOLDER |
| `afford_strategy` | `QID19` | 59 | In your opinion, what is the most effective strategy to improve housing affordability in High Ridge Estates? ( | 7 | Click to write Choice 7 | PLACEHOLDER |
| `intv_roof_walls` | `QID195_1` | 67 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_windows_doors` | `QID195_2` | 68 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_rain_gardens` | `QID195_3` | 69 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_hvac` | `QID195_4` | 70 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_plumbing_elec` | `QID195_5` | 71 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_well_septic` | `QID195_6` | 72 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_ccua_water` | `QID195_7` | 73 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_fence` | `QID195_8` | 74 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_trees_shade` | `QID195_9` | 75 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_trim_trees` | `QID195_10` | 76 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_drainage` | `QID195_11` | 77 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `exp_flooding` | `QID124_1` | 84 | Since you've lived in High Ridge Estates, have you experienced... - Flooding of house due to any disaster such | 2 | Weekly | RECODE |
| `exp_flood_help` | `QID124_2` | 85 | Since you've lived in High Ridge Estates, have you experienced... - In case of flooding experience, have you r | 3 | Biweekly | RECODE |
| `exp_extreme_heat` | `QID124_3` | 86 | Since you've lived in High Ridge Estates, have you experienced... - Extreme heat in recent years? | 1 | Daily | RECODE |
| `exp_school_change` | `QID124_4` | 87 | Since you've lived in High Ridge Estates, have you experienced... - Changing your kids' school due to moving? | 3 | Biweekly | RECODE |
| `exp_law_enf` | `QID124_5` | 88 | Since you've lived in High Ridge Estates, have you experienced... - Calling law enforcement because of problem | 1 | Daily | RECODE |
| `exp_insurance_loss` | `QID124_6` | 89 | Since you've lived in High Ridge Estates, have you experienced... - Losing home owners insurance due to age of | 3 | Biweekly | RECODE |
| `exp_well_dry` | `QID124_7` | 90 | Since you've lived in High Ridge Estates, have you experienced... - Well drying up? | 2 | Weekly | RECODE |
| `exp_pests` | `QID124_8` | 91 | Since you've lived in High Ridge Estates, have you experienced... - A problem with pests in your home? | 1 | Daily | RECODE |
| `exp_water_leaks` | `QID124_9` | 92 | Since you've lived in High Ridge Estates, have you experienced... - A problem with water leaks? | 2 | Weekly | RECODE |
| `exp_loose_animals` | `QID124_10` | 93 | Since you've lived in High Ridge Estates, have you experienced... - A problem with loose animals? | 1 | Daily | RECODE |
| `car_access` | `QID211` | 133 | Do you (or your household) own or have regular access to a car? | 1 | Yes | RECODE |
| `hurricane_transport` | `QID219` | 134 | During disasters such as hurricanes, have you experienced transportation problems (for example, difficulty eva | 2 | No | RECODE |
| `education` | `QID178` | 142 | What is the highest level of education you have completed? (select the most applicable choice) | 7 | Bachelor's Degree | RECODE |
| `employment` | `QID176` | 143 | Which best describes your employment status? | 1 | Employed- Full time | RECODE |

## 18. `R_8iSqFy8YDl9Xt1b` — 6397 Cascade Drive

| Field | QID | CSV col | Verbatim question (CSV row 1) | CSV cell | Popup / payload shows | Verdict |
|---|---|---|---|---|---|---|
| `years_in_hre` | `QID12_TEXT` | 27 | How long have you lived in High Ridge Estates? (years) | 3 years | 3 years | MATCH |
| `reloc_factor_emp` | `QID181_1` | 29 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_aff` | `QID181_2` | 30 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 4 | Click to write Scale Point 4 | PLACEHOLDER |
| `reloc_factor_qol` | `QID181_3` | 31 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 4 | Click to write Scale Point 4 | PLACEHOLDER |
| `reloc_factor_fam` | `QID181_4` | 32 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 4 | Click to write Scale Point 4 | PLACEHOLDER |
| `reloc_factor_ret` | `QID181_5` | 33 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 4 | Click to write Scale Point 4 | PLACEHOLDER |
| `reloc_factor_env` | `QID181_6` | 34 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 4 | Click to write Scale Point 4 | PLACEHOLDER |
| `reloc_factor_inh` | `QID181_7` | 35 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_oth` | `QID181_8` | 36 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | — | — | EMPTY-BOTH |
| `mh_skirting` | `QID100` | 42 | If you live in a mobile home, does your home have its skirting intact? | 1 | Click to write Choice 3 | PLACEHOLDER |
| `anticipated_stay` | `QID47` | 44 | How long do you anticipate continuing to live in your current house? (select the most applicable choice) | 4 | Others | RECODE |
| `safety_env` | `QID21` | 56 | Do you feel safe in your house in terms of environmental threats (e.g., flooding, heatwaves, heavy rain or win | 1 | Less than 6 months | RECODE |
| `safety_social` | `QID194` | 57 | Do you feel safe in your house in terms of social threats (e.g., loose pets, concern about neighbor's behavior | 2 | More than 6 months | RECODE |
| `afford_urgency` | `QID17` | 58 | How would you rate the urgency of having affordable housing in High Ridge Estates? (select the most applicable | 1 | Click to write Choice 3 | PLACEHOLDER |
| `afford_strategy` | `QID19` | 59 | In your opinion, what is the most effective strategy to improve housing affordability in High Ridge Estates? ( | 1,2,6 | Yes - Portable (Which Room(s)),Yes- Integrated into central air heating system,Click to write Choice 6 | DIFFERENT |
| `intv_roof_walls` | `QID195_1` | 67 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_windows_doors` | `QID195_2` | 68 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_rain_gardens` | `QID195_3` | 69 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_hvac` | `QID195_4` | 70 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_plumbing_elec` | `QID195_5` | 71 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_well_septic` | `QID195_6` | 72 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_ccua_water` | `QID195_7` | 73 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_fence` | `QID195_8` | 74 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_trees_shade` | `QID195_9` | 75 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_trim_trees` | `QID195_10` | 76 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_drainage` | `QID195_11` | 77 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `exp_flooding` | `QID124_1` | 84 | Since you've lived in High Ridge Estates, have you experienced... - Flooding of house due to any disaster such | 2 | Weekly | RECODE |
| `exp_flood_help` | `QID124_2` | 85 | Since you've lived in High Ridge Estates, have you experienced... - In case of flooding experience, have you r | 2 | Weekly | RECODE |
| `exp_extreme_heat` | `QID124_3` | 86 | Since you've lived in High Ridge Estates, have you experienced... - Extreme heat in recent years? | 1 | Daily | RECODE |
| `exp_school_change` | `QID124_4` | 87 | Since you've lived in High Ridge Estates, have you experienced... - Changing your kids' school due to moving? | 2 | Weekly | RECODE |
| `exp_law_enf` | `QID124_5` | 88 | Since you've lived in High Ridge Estates, have you experienced... - Calling law enforcement because of problem | 2 | Weekly | RECODE |
| `exp_insurance_loss` | `QID124_6` | 89 | Since you've lived in High Ridge Estates, have you experienced... - Losing home owners insurance due to age of | 2 | Weekly | RECODE |
| `exp_well_dry` | `QID124_7` | 90 | Since you've lived in High Ridge Estates, have you experienced... - Well drying up? | 1 | Daily | RECODE |
| `exp_pests` | `QID124_8` | 91 | Since you've lived in High Ridge Estates, have you experienced... - A problem with pests in your home? | 1 | Daily | RECODE |
| `exp_water_leaks` | `QID124_9` | 92 | Since you've lived in High Ridge Estates, have you experienced... - A problem with water leaks? | 1 | Daily | RECODE |
| `exp_loose_animals` | `QID124_10` | 93 | Since you've lived in High Ridge Estates, have you experienced... - A problem with loose animals? | 1 | Daily | RECODE |
| `car_access` | `QID211` | 133 | Do you (or your household) own or have regular access to a car? | 1 | Yes | RECODE |
| `hurricane_transport` | `QID219` | 134 | During disasters such as hurricanes, have you experienced transportation problems (for example, difficulty eva | 2 | No | RECODE |
| `education` | `QID178` | 142 | What is the highest level of education you have completed? (select the most applicable choice) | 8 | Graduate Degree | RECODE |
| `employment` | `QID176` | 143 | Which best describes your employment status? | 4 | Retired | RECODE |

## 19. `R_aPZYZkLLHTo3YDR` — 6392 Beloit Avenue

| Field | QID | CSV col | Verbatim question (CSV row 1) | CSV cell | Popup / payload shows | Verdict |
|---|---|---|---|---|---|---|
| `years_in_hre` | `QID12_TEXT` | 27 | How long have you lived in High Ridge Estates? (years) | 7 y | 7 y | MATCH |
| `reloc_factor_emp` | `QID181_1` | 29 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | — | — | EMPTY-BOTH |
| `reloc_factor_aff` | `QID181_2` | 30 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | — | — | EMPTY-BOTH |
| `reloc_factor_qol` | `QID181_3` | 31 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 4 | Click to write Scale Point 4 | PLACEHOLDER |
| `reloc_factor_fam` | `QID181_4` | 32 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | — | — | EMPTY-BOTH |
| `reloc_factor_ret` | `QID181_5` | 33 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | — | — | EMPTY-BOTH |
| `reloc_factor_env` | `QID181_6` | 34 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | — | — | EMPTY-BOTH |
| `reloc_factor_inh` | `QID181_7` | 35 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | — | — | EMPTY-BOTH |
| `reloc_factor_oth` | `QID181_8` | 36 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | — | — | EMPTY-BOTH |
| `mh_skirting` | `QID100` | 42 | If you live in a mobile home, does your home have its skirting intact? | 1 | Click to write Choice 3 | PLACEHOLDER |
| `anticipated_stay` | `QID47` | 44 | How long do you anticipate continuing to live in your current house? (select the most applicable choice) | 5 | Don't know | RECODE |
| `safety_env` | `QID21` | 56 | Do you feel safe in your house in terms of environmental threats (e.g., flooding, heatwaves, heavy rain or win | 2 | More than 6 months | RECODE |
| `safety_social` | `QID194` | 57 | Do you feel safe in your house in terms of social threats (e.g., loose pets, concern about neighbor's behavior | 2 | More than 6 months | RECODE |
| `afford_urgency` | `QID17` | 58 | How would you rate the urgency of having affordable housing in High Ridge Estates? (select the most applicable | 1 | Click to write Choice 3 | PLACEHOLDER |
| `afford_strategy` | `QID19` | 59 | In your opinion, what is the most effective strategy to improve housing affordability in High Ridge Estates? ( | 4,7 | Don’t Know,Click to write Choice 7 | DIFFERENT |
| `intv_roof_walls` | `QID195_1` | 67 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_windows_doors` | `QID195_2` | 68 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_rain_gardens` | `QID195_3` | 69 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_hvac` | `QID195_4` | 70 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_plumbing_elec` | `QID195_5` | 71 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_well_septic` | `QID195_6` | 72 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_ccua_water` | `QID195_7` | 73 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_fence` | `QID195_8` | 74 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_trees_shade` | `QID195_9` | 75 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_trim_trees` | `QID195_10` | 76 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_drainage` | `QID195_11` | 77 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `exp_flooding` | `QID124_1` | 84 | Since you've lived in High Ridge Estates, have you experienced... - Flooding of house due to any disaster such | 2 | Weekly | RECODE |
| `exp_flood_help` | `QID124_2` | 85 | Since you've lived in High Ridge Estates, have you experienced... - In case of flooding experience, have you r | 2 | Weekly | RECODE |
| `exp_extreme_heat` | `QID124_3` | 86 | Since you've lived in High Ridge Estates, have you experienced... - Extreme heat in recent years? | 1 | Daily | RECODE |
| `exp_school_change` | `QID124_4` | 87 | Since you've lived in High Ridge Estates, have you experienced... - Changing your kids' school due to moving? | 2 | Weekly | RECODE |
| `exp_law_enf` | `QID124_5` | 88 | Since you've lived in High Ridge Estates, have you experienced... - Calling law enforcement because of problem | 2 | Weekly | RECODE |
| `exp_insurance_loss` | `QID124_6` | 89 | Since you've lived in High Ridge Estates, have you experienced... - Losing home owners insurance due to age of | 3 | Biweekly | RECODE |
| `exp_well_dry` | `QID124_7` | 90 | Since you've lived in High Ridge Estates, have you experienced... - Well drying up? | 2 | Weekly | RECODE |
| `exp_pests` | `QID124_8` | 91 | Since you've lived in High Ridge Estates, have you experienced... - A problem with pests in your home? | 1 | Daily | RECODE |
| `exp_water_leaks` | `QID124_9` | 92 | Since you've lived in High Ridge Estates, have you experienced... - A problem with water leaks? | 2 | Weekly | RECODE |
| `exp_loose_animals` | `QID124_10` | 93 | Since you've lived in High Ridge Estates, have you experienced... - A problem with loose animals? | 2 | Weekly | RECODE |
| `car_access` | `QID211` | 133 | Do you (or your household) own or have regular access to a car? | 1 | Yes | RECODE |
| `hurricane_transport` | `QID219` | 134 | During disasters such as hurricanes, have you experienced transportation problems (for example, difficulty eva | 3 | Not Sure | RECODE |
| `education` | `QID178` | 142 | What is the highest level of education you have completed? (select the most applicable choice) | 1 | less than high school | RECODE |
| `employment` | `QID176` | 143 | Which best describes your employment status? | 3 | Unemployed | RECODE |

## 20. `R_bt9KhSC0xqF2xuS` — Beloit Ave

| Field | QID | CSV col | Verbatim question (CSV row 1) | CSV cell | Popup / payload shows | Verdict |
|---|---|---|---|---|---|---|
| `years_in_hre` | `QID12_TEXT` | 27 | How long have you lived in High Ridge Estates? (years) | 5 | 5 | MATCH |
| `reloc_factor_emp` | `QID181_1` | 29 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_aff` | `QID181_2` | 30 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_qol` | `QID181_3` | 31 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_fam` | `QID181_4` | 32 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 4 | Click to write Scale Point 4 | PLACEHOLDER |
| `reloc_factor_ret` | `QID181_5` | 33 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_env` | `QID181_6` | 34 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_inh` | `QID181_7` | 35 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_oth` | `QID181_8` | 36 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | — | — | EMPTY-BOTH |
| `mh_skirting` | `QID100` | 42 | If you live in a mobile home, does your home have its skirting intact? | 1 | Click to write Choice 3 | PLACEHOLDER |
| `anticipated_stay` | `QID47` | 44 | How long do you anticipate continuing to live in your current house? (select the most applicable choice) | 4 | Others | RECODE |
| `safety_env` | `QID21` | 56 | Do you feel safe in your house in terms of environmental threats (e.g., flooding, heatwaves, heavy rain or win | 2 | More than 6 months | RECODE |
| `safety_social` | `QID194` | 57 | Do you feel safe in your house in terms of social threats (e.g., loose pets, concern about neighbor's behavior | 1 | Less than 6 months | RECODE |
| `afford_urgency` | `QID17` | 58 | How would you rate the urgency of having affordable housing in High Ridge Estates? (select the most applicable | 1 | Click to write Choice 3 | PLACEHOLDER |
| `afford_strategy` | `QID19` | 59 | In your opinion, what is the most effective strategy to improve housing affordability in High Ridge Estates? ( | 2,6 | Yes- Integrated into central air heating system,Click to write Choice 6 | DIFFERENT |
| `intv_roof_walls` | `QID195_1` | 67 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_windows_doors` | `QID195_2` | 68 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_rain_gardens` | `QID195_3` | 69 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_hvac` | `QID195_4` | 70 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_plumbing_elec` | `QID195_5` | 71 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_well_septic` | `QID195_6` | 72 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_ccua_water` | `QID195_7` | 73 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_fence` | `QID195_8` | 74 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_trees_shade` | `QID195_9` | 75 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_trim_trees` | `QID195_10` | 76 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_drainage` | `QID195_11` | 77 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `exp_flooding` | `QID124_1` | 84 | Since you've lived in High Ridge Estates, have you experienced... - Flooding of house due to any disaster such | 2 | Weekly | RECODE |
| `exp_flood_help` | `QID124_2` | 85 | Since you've lived in High Ridge Estates, have you experienced... - In case of flooding experience, have you r | 2 | Weekly | RECODE |
| `exp_extreme_heat` | `QID124_3` | 86 | Since you've lived in High Ridge Estates, have you experienced... - Extreme heat in recent years? | 1 | Daily | RECODE |
| `exp_school_change` | `QID124_4` | 87 | Since you've lived in High Ridge Estates, have you experienced... - Changing your kids' school due to moving? | 2 | Weekly | RECODE |
| `exp_law_enf` | `QID124_5` | 88 | Since you've lived in High Ridge Estates, have you experienced... - Calling law enforcement because of problem | 2 | Weekly | RECODE |
| `exp_insurance_loss` | `QID124_6` | 89 | Since you've lived in High Ridge Estates, have you experienced... - Losing home owners insurance due to age of | 2 | Weekly | RECODE |
| `exp_well_dry` | `QID124_7` | 90 | Since you've lived in High Ridge Estates, have you experienced... - Well drying up? | 2 | Weekly | RECODE |
| `exp_pests` | `QID124_8` | 91 | Since you've lived in High Ridge Estates, have you experienced... - A problem with pests in your home? | 2 | Weekly | RECODE |
| `exp_water_leaks` | `QID124_9` | 92 | Since you've lived in High Ridge Estates, have you experienced... - A problem with water leaks? | 2 | Weekly | RECODE |
| `exp_loose_animals` | `QID124_10` | 93 | Since you've lived in High Ridge Estates, have you experienced... - A problem with loose animals? | 2 | Weekly | RECODE |
| `car_access` | `QID211` | 133 | Do you (or your household) own or have regular access to a car? | 1 | Yes | RECODE |
| `hurricane_transport` | `QID219` | 134 | During disasters such as hurricanes, have you experienced transportation problems (for example, difficulty eva | 1 | Yes | RECODE |
| `education` | `QID178` | 142 | What is the highest level of education you have completed? (select the most applicable choice) | 5 | High school diploma or equivalent | RECODE |
| `employment` | `QID176` | 143 | Which best describes your employment status? | 4 | Retired | RECODE |

## 21. `R_bxz0eWgFA4AstpB` — 7239 Purdue Street

| Field | QID | CSV col | Verbatim question (CSV row 1) | CSV cell | Popup / payload shows | Verdict |
|---|---|---|---|---|---|---|
| `years_in_hre` | `QID12_TEXT` | 27 | How long have you lived in High Ridge Estates? (years) | 20 years | 20 years | MATCH |
| `reloc_factor_emp` | `QID181_1` | 29 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_aff` | `QID181_2` | 30 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_qol` | `QID181_3` | 31 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 4 | Click to write Scale Point 4 | PLACEHOLDER |
| `reloc_factor_fam` | `QID181_4` | 32 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 4 | Click to write Scale Point 4 | PLACEHOLDER |
| `reloc_factor_ret` | `QID181_5` | 33 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_env` | `QID181_6` | 34 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_inh` | `QID181_7` | 35 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_oth` | `QID181_8` | 36 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | — | — | EMPTY-BOTH |
| `mh_skirting` | `QID100` | 42 | If you live in a mobile home, does your home have its skirting intact? | 2 | Click to write Choice 4 | PLACEHOLDER |
| `anticipated_stay` | `QID47` | 44 | How long do you anticipate continuing to live in your current house? (select the most applicable choice) | 4 | Others | RECODE |
| `safety_env` | `QID21` | 56 | Do you feel safe in your house in terms of environmental threats (e.g., flooding, heatwaves, heavy rain or win | 1 | Less than 6 months | RECODE |
| `safety_social` | `QID194` | 57 | Do you feel safe in your house in terms of social threats (e.g., loose pets, concern about neighbor's behavior | 1 | Less than 6 months | RECODE |
| `afford_urgency` | `QID17` | 58 | How would you rate the urgency of having affordable housing in High Ridge Estates? (select the most applicable | 3 | Click to write Choice 5 | PLACEHOLDER |
| `afford_strategy` | `QID19` | 59 | In your opinion, what is the most effective strategy to improve housing affordability in High Ridge Estates? ( | 6 | Click to write Choice 6 | PLACEHOLDER |
| `intv_roof_walls` | `QID195_1` | 67 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_windows_doors` | `QID195_2` | 68 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_rain_gardens` | `QID195_3` | 69 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_hvac` | `QID195_4` | 70 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_plumbing_elec` | `QID195_5` | 71 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_well_septic` | `QID195_6` | 72 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_ccua_water` | `QID195_7` | 73 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_fence` | `QID195_8` | 74 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_trees_shade` | `QID195_9` | 75 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_trim_trees` | `QID195_10` | 76 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_drainage` | `QID195_11` | 77 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `exp_flooding` | `QID124_1` | 84 | Since you've lived in High Ridge Estates, have you experienced... - Flooding of house due to any disaster such | 2 | Weekly | RECODE |
| `exp_flood_help` | `QID124_2` | 85 | Since you've lived in High Ridge Estates, have you experienced... - In case of flooding experience, have you r | 3 | Biweekly | RECODE |
| `exp_extreme_heat` | `QID124_3` | 86 | Since you've lived in High Ridge Estates, have you experienced... - Extreme heat in recent years? | 2 | Weekly | RECODE |
| `exp_school_change` | `QID124_4` | 87 | Since you've lived in High Ridge Estates, have you experienced... - Changing your kids' school due to moving? | 2 | Weekly | RECODE |
| `exp_law_enf` | `QID124_5` | 88 | Since you've lived in High Ridge Estates, have you experienced... - Calling law enforcement because of problem | 1 | Daily | RECODE |
| `exp_insurance_loss` | `QID124_6` | 89 | Since you've lived in High Ridge Estates, have you experienced... - Losing home owners insurance due to age of | 3 | Biweekly | RECODE |
| `exp_well_dry` | `QID124_7` | 90 | Since you've lived in High Ridge Estates, have you experienced... - Well drying up? | 2 | Weekly | RECODE |
| `exp_pests` | `QID124_8` | 91 | Since you've lived in High Ridge Estates, have you experienced... - A problem with pests in your home? | 2 | Weekly | RECODE |
| `exp_water_leaks` | `QID124_9` | 92 | Since you've lived in High Ridge Estates, have you experienced... - A problem with water leaks? | 1 | Daily | RECODE |
| `exp_loose_animals` | `QID124_10` | 93 | Since you've lived in High Ridge Estates, have you experienced... - A problem with loose animals? | 1 | Daily | RECODE |
| `car_access` | `QID211` | 133 | Do you (or your household) own or have regular access to a car? | 2 | No | RECODE |
| `hurricane_transport` | `QID219` | 134 | During disasters such as hurricanes, have you experienced transportation problems (for example, difficulty eva | 2 | No | RECODE |
| `education` | `QID178` | 142 | What is the highest level of education you have completed? (select the most applicable choice) | 9 | Vocational/Technical Licensing or Certification | RECODE |
| `employment` | `QID176` | 143 | Which best describes your employment status? | 4 | Retired | RECODE |

## 22. `R_d4T4ee11cH6ntjW` — 7197 Pembroke Street

| Field | QID | CSV col | Verbatim question (CSV row 1) | CSV cell | Popup / payload shows | Verdict |
|---|---|---|---|---|---|---|
| `years_in_hre` | `QID12_TEXT` | 27 | How long have you lived in High Ridge Estates? (years) | 20 years | 20 years | MATCH |
| `reloc_factor_emp` | `QID181_1` | 29 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_aff` | `QID181_2` | 30 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `reloc_factor_qol` | `QID181_3` | 31 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 4 | Click to write Scale Point 4 | PLACEHOLDER |
| `reloc_factor_fam` | `QID181_4` | 32 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_ret` | `QID181_5` | 33 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_env` | `QID181_6` | 34 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_inh` | `QID181_7` | 35 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_oth` | `QID181_8` | 36 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | — | — | EMPTY-BOTH |
| `mh_skirting` | `QID100` | 42 | If you live in a mobile home, does your home have its skirting intact? | 1 | Click to write Choice 3 | PLACEHOLDER |
| `anticipated_stay` | `QID47` | 44 | How long do you anticipate continuing to live in your current house? (select the most applicable choice) | 4 | Others | RECODE |
| `safety_env` | `QID21` | 56 | Do you feel safe in your house in terms of environmental threats (e.g., flooding, heatwaves, heavy rain or win | 3 | Don't know | RECODE |
| `safety_social` | `QID194` | 57 | Do you feel safe in your house in terms of social threats (e.g., loose pets, concern about neighbor's behavior | 2 | More than 6 months | RECODE |
| `afford_urgency` | `QID17` | 58 | How would you rate the urgency of having affordable housing in High Ridge Estates? (select the most applicable | 1 | Click to write Choice 3 | PLACEHOLDER |
| `afford_strategy` | `QID19` | 59 | In your opinion, what is the most effective strategy to improve housing affordability in High Ridge Estates? ( | 1,2,3 | Yes - Portable (Which Room(s)),Yes- Integrated into central air heating system,No | DIFFERENT |
| `intv_roof_walls` | `QID195_1` | 67 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_windows_doors` | `QID195_2` | 68 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_rain_gardens` | `QID195_3` | 69 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_hvac` | `QID195_4` | 70 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_plumbing_elec` | `QID195_5` | 71 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_well_septic` | `QID195_6` | 72 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_ccua_water` | `QID195_7` | 73 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_fence` | `QID195_8` | 74 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_trees_shade` | `QID195_9` | 75 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_trim_trees` | `QID195_10` | 76 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_drainage` | `QID195_11` | 77 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `exp_flooding` | `QID124_1` | 84 | Since you've lived in High Ridge Estates, have you experienced... - Flooding of house due to any disaster such | 2 | Weekly | RECODE |
| `exp_flood_help` | `QID124_2` | 85 | Since you've lived in High Ridge Estates, have you experienced... - In case of flooding experience, have you r | 2 | Weekly | RECODE |
| `exp_extreme_heat` | `QID124_3` | 86 | Since you've lived in High Ridge Estates, have you experienced... - Extreme heat in recent years? | 1 | Daily | RECODE |
| `exp_school_change` | `QID124_4` | 87 | Since you've lived in High Ridge Estates, have you experienced... - Changing your kids' school due to moving? | 2 | Weekly | RECODE |
| `exp_law_enf` | `QID124_5` | 88 | Since you've lived in High Ridge Estates, have you experienced... - Calling law enforcement because of problem | 1 | Daily | RECODE |
| `exp_insurance_loss` | `QID124_6` | 89 | Since you've lived in High Ridge Estates, have you experienced... - Losing home owners insurance due to age of | 2 | Weekly | RECODE |
| `exp_well_dry` | `QID124_7` | 90 | Since you've lived in High Ridge Estates, have you experienced... - Well drying up? | 2 | Weekly | RECODE |
| `exp_pests` | `QID124_8` | 91 | Since you've lived in High Ridge Estates, have you experienced... - A problem with pests in your home? | 1 | Daily | RECODE |
| `exp_water_leaks` | `QID124_9` | 92 | Since you've lived in High Ridge Estates, have you experienced... - A problem with water leaks? | 1 | Daily | RECODE |
| `exp_loose_animals` | `QID124_10` | 93 | Since you've lived in High Ridge Estates, have you experienced... - A problem with loose animals? | 1 | Daily | RECODE |
| `car_access` | `QID211` | 133 | Do you (or your household) own or have regular access to a car? | 1 | Yes | RECODE |
| `hurricane_transport` | `QID219` | 134 | During disasters such as hurricanes, have you experienced transportation problems (for example, difficulty eva | 4 | Name the problem | RECODE |
| `education` | `QID178` | 142 | What is the highest level of education you have completed? (select the most applicable choice) | 5 | High school diploma or equivalent | RECODE |
| `employment` | `QID176` | 143 | Which best describes your employment status? | 3 | Unemployed | RECODE |

## 23. `R_h0LfcAVvLrGULaj` — 7166 Pembroke Street

| Field | QID | CSV col | Verbatim question (CSV row 1) | CSV cell | Popup / payload shows | Verdict |
|---|---|---|---|---|---|---|
| `years_in_hre` | `QID12_TEXT` | 27 | How long have you lived in High Ridge Estates? (years) | 40yrs | 40yrs | MATCH |
| `reloc_factor_emp` | `QID181_1` | 29 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `reloc_factor_aff` | `QID181_2` | 30 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `reloc_factor_qol` | `QID181_3` | 31 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `reloc_factor_fam` | `QID181_4` | 32 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `reloc_factor_ret` | `QID181_5` | 33 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `reloc_factor_env` | `QID181_6` | 34 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `reloc_factor_inh` | `QID181_7` | 35 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `reloc_factor_oth` | `QID181_8` | 36 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `mh_skirting` | `QID100` | 42 | If you live in a mobile home, does your home have its skirting intact? | 1 | Click to write Choice 3 | PLACEHOLDER |
| `anticipated_stay` | `QID47` | 44 | How long do you anticipate continuing to live in your current house? (select the most applicable choice) | 4 | Others | RECODE |
| `safety_env` | `QID21` | 56 | Do you feel safe in your house in terms of environmental threats (e.g., flooding, heatwaves, heavy rain or win | 4 | Click to write Choice 4 | PLACEHOLDER |
| `safety_social` | `QID194` | 57 | Do you feel safe in your house in terms of social threats (e.g., loose pets, concern about neighbor's behavior | 3 | Don't know | RECODE |
| `afford_urgency` | `QID17` | 58 | How would you rate the urgency of having affordable housing in High Ridge Estates? (select the most applicable | 1 | Click to write Choice 3 | PLACEHOLDER |
| `afford_strategy` | `QID19` | 59 | In your opinion, what is the most effective strategy to improve housing affordability in High Ridge Estates? ( | 2,6 | Yes- Integrated into central air heating system,Click to write Choice 6 | DIFFERENT |
| `intv_roof_walls` | `QID195_1` | 67 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_windows_doors` | `QID195_2` | 68 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_rain_gardens` | `QID195_3` | 69 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_hvac` | `QID195_4` | 70 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_plumbing_elec` | `QID195_5` | 71 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_well_septic` | `QID195_6` | 72 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_ccua_water` | `QID195_7` | 73 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_fence` | `QID195_8` | 74 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_trees_shade` | `QID195_9` | 75 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_trim_trees` | `QID195_10` | 76 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_drainage` | `QID195_11` | 77 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `exp_flooding` | `QID124_1` | 84 | Since you've lived in High Ridge Estates, have you experienced... - Flooding of house due to any disaster such | 2 | Weekly | RECODE |
| `exp_flood_help` | `QID124_2` | 85 | Since you've lived in High Ridge Estates, have you experienced... - In case of flooding experience, have you r | 2 | Weekly | RECODE |
| `exp_extreme_heat` | `QID124_3` | 86 | Since you've lived in High Ridge Estates, have you experienced... - Extreme heat in recent years? | 1 | Daily | RECODE |
| `exp_school_change` | `QID124_4` | 87 | Since you've lived in High Ridge Estates, have you experienced... - Changing your kids' school due to moving? | 2 | Weekly | RECODE |
| `exp_law_enf` | `QID124_5` | 88 | Since you've lived in High Ridge Estates, have you experienced... - Calling law enforcement because of problem | 1 | Daily | RECODE |
| `exp_insurance_loss` | `QID124_6` | 89 | Since you've lived in High Ridge Estates, have you experienced... - Losing home owners insurance due to age of | 2 | Weekly | RECODE |
| `exp_well_dry` | `QID124_7` | 90 | Since you've lived in High Ridge Estates, have you experienced... - Well drying up? | 2 | Weekly | RECODE |
| `exp_pests` | `QID124_8` | 91 | Since you've lived in High Ridge Estates, have you experienced... - A problem with pests in your home? | 2 | Weekly | RECODE |
| `exp_water_leaks` | `QID124_9` | 92 | Since you've lived in High Ridge Estates, have you experienced... - A problem with water leaks? | 2 | Weekly | RECODE |
| `exp_loose_animals` | `QID124_10` | 93 | Since you've lived in High Ridge Estates, have you experienced... - A problem with loose animals? | 2 | Weekly | RECODE |
| `car_access` | `QID211` | 133 | Do you (or your household) own or have regular access to a car? | 1 | Yes | RECODE |
| `hurricane_transport` | `QID219` | 134 | During disasters such as hurricanes, have you experienced transportation problems (for example, difficulty eva | 2 | No | RECODE |
| `education` | `QID178` | 142 | What is the highest level of education you have completed? (select the most applicable choice) | 5 | High school diploma or equivalent | RECODE |
| `employment` | `QID176` | 143 | Which best describes your employment status? | 1 | Employed- Full time | RECODE |

## 24. `R_iGZqrFKoHdcjKOH` — 6394 Baylor Avenue

| Field | QID | CSV col | Verbatim question (CSV row 1) | CSV cell | Popup / payload shows | Verdict |
|---|---|---|---|---|---|---|
| `years_in_hre` | `QID12_TEXT` | 27 | How long have you lived in High Ridge Estates? (years) | 5 | 5 | MATCH |
| `reloc_factor_emp` | `QID181_1` | 29 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_aff` | `QID181_2` | 30 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_qol` | `QID181_3` | 31 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_fam` | `QID181_4` | 32 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_ret` | `QID181_5` | 33 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_env` | `QID181_6` | 34 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_inh` | `QID181_7` | 35 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_oth` | `QID181_8` | 36 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | — | — | EMPTY-BOTH |
| `mh_skirting` | `QID100` | 42 | If you live in a mobile home, does your home have its skirting intact? | 1 | Click to write Choice 3 | PLACEHOLDER |
| `anticipated_stay` | `QID47` | 44 | How long do you anticipate continuing to live in your current house? (select the most applicable choice) | 5 | Don't know | RECODE |
| `safety_env` | `QID21` | 56 | Do you feel safe in your house in terms of environmental threats (e.g., flooding, heatwaves, heavy rain or win | 2 | More than 6 months | RECODE |
| `safety_social` | `QID194` | 57 | Do you feel safe in your house in terms of social threats (e.g., loose pets, concern about neighbor's behavior | 4 | Click to write Choice 4 | PLACEHOLDER |
| `afford_urgency` | `QID17` | 58 | How would you rate the urgency of having affordable housing in High Ridge Estates? (select the most applicable | 1 | Click to write Choice 3 | PLACEHOLDER |
| `afford_strategy` | `QID19` | 59 | In your opinion, what is the most effective strategy to improve housing affordability in High Ridge Estates? ( | 1,6 | Yes - Portable (Which Room(s)),Click to write Choice 6 | DIFFERENT |
| `intv_roof_walls` | `QID195_1` | 67 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_windows_doors` | `QID195_2` | 68 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_rain_gardens` | `QID195_3` | 69 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_hvac` | `QID195_4` | 70 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_plumbing_elec` | `QID195_5` | 71 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_well_septic` | `QID195_6` | 72 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_ccua_water` | `QID195_7` | 73 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_fence` | `QID195_8` | 74 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_trees_shade` | `QID195_9` | 75 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_trim_trees` | `QID195_10` | 76 | Please indicate whether you would like or would not like to have the following interventions to improve your h | — | — | EMPTY-BOTH |
| `intv_drainage` | `QID195_11` | 77 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `exp_flooding` | `QID124_1` | 84 | Since you've lived in High Ridge Estates, have you experienced... - Flooding of house due to any disaster such | 2 | Weekly | RECODE |
| `exp_flood_help` | `QID124_2` | 85 | Since you've lived in High Ridge Estates, have you experienced... - In case of flooding experience, have you r | 2 | Weekly | RECODE |
| `exp_extreme_heat` | `QID124_3` | 86 | Since you've lived in High Ridge Estates, have you experienced... - Extreme heat in recent years? | 1 | Daily | RECODE |
| `exp_school_change` | `QID124_4` | 87 | Since you've lived in High Ridge Estates, have you experienced... - Changing your kids' school due to moving? | 2 | Weekly | RECODE |
| `exp_law_enf` | `QID124_5` | 88 | Since you've lived in High Ridge Estates, have you experienced... - Calling law enforcement because of problem | 2 | Weekly | RECODE |
| `exp_insurance_loss` | `QID124_6` | 89 | Since you've lived in High Ridge Estates, have you experienced... - Losing home owners insurance due to age of | 2 | Weekly | RECODE |
| `exp_well_dry` | `QID124_7` | 90 | Since you've lived in High Ridge Estates, have you experienced... - Well drying up? | 2 | Weekly | RECODE |
| `exp_pests` | `QID124_8` | 91 | Since you've lived in High Ridge Estates, have you experienced... - A problem with pests in your home? | 2 | Weekly | RECODE |
| `exp_water_leaks` | `QID124_9` | 92 | Since you've lived in High Ridge Estates, have you experienced... - A problem with water leaks? | 2 | Weekly | RECODE |
| `exp_loose_animals` | `QID124_10` | 93 | Since you've lived in High Ridge Estates, have you experienced... - A problem with loose animals? | 2 | Weekly | RECODE |
| `car_access` | `QID211` | 133 | Do you (or your household) own or have regular access to a car? | 2 | No | RECODE |
| `hurricane_transport` | `QID219` | 134 | During disasters such as hurricanes, have you experienced transportation problems (for example, difficulty eva | 3 | Not Sure | RECODE |
| `education` | `QID178` | 142 | What is the highest level of education you have completed? (select the most applicable choice) | 9 | Vocational/Technical Licensing or Certification | RECODE |
| `employment` | `QID176` | 143 | Which best describes your employment status? | 3 | Unemployed | RECODE |

## 25. `R_jIMWa4XhirJ5WDy` — 6301 Columbia Avenue

| Field | QID | CSV col | Verbatim question (CSV row 1) | CSV cell | Popup / payload shows | Verdict |
|---|---|---|---|---|---|---|
| `years_in_hre` | `QID12_TEXT` | 27 | How long have you lived in High Ridge Estates? (years) | 2.5 years | 2.5 years | MATCH |
| `reloc_factor_emp` | `QID181_1` | 29 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_aff` | `QID181_2` | 30 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_qol` | `QID181_3` | 31 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_fam` | `QID181_4` | 32 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 4 | Click to write Scale Point 4 | PLACEHOLDER |
| `reloc_factor_ret` | `QID181_5` | 33 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 4 | Click to write Scale Point 4 | PLACEHOLDER |
| `reloc_factor_env` | `QID181_6` | 34 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `reloc_factor_inh` | `QID181_7` | 35 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_oth` | `QID181_8` | 36 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | — | — | EMPTY-BOTH |
| `mh_skirting` | `QID100` | 42 | If you live in a mobile home, does your home have its skirting intact? | 1 | Click to write Choice 3 | PLACEHOLDER |
| `anticipated_stay` | `QID47` | 44 | How long do you anticipate continuing to live in your current house? (select the most applicable choice) | 4 | Others | RECODE |
| `safety_env` | `QID21` | 56 | Do you feel safe in your house in terms of environmental threats (e.g., flooding, heatwaves, heavy rain or win | 3 | Don't know | RECODE |
| `safety_social` | `QID194` | 57 | Do you feel safe in your house in terms of social threats (e.g., loose pets, concern about neighbor's behavior | 2 | More than 6 months | RECODE |
| `afford_urgency` | `QID17` | 58 | How would you rate the urgency of having affordable housing in High Ridge Estates? (select the most applicable | 1 | Click to write Choice 3 | PLACEHOLDER |
| `afford_strategy` | `QID19` | 59 | In your opinion, what is the most effective strategy to improve housing affordability in High Ridge Estates? ( | 2 | Yes- Integrated into central air heating system | RECODE |
| `intv_roof_walls` | `QID195_1` | 67 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_windows_doors` | `QID195_2` | 68 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_rain_gardens` | `QID195_3` | 69 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_hvac` | `QID195_4` | 70 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_plumbing_elec` | `QID195_5` | 71 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_well_septic` | `QID195_6` | 72 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_ccua_water` | `QID195_7` | 73 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_fence` | `QID195_8` | 74 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_trees_shade` | `QID195_9` | 75 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_trim_trees` | `QID195_10` | 76 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_drainage` | `QID195_11` | 77 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `exp_flooding` | `QID124_1` | 84 | Since you've lived in High Ridge Estates, have you experienced... - Flooding of house due to any disaster such | 1 | Daily | RECODE |
| `exp_flood_help` | `QID124_2` | 85 | Since you've lived in High Ridge Estates, have you experienced... - In case of flooding experience, have you r | 2 | Weekly | RECODE |
| `exp_extreme_heat` | `QID124_3` | 86 | Since you've lived in High Ridge Estates, have you experienced... - Extreme heat in recent years? | 1 | Daily | RECODE |
| `exp_school_change` | `QID124_4` | 87 | Since you've lived in High Ridge Estates, have you experienced... - Changing your kids' school due to moving? | 2 | Weekly | RECODE |
| `exp_law_enf` | `QID124_5` | 88 | Since you've lived in High Ridge Estates, have you experienced... - Calling law enforcement because of problem | 1 | Daily | RECODE |
| `exp_insurance_loss` | `QID124_6` | 89 | Since you've lived in High Ridge Estates, have you experienced... - Losing home owners insurance due to age of | 2 | Weekly | RECODE |
| `exp_well_dry` | `QID124_7` | 90 | Since you've lived in High Ridge Estates, have you experienced... - Well drying up? | 1 | Daily | RECODE |
| `exp_pests` | `QID124_8` | 91 | Since you've lived in High Ridge Estates, have you experienced... - A problem with pests in your home? | 1 | Daily | RECODE |
| `exp_water_leaks` | `QID124_9` | 92 | Since you've lived in High Ridge Estates, have you experienced... - A problem with water leaks? | 1 | Daily | RECODE |
| `exp_loose_animals` | `QID124_10` | 93 | Since you've lived in High Ridge Estates, have you experienced... - A problem with loose animals? | 2 | Weekly | RECODE |
| `car_access` | `QID211` | 133 | Do you (or your household) own or have regular access to a car? | 1 | Yes | RECODE |
| `hurricane_transport` | `QID219` | 134 | During disasters such as hurricanes, have you experienced transportation problems (for example, difficulty eva | 1 | Yes | RECODE |
| `education` | `QID178` | 142 | What is the highest level of education you have completed? (select the most applicable choice) | 5 | High school diploma or equivalent | RECODE |
| `employment` | `QID176` | 143 | Which best describes your employment status? | 3 | Unemployed | RECODE |

## 26. `R_kVLcdKScFHPgWVR` — 6308 Bucknell

| Field | QID | CSV col | Verbatim question (CSV row 1) | CSV cell | Popup / payload shows | Verdict |
|---|---|---|---|---|---|---|
| `years_in_hre` | `QID12_TEXT` | 27 | How long have you lived in High Ridge Estates? (years) | 1 | 1 | MATCH |
| `reloc_factor_emp` | `QID181_1` | 29 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_aff` | `QID181_2` | 30 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_qol` | `QID181_3` | 31 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_fam` | `QID181_4` | 32 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_ret` | `QID181_5` | 33 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 4 | Click to write Scale Point 4 | PLACEHOLDER |
| `reloc_factor_env` | `QID181_6` | 34 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 4 | Click to write Scale Point 4 | PLACEHOLDER |
| `reloc_factor_inh` | `QID181_7` | 35 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_oth` | `QID181_8` | 36 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | — | — | EMPTY-BOTH |
| `mh_skirting` | `QID100` | 42 | If you live in a mobile home, does your home have its skirting intact? | 1 | Click to write Choice 3 | PLACEHOLDER |
| `anticipated_stay` | `QID47` | 44 | How long do you anticipate continuing to live in your current house? (select the most applicable choice) | 4 | Others | RECODE |
| `safety_env` | `QID21` | 56 | Do you feel safe in your house in terms of environmental threats (e.g., flooding, heatwaves, heavy rain or win | 1 | Less than 6 months | RECODE |
| `safety_social` | `QID194` | 57 | Do you feel safe in your house in terms of social threats (e.g., loose pets, concern about neighbor's behavior | 1 | Less than 6 months | RECODE |
| `afford_urgency` | `QID17` | 58 | How would you rate the urgency of having affordable housing in High Ridge Estates? (select the most applicable | 3 | Click to write Choice 5 | PLACEHOLDER |
| `afford_strategy` | `QID19` | 59 | In your opinion, what is the most effective strategy to improve housing affordability in High Ridge Estates? ( | 2 | Yes- Integrated into central air heating system | RECODE |
| `intv_roof_walls` | `QID195_1` | 67 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_windows_doors` | `QID195_2` | 68 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_rain_gardens` | `QID195_3` | 69 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_hvac` | `QID195_4` | 70 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_plumbing_elec` | `QID195_5` | 71 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_well_septic` | `QID195_6` | 72 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_ccua_water` | `QID195_7` | 73 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_fence` | `QID195_8` | 74 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_trees_shade` | `QID195_9` | 75 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_trim_trees` | `QID195_10` | 76 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_drainage` | `QID195_11` | 77 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `exp_flooding` | `QID124_1` | 84 | Since you've lived in High Ridge Estates, have you experienced... - Flooding of house due to any disaster such | 2 | Weekly | RECODE |
| `exp_flood_help` | `QID124_2` | 85 | Since you've lived in High Ridge Estates, have you experienced... - In case of flooding experience, have you r | 3 | Biweekly | RECODE |
| `exp_extreme_heat` | `QID124_3` | 86 | Since you've lived in High Ridge Estates, have you experienced... - Extreme heat in recent years? | 2 | Weekly | RECODE |
| `exp_school_change` | `QID124_4` | 87 | Since you've lived in High Ridge Estates, have you experienced... - Changing your kids' school due to moving? | 2 | Weekly | RECODE |
| `exp_law_enf` | `QID124_5` | 88 | Since you've lived in High Ridge Estates, have you experienced... - Calling law enforcement because of problem | 2 | Weekly | RECODE |
| `exp_insurance_loss` | `QID124_6` | 89 | Since you've lived in High Ridge Estates, have you experienced... - Losing home owners insurance due to age of | 2 | Weekly | RECODE |
| `exp_well_dry` | `QID124_7` | 90 | Since you've lived in High Ridge Estates, have you experienced... - Well drying up? | 2 | Weekly | RECODE |
| `exp_pests` | `QID124_8` | 91 | Since you've lived in High Ridge Estates, have you experienced... - A problem with pests in your home? | 2 | Weekly | RECODE |
| `exp_water_leaks` | `QID124_9` | 92 | Since you've lived in High Ridge Estates, have you experienced... - A problem with water leaks? | 2 | Weekly | RECODE |
| `exp_loose_animals` | `QID124_10` | 93 | Since you've lived in High Ridge Estates, have you experienced... - A problem with loose animals? | 2 | Weekly | RECODE |
| `car_access` | `QID211` | 133 | Do you (or your household) own or have regular access to a car? | 1 | Yes | RECODE |
| `hurricane_transport` | `QID219` | 134 | During disasters such as hurricanes, have you experienced transportation problems (for example, difficulty eva | 2 | No | RECODE |
| `education` | `QID178` | 142 | What is the highest level of education you have completed? (select the most applicable choice) | 5 | High school diploma or equivalent | RECODE |
| `employment` | `QID176` | 143 | Which best describes your employment status? | 4 | Retired | RECODE |

## 27. `R_l1yOBZ0aTpnAxq3` — 7358 Yale St.

| Field | QID | CSV col | Verbatim question (CSV row 1) | CSV cell | Popup / payload shows | Verdict |
|---|---|---|---|---|---|---|
| `years_in_hre` | `QID12_TEXT` | 27 | How long have you lived in High Ridge Estates? (years) | 5months | 5months | MATCH |
| `reloc_factor_emp` | `QID181_1` | 29 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_aff` | `QID181_2` | 30 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 2 | Click to write Scale Point 2 | PLACEHOLDER |
| `reloc_factor_qol` | `QID181_3` | 31 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 2 | Click to write Scale Point 2 | PLACEHOLDER |
| `reloc_factor_fam` | `QID181_4` | 32 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_ret` | `QID181_5` | 33 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_env` | `QID181_6` | 34 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_inh` | `QID181_7` | 35 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_oth` | `QID181_8` | 36 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | — | — | EMPTY-BOTH |
| `mh_skirting` | `QID100` | 42 | If you live in a mobile home, does your home have its skirting intact? | 1 | Click to write Choice 3 | PLACEHOLDER |
| `anticipated_stay` | `QID47` | 44 | How long do you anticipate continuing to live in your current house? (select the most applicable choice) | 1 | Wood | RECODE |
| `safety_env` | `QID21` | 56 | Do you feel safe in your house in terms of environmental threats (e.g., flooding, heatwaves, heavy rain or win | 1 | Less than 6 months | RECODE |
| `safety_social` | `QID194` | 57 | Do you feel safe in your house in terms of social threats (e.g., loose pets, concern about neighbor's behavior | 3 | Don't know | RECODE |
| `afford_urgency` | `QID17` | 58 | How would you rate the urgency of having affordable housing in High Ridge Estates? (select the most applicable | 1 | Click to write Choice 3 | PLACEHOLDER |
| `afford_strategy` | `QID19` | 59 | In your opinion, what is the most effective strategy to improve housing affordability in High Ridge Estates? ( | 2 | Yes- Integrated into central air heating system | RECODE |
| `intv_roof_walls` | `QID195_1` | 67 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_windows_doors` | `QID195_2` | 68 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_rain_gardens` | `QID195_3` | 69 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_hvac` | `QID195_4` | 70 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_plumbing_elec` | `QID195_5` | 71 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_well_septic` | `QID195_6` | 72 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_ccua_water` | `QID195_7` | 73 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_fence` | `QID195_8` | 74 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_trees_shade` | `QID195_9` | 75 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_trim_trees` | `QID195_10` | 76 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_drainage` | `QID195_11` | 77 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `exp_flooding` | `QID124_1` | 84 | Since you've lived in High Ridge Estates, have you experienced... - Flooding of house due to any disaster such | 2 | Weekly | RECODE |
| `exp_flood_help` | `QID124_2` | 85 | Since you've lived in High Ridge Estates, have you experienced... - In case of flooding experience, have you r | 2 | Weekly | RECODE |
| `exp_extreme_heat` | `QID124_3` | 86 | Since you've lived in High Ridge Estates, have you experienced... - Extreme heat in recent years? | 2 | Weekly | RECODE |
| `exp_school_change` | `QID124_4` | 87 | Since you've lived in High Ridge Estates, have you experienced... - Changing your kids' school due to moving? | 2 | Weekly | RECODE |
| `exp_law_enf` | `QID124_5` | 88 | Since you've lived in High Ridge Estates, have you experienced... - Calling law enforcement because of problem | 2 | Weekly | RECODE |
| `exp_insurance_loss` | `QID124_6` | 89 | Since you've lived in High Ridge Estates, have you experienced... - Losing home owners insurance due to age of | 2 | Weekly | RECODE |
| `exp_well_dry` | `QID124_7` | 90 | Since you've lived in High Ridge Estates, have you experienced... - Well drying up? | 2 | Weekly | RECODE |
| `exp_pests` | `QID124_8` | 91 | Since you've lived in High Ridge Estates, have you experienced... - A problem with pests in your home? | 2 | Weekly | RECODE |
| `exp_water_leaks` | `QID124_9` | 92 | Since you've lived in High Ridge Estates, have you experienced... - A problem with water leaks? | 2 | Weekly | RECODE |
| `exp_loose_animals` | `QID124_10` | 93 | Since you've lived in High Ridge Estates, have you experienced... - A problem with loose animals? | 1 | Daily | RECODE |
| `car_access` | `QID211` | 133 | Do you (or your household) own or have regular access to a car? | 1 | Yes | RECODE |
| `hurricane_transport` | `QID219` | 134 | During disasters such as hurricanes, have you experienced transportation problems (for example, difficulty eva | 2 | No | RECODE |
| `education` | `QID178` | 142 | What is the highest level of education you have completed? (select the most applicable choice) | 6 | Some college, no degree | RECODE |
| `employment` | `QID176` | 143 | Which best describes your employment status? | 1 | Employed- Full time | RECODE |

## 28. `R_mhCImQQ64DBmsPH` — 6389 Baylor

| Field | QID | CSV col | Verbatim question (CSV row 1) | CSV cell | Popup / payload shows | Verdict |
|---|---|---|---|---|---|---|
| `years_in_hre` | `QID12_TEXT` | 27 | How long have you lived in High Ridge Estates? (years) | 50 yrs family land | 50 yrs family land | MATCH |
| `reloc_factor_emp` | `QID181_1` | 29 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_aff` | `QID181_2` | 30 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `reloc_factor_qol` | `QID181_3` | 31 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `reloc_factor_fam` | `QID181_4` | 32 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `reloc_factor_ret` | `QID181_5` | 33 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `reloc_factor_env` | `QID181_6` | 34 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `reloc_factor_inh` | `QID181_7` | 35 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `reloc_factor_oth` | `QID181_8` | 36 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | — | — | EMPTY-BOTH |
| `mh_skirting` | `QID100` | 42 | If you live in a mobile home, does your home have its skirting intact? | 1 | Click to write Choice 3 | PLACEHOLDER |
| `anticipated_stay` | `QID47` | 44 | How long do you anticipate continuing to live in your current house? (select the most applicable choice) | 4 | Others | RECODE |
| `safety_env` | `QID21` | 56 | Do you feel safe in your house in terms of environmental threats (e.g., flooding, heatwaves, heavy rain or win | 1 | Less than 6 months | RECODE |
| `safety_social` | `QID194` | 57 | Do you feel safe in your house in terms of social threats (e.g., loose pets, concern about neighbor's behavior | 3 | Don't know | RECODE |
| `afford_urgency` | `QID17` | 58 | How would you rate the urgency of having affordable housing in High Ridge Estates? (select the most applicable | 3 | Click to write Choice 5 | PLACEHOLDER |
| `afford_strategy` | `QID19` | 59 | In your opinion, what is the most effective strategy to improve housing affordability in High Ridge Estates? ( | 2 | Yes- Integrated into central air heating system | RECODE |
| `intv_roof_walls` | `QID195_1` | 67 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_windows_doors` | `QID195_2` | 68 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_rain_gardens` | `QID195_3` | 69 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_hvac` | `QID195_4` | 70 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 7 | Nature reserves and preserves | RECODE |
| `intv_plumbing_elec` | `QID195_5` | 71 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_well_septic` | `QID195_6` | 72 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_ccua_water` | `QID195_7` | 73 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_fence` | `QID195_8` | 74 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_trees_shade` | `QID195_9` | 75 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_trim_trees` | `QID195_10` | 76 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_drainage` | `QID195_11` | 77 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `exp_flooding` | `QID124_1` | 84 | Since you've lived in High Ridge Estates, have you experienced... - Flooding of house due to any disaster such | 2 | Weekly | RECODE |
| `exp_flood_help` | `QID124_2` | 85 | Since you've lived in High Ridge Estates, have you experienced... - In case of flooding experience, have you r | 2 | Weekly | RECODE |
| `exp_extreme_heat` | `QID124_3` | 86 | Since you've lived in High Ridge Estates, have you experienced... - Extreme heat in recent years? | 2 | Weekly | RECODE |
| `exp_school_change` | `QID124_4` | 87 | Since you've lived in High Ridge Estates, have you experienced... - Changing your kids' school due to moving? | 2 | Weekly | RECODE |
| `exp_law_enf` | `QID124_5` | 88 | Since you've lived in High Ridge Estates, have you experienced... - Calling law enforcement because of problem | 1 | Daily | RECODE |
| `exp_insurance_loss` | `QID124_6` | 89 | Since you've lived in High Ridge Estates, have you experienced... - Losing home owners insurance due to age of | 2 | Weekly | RECODE |
| `exp_well_dry` | `QID124_7` | 90 | Since you've lived in High Ridge Estates, have you experienced... - Well drying up? | 2 | Weekly | RECODE |
| `exp_pests` | `QID124_8` | 91 | Since you've lived in High Ridge Estates, have you experienced... - A problem with pests in your home? | 2 | Weekly | RECODE |
| `exp_water_leaks` | `QID124_9` | 92 | Since you've lived in High Ridge Estates, have you experienced... - A problem with water leaks? | 1 | Daily | RECODE |
| `exp_loose_animals` | `QID124_10` | 93 | Since you've lived in High Ridge Estates, have you experienced... - A problem with loose animals? | 2 | Weekly | RECODE |
| `car_access` | `QID211` | 133 | Do you (or your household) own or have regular access to a car? | 1 | Yes | RECODE |
| `hurricane_transport` | `QID219` | 134 | During disasters such as hurricanes, have you experienced transportation problems (for example, difficulty eva | 1 | Yes | RECODE |
| `education` | `QID178` | 142 | What is the highest level of education you have completed? (select the most applicable choice) | 5 | High school diploma or equivalent | RECODE |
| `employment` | `QID176` | 143 | Which best describes your employment status? | 4 | Retired | RECODE |

## 29. `R_oAELLLNZllsvEkJ` — 6413 Bowdoin Ave

| Field | QID | CSV col | Verbatim question (CSV row 1) | CSV cell | Popup / payload shows | Verdict |
|---|---|---|---|---|---|---|
| `years_in_hre` | `QID12_TEXT` | 27 | How long have you lived in High Ridge Estates? (years) | 9 | 9 | MATCH |
| `reloc_factor_emp` | `QID181_1` | 29 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 2 | Click to write Scale Point 2 | PLACEHOLDER |
| `reloc_factor_aff` | `QID181_2` | 30 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_qol` | `QID181_3` | 31 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_fam` | `QID181_4` | 32 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 2 | Click to write Scale Point 2 | PLACEHOLDER |
| `reloc_factor_ret` | `QID181_5` | 33 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_env` | `QID181_6` | 34 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 2 | Click to write Scale Point 2 | PLACEHOLDER |
| `reloc_factor_inh` | `QID181_7` | 35 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 2 | Click to write Scale Point 2 | PLACEHOLDER |
| `reloc_factor_oth` | `QID181_8` | 36 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | — | — | EMPTY-BOTH |
| `mh_skirting` | `QID100` | 42 | If you live in a mobile home, does your home have its skirting intact? | 1 | Click to write Choice 3 | PLACEHOLDER |
| `anticipated_stay` | `QID47` | 44 | How long do you anticipate continuing to live in your current house? (select the most applicable choice) | 4 | Others | RECODE |
| `safety_env` | `QID21` | 56 | Do you feel safe in your house in terms of environmental threats (e.g., flooding, heatwaves, heavy rain or win | 2 | More than 6 months | RECODE |
| `safety_social` | `QID194` | 57 | Do you feel safe in your house in terms of social threats (e.g., loose pets, concern about neighbor's behavior | 2 | More than 6 months | RECODE |
| `afford_urgency` | `QID17` | 58 | How would you rate the urgency of having affordable housing in High Ridge Estates? (select the most applicable | 2 | Click to write Choice 4 | PLACEHOLDER |
| `afford_strategy` | `QID19` | 59 | In your opinion, what is the most effective strategy to improve housing affordability in High Ridge Estates? ( | 2 | Yes- Integrated into central air heating system | RECODE |
| `intv_roof_walls` | `QID195_1` | 67 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_windows_doors` | `QID195_2` | 68 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_rain_gardens` | `QID195_3` | 69 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_hvac` | `QID195_4` | 70 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_plumbing_elec` | `QID195_5` | 71 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_well_septic` | `QID195_6` | 72 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_ccua_water` | `QID195_7` | 73 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_fence` | `QID195_8` | 74 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_trees_shade` | `QID195_9` | 75 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_trim_trees` | `QID195_10` | 76 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_drainage` | `QID195_11` | 77 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `exp_flooding` | `QID124_1` | 84 | Since you've lived in High Ridge Estates, have you experienced... - Flooding of house due to any disaster such | 2 | Weekly | RECODE |
| `exp_flood_help` | `QID124_2` | 85 | Since you've lived in High Ridge Estates, have you experienced... - In case of flooding experience, have you r | 2 | Weekly | RECODE |
| `exp_extreme_heat` | `QID124_3` | 86 | Since you've lived in High Ridge Estates, have you experienced... - Extreme heat in recent years? | 2 | Weekly | RECODE |
| `exp_school_change` | `QID124_4` | 87 | Since you've lived in High Ridge Estates, have you experienced... - Changing your kids' school due to moving? | 2 | Weekly | RECODE |
| `exp_law_enf` | `QID124_5` | 88 | Since you've lived in High Ridge Estates, have you experienced... - Calling law enforcement because of problem | 1 | Daily | RECODE |
| `exp_insurance_loss` | `QID124_6` | 89 | Since you've lived in High Ridge Estates, have you experienced... - Losing home owners insurance due to age of | 3 | Biweekly | RECODE |
| `exp_well_dry` | `QID124_7` | 90 | Since you've lived in High Ridge Estates, have you experienced... - Well drying up? | 3 | Biweekly | RECODE |
| `exp_pests` | `QID124_8` | 91 | Since you've lived in High Ridge Estates, have you experienced... - A problem with pests in your home? | 2 | Weekly | RECODE |
| `exp_water_leaks` | `QID124_9` | 92 | Since you've lived in High Ridge Estates, have you experienced... - A problem with water leaks? | 1 | Daily | RECODE |
| `exp_loose_animals` | `QID124_10` | 93 | Since you've lived in High Ridge Estates, have you experienced... - A problem with loose animals? | 1 | Daily | RECODE |
| `car_access` | `QID211` | 133 | Do you (or your household) own or have regular access to a car? | 1 | Yes | RECODE |
| `hurricane_transport` | `QID219` | 134 | During disasters such as hurricanes, have you experienced transportation problems (for example, difficulty eva | 2 | No | RECODE |
| `education` | `QID178` | 142 | What is the highest level of education you have completed? (select the most applicable choice) | 6 | Some college, no degree | RECODE |
| `employment` | `QID176` | 143 | Which best describes your employment status? | 4 | Retired | RECODE |

## 30. `R_orcmMnaQVATvgHJ` — 7183 Duke St

| Field | QID | CSV col | Verbatim question (CSV row 1) | CSV cell | Popup / payload shows | Verdict |
|---|---|---|---|---|---|---|
| `years_in_hre` | `QID12_TEXT` | 27 | How long have you lived in High Ridge Estates? (years) | 20 | 20 | MATCH |
| `reloc_factor_emp` | `QID181_1` | 29 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_aff` | `QID181_2` | 30 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `reloc_factor_qol` | `QID181_3` | 31 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 5 | Click to write Scale Point 5 | PLACEHOLDER |
| `reloc_factor_fam` | `QID181_4` | 32 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 2 | Click to write Scale Point 2 | PLACEHOLDER |
| `reloc_factor_ret` | `QID181_5` | 33 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_env` | `QID181_6` | 34 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 3 | Click to write Scale Point 3 | PLACEHOLDER |
| `reloc_factor_inh` | `QID181_7` | 35 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `reloc_factor_oth` | `QID181_8` | 36 | If you lived in another place before, how important were the following factors in relocating to High Ridge Est | — | — | EMPTY-BOTH |
| `mh_skirting` | `QID100` | 42 | If you live in a mobile home, does your home have its skirting intact? | 1 | Click to write Choice 3 | PLACEHOLDER |
| `anticipated_stay` | `QID47` | 44 | How long do you anticipate continuing to live in your current house? (select the most applicable choice) | 4 | Others | RECODE |
| `safety_env` | `QID21` | 56 | Do you feel safe in your house in terms of environmental threats (e.g., flooding, heatwaves, heavy rain or win | 4 | Click to write Choice 4 | PLACEHOLDER |
| `safety_social` | `QID194` | 57 | Do you feel safe in your house in terms of social threats (e.g., loose pets, concern about neighbor's behavior | 2 | More than 6 months | RECODE |
| `afford_urgency` | `QID17` | 58 | How would you rate the urgency of having affordable housing in High Ridge Estates? (select the most applicable | 1 | Click to write Choice 3 | PLACEHOLDER |
| `afford_strategy` | `QID19` | 59 | In your opinion, what is the most effective strategy to improve housing affordability in High Ridge Estates? ( | 1 | Yes - Portable (Which Room(s)) | RECODE |
| `intv_roof_walls` | `QID195_1` | 67 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_windows_doors` | `QID195_2` | 68 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 6 | Cultural & Historical sites and buildings (e.g., historical sites, iconic lighthouses, churches) | RECODE |
| `intv_rain_gardens` | `QID195_3` | 69 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_hvac` | `QID195_4` | 70 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_plumbing_elec` | `QID195_5` | 71 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_well_septic` | `QID195_6` | 72 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_ccua_water` | `QID195_7` | 73 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_fence` | `QID195_8` | 74 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_trees_shade` | `QID195_9` | 75 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_trim_trees` | `QID195_10` | 76 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `intv_drainage` | `QID195_11` | 77 | Please indicate whether you would like or would not like to have the following interventions to improve your h | 1 | Click to write Scale Point 1 | PLACEHOLDER |
| `exp_flooding` | `QID124_1` | 84 | Since you've lived in High Ridge Estates, have you experienced... - Flooding of house due to any disaster such | 2 | Weekly | RECODE |
| `exp_flood_help` | `QID124_2` | 85 | Since you've lived in High Ridge Estates, have you experienced... - In case of flooding experience, have you r | 2 | Weekly | RECODE |
| `exp_extreme_heat` | `QID124_3` | 86 | Since you've lived in High Ridge Estates, have you experienced... - Extreme heat in recent years? | 1 | Daily | RECODE |
| `exp_school_change` | `QID124_4` | 87 | Since you've lived in High Ridge Estates, have you experienced... - Changing your kids' school due to moving? | 2 | Weekly | RECODE |
| `exp_law_enf` | `QID124_5` | 88 | Since you've lived in High Ridge Estates, have you experienced... - Calling law enforcement because of problem | 2 | Weekly | RECODE |
| `exp_insurance_loss` | `QID124_6` | 89 | Since you've lived in High Ridge Estates, have you experienced... - Losing home owners insurance due to age of | 2 | Weekly | RECODE |
| `exp_well_dry` | `QID124_7` | 90 | Since you've lived in High Ridge Estates, have you experienced... - Well drying up? | 2 | Weekly | RECODE |
| `exp_pests` | `QID124_8` | 91 | Since you've lived in High Ridge Estates, have you experienced... - A problem with pests in your home? | 2 | Weekly | RECODE |
| `exp_water_leaks` | `QID124_9` | 92 | Since you've lived in High Ridge Estates, have you experienced... - A problem with water leaks? | 1 | Daily | RECODE |
| `exp_loose_animals` | `QID124_10` | 93 | Since you've lived in High Ridge Estates, have you experienced... - A problem with loose animals? | 1 | Daily | RECODE |
| `car_access` | `QID211` | 133 | Do you (or your household) own or have regular access to a car? | 1 | Yes | RECODE |
| `hurricane_transport` | `QID219` | 134 | During disasters such as hurricanes, have you experienced transportation problems (for example, difficulty eva | 2 | No | RECODE |
| `education` | `QID178` | 142 | What is the highest level of education you have completed? (select the most applicable choice) | 9 | Vocational/Technical Licensing or Certification | RECODE |
| `employment` | `QID176` | 143 | Which best describes your employment status? | 4 | Retired | RECODE |

