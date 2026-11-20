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

- Old Attio Writing Rules renamed ARCHIVED; past_meeting_context, past_meeting_summary, meeting_context archived; old attio-* skills removed from claude.ai by John.

- TEMP excludes for the first run: excludes/cpm-first-run.json (Attio record ids of exact name matches from John's Orum list: 2 people). Rule: names only, exact match only; near matches go to John (Brent Nelson vs Brian Nelson: not excluded). Call notes are never used. Delete the file and the --exclude flags after Attio hygiene.
- First test drafts in Attio (Reviewed): Brian Nelson, Nahuel Chinchilla, Rick DeLoach. Waiting for John to set one to Approved for a single live push.

Open
- 11 companies have no rep in Attio (no combined parent record with a rep either) → emails name no rep.
- 2 disputed stall reasons written as Unknown (Jeff Morris, Phillip Graves).
- Where the skill runs: local Claude Code plugin, or upload to claude.ai skills for cloud/Cowork.

Next
- outreach-push skill built (sequence 1419, greeting/sign-off stripped by script). Not yet run against Clay: first live push needs John's yes.
- Run the skill on 3 people with a separate reviewer, then the full batch (32 drafts + 9 cards).
