# SPEC – Attio data reliability + loop-you-in pilot

Status: CLOSED 2026-11-20. Inventory done (docs/attio-reliability-2026-11-20.md): Attio meeting data is stale or wrong, and John cannot connect Attio to company email/calendar. Decision: never use Attio meeting fields (rules v10). Loop-you-in only when John names a very recent meeting.

## Goal
1. Measure how reliable and current each Attio field is that could tell us "who at this company met with us recently, when, and about what".
2. Pilot the loop-you-in fallback (Robert Simms example) on a few people with no usable context, using only fields that pass step 1.

## Personas (definition of done)
- I am John using the cpm-email skill. I get a draft for a person with no context. I trust that the "we recently met with X in MONTH about TOPIC" line is true. I never have to check Salesforce to catch a wrong name or date.
- I am John reading the reliability report. I see each field with a coverage %, a freshness date and an error rate from a checked sample. I never have to guess which Attio fields are safe to use.

## Scope
- Read-only inventory of Attio. No writes except the report.
- Pilot: drafts only, reviewed by a separate agent, never pushed without John.
- The guardrail "Attio only for rep and contact details" stays for all other drafting. The pilot is the only exception, and only for the fields the inventory passes.

## Rule changes from John's examples (1–7, 9 applied in v9; 8 waits)
1. A support case or install detail counts as a topic (Kevin Porter: Interceptor; Brian Applegarth: AD, file servers); keep it broad. Card only when there is no topic at all.
2. Meeting one year ago or less: casual timing ("as this year comes to an end"), "a few key updates", no "major".
3. Executive titles: original topic plus at most one big platform (AI security); never a narrow feature.
4. No-context fallback ¶3: "how we've rebuilt the platform around AI, securing AI use while automating detection, response and data protection."
5. SFG-type pattern (office hours/syncs, no invite near the meeting date): vague "back and forth with Varonis a few years ago" email + fallback line.
6. Same evidence for several people at one account: flag "possible account-level data" for John; email may still use "in contract with us … split off".
7. Inactive email: disqualify, no card (done for Tim Anderson, Clayton Langston).
8. Loop-you-in fallback: this spec.
9. Add John's examples (Robert, Brian Peck, Brian/Scott, Kevin) to the rules as few-shot examples.

## Decisions (John, 2026-11-20)
- Fields to check: Attio meetings, emails, Salesforce-synced people and company fields.
- Accuracy check: John confirms the latest meeting at about 10 companies against Salesforce.
- Pilot people: Randy Remington, Justin Barta, Paul Forst, Jason Duff, Samuel Wolf (+ Robert Simms as the known-answer case: John says we met Tim Marczewski and Greg Colvin in Oct 2026 about the AI security platform).

## Plan
1. Inventory (one agent, read-only) → docs/attio-reliability-2026-11-20.md. Check: the file has a per-field table (coverage %, newest date, notes) and a 10-company sample table (company, latest meeting date, attendees, title/topic, source field). Robert Simms's company must show the Oct 2026 meeting, or the report says why not.
2. John marks each sample row right/wrong against Salesforce.
3. Fields with no wrong rows → allowed for loop-you-in. Then pilot drafts for the 5 (+ Robert), separate reviewer, John approves.

## Robert Simms example (John, loop-you-in + past meeting)
Hey Robert - understand you were part of the Varonis POC back in 2024 but it looks like that stalled.

We recently met with Tim Marczewski and Greg Colvin back in October regarding our new AI security platform

Looking to loop you in to our more recent conversations to get your perspective on the tool.

Think you could squeeze in a 30 minute convo before the holidays?
