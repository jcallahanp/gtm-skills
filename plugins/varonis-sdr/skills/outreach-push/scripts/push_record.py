"""Record the push result on a draft. Only Approved drafts can change; only stage, pushed_at, push_result are written.
Usage: python3 push_record.py DRAFT_ID pushed|failed "result text (Clay task id or error)" """
import datetime, sys
from attio import call, flat, DRAFT_WRITE
rid, outcome, note = sys.argv[1], sys.argv[2], sys.argv[3]
cur = flat(call("GET", f"/objects/email_drafts/records/{rid}")["data"]["values"], "stage")
if cur != "Approved": raise SystemExit(f"Draft status is {cur}; only Approved drafts can be recorded as pushed or failed.")
values = {"stage": "Pushed" if outcome == "pushed" else "Failed", "push_result": note,
          "pushed_at": datetime.datetime.now(datetime.timezone.utc).isoformat()}
assert set(values) <= set(DRAFT_WRITE)
call("PATCH", f"/objects/email_drafts/records/{rid}", {"data": {"values": values}})
print("recorded", rid, values["stage"])
