# SPEC – Attio data reliability + loop-you-in pilot

Status: draft, waiting for John's answers (bottom). Started 2026-11-20.

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

## Rule changes from John's examples (proposed, not yet applied)
1. A support case or install detail counts as a topic (Kevin Porter: Interceptor; Brian Applegarth: AD, file servers); keep it broad. Card only when there is no topic at all.
2. Meeting one year ago or less: casual timing ("as this year comes to an end"), "a few key updates", no "major".
3. Executive titles: original topic plus at most one big platform (AI security); never a narrow feature.
4. No-context fallback ¶3: "how we've rebuilt the platform around AI, securing AI use while automating detection, response and data protection."
5. SFG-type pattern (office hours/syncs, no invite near the meeting date): vague "back and forth with Varonis a few years ago" email + fallback line.
6. Same evidence for several people at one account: flag "possible account-level data" for John; email may still use "in contract with us … split off".
7. Inactive email: disqualify, no card (done for Tim Anderson, Clayton Langston).
8. Loop-you-in fallback: this spec.
9. Add John's examples (Robert, Brian Peck, Brian/Scott, Kevin) to the rules as few-shot examples.

## Open questions for John
See chat 2026-11-20.
