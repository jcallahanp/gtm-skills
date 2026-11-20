# gtm-skills

John's Claude skills, one place. Each plugin folder holds skills; each skill holds its `SKILL.md` and scripts.

```
.claude-plugin/marketplace.json        catalog (Claude Code plugin marketplace)
plugins/varonis-sdr/                   plugin: SDR skills that run off Attio
  skills/cpm-email/                    drafts reconnect emails for past meetings (Attio Email Drafts)
  skills/outreach-push/                pushes Approved drafts to Outreach via Clay (sequence 1419)
tools/attio-load/                      one-off loaders that set up Attio for a skill
PROGRESS.md                            current state – read first
```

## How it reaches Claude

| Where you run | How the skill loads |
| --- | --- |
| Claude Code on your computer | `/plugin marketplace add jcallahanp/gtm-skills` then `/plugin install varonis-sdr@gtm-skills` |
| Claude Code cloud sessions (claude.ai/code) and Cowork | Plugins from a marketplace are not installed there. Upload the skill folder as a skill on claude.ai (Customize → Skills), or open the session on this repo after copying the skill to `.claude/skills/`. |

Source of truth for wording: the Drive docs in "Past Meetings Skills". Their content is copied into the Attio Writing Rules record that the skill reads at run time.

## cpm-email – Attio fields

People (view "Prioritized - Past Meetings"): `cpm_obtained`, `cpm_not_obtained_reason`, `cpm_route`, `cpm_route_reason`, `cpm_concepts`, `cpm_concept_tags`, `cpm_evidence`, `cpm_past_rep`, `cpm_stall_reason`, `cpm_stall_quote`.
Email Drafts (object `email_drafts`): `name`, `person`, `campaign`, `kind`, `subject`, `body`, `body_html`, `updates_used`, `rules_version`, `status` (Drafted → Reviewed → Approved → Pushed / Failed / Superseded), `drafted_at`, `review_notes`, `supersedes`, `pushed_at`, `push_result`. Text is never edited after it is written; corrections are new records.
Companies: `account_rep` (select: Todd Cencich, Rob Andersen, Patrick Dolan).
Varonis Updates: adds `concept_tags`, `use_case`, `category`, `quote`, `verification`.
Writing Rules: record "CPM email" (`rules`, `examples`).

The skill reads ONLY these plus `name`, `email_addresses`, `job_title`, `salesforce_title`, `company`, `past_meeting_date` (see `scripts/attio.py`). It writes only Email Draft records: new drafts, and status/review notes on its own Drafted records. Approved is set by John; Pushed/Failed by the push skill. The old people fields `cpm_draft`, `cpm_draft_status`, `cpm_updates_used` are archived.

Secrets: `ATTIO_API_KEY` from the environment. Never commit keys or prospect data.

## Company mapping in Attio

Some old company records were merged into combined records (subsidiaries, renamed parents), for example "FIS (Fidelity Information Services, FIS Global)". The skill always follows the person's current Attio company link for `account_rep` and the company name, never the name in the old source sheet.

## outreach-push

Reads only Email Drafts with status Approved and kind Email. Cleans them mechanically (removes the greeting to the person and any sign-off, because sequence 1419 adds "Hi {first name}," and the signature), builds the `<p>` HTML, and starts Clay "Daily Queue - API" (sequence 1419) one draft at a time. Writes only status (Pushed/Failed), `pushed_at`, `push_result` on the draft. Dry run first, push only on John's yes.
