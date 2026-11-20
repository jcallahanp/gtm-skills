"""Mechanical clean-up of an approved draft for Outreach sequence 1419.
The 1419 template adds "Hi {first name}," and the signature, so the body must have neither.
Rules (in order):
 1. Drop a leading greeting addressed to the person: "Hey Darin - ", "Hi Mark - ", "Steve - ", "Hey Josh," (greeting-only paragraph is dropped).
 2. Capitalize the first letter of what is left.
 3. Drop trailing sign-off paragraphs (Best / Thanks / Regards / Cheers / Sincerely, with or without a name) and a last paragraph that is only a name.
 3b. Add "Best," as the last paragraph (the sequence adds the full signature under it).
 4. Build HTML: one <p> per paragraph, <p><br></p> between paragraphs, <br> for a line break inside a paragraph, text HTML-escaped.
 5. Refuse (raise) if the first name still appears in the first 4 words, or a sign-off is still present.
"""
import html, re

SIGNOFF = re.compile(r"^(best|thanks|thank you|many thanks|regards|best regards|kind regards|cheers|sincerely|talk soon)\b[\s,.!]*([A-Z][a-z]+(\s[A-Z][a-z]+)?)?\s*$", re.I)


def clean(body, first_name):
    paras = [p.strip() for p in re.split(r"\n\s*\n", body.strip()) if p.strip()]
    fn = re.escape(first_name.strip())
    greet = re.compile(rf"^(?:(?:hey|hi|hello|good morning|good afternoon)\s+)?{fn}\s*(?:-|–|—|,|:)\s*", re.I)
    if paras:
        first = greet.sub("", paras[0], count=1).strip()
        if first:
            paras[0] = first[0].upper() + first[1:]
        else:
            paras.pop(0)
    while paras and (SIGNOFF.match(paras[-1]) or re.fullmatch(r"[A-Z][a-z]+(\s[A-Z][a-z]+)?", paras[-1])):
        paras.pop()
    if not paras: raise ValueError("empty body after clean-up")
    if re.search(rf"\b{fn}\b", " ".join(paras[0].split()[:4]), re.I): raise ValueError("first name still at the top")
    if SIGNOFF.match(paras[-1]): raise ValueError("sign-off still present")
    paras.append("Best,")
    text = "\n\n".join(paras)
    html_body = "<p><br></p>".join("<p>" + html.escape(p).replace("\n", "<br>") + "</p>" for p in paras)
    return text, html_body
