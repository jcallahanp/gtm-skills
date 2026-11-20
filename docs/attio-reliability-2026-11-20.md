# Attio reliability inventory – 2026-11-20

Question: can Attio tell us "who at this company met with Varonis recently, when, and about what"?
Read-only check. Population: people view "Prioritized - Past Meetings" (filter rebuilt via REST: 61 people, close to the ~64 John sees; the gap is likely the view's relative 180-day date boundary) and their 40 companies. Workspace-wide numbers (7,576 people) are given where they matter.

## Headline
- **Attio has no calendar or email sync.** `search-meetings` (2015–2027) and the REST `/meetings` endpoint return 0 meetings; `search-emails-by-metadata` returns 0 emails (also for mo.gov); `last_calendar_interaction`, `last_email_interaction`, `last_interaction` are empty on all 7,576 people and all 40 companies. The only activity type is phone calls.
- **Salesforce data is a one-time snapshot, not a live sync.** Every `salesforce_*` value was written by an API token on 2026-11-07/08. Newest Salesforce meeting date in the whole workspace: 2026-10-27. Nothing after ~7 Nov will appear.
- **No source records Varonis-side attendees.** Company `rep`/`account_rep` is the account owner, not who attended. `cpm_evidence` says "Varonis sender: unknown".
- **No source records the topic as data.** Topics only exist in free text (human `past_meetings`, agent-written `account_meetings` / `synthesis_note_6` / `warm_note`), and these contain errors (below).

## 1. Per-field table (61 people / 40 companies in the view)

| Field | What it claims | Coverage | Newest | Oldest | Notes |
|---|---|---|---|---|---|
| Attio meetings (calendar sync) | Meetings + participants | 0% | – | – | No meetings exist in the workspace. |
| Attio emails (mailbox sync) | Email threads | 0% | – | – | No emails exist in the workspace. |
| people/companies `*_calendar_interaction`, `*_email_interaction`, `last_interaction` | Attio-computed last touch | 0% | – | – | Empty everywhere (follows from no sync). |
| people.`salesforce_last_meeting` | SF last completed meeting (person) | 91% (56/61) | 2026-05-21 (view) / 2026-10-27 (workspace) | 2014-01-15 | Snapshot 2026-11-07/08. Date only: no topic, no Varonis attendee. Misses SDR-booked meetings (21 people workspace-wide have a `meeting_date` but no SF date, e.g. Tim Marczewski, Diego Idi, Cole Hutchcraft, John Bailey). Differs from `meeting_date` for 4 of 9 people having both (Hasan Erden 10-01 vs 10-03; Tim Glen 10-23 vs 10-24; Nikoloz Lartsuliani 10-20 vs 09-15; Michael Brown 2025-12-29 vs 2026-11-04). |
| people.`past_meeting_date` | Past meeting date used by skills | 91% (56/61) | 2026-05-21 | 2014-01-15 | Identical to `salesforce_last_meeting` for all 61 (a copy, not a second source). View filter excludes anyone met in last 180 days, so view newest is May 2026 by design. |
| people.`salesforce_last_cancelled` / `cancelled_meeting_date` | Last cancelled meeting | 5% (3/61) | 2026-05-08 | 2025-06-17 | Same snapshot. |
| people.`meeting_date` + `meeting_result` / `call_result` | SDR-logged booked meeting and outcome | 0% in view; 30 people workspace-wide | 2026-12-04 (future) | – | John's own booking log, set when booked. Best source for meetings John booked (incl. Tim Marczewski). Covers only SDR-booked meetings since Oct 2026. |
| people.`salesforce_comments`, `salesforce_sales_notes`, `salesforce_latest_campaign` | SF free text | 78% / 73% / 67% | – | – | Snapshot. Call notes and campaign tags, not meeting records. |
| people.`salesforce_account_owner` | SF account owner | 100% | – | – | Owner, not a meeting attendee. |
| people.`cpm_evidence` | Agent-cited evidence list | 63% (39/61) | – | – | Agent output; cites "Varonis sender: unknown". |
| people.`warm_note`, `synthesis_note_6`, `prep_note` | Agent/SDR summaries | 89% / 100% / 100% | – | – | Can be stale or wrong: Tom Scroggins warm_note "Met April 2026" but SF says 2026-10-27; Greg Colvin synthesis_note says we "also recently" met Robert Simms and Theresa Frommel (2024-11-22 and 2023-04-28). |
| companies.`past_meetings` | Dated list: person, title, note | 47% (19/40) | 2026-10-13 | 2025-08-22 (newest per company) | Hand-written by a workspace member on 2026-10-21; frozen since. Misses later meetings (Principal: Tom Scroggins 2026-10-27; Missouri: Tim Marczewski 2026-10-13). Most lines say "No notes". Best topic source when notes exist. |
| companies.`account_meetings` | Person: topic (year) | 97% (39/40) | year only (newest "2026"); its ISO dates are deal close dates | year only | Agent-written by API token 2026-11-11/12. Year errors: ITA Group shows Randy Remington "(2026)" (met 2025-12-08) and David Benz "(2026)" (met 2021-03-09). Missouri topic "AI security" for Greg Colvin is not backed by `past_meetings` ("No notes"). |
| companies.`salesforce_history` | SF deals + next-steps log | 90% (36/40) | 2027-06-17 (close dates) | 2017-11-27 | Snapshot 2026-11-11. Deal-level, not meeting-level. Good for old context (e.g. Missouri 2024 POC). |
| companies.`timing_note` | Human summary | 42% (17/40) | – | – | Written 2026-10-21. |
| companies.`rep` / `account_rep` | Account rep | 75% / 75% | – | – | Owner only. |
| Notes (`search-notes-by-metadata`) | Notes on records | Missouri company: 0 | – | – | Workspace notes are Clay import notes, not meeting notes. |

## 2. 10-company sample (for John to mark right/wrong against Salesforce)

Varonis attendees are not recorded in any Attio source for any row.

| Company | Latest meeting found | Customer attendees | Title/topic | Source |
|---|---|---|---|---|
| State of Missouri (Robert Simms) | 2026-10-13 | Greg Colvin; Tim Marczewski (SDR log only) | "AI security (2026)" in agent text only; `past_meetings` says "No notes" | SF `salesforce_last_meeting` (Greg); `meeting_date`+`meeting_result`=Completed (Tim, Greg); `past_meetings`; `account_meetings` |
| ITA Group (Randy Remington) | 2025-12-08 | Randy Remington | Securing Microsoft 365 and Salesforce; referred by CIO | SF last meeting; `past_meetings` (`account_meetings` says 2026: wrong year) |
| Jabil (Justin Barta, Jason Duff) | 2026-10-01 (SF) / 2026-10-03 (SDR log) | Hasan Erden | "Jabil sync"; no notes | SF; `meeting_date` (2-day mismatch). Barta/Duff: 2025-11-13 group meeting, topic "met" only |
| Nature's Bounty (Paul Forst) | 2022-11-01 | Matthew Tucker (Paul Forst 2022-02-16) | Varonis overview (2022) | SF; `account_meetings`. No `past_meetings`, no rep |
| Principal Financial Group (Samuel Wolf) | 2026-10-27 | Tom Scroggins | DAM (agent text); `past_meetings` stops at 2026-10-07 (Robert Urich, "No notes") | SF; `meeting_date`. `past_meetings` stale |
| Casey's General Stores | 2026-10-10 (SDR) / 2026-10-09 (`past_meetings`) | Diego Idi | No notes | `meeting_date`; `past_meetings`. Not in SF snapshot (SF latest 2026-08-25 Jeff Potter, Copilot rollout trial) |
| Belden | 2026-09-16 | Cole Hutchcraft | No notes; earlier emails on sensitive data in file shares/SharePoint/M365 | `meeting_date`; `past_meetings`. Not in SF (SF latest 2026-06-04 Joel Naumoff, RSAC, Salesforce + AI security eval) |
| Steelcase | 2026-08-21 | Dirk Dykstra | No notes; met at CloudCon | SF; `past_meetings` |
| Washington University in St. Louis | 2026-08-17 | John Bailey | No notes; "linked to current AI (Atlas) talks" | `meeting_date`; `past_meetings`. Not in SF (SF latest 2025-07-08) |
| Emerson Electric | 2026-07-30 | James Shewmake | No notes | `past_meetings` only (SF latest 2025-10-14; Mike Hahn 2026-07-23 in SDR log only) |

## 3. Known-answer check: State of Missouri, Oct 2026, Tim Marczewski + Greg Colvin, AI security platform

- **Date and Greg: yes.** Greg Colvin: `salesforce_last_meeting` = `past_meeting_date` = 2026-10-13; `meeting_date` 2026-10-13, `meeting_result` Completed, `result_note` "Met on the 13th; can't contact him till April 13, 2027." Company `past_meetings` line 2026-10-13 Greg Colvin.
- **Tim: only in John's SDR fields.** Tim Marczewski (Director of Artificial Intelligence and Innovation, linked to State of Missouri): `meeting_date` 2026-10-13, `meeting_result` Completed, `call_result` "Meeting Completed", `result_note` "Ended up meeting with us." He has **no** Salesforce meeting date (`from_salesforce` = false, not in the SF snapshot) and is **not** in company `past_meetings`. Nothing in Attio links Tim and Greg to the same meeting.
- **Topic: not source-backed.** "AI security" appears only in agent-written text (`account_meetings` "Greg Colvin…: AI security (2026)", Greg's `synthesis_note_6`). The human `past_meetings` line says "No notes". Tim's title and Megan Stokes's 2026-09-29 meeting "with the broader AI team" make it plausible, but Attio has no record of the topic.
- **Why:** no calendar/email sync in Attio, the Salesforce data is a one-off snapshot without topics, and `past_meetings` was hand-written on 2026-10-21 from Salesforce records that did not include Tim.

## 4. Verdict

- **Usable for WHO + WHEN (customer side), with care:** `salesforce_last_meeting` (= `past_meeting_date`) for meetings before ~2026-11-07, plus `meeting_date` + `meeting_result`=Completed for meetings John booked. Use both; they disagree on the date in 4 of 9 overlaps, so state the month, not the day.
- **Usable for TOPIC only when it is a real note:** company `past_meetings` lines that have notes (not "No notes"). Frozen at 2026-10-21.
- **Not safe:** Attio meetings/emails/interaction fields (empty); `account_meetings` (wrong years, inferred topics); `synthesis_note_6` / `warm_note` / `prep_note` (stale or wrong "recently" claims); `rep`/`account_owner` as an attendee.
- **Not available anywhere in Attio:** Varonis-side attendees; meetings after ~2026-11-07; topic for most meetings (most lines are "No notes").
- **John must check:** the topic of every meeting (including Missouri's "AI security platform"), the exact month when SF and SDR dates differ, any co-attendee pairing (e.g. Tim + Greg), and any meeting after 7 Nov. Connecting Attio calendar/email sync, or a fresh Salesforce activity export with subjects, would fix the root cause.
