"""CPM results ledger: one row per person who has CPM data or a CPM draft in Attio.
Usage: python3 cpm_ledger.py OUT_DIR
Writes OUT_DIR/cpm-ledger-YYYY-MM-DD.csv (rows) and OUT_DIR/cpm-summary-YYYY-MM-DD.md (counts + lists).
Contains prospect names and emails: keep the output OUT of git. Upload it to Drive and lock it (read-only)
as the immutable snapshot; Attio Email Drafts stays the live source.
Outcome per person (latest non-superseded draft):
  Emailed (in 1419)        stage Pushed
  Failed (push)            stage Failed, reason = push_result
  Needs John               stage Needs John, or card
  In progress              stage Drafted / Reviewed / Approved
  No draft                 no draft; reason = not obtained reason, 180-day rule, disqualified or excluded
"""
import csv, datetime, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../plugins/varonis-sdr/skills/cpm-email/scripts"))
from attio import call, flat

today = datetime.date.today()
cut = (today - datetime.timedelta(days=180)).isoformat()
excl_path = os.path.join(os.path.dirname(__file__), "../../excludes/cpm-first-run.json")
EXCL = set(json.load(open(excl_path))["attio_person_record_ids"]) if os.path.exists(excl_path) else set()

drafts = call("POST", "/objects/email_drafts/records/query", {"filter": {"campaign": "CPM"}, "limit": 2000})["data"]
drafts.sort(key=lambda r: r["created_at"], reverse=True)
latest = {}
for d in drafts:
    v = d["values"]
    if flat(v, "stage") == "Superseded": continue
    pid = flat(v, "person")
    if pid and pid not in latest: latest[pid] = d

people = [x for o in ("Obtained", "Not obtained") for x in call("POST", "/objects/people/records/query", {"filter": {"cpm_obtained": o}, "limit": 2000})["data"]]
ids = {p["id"]["record_id"] for p in people} | set(latest)
companies, rows = {}, []
for pid in sorted(ids):
    p = next((x for x in people if x["id"]["record_id"] == pid), None) or call("GET", f"/objects/people/records/{pid}")["data"]
    pv = p["values"]
    cid = flat(pv, "company")
    if cid and cid not in companies:
        companies[cid] = call("GET", f"/objects/companies/records/{cid}")["data"]["values"]["name"][0]["value"]
    d = latest.get(pid); dv = d["values"] if d else {}
    stage, kind = flat(dv, "stage") if d else None, flat(dv, "kind") if d else None
    pm = flat(pv, "past_meeting_date")
    if stage == "Pushed": outcome, reason = "Emailed (in 1419)", flat(dv, "push_result")
    elif stage == "Failed": outcome, reason = "Failed (push)", flat(dv, "push_result")
    elif stage == "Needs John" or (kind and kind != "Email" and stage != "Superseded"): outcome, reason = "Needs John", flat(dv, "review_notes")
    elif stage in ("Drafted", "Reviewed", "Approved"): outcome, reason = "In progress", f"stage {stage}"
    else:
        outcome = "No draft"
        if pid in EXCL: reason = "Excluded (excludes file)"
        elif flat(pv, "disqualified"): reason = "Disqualified"
        elif pm and pm >= cut: reason = f"Met in the last 180 days ({pm})"
        elif flat(pv, "cpm_obtained") == "Not obtained": reason = "Not obtained: " + (flat(pv, "cpm_not_obtained_reason") or "")[:200]
        else: reason = "Not drafted yet"
    emails = flat(pv, "email_addresses")
    rows.append({"person": flat(pv, "name"), "email": emails[0] if isinstance(emails, list) else emails, "company": companies.get(cid),
                 "outcome": outcome, "reason": (reason or "").replace("\n", " ")[:300], "stage": stage, "kind": kind,
                 "past_meeting_date": pm, "drafted_at": flat(dv, "drafted_at") if d else None, "pushed_at": flat(dv, "pushed_at") if d else None,
                 "draft_name": flat(dv, "name") if d else None, "attio_person_id": pid, "attio_draft_id": d["id"]["record_id"] if d else None})

out = sys.argv[1]; os.makedirs(out, exist_ok=True)
stamp = today.isoformat()
with open(f"{out}/cpm-ledger-{stamp}.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(sorted(rows, key=lambda r: (r["outcome"], r["person"] or "")))
order = ["Emailed (in 1419)", "Failed (push)", "Needs John", "In progress", "No draft"]
md = [f"# CPM results – snapshot {stamp}", "", "Source: Attio (Email Drafts + people CPM fields). Live view: Attio \"Email Drafts – Kanban\".", ""]
md += [f"- **{o}:** {sum(r['outcome'] == o for r in rows)}" for o in order] + [""]
for o in order:
    md += [f"## {o}", ""] + [f"- {r['person']} ({r['company']}) – {r['reason']}" for r in sorted(rows, key=lambda r: r["person"] or "") if r["outcome"] == o] + [""]
open(f"{out}/cpm-summary-{stamp}.md", "w", encoding="utf-8").write("\n".join(md))
print(json.dumps({o: sum(r["outcome"] == o for r in rows) for o in order}))
