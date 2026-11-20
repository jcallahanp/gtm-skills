"""Read everything the CPM skill needs from Attio, allow-listed.
Usage:
  python3 cpm_read.py people [--only-pending]   -> people in "Prioritized - Past Meetings" + their latest CPM draft status
  python3 cpm_read.py updates                   -> Varonis Updates rows
  python3 cpm_read.py rules                     -> Writing Rules record "CPM email" (rules + examples)
  python3 cpm_read.py drafts                    -> all CPM Email Drafts (newest first)
--only-pending keeps people with no live draft (none, or only Superseded/Failed).
--exclude FILE drops every person whose Attio record id is in FILE ("attio_person_record_ids").
"""
import datetime, json, sys
from attio import call, flat, project, PERSON_READ, COMPANY_READ, UPDATE_READ, DRAFT_READ, REPS


def view_people():
    # Same filter as the Attio view "Prioritized - Past Meetings" (people).
    q = {"filter": {"$and": [{"view_segment": "Past Meeting"}, {"prioritization": "Prioritized"},
                             {"needs_john_review": False}, {"disqualified": False}, {"warm_follow_up_4": False}]},
         "limit": 500}
    recs = call("POST", "/objects/people/records/query", q)["data"]
    cut = (datetime.date.today() - datetime.timedelta(days=180)).isoformat()
    keep = []
    for r in recs:
        v = r["values"]
        if not (v.get("mobile") or v.get("direct")): continue
        pm = flat(v, "past_meeting_date")
        if pm and not pm < cut: continue
        if not v.get("synthesis_note_6"): continue  # view filter only; value is never read
        keep.append(r)
    return keep


def drafts():
    recs = call("POST", "/objects/email_drafts/records/query", {"filter": {"campaign": "CPM"}, "limit": 1000})["data"]
    rows = [project(r, DRAFT_READ) for r in recs]
    for r, raw in zip(rows, recs): r["created_at"] = raw["created_at"]
    return sorted(rows, key=lambda x: x["created_at"], reverse=True)


def latest_by_person(rows):
    out = {}
    for d in rows:  # newest first
        if d["stage"] == "Superseded": continue
        out.setdefault(d["person"], d)
    return out


def people(only_pending):
    out, companies = [], {}
    live = latest_by_person(drafts())
    for r in view_people():
        p = project(r, PERSON_READ)
        cid = p.pop("company")
        if cid and cid not in companies:
            c = project(call("GET", f"/objects/companies/records/{cid}")["data"], COMPANY_READ)
            if c["account_rep"] not in REPS: c["account_rep"] = None
            companies[cid] = c
        p["company_name"] = companies.get(cid, {}).get("name")
        p["account_rep"] = companies.get(cid, {}).get("account_rep")
        d = live.get(p["record_id"])
        p["latest_draft_id"], p["latest_draft_status"] = (d["record_id"], d["stage"]) if d else (None, None)
        if only_pending and p["latest_draft_status"] is not None: continue
        if p["record_id"] in EXCLUDE: continue
        out.append(p)
    return out


def updates():
    recs = call("POST", "/objects/varonis_updates/records/query", {"limit": 1000})["data"]
    rows = [project(r, UPDATE_READ) for r in recs]
    return sorted(rows, key=lambda x: x["released_5"] or "", reverse=True)


def rules():
    recs = call("POST", "/objects/writing_rules/records/query", {"filter": {"name": "CPM email"}, "limit": 1})["data"]
    if not recs: raise SystemExit("Writing Rules record 'CPM email' not found.")
    return {"rules": flat(recs[0]["values"], "rules"), "examples": flat(recs[0]["values"], "examples")}


EXCLUDE = set()
if "--exclude" in sys.argv:
    EXCLUDE = set(json.load(open(sys.argv[sys.argv.index("--exclude") + 1]))["attio_person_record_ids"])

if __name__ == "__main__":
    cmd = sys.argv[1]
    data = {"people": lambda: people("--only-pending" in sys.argv), "updates": updates, "rules": rules, "drafts": drafts}[cmd]()
    print(json.dumps(data, indent=1, ensure_ascii=False))
