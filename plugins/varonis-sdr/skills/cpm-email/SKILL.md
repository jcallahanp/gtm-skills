---
name: cpm-email
description: Use when John asks for reconnect emails to people we met with before ("past meetings", "CPM emails", "write the past meeting emails", "redo Brian's CPM email"). Reads everything from Attio through allow-listed scripts, writes drafts back to Attio, never sends.
---

# CPM (Contacts Past Meetings) reconnect emails

Everything this skill knows comes from Attio, read ONLY through the scripts in `scripts/`. Never call Attio any other way for this skill (no MCP record reads, no extra fields). The rules and John's examples live in the Attio Writing Rules record "CPM email"; follow them exactly.

## Guardrails

1. Read data only with `scripts/cpm_read.py`. It returns only allow-listed fields. If a fact is not in its output, it is unknown. Never use memory, the web or other Attio fields.
2. Write only with `scripts/cpm_write.py`. It can set only `cpm_draft`, `cpm_draft_status` (Drafted, Reviewed, Skipped) and `cpm_updates_used`. Never send email.
3. `cpm_route` = "Needs John" → write the card from the rules, not an email.
4. A different agent reviews each draft. The writer never reviews its own work.

## Steps

1. `python3 ${CLAUDE_SKILL_DIR}/scripts/cpm_read.py rules > rules.json` – read it fully before writing anything.
2. `python3 ${CLAUDE_SKILL_DIR}/scripts/cpm_read.py people --only-pending > people.json` (drop `--only-pending` to redo all, or pick the person John named).
3. `python3 ${CLAUDE_SKILL_DIR}/scripts/cpm_read.py updates > updates.json`
4. For each person with `cpm_obtained` = "Obtained":
   1. `python3 ${CLAUDE_SKILL_DIR}/scripts/cpm_match.py people.json updates.json RECORD_ID` → candidate updates.
   2. Write the email (or the card) by the rules; pick the closest example.
   3. Save the person object to `person.json` and the email to `draft.txt`; run `python3 ${CLAUDE_SKILL_DIR}/scripts/cpm_check.py person.json draft.txt`. Fix until it passes. Cards skip this check.
   4. `python3 ${CLAUDE_SKILL_DIR}/scripts/cpm_write.py RECORD_ID draft.txt Drafted [UPDATE_RECORD_IDS…]`
5. Review pass by a separate agent with only `rules.json`, the person object, the matched updates and the draft. It checks every fact traces to `cpm_concepts` / `cpm_evidence` / `cpm_stall_quote`, every update to a Varonis Updates row, "major" use, and no narrow detail that was not discussed. Pass → `cpm_write.py … Reviewed`; fail → fix and recheck.
6. Report to John: counts (drafted, reviewed, cards, skipped) and any person the reviewer flagged. John approves and sends in Attio.

## Needs

- `ATTIO_API_KEY` in the environment (cloud environment secret or local env).
- The Attio fields described in `README.md` of this repo.
