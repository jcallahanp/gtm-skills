"""Read everything the CPM skill needs from Attio, allow-listed.
Usage:
  python3 cpm_read.py people [--only-pending]   -> people in "Prioritized - Past Meetings" (JSON)
  python3 cpm_read.py updates                   -> Varonis Updates rows (JSON)
  python3 cpm_read.py rules                     -> Writing Rules record "CPM email" (rules + examples)
"""
import datetime, json, sys
from attio import call, flat, project, PERSON_READ, COMPANY_READ, UPDATE_READ, REPS


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


def people(only_pending):
    out, companies = [], {}
    for r in view_people():
        p = project(r, PERSON_READ)
        cid = p.pop("company")
        if cid and cid not in companies:
            c = project(call("GET", f"/objects/companies/records/{cid}")["data"], COMPANY_READ)
            if c["account_rep"] not in REPS: c["account_rep"] = None
            companies[cid] = c
        p["company_name"] = companies.get(cid, {}).get("name")
        p["account_rep"] = companies.get(cid, {}).get("account_rep")
        if only_pending and p.get("cpm_draft_status") not in (None, "Drafted"): continue
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


if __name__ == "__main__":
    cmd = sys.argv[1]
    data = {"people": lambda: people("--only-pending" in sys.argv), "updates": updates, "rules": rules}[cmd]()
    print(json.dumps(data, indent=1, ensure_ascii=False))
