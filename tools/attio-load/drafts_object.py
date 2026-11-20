"""Create the Attio object "Email Drafts" and its fields, archive the old cpm_draft* people fields.
Usage: python3 drafts_object.py plan|apply"""
import json, os, sys, urllib.request, urllib.error
def call(m, path, body=None):
    req = urllib.request.Request("https://api.attio.com/v2" + path, method=m, data=json.dumps(body).encode() if body else None,
                                 headers={"Authorization": "Bearer " + os.environ["ATTIO_API_KEY"], "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r: return json.load(r)
    except urllib.error.HTTPError as e: return {"error": e.code, "body": e.read().decode()[:300]}
O = "email_drafts"
FIELDS = [
 ("name", "Name", "text", False, None, None, "CAMPAIGN – Person – YYYY-MM-DD (vN)."),
 ("person", "Person", "record-reference", False, None, ["people"], "The person this draft is for."),
 ("campaign", "Campaign", "select", False, ["CPM"], None, "Which email skill wrote it."),
 ("kind", "Kind", "select", False, ["Email", "Needs John card"], None, "Email to send, or a card for John to handle."),
 ("subject", "Subject", "text", False, None, None, "Subject line."),
 ("body", "Body", "text", False, None, None, "Plain-text body. Never edited after Approved."),
 ("body_html", "Body HTML", "text", False, None, None, "HTML body for Outreach. Never edited after Approved."),
 ("updates_used", "Updates used", "record-reference", True, None, ["varonis_updates"], "Varonis Updates rows used in the body."),
 ("rules_version", "Rules version", "text", False, None, None, "Writing Rules version used, e.g. v8."),
 ("status", "Status", "select", False, ["Drafted", "Reviewed", "Approved", "Pushed", "Failed", "Superseded"], None, "Drafted/Reviewed set by the skill; Approved by John; Pushed/Failed by the push skill."),
 ("drafted_at", "Drafted at", "date", False, None, None, "Date the draft was written."),
 ("review_notes", "Review notes", "text", False, None, None, "Reviewer agent findings."),
 ("supersedes", "Supersedes", "record-reference", False, None, ["email_drafts"], "Earlier draft this one replaces."),
 ("pushed_at", "Pushed at", "timestamp", False, None, None, "When the push skill sent it to Outreach."),
 ("push_result", "Push result", "text", False, None, None, "Push outcome or error."),
]
mode = sys.argv[1]
objs = {o["api_slug"] for o in call("GET", "/objects")["data"]}
if O not in objs:
    print("CREATE object", O)
    if mode == "apply": print(call("POST", "/objects", {"data": {"api_slug": O, "singular_noun": "Email Draft", "plural_noun": "Email Drafts"}}).get("error", "ok"))
have = {a["api_slug"] for a in call("GET", f"/objects/{O}/attributes?limit=100").get("data", [])} if (O in objs or mode == "apply") else set()
for slug, title, typ, multi, opts, targets, desc in FIELDS:
    if slug in have: print("EXISTS", slug); continue
    print("CREATE", slug, typ)
    if mode != "apply": continue
    cfg = {"record_reference": {"allowed_objects": targets}} if targets else {}
    r = call("POST", f"/objects/{O}/attributes", {"data": {"title": title, "description": desc, "api_slug": slug, "type": typ,
             "is_required": False, "is_unique": False, "is_multiselect": multi, "config": cfg}})
    if "error" in r: print("  FAIL", r); continue
    for t in opts or []:
        rr = call("POST", f"/objects/{O}/attributes/{slug}/options", {"data": {"title": t}})
        if "error" in rr: print("  OPTION FAIL", t, rr)
for slug in ("cpm_draft", "cpm_draft_status", "cpm_updates_used"):
    print("ARCHIVE people", slug)
    if mode == "apply":
        r = call("PATCH", f"/objects/people/attributes/{slug}", {"data": {"is_archived": True}})
        print("  ", r.get("error", "ok"), r.get("body", ""))
