"""Load a "Past Meeting Lookup" doc (Salesforce lookup, exported from Drive as text/plain) into the
Attio people fields the cpm-email skill reads.

Usage:
  python3 load_lookup_doc.py DOC.txt            # dry run: prints what would be written
  python3 load_lookup_doc.py DOC.txt --apply    # writes, then reads back and compares

Doc format (one block per person):
  First Last — Company (Title)
  Last meeting / Concept / Evidence / Blockers / Confidence   (label line, then value lines)

Mapping (only these fields are written):
  past_meeting_date   first YYYY-MM-DD in "Last meeting" (none if "No past meeting")
  cpm_past_rep        first name in the first "(First Last)" of "Last meeting"
  cpm_obtained        "Not obtained" if Concept is Null/empty or there is no meeting, else "Obtained"
  cpm_not_obtained_reason  Evidence text when Not obtained
  cpm_concepts        Concept text + source line
  cpm_evidence        one line per Evidence entry, numbered E1, E2 ...
  cpm_stall_reason    keyword rule on Blockers (Budget / No interest / Pending then silence / Timing / Unknown)
  cpm_stall_quote     "Blockers (lookup): " + Blockers text
  cpm_concept_tags    keyword rule on Concept
  cpm_route           "Draft" when Obtained (Confidence Low -> "Needs John"); cleared otherwise
The person is found by exact first + last name and company name; ambiguous or missing -> skipped.
Recent meetings drop out of the skill by the existing 180-day rule on past_meeting_date.
"""
import json, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../plugins/varonis-sdr/skills/cpm-email/scripts"))
from attio import call, flat

LABELS = ["Last meeting", "Concept", "Evidence", "Blockers", "Confidence"]
SOURCE = "Source: Salesforce lookup doc"
TAG_RULES = [
    ("AI & Copilot Security", r"\bAI\b|copilot|agent"), ("DSPM", r"DSPM|posture"), ("DLP", r"\bDLP\b"),
    ("Data Classification & Discovery", r"classif|label|discover|sensitive|PII|PHI|PCI|HIPAA|CUI"),
    ("Data Risk Assessment", r"risk assessment|\bDRA\b|POC|POV"),
    ("Least Privilege & Permissions", r"permission|access|least privilege|remediat"),
    ("Identity & Active Directory", r"Active Directory|\bAD\b|identity"),
    ("Threat Detection & Response", r"MDDR|MDR|detection|UBA|threat|perimeter|DatAlert"),
    ("Audit & Activity Monitoring", r"monitor|telemetry|audit"),
    ("Compliance & Privacy", r"ISO27001|SOX|HIPAA|PCI|compliance|CMMC"),
    ("Data Governance & Ownership", r"governance|ownership"),
    ("Microsoft 365", r"M365|Microsoft 365|O365|SharePoint|OneDrive|Teams"),
    ("Microsoft Purview", r"Purview"), ("Cloud & IaaS", r"AWS|S3|Azure|Kubernetes|cloud|Nasuni"),
    ("Database Security (DAM)", r"Oracle|database|\bDB|DAM"),
    ("On-prem File Servers & NAS", r"Windows|file[- ]share|file server|Nasuni|NAS\b|on-prem"),
    ("Email Security", r"email|Interceptor"), ("Network & Perimeter", r"Edge|perimeter|VPN|network"),
]


def parse(text):
    lines = [l.replace("﻿", "").replace("\r", "").strip() for l in text.split("\n")]
    people, cur, label = [], None, None
    for l in lines:
        if not l: continue
        m = re.match(r"^(.+?) — (.+) \((.+)\)$", l)
        if m and l != lines[0].strip():
            cur = {"name": m.group(1).strip(), "company": m.group(2).strip(), "title": m.group(3).strip(), **{k: [] for k in LABELS}}
            people.append(cur); label = None; continue
        if cur is None: continue
        if l in LABELS: label = l; continue
        if label: cur[label].append(l)
    return people


def stall(blockers):
    b = blockers.lower()
    if "budget" in b: return "Budget"
    if re.search(r"let it expire|not interested|declined edge|declined po|decommission", b): return "No interest"
    if re.search(r"unresponsive|no reply|never booked|not held|unverified|no recap|no notes|stalled", b): return "Pending then silence"
    if re.search(r"pending|tbd|deferred|audit|timing|later", b): return "Timing"
    return "Unknown"


def values(p):
    lm, concept = " ".join(p["Last meeting"]), " ".join(p["Concept"]).strip()
    conf, blockers = " ".join(p["Confidence"]), " ".join(p["Blockers"]).strip()
    date = re.search(r"\d{4}-\d{2}-\d{2}", lm)
    no_meeting = (not date) or lm.lower().startswith("no past meeting")
    obtained = not no_meeting and concept and concept.lower() != "null"
    rep = re.search(r"\(([A-Z][a-z]+) [A-Z][\w'-]+", lm)
    ev = "\n".join(f"E{i} – {e}" for i, e in enumerate(p["Evidence"], 1))
    v = {"past_meeting_date": date.group(0) if date else None, "cpm_past_rep": rep.group(1) if rep else None,
         "cpm_obtained": "Obtained" if obtained else "Not obtained", "cpm_evidence": ev,
         "cpm_stall_quote": "Blockers (lookup): " + blockers if blockers else None,
         "cpm_stall_reason": stall(blockers) if obtained else None}
    if obtained:
        v["cpm_concepts"] = f"{concept}\n[{SOURCE}; confidence {conf}]"
        v["cpm_concept_tags"] = [t for t, rx in TAG_RULES if re.search(rx, concept, re.I)] or ["Data Security (general)"]
        v["cpm_route"] = "Needs John" if conf.lower().startswith("low") else "Draft"
        v["cpm_not_obtained_reason"] = None
    else:
        v["cpm_concepts"] = None; v["cpm_concept_tags"] = []; v["cpm_route"] = None
        v["cpm_not_obtained_reason"] = ("No past meeting. " if no_meeting else "No technical concept. ") + ev
    return v


def find(p):
    first, last = p["name"].split(" ", 1)
    recs = call("POST", "/objects/people/records/query", {"filter": {"name": {"first_name": first, "last_name": last}}, "limit": 20})["data"]
    hits = []
    for r in recs:
        cid = flat(r["values"], "company")
        cname = call("GET", f"/objects/companies/records/{cid}")["data"]["values"]["name"][0]["value"] if cid else ""
        key = re.sub(r"[^a-z]", "", p["company"].lower())[:5]
        if key and key in re.sub(r"[^a-z]", "", cname.lower()): hits.append(r["id"]["record_id"])
    if not hits and len(recs) == 1: hits = [recs[0]["id"]["record_id"]]
    return hits


def main():
    text = open(sys.argv[1], encoding="utf-8").read()
    apply = "--apply" in sys.argv
    out = []
    for p in parse(text):
        hits, v = find(p), values(p)
        row = {"name": p["name"], "company": p["company"], "record_ids": hits, "values": v}
        if len(hits) != 1: row["skipped"] = "not found" if not hits else "ambiguous"
        elif apply:
            rid = hits[0]
            call("PATCH", f"/objects/people/records/{rid}", {"data": {"values": {k: (x if x is not None else []) for k, x in v.items()}}})
            got = call("GET", f"/objects/people/records/{rid}")["data"]["values"]
            bad = [k for k, x in v.items() if (flat(got, k) or None) != (x or None) and not (isinstance(x, list) and sorted(flat(got, k) if isinstance(flat(got, k), list) else [flat(got, k)] if flat(got, k) else []) == sorted(x))]
            row["readback_mismatch"] = bad
        out.append(row)
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
