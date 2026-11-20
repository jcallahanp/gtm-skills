"""Record the reviewer's result on a draft. Only stage and review_notes can change.
Usage: python3 cpm_review.py DRAFT_RECORD_ID pass|fail "notes"
pass: email -> Reviewed; card -> Needs John.  fail: stays Drafted (writer makes a new draft)."""
import sys
from attio import call, flat, DRAFT_UPDATE
rid, result, notes = sys.argv[1], sys.argv[2], sys.argv[3]
vals = call("GET", f"/objects/email_drafts/records/{rid}")["data"]["values"]
cur, kind = flat(vals, "stage"), flat(vals, "kind")
if cur != "Drafted": raise SystemExit(f"Draft stage is {cur}; only Drafted drafts can be reviewed.")
values = {"review_notes": notes}
if result == "pass": values["stage"] = "Reviewed" if kind == "Email" else "Needs John"
assert set(values) <= set(DRAFT_UPDATE)
call("PATCH", f"/objects/email_drafts/records/{rid}", {"data": {"values": values}})
print("review recorded", rid, values.get("stage", "Drafted (failed review)"))
