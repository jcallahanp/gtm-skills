"""Candidate updates for one person: tag overlap + released after the meeting month.
Usage: python3 cpm_match.py PEOPLE_JSON UPDATES_JSON RECORD_ID"""
import json, sys
people = {p["record_id"]: p for p in json.load(open(sys.argv[1]))}
ups = json.load(open(sys.argv[2]))
p = people[sys.argv[3]]
tags = set(p.get("cpm_concept_tags") or [])
month = (p.get("past_meeting_date") or "0000-00")[:7]
hits = [u for u in ups if (u["released_5"] or "")[:7] > month and tags & set(u.get("concept_tags") or [])]
for u in hits:
    u["tag_overlap"] = sorted(tags & set(u["concept_tags"]))
print(json.dumps(hits, indent=1, ensure_ascii=False))
