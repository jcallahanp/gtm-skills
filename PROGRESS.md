# Progress

## cpm-email (2026-11-20)

Done
- Attio fields created (people cpm_*, companies account_rep, Varonis Updates concept_tags/use_case/category/quote/verification).
- Load applied: 372 writes OK. Verified by reading back through cpm_read.py: 64 people, 0 field mismatches vs plan;
  41 Obtained / 23 Not obtained; route 32 Draft / 9 Needs John; 52 of 64 people have an account_rep.
- Varonis Updates: 261 rows (75 existing + 204 new − 18 merged near-duplicates). 7 similar-name pairs kept separate on purpose.
- Writing Rules record "CPM email" holds the v8 rules + examples A–I word for word, plus the Attio field map.
- Skill scripts: read (allow-listed), match, check, write.

- Email Drafts object created (2026-11-20) with drafted_at; skill writes drafts there. Tested create → supersede → review → Approved lock; test records deleted.

Open
- 11 companies have no rep in Attio (no combined parent record with a rep either) → emails name no rep.
- 2 disputed stall reasons written as Unknown (Jeff Morris, Phillip Graves).
- Where the skill runs: local Claude Code plugin, or upload to claude.ai skills for cloud/Cowork.

Next
- Build the outreach-push skill (Clay "Daily Queue - API"; needs CPM sequence ID).
- Run the skill on 3 people with a separate reviewer, then the full batch (32 drafts + 9 cards).
