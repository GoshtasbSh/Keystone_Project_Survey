# test_ artifacts to delete after verification (Feature 1 + 2)

Project: keystore_Field (ioejtwseqsgidefkeyji). All ADDITIVE; no existing row modified.

## Auth + team_members
- auth user `test_member_qa@example.com` — uid `b545e67f-b056-47bd-a62d-da810dd982de` (+ its team_members row, role=member)
- (admin login reused: `test@test.com` — pre-existing sanctioned test admin, NOT created here, do NOT delete)

## field_guest_sessions
- gone guest `test_gone_guest` — id `9edf7239-01b7-4c12-b0c6-476bda977fbb`
- active guest `test_active_guest` — id `ea362464-edb9-40d4-85cc-561f01cf7c74`

## field_survey_points
- gone-guest authored point — id `98993890-7714-4d8b-89f6-b4e58012b191` (status No Answer, collector_name test_gone_guest)
- Feature-1 flip test point — id `64d0a8ef-ad05-4afe-9a3b-c7d5da8b5c5e` (collector_name test_qa_flip; created Inaccessible, flipped to Completed)

## Migration (separate — leave unless reverting feature)
- migration 24 functions: list_roster, active_member_ids, active_guests (DROP FUNCTION to revert)
