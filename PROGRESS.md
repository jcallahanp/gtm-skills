# Progress

## cpm-email (2026-11-20)

Done
- Attio fields created (people cpm_*, companies account_rep, Varonis Updates concept_tags/use_case/category/quote/verification).
- Skill scripts: read (allow-listed), match, check, write. Read tested against Attio: 64 people, only allow-listed keys.
- Dry-run load plan reviewed file: Drive "Past Meetings Skills/Attio Load – DRY RUN 2026-11-20".

Waiting on John
- Approve the dry run → run `tools/attio-load/apply_plan.py … --apply`.
- 11 companies have no rep in Attio; 25 near-duplicate update names to decide; 2 disputed stall reasons.
- Decide where the skill runs (local Claude Code plugin vs claude.ai skill upload).

Next
- After load: run the skill on 3 people, reviewer pass, then the full batch.
