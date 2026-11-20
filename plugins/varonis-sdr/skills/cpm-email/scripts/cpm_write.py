"""Write the draft back to Attio. Only cpm_draft, cpm_draft_status, cpm_updates_used can be written.
Usage: python3 cpm_write.py RECORD_ID DRAFT_TXT_FILE STATUS [UPDATE_RECORD_ID ...]"""
import sys
from attio import call, PERSON_WRITE
rid, txt, status, ups = sys.argv[1], open(sys.argv[2]).read().strip(), sys.argv[3], sys.argv[4:]
if status not in ("Drafted", "Reviewed", "Skipped"): raise SystemExit("Agent may only set Drafted, Reviewed or Skipped.")
values = {"cpm_draft": txt, "cpm_draft_status": status,
          "cpm_updates_used": [{"target_object": "varonis_updates", "target_record_id": u} for u in ups]}
assert set(values) <= set(PERSON_WRITE)
call("PATCH", f"/objects/people/records/{rid}", {"data": {"values": values}})
print("written", rid, status)
