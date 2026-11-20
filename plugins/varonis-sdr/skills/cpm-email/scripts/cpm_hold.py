"""Move a draft to stage "Needs John" with a reason (held for John's judgment). Never Approved/Pushed drafts.
Usage: python3 cpm_hold.py DRAFT_RECORD_ID "reason" """
import sys
from attio import call, flat, DRAFT_UPDATE
rid, reason = sys.argv[1], sys.argv[2]
vals = call("GET", f"/objects/email_drafts/records/{rid}")["data"]["values"]
cur, old = flat(vals, "stage"), flat(vals, "review_notes") or ""
if cur in ("Approved", "Pushed", "Superseded"): raise SystemExit(f"Draft stage is {cur}; not moved.")
values = {"stage": "Needs John", "review_notes": (old + "\nHELD: " + reason).strip()}
assert set(values) <= set(DRAFT_UPDATE)
call("PATCH", f"/objects/email_drafts/records/{rid}", {"data": {"values": values}})
print("held", rid)
