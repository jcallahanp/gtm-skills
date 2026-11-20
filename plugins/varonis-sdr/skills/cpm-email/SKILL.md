---
name: cpm-email
description: Use when John asks for reconnect emails to people we met with before ("past meetings", "CPM emails", "write the past meeting emails", "redo Brian's CPM email"). Reads everything from Attio through allow-listed scripts and saves each draft as an Attio "Email Draft" record. Never approves, never pushes, never sends.
---

# CPM (Contacts Past Meetings) reconnect emails – drafting only

Everything this skill knows comes from Attio, read ONLY through the scripts in `scripts/`. Never call Attio any other way for this skill (no MCP record reads, no extra fields). The rules and John's examples live in the Attio Writing Rules record "CPM email"; follow them exactly. Pushing to Outreach is a separate skill.

## Guardrails

1. Read data only with `scripts/cpm_read.py`. It returns only allow-listed fields. If a fact is not in its output, it is unknown. Never use memory, the web or other Attio fields.
2. Write only Email Draft records, only with `scripts/cpm_write.py` (new draft) and `scripts/cpm_review.py` (review result). A draft's text is never edited: a correction is a new draft and the old one becomes Superseded.
3. This skill may set status Drafted, Reviewed or Superseded only. Approved is John's. Pushed/Failed belong to the push skill. If a person's latest draft is Approved or Pushed, stop and ask John.
4. `cpm_route` = "Needs John" → write the card from the rules (kind `card`), not an email.
5. A different agent reviews each draft. The writer never reviews its own work.

## Steps

1. `python3 ${CLAUDE_SKILL_DIR}/scripts/cpm_read.py rules > rules.json` – read it fully before writing anything.
2. `python3 ${CLAUDE_SKILL_DIR}/scripts/cpm_read.py people --only-pending > people.json` (no flag = everyone; or pick the person John named).
3. `python3 ${CLAUDE_SKILL_DIR}/scripts/cpm_read.py updates > updates.json`
4. For each person with `cpm_obtained` = "Obtained":
   1. `python3 ${CLAUDE_SKILL_DIR}/scripts/cpm_match.py people.json updates.json PERSON_RECORD_ID` → candidate updates.
   2. Write the email (or card) by the rules; pick the closest example.
   3. Save the person object to `person.json` and the text to `draft.txt`. For emails run `python3 ${CLAUDE_SKILL_DIR}/scripts/cpm_check.py person.json draft.txt` and fix until it passes.
   4. `python3 ${CLAUDE_SKILL_DIR}/scripts/cpm_write.py PERSON_RECORD_ID "Full Name" email|card "continued conversations" draft.txt --updates UPDATE_IDS…`
5. Review by a separate agent with only `rules.json`, the person object, the matched updates and the draft. It checks every fact traces to `cpm_concepts` / `cpm_evidence` / `cpm_stall_quote`, every update to a Varonis Updates row, "major" use, and no narrow detail that was not discussed. Then `python3 ${CLAUDE_SKILL_DIR}/scripts/cpm_review.py DRAFT_ID pass|fail "notes"`. On fail: write a corrected new draft (step 4) and review again.
6. Report to John: counts (drafted, reviewed, cards) and anything the reviewer flagged. John sets Approved in Attio.

## Needs

- `ATTIO_API_KEY` in the environment.
- The Attio setup described in this repo's `README.md`.
