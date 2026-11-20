"""Minimal Attio REST client. Needs ATTIO_API_KEY. All field access is allow-listed here."""
import json, os, urllib.request, urllib.error

BASE = "https://api.attio.com/v2"

# The ONLY fields the push skill may read and write.
DRAFT_READ = ["name", "person", "campaign", "kind", "subject", "body", "status", "drafted_at"]
PERSON_READ = ["name", "email_addresses", "outreach_prospect_id"]
DRAFT_WRITE = ["status", "pushed_at", "push_result"]
SEQUENCE_ID = "1419"


def call(method, path, body=None):
    req = urllib.request.Request(BASE + path, method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": "Bearer " + os.environ["ATTIO_API_KEY"],
                                          "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Attio {method} {path} failed: {e.code} {e.read().decode()[:300]}")


def flat(values, slug):
    """Return a plain Python value for one attribute (list for multi-value)."""
    out = []
    for v in values.get(slug) or []:
        if "option" in v: out.append(v["option"]["title"])
        elif "status" in v: out.append(v["status"]["title"])
        elif "full_name" in v: out.append(v["full_name"])
        elif "email_address" in v: out.append(v["email_address"])
        elif "target_record_id" in v: out.append(v["target_record_id"])
        elif "value" in v: out.append(v["value"])
    if not out: return None
    return out if len(out) > 1 or slug in ("cpm_concept_tags", "cpm_route_reason", "concept_tags", "updates_used") else out[0]


def project(record, allow):
    vals = record["values"]
    return {"record_id": record["id"]["record_id"], **{a: flat(vals, a) for a in allow}}
