"""Script checks for one draft. Usage: python3 cpm_check.py PERSON_JSON_FILE DRAFT_TXT_FILE [YYYY-MM-DD]
PERSON_JSON_FILE = one person object from cpm_read.py people. Exit 1 if any check fails."""
import datetime, json, re, sys
p = json.load(open(sys.argv[1])); body = open(sys.argv[2]).read().strip()
today = datetime.date.fromisoformat(sys.argv[3]) if len(sys.argv) > 3 else datetime.date.today()
plan_year = today.year + 1 if today.month >= 10 else today.year
asks = ["Might one day this week afford 30 minutes for this convo?",
        "Would sometime next week afford 30 minutes for this conversation?",
        "Think you could squeeze 30 minutes in for this convo before the holidays?"]
holiday_ok = (today.month == 11 and today.day >= 15) or today.month == 12
paras = [x.strip() for x in re.split(r"\n\s*\n", body) if x.strip()]
fails = []
if p.get("cpm_route") != "Draft": fails.append("route is not Draft – write a card instead")
if len(paras) != 4: fails.append(f"{len(paras)} paragraphs, need 4")
if paras and paras[-1] not in asks: fails.append("¶4 is not an approved ask word for word")
if paras and paras[-1] == asks[2] and not holiday_ok: fails.append("holiday ask outside mid-Nov–Dec")
if len(paras) > 2 and f"{plan_year} roadmap" not in paras[2]: fails.append(f"¶3 lacks '{plan_year} roadmap'")
if len(body.split()) >= 90: fails.append(f"{len(body.split())} words, need under 90")
if re.search(r"\bports?\b|firewall|service account|collector|helm|\beks\b|cloudformation|app registration|prerequisite|\bpatch", body, re.I): fails.append("setup word present")
if re.search(r"cutting-edge|industry-leading|best-in-class|revolutionary|!", body, re.I): fails.append("hype word or exclamation mark")
for rep in ["Todd Cencich", "Rob Andersen", "Patrick Dolan"]:
    if rep in body and rep != p.get("account_rep"): fails.append(f"names {rep} but account_rep is {p.get('account_rep')}")
print(json.dumps({"pass": not fails, "fails": fails, "words": len(body.split())}, ensure_ascii=False))
sys.exit(1 if fails else 0)
