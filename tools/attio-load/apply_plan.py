"""Apply a reviewed load plan (plan.json, built outside the repo – it holds prospect data) to Attio.
Usage: python3 apply_plan.py plan.json rules.txt examples.txt [--apply]   (without --apply: dry run, prints counts)"""
import json, os, sys, urllib.request, urllib.error
apply = "--apply" in sys.argv
plan = json.load(open(sys.argv[1])); rules = open(sys.argv[2]).read(); examples = open(sys.argv[3]).read()
def call(m, path, body=None):
    req = urllib.request.Request("https://api.attio.com/v2" + path, method=m, data=json.dumps(body).encode() if body else None,
                                 headers={"Authorization": "Bearer " + os.environ["ATTIO_API_KEY"], "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r: return json.load(r)
    except urllib.error.HTTPError as e: return {"error": e.code, "body": e.read().decode()[:300]}
log = []
def do(m, path, body, label):
    if not apply: log.append(("DRY", label)); return
    r = call(m, path, body); log.append(("FAIL" if "error" in r else "OK", label, r.get("body", "")))
for p in plan["people"]:
    vals = {k: v for k, v in p["values"].items() if v not in (None, [], "")}
    do("PATCH", f"/objects/people/records/{p['record_id']}", {"data": {"values": vals}}, "person " + p["name"])
for c in plan["companies"]:
    if c["account_rep"]: do("PATCH", f"/objects/companies/records/{c['record_id']}", {"data": {"values": {"account_rep": c["account_rep"]}}}, "company " + c["name"])
for u in plan["updates"]["tag_existing"]:
    if u["concept_tags"]: do("PATCH", f"/objects/varonis_updates/records/{u['record_id']}", {"data": {"values": {"concept_tags": u["concept_tags"]}}}, "tag update " + u["name"])
for u in plan["updates"]["create"]:
    vals = {k: v for k, v in u.items() if v not in (None, [], "")}
    do("POST", "/objects/varonis_updates/records", {"data": {"values": vals}}, "new update " + u["name"])
do("POST", "/objects/writing_rules/records", {"data": {"values": {"name": "CPM email", "rules": rules, "examples": examples}}}, "writing rule CPM email")
import collections
print(collections.Counter(x[0] for x in log))
for x in log:
    if x[0] == "FAIL": print(x)
