"""List Approved CPM email drafts and build the exact Clay payload for each. Writes nothing.
Usage: python3 push_prepare.py [DRAFT_ID ...] > payloads.json
Each payload's "clay_inputs" is passed unchanged to Clay "Daily Queue - API" (run_subroutine_direct)."""
import datetime, json, sys
from attio import call, project, flat, DRAFT_READ, PERSON_READ, SEQUENCE_ID
from transform import clean

ids = sys.argv[1:]
recs = call("POST", "/objects/email_drafts/records/query", {"filter": {"$and": [{"status": "Approved"}, {"kind": "Email"}]}, "limit": 500})["data"]
out, problems = [], []
for r in recs:
    d = project(r, DRAFT_READ)
    if ids and d["record_id"] not in ids: continue
    p = project(call("GET", f"/objects/people/records/{d['person']}")["data"], PERSON_READ)
    email = p["email_addresses"][0] if isinstance(p["email_addresses"], list) else p["email_addresses"]
    first = (p["name"] or "").split()[0] if p["name"] else ""
    try:
        if not email: raise ValueError("person has no email")
        if not first: raise ValueError("person has no name")
        text, body_html = clean(d["body"], first)
    except ValueError as e:
        problems.append({"draft_id": d["record_id"], "draft": d["name"], "problem": str(e)}); continue
    out.append({"draft_id": d["record_id"], "draft": d["name"], "to": email,
                "clay_inputs": {"body": text, "body_html": body_html, "email": email, "subject": d["subject"],
                                "record_id": d["person"], "prospect_id": p["outreach_prospect_id"] or "",
                                "sequence_id": SEQUENCE_ID, "today": datetime.date.today().isoformat()}})
print(json.dumps({"ready": out, "problems": problems}, indent=1, ensure_ascii=False))
