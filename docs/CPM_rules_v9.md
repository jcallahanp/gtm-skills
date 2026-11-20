# Contacts Past Meetings (CPM) – how to write the email

Version 9. Replaces v8 (2026-11-20: fewer cards, examples J–L, new asks, no-context line, recent-meeting tone). Data: "Past Meetings Consolidated v6" (sheet "Obtained") and "Varonis Updates Master v2", both in the Past Meetings Skills folder. Run steps are in "Past Meetings Email – HOW TO RUN". John's examples and the original template are kept word for word (sections 9 and 10).

How to use this doc: the rules in sections 0–8 are the few things that must always hold. For tone, framing and judgment calls, follow John's examples in section 9 – pick the example closest to the case and write the way John wrote it. When a rule and an example seem to differ on style, follow the example; when they differ on a guardrail (section 0), follow the guardrail.

## 0. GUARDRAILS – read first, never break

### 0.1 Attio is for the rep and contact details only

- Attio is used ONLY for the current account rep (company field `rep`) and contact details (name, email, account name).  
- Everything about **what we talked about** (topic, past rep, when, why it stalled) comes **only** from the "Obtained" sheet.  
- Everything about **what to update them on** comes **only** from the Varonis Updates Master (or a platform-level line as in Examples D and F).  
- Never use any other Attio field (deal history, Salesforce history, success criteria, pains, signals, research notes, tool stack, account news). If the sheet does not state something, it is unknown. Do not fill the gap from Attio, memory or the web.

### 0.2 Technical concepts only – never setup items

- The "Obtained" sheet splits concepts into **Technical concepts** and **Setup items** (ports, firewall rules, service accounts, collectors, agents, EKS/Helm, CloudFormation, app registrations, prerequisite checker, CAB approvals, patches, support troubleshooting).  
- The email topic (¶1) and the update matching (¶3) use **Technical concepts only**. Setup items never appear in the email.  
- A setup item or support case may still point to a topic: use the product or system it is about, stated broadly (section 0.3).

### 0.3 Hand it to John – do not draft

Write a "Needs John" card (section 2) instead of an email ONLY when there is no topic at all: no technical concept, and no support case, install document or product/system name in the evidence.

Everything else gets a draft:

1. **Support cases and install details count as a topic.** Name the product or system broadly (for example Interceptor, Active Directory, Windows file servers). Never mention the setup step itself (section 0.2). See Example L.
2. **Recurring / customer pattern** (office hours, syncs, QBR, huddle, health check; no invite near the meeting date): write a vague email ("you were part of the back and forth with Varonis a few years ago") and use the no-context line in section 4.8. See Example K.
3. **Same evidence for several people at one account** (the data may describe the account, not the person): still write the email (Example J), and the reviewer adds "possible account-level data" to review notes.
4. **Inactive email**: no card and no draft. The person is disqualified in Attio (John's decision, 2026-11-20).

Every other person gets a draft, even with a vague topic, an unknown reason or no matching update.

## 1. What this email is

A short reconnect email to a person we met with before. It names the past meeting, offers to reconnect them with the team (often by naming the rep), and ties the past topic to something new at Varonis.

The template is a guide for structure, not fixed wording. Each paragraph is a snippet with a purpose. Keep the purpose and the order; reword freely in a casual, specific tone, the way John's examples do.

## 2. "Needs John" card (instead of a draft)

| Field | Content |
| :---- | :---- |
| Person | Name, title, company |
| Current rep | From Attio `rep` |
| Why flagged | The Route reason from the sheet |
| Key facts | 2–3 quotes from the sheet, each with its E# and date |
| Candidate updates | Up to 3 Updates Master rows (date, feature, one line) |
| Recurring pattern only | "Check Salesforce for newer meetings or emails where this person was a recipient." |

No draft text.

## 3. Inputs – collect all of these before writing

| Input | Allowed source (only) | Rule |
| :---- | :---- | :---- |
| Route | "Obtained" sheet, column "Route" | If "Needs John", write the card. |
| First name | "Obtained" sheet | The first name the person goes by. |
| Past rep (first name) | "Obtained" sheet evidence | The Varonis person on the entries. If none is named, write "we" or "our teams". |
| When | "Obtained" sheet, column "Meeting date" | Casual time phrase, as in the examples. |
| Topic | "Obtained" sheet, column "Technical concepts" | Pick 1–3 specific concepts. Skip items that only came from a standard agenda list. |
| Why it stalled | "Obtained" sheet evidence quotes | Use it if stated. If unknown, leave it out – never guess (the one allowed soft inference is in section 5). |
| Current rep | Attio company field `rep` | Always one of Todd Cencich, Rob Andersen or Patrick Dolan. If empty or anyone else, do not name a rep. Whether to name him at all: section 5, ¶2. |
| Title and seniority | "Obtained" sheet, column "Title" | Used only for the ¶2 naming choice. |
| Planning year | Today's date | Next calendar year from October to December, else the current year. In Nov 2026 this is 2027. |
| Updates | Varonis Updates Master | Section 4. |

## 4. Picking and describing updates (¶3)

1. Use the person's "Concept tags" column. Keep only Updates Master rows whose Sort key (YYYY-MM) is later than the meeting month.  
2. Prefer rows that match the person's main topic over rows that only share a broad tag; among those, prefer the newest.  
3. **Describe updates by their category, not their narrow detail** (labeling, classification, monitoring, access, detection, remediation), linked to their past topic. Name a specific feature, data type or product only if the sheet shows they discussed it. (See Example E.)  
4. **Say "major" only when it is true for this person:** either one specific, big shift (for example the launch of the AI security platform, or Proofpoint's pending acquisition of Varonis), or a specific update that is highly relevant to what they talked about. For broad platform development or small changes in their space, use plain wording ("share our platform updates including …"). If "major" would sound salesy, or the rep would only be catching them up on small changes in the meeting, leave it out.  
5. **Proofpoint's pending acquisition of Varonis** (Updates Master, Oct 2026) may be mentioned when Proofpoint came up, or when the area they looked at is strongly affected by it (for example email security / Interceptor). See Example G.  
6. **If the reason it stalled was budget, mention our pricing changes** in ¶2 or ¶3 (Examples A and F).  
7. When nothing in the Updates Master fits the topic, write a platform-level line instead, the way Examples D and F do. Choose the angle closest to their topic.  
8. **No context at all** (vague topic, recurring pattern, account-level data): use the broad AI line so that an AI, SOC or DAM reader all stay interested: "how we've rebuilt the platform around AI, securing AI use while automating detection, response and data protection" (Example K), or "our major identity and SOC developments, including identity-aware control of AI agents and faster AI-driven investigation" when the topic was identity or SOC (Example J).  
9. **Title sets the breadth.** For executives (CIO, CISO, VP), name the original topic and at most one big platform (for example the AI security platform). Never a narrow feature, even if one exists (Example L).

## 5. The four paragraphs

Write four short paragraphs, in this order.

- **¶1 – The past meeting.** Who they met (past rep first name + "from my team", or "we" / "our teams"), when, the topic, and why it stalled if the sheet says so. One soft inference is allowed: if the sheet shows a decision pending and nothing after it, "it looks like that ended up falling through" (Example E). Otherwise never guess a reason.  
- **¶2 – Reconnect.** Naming the rep is optional. Name him (Todd, Rob or Patrick, full name) mainly when the meeting was fairly recent, especially with senior people, where the name carries weight and they may already know him (Examples D, E, H, I). For distant meetings or more junior people, keep it broad with no name (Example F: "Looking to reconnect now that it's been quite some time."). Add a short "why now" if it fits – see the examples for phrasing.  
- **¶3 – Purpose and what is new.** "your PLANNING YEAR roadmap" plus the update phrase from section 4.  
- **Met one year ago or less:** keep it low-key. Casual timing in ¶2 ("as this year comes to an end"), "a few key updates" in ¶3, no "major" unless it is one big launch (Example L).  
- **¶4 – The ask.** One of the approved asks below, word for word.

### Approved asks (¶4)

- "Might one day this week afford 30 minutes for this convo?"  
- "Would sometime next week afford 30 minutes for this conversation?"  
- "Think you could squeeze 30 minutes in for this convo before the holidays?" (only from mid-November through December)  
- "Would one day next week afford 30 minutes for this convo?"  
- "Would some time next week afford 30 minutes for this conversation?"  
- "Would one day afford 30 minutes for this convo over the next few weeks?"

## 6. What is fixed

1. Four paragraphs, in the order above.  
2. ¶4 is an approved ask, word for word.  
3. ¶1 has the time and a technical concept; the reason only as section 5 allows.  
4. ¶3 has the planning-year roadmap.  
5. No setup items, no feature lists, no marketing adjectives ("cutting-edge", "industry-leading"), no exclamation marks; "major" only as section 4 allows.  
6. Under 90 words in the body.  
7. All guardrails in section 0.

Everything else – greeting, verbs, connectors, light remarks, how much detail, whether to name the rep – follow the closest example in section 9.

## 7. Which example to follow

| Case | Example |
| :---- | :---- |
| Unclear topic, reason known | A – Darin |
| Met recently | B – Mark, G – Brian |
| Explicit "no" or many concepts | C – Josh, H – Nahuel |
| Unclear topic, reason unknown, no matching update | D – Steve |
| Decision pending, then silence | E – Kong |
| Topic outside Varonis's core (network, VPN), very old meeting, no rep named | F – Eric |
| Proofpoint relevant to their area | G – Brian |
| Past rep is also the current rep; senior contact with doubts about Varonis | I – Rick |
| Same evidence for several people at the account; former customer | J – Brian / Scott |
| Recurring / customer pattern, no clear topic | K – Brian Peck |
| Recent meeting, executive title, topic from an install or support detail | L – Kevin |
| No topic at all | Card (section 2) |

## 8. Checklist – run before giving the email

1. A draft is right for this person (section 0.3): not inactive, and some topic exists?  
2. Four paragraphs in order; ¶4 is an approved ask word for word (holiday ask only mid-Nov to Dec)?  
3. ¶1 has the time and a technical concept; reason only if stated (or the one soft inference)?  
4. ¶2 names Todd, Rob or Patrick only if Attio `rep` is one of them, and only where naming fits (recent and/or senior)?  
5. ¶3 has the planning year and category-level updates dated after the meeting month, or a platform-level line like Examples D and F?  
6. "Major" used only for one big shift or an update highly relevant to their topic?  
7. If budget was the reason, pricing changes are mentioned?  
8. No setup items; no narrow feature or data type unless the sheet shows it was discussed?  
9. Every fact about the meeting comes from the "Obtained" sheet, every update from the Updates Master, Attio only for rep and contact details?  
10. Under 90 words, no feature list, no hype words?

## 9. Examples (A–F and J–L written by John, G–I drafted and approved by John; all word for word)

### Example A – unclear topic, reason known (Darin, VT Industries)

Hey Darin - understand that you met with Tony from my team back in 2024 regarding your all's data security project, but budget did not align.

Reaching out to reconnect you with (rep who owns that account) now, as we've had several major changes with our offerings and pricing.

Purpose would be to discuss your 2027 roadmap and share our updates with you including our AI security platform.

Might one day this week afford 30 minutes for this Convo?

### Example B – met recently (Mark, O'Reilly Auto Parts)

Hi Mark - understand you met with Pat from my team earlier this year about DLP/DSPM and how Varonis could complement Purview, but decided this would go on the back burner until 2027.

Looking to reconnect as we approach the new year.

Purpose would be to regroup on your 2027 roadmap and update you on our major developments with AI-SPM.

Might one day this week afford 30 minutes for this convo?

### Example C – explicit "no" (Josh, Kent Corporation)

Hey Josh,

Understand we met with you several years back in 2023 regarding DLP, oversharing, and data classification. Looks like expanding DLP wasn't worth expanding at the time.

Looking to reconnect you with (reps name).

Purpose would be to discuss your 2027 roadmap and update you on several of our expanded capabilities including EDM classification extended to tabular files and AI classification.

Might one day this week afford 30 minutes for this convo?

### Example D – unclear topic, reason unknown, no update (Steve, Drury Hotels)

Steve - understand we ran a risk assessment back in 2024.

Looking to reconnect you with Patrick Dolan now that it has been a couple years.

Purpose would be to discuss your 2027 update you on our major platform changes with our all in one AI solution for security, governance, spend, and agent intent.

Might one day this week afford 30 minutes for this convo.

John's rationale: "We do not know what he is concerned with. We can take a educated guess that based on his title and the fact that almost everyone is concerned with AI in some regards a very broad summary of the Ai platform phrased in a casual update and show you this as opposed to an extremely speicifc pigeon hold will work."

### Example E – decision pending, then silence (Kong, Belden)

Hey Kong - understand we had an RFP going for you guys back in late 2023 for our DLP solution but it looks like that ended up falling through.

Looking to reconnect you with Patrick Dolan now that is been a few years.

Purpose would be to discuss your 2027 roadmap and introduce our major DLP updates including automated labeling built for DLP enforcement and more precise sensitive data classification.

Would sometime next week afford 30 minutes for this conversation?

### Example F – topic outside Varonis's core, very old meeting, no rep named (Eric, University of Northern Iowa)

Hey Eric - understand our teams chatted back 2020 during the COVID days - good times. Looks like you all were trying to get VPN and network access configured, but budget did not align.

Looking to reconnect now that it's been quite some time.

Purpose would be to discuss your all’s 2027 roadmap and share our completely transformed platform, which has undergone some major pricing shifts along side  developing from visibility to automated remediation across proxy traffic, browsers, endpoints and every connecting identity.

Think you could squeeze 30 minutes in for this convo before the holidays?

### Example G – met recently, Proofpoint relevant (Brian, O'Reilly Auto Parts)

Hey Brian - understand we walked you and the team through an Interceptor demo earlier this year around email security.

Looking to reconnect you with Patrick Dolan as we approach the new year.

Purpose would be to discuss your 2027 roadmap and share our platform updates, including Proofpoint's pending acquisition of Varonis bringing email and data security together.

Think you could squeeze 30 minutes in for this convo before the holidays?

John's note: say "major" only for one specific big shift or an update highly relevant to them; otherwise plain "platform updates".

### Example H – many concepts, ownership changing (Nahuel, Emerson Electric)

Hi Nahuel - understand we met with you and the team back in late 2025 around DSPM, a potential PoC, and how Varonis complements your SSE and SIEM tools.

Looking to reconnect you with Patrick Dolan as we approach the new year.

Purpose would be to discuss your 2027 roadmap and update you on our major DSPM developments including SSE integrations that tie web traffic to your sensitive data and more precise AI-driven classification.

Might one day this week afford 30 minutes for this convo?

### Example I – past rep is the current rep, senior contact with doubts (Rick, ADT)

Hey Rick - understand you grabbed lunch with Todd from my team back in mid 2025 around our move to SaaS, pricing, and whether Varonis was still a legacy product.

Looking to reconnect you with Todd Cencich now that it has been over a year.

Purpose would be to discuss your 2027 roadmap and share how far the platform has come since, including AI gateways that control what agents and models can reach and expanded cloud data security.

Might one day this week afford 30 minutes for this convo?

### Example J – same evidence across the account, former customer (Brian / Scott, Sammons) – John, 2026-11-20

Hey - (brian/scott) understand you all were in contract with us several years back but we ended up splitting off.

Looking to reconnect you with Rob Andersen to reintroduce Varonis.

Purpose would be to discuss your 2027 roadmap and update you on our major identity and SOC developments, including identity-aware control of AI agents and faster AI-driven investigation.

Would one day afford 30 minutes for this convo over the next few weeks?

(Reviewer: add "possible account-level data" to review notes for this case.)

### Example K – recurring / customer pattern, no clear topic (Brian Peck, Sammons) – John, 2026-11-20

Hey Brian - looks like you were part of the back and fourth with Varonis a few years ago.

Looking to reconnect you with Rob Andersen to reintroduce Varonis now that it's been some time.

Purpose would be to discuss this years roadmap and share how we’ve rebuilt the platform around AI, securing AI use while automating detection, response and data protection.

Would some time next week afford 30 minutes for this conversation?

(Script check still requires "PLANNING YEAR roadmap", for example "your 2027 roadmap".)

### Example L – recent meeting, CIO, topic from an install document (Kevin Porter, Watson Realty) – John, 2026-11-20

Hey Kevin, 

Understand we met with you toward the end of last year regarding our email security platform, Interceptor, looks like we lost thread.

Hoping to reconnect you with Todd Cencich as this year comes to an end.

Purpose would be to discuss your 2027 roadmap and share a few key updates with you regarding our email security platform and our major AI security platform launch.

Would one day next week afford 30 minutes for this convo?

John's notes: "as this year comes to an end" sounds natural for a meeting only a year ago. "A few key updates" keeps it low-key after a recent meeting. A CIO is not 100% focused on email security, so in this limited case touch briefly on AI as a second angle, still name the original topic (Interceptor), and stay broad; never get specific about one small update with a CIO.

## 10. Original template and example (word for word)

### Template

Subject Line #1: continued conversations Subject Line #2: reconnect Subject Line #3: COMPANY – varonis touch base

Hey NAME – understand PERSONALIZATION ON PAST MEETING (DATE, TOPIC, WHY IT DIDN’T MOVE FORWARD).

Looking to connect you with SR FULL NAME to re-introduce Varonis now that it’s been some time.

Purpose would be to discuss your THIS YEAR roadmap and update you on our expanded capabilities into PRODUCT / USE CASE THAT TIES TO PAST MEETING.

Might one day this week afford 30 minutes for this convo?

### Example

Subject Line: continued conversations

Hey John – understand we were meeting with you and the rest of the security team back in September around your DLP project, but a budget freeze stalled discussions.

Looking to connect you with Yaki Faitelson to re-introduce Varonis now that it’s been some time.

Purpose would be to discuss your 2026 roadmap and update you on our expanded capabilities into DLP, including multi-layer AI data classification and data discovery and visibility into data within AI agents & LLMs.

Might one day this week afford 30 minutes for this convo?

## 11. Subject line

Default: "continued conversations". Use "reconnect" or "COMPANY – varonis touch base" only if John asks.