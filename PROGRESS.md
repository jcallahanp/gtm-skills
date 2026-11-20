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
- Drive run book is now "HOW TO RUN (v3)" (Attio + two skills); v2 SUPERSEDED.
- Where the skill runs: local Claude Code plugin, or upload to claude.ai skills for cloud/Cowork.

Next
- outreach-push skill built (sequence 1419, greeting/sign-off stripped by script).
- 2026-11-20: push path fixed. Cause: the workflow's manual trigger was paused (connector ERROR_BAD_REQUEST, API "Trigger not found"). Trigger set to live (no paused runs resumed). Verified: connector run wfr_0tot7y3YzYAyPFBjAkP on the published snapshot, fake email → skip "Not found in Outreach". Skill now reads the decision via get-task-context; skip → Failed.
- 2026-11-20: first live push done. Nahuel v2 → Approved (chat) → Clay run wfr_0tot86k2MWnKw2T8pDo, all steps completed, decision ok → Outreach prospect 1046615, sequence 1419 → draft Pushed. Waiting for John to check it in Outreach.
- Run the skill on 3 people with a separate reviewer, then the full batch (32 drafts + 9 cards).

## Full run (started 2026-11-20)
John: "draft them out for all the eligible past meetings and then approve and push them all".
- Scope: 36 Obtained people with no draft (27 Draft route → emails, 9 Needs John → cards). Excluded: excludes file (2). Already drafted: Brian Nelson, Rick DeLoach (Reviewed), Nahuel (Pushed).
- Process: 4 writer agents (9 people each) → 4 different reviewer agents → push only emails with review pass. Cards and Not-obtained people are never pushed.
- Restart: rerun `cpm_read.py people --only-pending`; anyone with latest_draft_status set is done for drafting. Push = Approved/Reviewed emails not yet Pushed.

### Full run results (2026-11-20)
- Drafted 36 (27 emails, 9 cards). Review round 1: 28 pass, 8 fail. Rewrite: 4 new drafts (Phillip Graves, Samuel Wolf, Scott Edmonston, Philip Tyson) under re-review; 4 sent to John, no real concept beyond invite agenda/placeholder (Randy Remington, Justin Barta, Paul Forst, Jason Duff).
- Held for John: Brian Nelson (John disliked earlier text), David Sypros (evidence emails addressed to "John" at Landstar; attendance unclear).
- Pushed 19 approved emails in one Clay task (mcp-task_0tot8spjmECmbbiQTQX):
  - Added to 1419 (Pushed): Carl Luke, Jim Mountain, Saif Arif, Pedameerasa Chennupalli, Eric Lukens, Chris Sundell.
  - Skipped, active in "Callahan: Email Sequence": Sam Kolars, Steve Hickle, Darin Gottman, Hermann Kelley, Kong Tran, Chris Gervich.
  - Skipped, active in "Cold Emails - Auto 8-Bump Sequence": Jeff Morris, Rick DeLoach, Bernita McCully.
  - Skipped, opted out: Mark Garton, Mark Wise.
  - Error, already been in 1419 before (personal notes written): Paul Suarez, Wesley Bard.
- Bug fixed: transform.py now strips nickname greetings ("Hey Wes -", "Hi Meer -").
- Open: workflow gap (no check for past 1419 membership); John to decide on the 9 + 2 + 2 skipped/errored, 9 cards, 4 no-concept people, 2 held.
