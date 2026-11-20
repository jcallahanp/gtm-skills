# Attio field plan for the CPM skill. Run: python3 -I fields.py plan|apply
import json,os,sys,urllib.request
TAGS=["AI & Copilot Security","DSPM","DLP","Data Classification & Discovery","Data Risk Assessment","Least Privilege & Permissions","Identity & Active Directory","Threat Detection & Response","SIEM & SOC Integrations","Audit & Activity Monitoring","Compliance & Privacy","Data Governance & Ownership","Data Security (general)","Microsoft 365","Microsoft Purview","Cloud & IaaS","SaaS Apps","Database Security (DAM)","On-prem File Servers & NAS","Email Security","Network & Perimeter","Deployment & Prerequisites"]
P="people"; C="companies"; U="varonis_updates"
PLAN=[
 (P,"cpm_concepts","CPM technical concepts","text",False,None,"Technical concepts only. One per line: label: \"verbatim quote\" [E#, date]. Source: Past Meetings sheet."),
 (P,"cpm_concept_tags","CPM concept tags","select",True,[t for t in TAGS if t!="Deployment & Prerequisites"],"Tags from technical concepts. Used to match Varonis Updates."),
 (P,"cpm_past_rep","CPM past rep","text",False,None,"Varonis first name from the meeting evidence, or blank."),
 (P,"cpm_stall_reason","CPM stall reason","select",False,["Budget","Timing","No interest","Pending then silence","Unknown"],"Why it did not move forward, from the evidence only."),
 (P,"cpm_stall_quote","CPM stall quote","text",False,None,"Verbatim quote behind the stall reason."),
 (P,"cpm_route","CPM route","select",False,["Draft","Needs John"],"Draft = write email. Needs John = write card only."),
 (P,"cpm_route_reason","CPM route reason","select",True,["No technical concepts","Inactive email","Support cases only","Recurring/customer pattern"],"Why the record needs John."),
 (P,"cpm_obtained","CPM obtained","select",False,["Obtained","Not obtained"],"Whether a clear technical concept exists."),
 (P,"cpm_not_obtained_reason","CPM not obtained reason","text",False,None,"Why no technical concept was found."),
 (P,"cpm_draft","CPM draft","text",False,None,"Output: email or Needs John card. Written by the CPM skill. Never sent automatically."),
 (P,"cpm_draft_status","CPM draft status","select",False,["Drafted","Reviewed","Approved","Sent","Skipped"],"Lifecycle of the CPM draft."),
 (P,"cpm_updates_used","CPM updates used","record-reference",True,None,"Varonis Updates rows used in the draft."),
 (C,"account_rep","Account rep","select",False,["Todd Cencich","Rob Andersen","Patrick Dolan"],"Current account rep. Only these three values. Copied from rep."),
 (U,"concept_tags","Concept tags","select",True,TAGS,"Same tag set as people cpm_concept_tags."),
 (U,"use_case","Use case","select",False,["Atlas & AI Security","Interceptor & Email Security","DAM & Database Security","Compliance & Governance","Threat Detection & Response","Access Management & IAM","Cloud Security"],"Use case group."),
 (U,"category","Category","text",False,None,"Sub-area within the use case."),
 (U,"quote","Supporting quote","text",False,None,"Verbatim sentence from the source proving the update."),
 (U,"verification","Verification","select",False,["Verified live","Cached only","Drive PDF","No URL"],"How the row was checked."),
]
def api(m,path,body=None):
    req=urllib.request.Request("https://api.attio.com/v2"+path,method=m,data=json.dumps(body).encode() if body else None,headers={"Authorization":"Bearer "+os.environ["ATTIO_API_KEY"],"Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req) as r: return json.load(r)
    except urllib.error.HTTPError as e: return {"error":e.code,"body":e.read().decode()[:300]}
def existing(o): return {a["api_slug"] for a in api("GET",f"/objects/{o}/attributes?limit=300")["data"]}
mode=sys.argv[1]
ex={o:existing(o) for o in (P,C,U)}
for o,slug,title,typ,multi,opts,desc in PLAN:
    if slug in ex[o]: print("EXISTS",o,slug); continue
    print("CREATE",o,slug,typ,"multi" if multi else "",len(opts or []),"options")
    if mode!="apply": continue
    cfg={}
    if typ=="record-reference": cfg={"record_reference":{"allowed_objects":[U]}}
    r=api("POST",f"/objects/{o}/attributes",{"data":{"title":title,"description":desc,"api_slug":slug,"type":typ,"is_required":False,"is_unique":False,"is_multiselect":multi,"config":cfg}})
    if "error" in r: print("  FAIL",r); continue
    for t in opts or []:
        rr=api("POST",f"/objects/{o}/attributes/{slug}/options",{"data":{"title":t}})
        if "error" in rr: print("  OPTION FAIL",t,rr)
    print("  ok")
