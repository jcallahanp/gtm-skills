---
name: outreach-push
description: Use when John says to push, send or load approved CPM emails into Outreach ("push the approved drafts", "send them to Outreach"). Takes ONLY Email Drafts that John set to Approved in Attio, cleans them mechanically for sequence 1419 and starts Clay "Daily Queue - API". Never writes or edits email text.
---

# Push approved drafts to Outreach (via Clay, sequence 1419)

## Guardrails

1. Only drafts with status **Approved** and kind **Email**. Never Drafted, Reviewed, cards, or anything already Pushed.
2. Never rewrite the email. The only changes are the mechanical ones in `scripts/transform.py`:
   - remove the greeting addressed to the person ("Hey Darin - ", "Steve - ", a "Hey Josh," line), because Outreach 1419 adds "Hi {first name},";
   - capitalize the new first letter;
   - remove any sign-off ("Best,", "Thanks", a name), because the sequence adds the signature;
   - build the HTML: one `<p>` per paragraph, `<p><br></p>` between paragraphs.
   If the script reports a problem for a draft, skip that draft and tell John.
3. Pass `clay_inputs` to Clay exactly as the script printed them. Do not edit any value.
4. Always show John the dry run first and push only after he says yes in this conversation.
5. One draft per Clay run. Record every result in Attio, so a rerun never pushes twice.

## Steps

1. `python3 ${CLAUDE_SKILL_DIR}/scripts/push_prepare.py > payloads.json` (or pass specific draft IDs).
2. Show John, for each ready draft: name, recipient, subject and the cleaned body. List every problem. Ask for a yes.
3. On yes, for each ready draft:
   1. Call the Clay MCP tool `run_subroutine_direct` with `subroutine_id` `workflow:wf_0tmyifbTzDS2gDK6xdo` ("Daily Queue - API") and `inputs` = `[clay_inputs]`.
   2. If Clay accepts the run: `python3 ${CLAUDE_SKILL_DIR}/scripts/push_record.py DRAFT_ID pushed "clay task TASK_ID"`.
   3. If it errors: `python3 ${CLAUDE_SKILL_DIR}/scripts/push_record.py DRAFT_ID failed "ERROR TEXT"` and continue with the next draft.
4. Report: pushed, failed (with reasons), skipped (with reasons).

## Needs

- `ATTIO_API_KEY` in the environment; the Clay MCP connector.
- Outreach sequence 1419 template adds "Hi {first name}," and the signature; Clay writes the body to Outreach's Personal Note fields.
