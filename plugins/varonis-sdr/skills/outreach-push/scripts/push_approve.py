"""Set drafts to Approved, only because John named them as approved in chat.
Only Reviewed, Drafted or Failed (retry) Email drafts can change; only stage is written.
Usage: python3 push_approve.py DRAFT_ID [DRAFT_ID ...]"""
import sys
from attio import call, flat, DRAFT_WRITE
for rid in sys.argv[1:]:
    vals = call("GET", f"/objects/email_drafts/records/{rid}")["data"]["values"]
    cur, kind = flat(vals, "stage"), flat(vals, "kind")
    if cur not in ("Reviewed", "Drafted", "Failed") or kind != "Email":
        print("skipped", rid, f"status {cur}, kind {kind}"); continue
    assert {"stage"} <= set(DRAFT_WRITE)
    call("PATCH", f"/objects/email_drafts/records/{rid}", {"data": {"values": {"stage": "Approved"}}})
    print("approved", rid)
