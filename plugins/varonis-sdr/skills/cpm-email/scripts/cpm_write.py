"""Create a new CPM Email Draft in Attio. Never edits an existing draft's text.
Usage: python3 cpm_write.py PERSON_RECORD_ID PERSON_NAME KIND SUBJECT DRAFT_TXT_FILE [--updates ID ID ...] [--rules-version v8] [--replace-approved]
KIND = email | card.
If the person already has a live draft:
  Drafted / Reviewed / Failed  -> that draft is marked Superseded and the new one links to it.
  Approved / Pushed            -> refused, unless --replace-approved (then the Approved one is Superseded; never a Pushed one).
"""
import argparse, datetime, html, json
from attio import call, DRAFT_CREATE
from cpm_read import drafts, latest_by_person

a = argparse.ArgumentParser()
a.add_argument("person"); a.add_argument("name"); a.add_argument("kind", choices=["email", "card"])
a.add_argument("subject"); a.add_argument("file")
a.add_argument("--updates", nargs="*", default=[]); a.add_argument("--rules-version", default="v11")
a.add_argument("--replace-approved", action="store_true")
x = a.parse_args()
body = open(x.file).read().strip()
all_drafts = drafts()
mine = [d for d in all_drafts if d["person"] == x.person]
live = latest_by_person(mine).get(x.person)
if live:
    if live["stage"] == "Pushed": raise SystemExit("Latest draft was already pushed. Not replacing.")
    if live["stage"] == "Approved" and not x.replace_approved: raise SystemExit("Latest draft is Approved. Ask John; rerun with --replace-approved only if he says so.")
today = datetime.date.today().isoformat()


def to_html(paras):
    """Each paragraph becomes its own <p>; an empty <p><br></p> sits between paragraphs so Outreach shows a blank line.
    A single line break inside a paragraph becomes <br>. Text is HTML-escaped."""
    return "<p><br></p>".join("<p>" + html.escape(p).replace("\n", "<br>") + "</p>" for p in paras)
paras = [p.strip() for p in body.split("\n\n") if p.strip()]
values = {
    "name": f"CPM – {x.name} – {today} (v{len(mine) + 1})",
    "person": [{"target_object": "people", "target_record_id": x.person}],
    "campaign": "CPM", "kind": "Email" if x.kind == "email" else "Needs John card",
    "subject": x.subject, "body": body,
    "body_html": to_html(paras),
    "updates_used": [{"target_object": "varonis_updates", "target_record_id": u} for u in x.updates],
    "rules_version": x.rules_version, "stage": "Drafted", "drafted_at": today,
}
if live: values["supersedes"] = [{"target_object": "email_drafts", "target_record_id": live["record_id"]}]
assert set(values) <= set(DRAFT_CREATE)
new = call("POST", "/objects/email_drafts/records", {"data": {"values": values}})["data"]["id"]["record_id"]
if live:
    call("PATCH", f"/objects/email_drafts/records/{live['record_id']}", {"data": {"values": {"stage": "Superseded"}}})
print(json.dumps({"created": new, "superseded": live["record_id"] if live else None, "name": values["name"]}))
