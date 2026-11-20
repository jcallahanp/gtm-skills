"""Record the reviewer's result on a draft. Only stage (Drafted -> Reviewed) and review_notes can change.
Usage: python3 cpm_review.py DRAFT_RECORD_ID pass|fail "notes" """
import sys
from attio import call, flat, DRAFT_UPDATE
rid, result, notes = sys.argv[1], sys.argv[2], sys.argv[3]
cur = flat(call("GET", f"/objects/email_drafts/records/{rid}")["data"]["values"], "stage")
if cur != "Drafted": raise SystemExit(f"Draft status is {cur}; only Drafted drafts can be reviewed.")
values = {"review_notes": notes}
if result == "pass": values["stage"] = "Reviewed"
assert set(values) <= set(DRAFT_UPDATE)
call("PATCH", f"/objects/email_drafts/records/{rid}", {"data": {"values": values}})
print("review recorded", rid, values.get("stage", "Drafted (failed review)"))
