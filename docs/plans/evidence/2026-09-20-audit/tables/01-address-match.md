# Table 01 — Address match across 4 independent sources

One row per sampled point. Every value is sourced: the popup column is the header of the popup opened by a real click on the live `-blue` dashboard; the Qualtrics column is the respondent's own typed address (`Q212`) read straight from the CSV; the contact column is the nearest addressed community-canvass record from the admin (unstripped) `/api/survey-points` payload.

`EXACT` = identical after case/whitespace/street-suffix normalisation. `NORMALIZED` = same address, differing only by suffix abbreviation or punctuation. `MISMATCH` = different household. `UNVERIFIED` = could not be sourced, with reason.

| # | ResponseId | Popup header (live) | Qualtrics `Q212` (CSV) | Nearest addressed contact | dist (m) | coord_source | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | `R_1E4YReRP6XTeX06` | 6390 Bucknell Ave | 6390 Bucknell Ave KH | 6390 Bucknell Ave | 0.0 | address_matched | NORMALIZED |
| 2 | `R_23kV7GlWM0LQkKc` | 6176 Harvard Avenue | 6176 Harvard Ave | 6176 Harvard Avenue | 0.0 | address_matched | EXACT |
| 3 | `R_378SeCJx2uslNli` | 6369 Dennison | 6369 Dennison Ave Keystone Heights Florida 32656 | 6369 Dennison | 0.0 | address_matched | NORMALIZED |
| 4 | `R_3N0BugWZGh4ufub` | 6348 Baylor Avenue | 6348 Baylor Ave | 6348 Baylor Avenue | 0.0 | address_matched | EXACT |
| 5 | `R_43YLnrxxRNRA5hW` | 6260 Baylor Avenue | 6260 Baylor Ave | 6260 Baylor Avenue | 0.0 | address_matched | EXACT |
| 6 | `R_5241irqeSjBwQi1` | 7171 Pembroke Street | 7171 Pembroke st | 7171 Pembroke Street | 0.0 | address_matched | EXACT |
| 7 | `R_53V7a6BGdQkzzSd` | 7160 Pembroke Street | 7160 Pembroke st | 7160 Pembroke Street | 0.0 | address_matched | EXACT |
| 8 | `R_5BmauNbh58cXIzf` | 6280 Dennison | 6280 dennison ave | 6280 Dennison | 0.0 | address_matched | NORMALIZED |
| 9 | `R_5CxQduTse6FT7Z4` | 7156 Duke Street | 7156 Duke Street Keystone heights FL 32656 | 7156 Duke Street | 0.0 | address_matched | NORMALIZED |
| 10 | `R_5TtaBRz99nWhzm1` | 7173 Duke Street | 7173 Duke Street | 7173 Duke Street | 0.0 | address_matched | EXACT |
| 11 | `R_5tJl6j6gNRyLVMe` | 6220 Colgate Rd | 6220 Colgate Rd | 6220 Colgate Rd | 0.0 | address_matched | EXACT |
| 12 | `R_6SGNzs6svx7pBbb` | Dennison | 6308 Dennison Avenue Keystone Heights FL 32656 | 6308 Dennison | 0.0 | address_matched | STREET-ONLY (address data agrees) |
| 13 | `R_6s0PVusMDUucFQY` | Dennison | 6255 Dennison ave keystone heights fl 32656 | 6255 Dennison | 0.0 | address_matched | STREET-ONLY (address data agrees) |
| 14 | `R_6xzTr24XxYm8KC4` | 7276 Temple | 7276 Temple St | 7276 Temple | 0.0 | address_matched | NORMALIZED |
| 15 | `R_71LqP7xFx71BPsl` | Baylor Ave | 6414 Baylor Avenue | 6414 Baylor Avenue | 0.0 | address_matched | STREET-ONLY (address data agrees) |
| 16 | `R_78TZ7UtnmZU0jKm` | 7201 Notre Dame St | 7201 Notre Dame | 7201 Notre Dame St | 0.0 | address_matched | NORMALIZED |
| 17 | `R_87qCLdadYRHhw4P` | 6200 Harvard Avenue | 6200 Harvard Ave | 6200 Harvard Avenue | 0.0 | address_matched | EXACT |
| 18 | `R_8iSqFy8YDl9Xt1b` | 6397 Cascade Drive | 6397 Cascade Drive | 6397 Cascade Drive | 0.0 | address_matched | EXACT |
| 19 | `R_aPZYZkLLHTo3YDR` | 6392 Beloit Avenue | 6392 Beloit KH | 6392 Beloit Avenue | 0.0 | address_matched | NORMALIZED |
| 20 | `R_bt9KhSC0xqF2xuS` | Beloit Ave | 6409 Beloit Ave KH | 6405 Beloit Avenue | 34.3 | parcel_exact | STREET-ONLY (contact differs) |
| 21 | `R_bxz0eWgFA4AstpB` | 7239 Purdue Street | 7239 Purdue St | 7239 Purdue Street | 0.0 | address_matched | EXACT |
| 22 | `R_d4T4ee11cH6ntjW` | 7197 Pembroke Street | 7197 Pembroke st., keystone Heights FL | 7197 Pembroke Street | 0.0 | address_matched | NORMALIZED |
| 23 | `R_h0LfcAVvLrGULaj` | 7166 Pembroke Street | 7166 Pembroke st | 7166 Pembroke Street | 0.0 | address_matched | EXACT |
| 24 | `R_iGZqrFKoHdcjKOH` | 6394 Baylor Avenue | 6394 Baylor Ave 32656 | 6394 Baylor Avenue | 0.0 | address_matched | NORMALIZED |
| 25 | `R_jIMWa4XhirJ5WDy` | 6301 Columbia Avenue | 6301 Columbia Avenue Apt C, Keystone Heights FL | 6301 Columbia Avenue | 0.0 | address_matched | NORMALIZED |
| 26 | `R_kVLcdKScFHPgWVR` | 6308 Bucknell | 6308 Bucknell Avenue, Keystone Heights, FL 32656 | 6308 Bucknell | 0.0 | address_matched | NORMALIZED |
| 27 | `R_l1yOBZ0aTpnAxq3` | 7358 Yale St. | 7358 Yale st | 7358 Yale St. | 0.0 | address_matched | EXACT |
| 28 | `R_mhCImQQ64DBmsPH` | 6389 Baylor | 6389 Baylor Ave kh FL 32656 | 6389 Baylor | 0.0 | address_matched | NORMALIZED |
| 29 | `R_oAELLLNZllsvEkJ` | 6413 Bowdoin Ave | 6413 bowdoin | 6413 Bowdoin Ave | 0.0 | address_matched | NORMALIZED |
| 30 | `R_orcmMnaQVATvgHJ` | 7183 Duke St | 7183 Duke Street, Keystone Heights, Florida, 32656 | 7183 Duke St | 0.0 | address_matched | NORMALIZED |

## Summary

| Verdict | Count |
|---|---|
| NORMALIZED | 14 |
| EXACT | 12 |
| STREET-ONLY (address data agrees) | 3 |
| STREET-ONLY (contact differs) | 1 |

Total sampled points: **30**.
