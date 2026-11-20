---
name: outreach-push
description: Use when John says to push, send or load approved CPM emails into Outreach ("push the approved drafts", "send them to Outreach"). Takes ONLY Email Drafts that John set to Approved in Attio, cleans them mechanically for sequence 1419 and starts Clay "Email Send Workflow" (formerly "Daily Queue - API"; always call it by its ID). Never writes or edits email text.
---

# Push approved drafts to Outreach (via Clay, sequence 1419)

## Guardrails

1. Only drafts with status **Approved** and kind **Email**. Never Drafted, Reviewed, cards, or anything already Pushed.
2. Never rewrite the email. The only changes are the mechanical ones in `scripts/transform.py`:
   - remove the greeting addressed to the person ("Hey Darin - ", "Steve - ", a "Hey Josh," line), because Outreach 1419 adds "Hi {first name},";
   - capitalize the new first letter;
   - remove any sign-off the draft has ("Best,", "Thanks", a name), then add exactly one "Best," as the last paragraph; the sequence adds the full email signature under it, so never add a name or signature block;
   - build the HTML: one `<p>` per paragraph, `<p><br></p>` between paragraphs.
   If the script reports a problem for a draft, skip that draft and tell John.
3. Pass `clay_inputs` to Clay exactly as the script printed them. Do not edit any value.
4. Approval is John's, given in chat. When John names drafts as approved, run `python3 ${CLAUDE_SKILL_DIR}/scripts/push_approve.py DRAFT_ID ...` (only Reviewed/Drafted Email drafts change; it writes status only). When John says "send those" / "send them", that is standing approval for every draft he approved: run the push for all of them with no more questions. Show the dry run (step 2) as information, not as a question. If a draft fails a guardrail, skip it and report it.
5. One draft per Clay run. Record every result in Attio, so a rerun never pushes twice.

## Steps

1. `python3 ${CLAUDE_SKILL_DIR}/scripts/push_prepare.py --exclude ${CLAUDE_PLUGIN_ROOT}/../../excludes/cpm-first-run.json > payloads.json` (while `excludes/cpm-first-run.json` exists in the repo, always pass it) (or pass specific draft IDs).
2. Show John, for each ready draft: name, recipient, subject and the cleaned body. List every problem.
3. After John's "send", for each ready draft:
   1. Call the Clay MCP tool `run_subroutine_direct` with `subroutine_id` `workflow:wf_0tmyifbTzDS2gDK6xdo` ("Email Send Workflow") and `inputs` = `[clay_inputs]`.
   2. Call the Clay MCP tool `get-task-context` with the returned `taskId` until `isComplete` is true. Read the enrichment `value` (JSON with `decision` and `reason`).
   3. `decision` is `skip` (not found, opted out, or already in a sequence), or the state is `error`: `python3 ${CLAUDE_SKILL_DIR}/scripts/push_record.py DRAFT_ID failed "REASON (clay task TASK_ID)"`.
   4. Otherwise: `python3 ${CLAUDE_SKILL_DIR}/scripts/push_record.py DRAFT_ID pushed "clay task TASK_ID"`.
   5. If the MCP call itself errors: record failed with the error text and continue with the next draft. Do not retry the same draft in the same run.
4. Report: pushed, failed (with reasons), skipped (with reasons).

## Needs

- `ATTIO_API_KEY` in the environment; the Clay MCP connector.
- The workflow's manual trigger (`cf33d8be-3be0-4bf0-85a1-a94de197e9a3`) must be **live**. If it is paused, the connector returns `ERROR_BAD_REQUEST` and the Public API returns "Trigger … not found". Fix: `clay workflows triggers update cf33d8be-3be0-4bf0-85a1-a94de197e9a3 --input '{"status":"live"}'` (never with `--resume-paused-runs`). The connector runs the **published** version of the workflow: publish changes in Clay before pushing.
- The workflow skips (never creates) people not found in Outreach, opted out, or active in any sequence. It looks them up by email or prospect id.
- Outreach sequence 1419 template adds "Hi {first name}," and the signature; Clay writes the body to Outreach's Personal Note fields.
