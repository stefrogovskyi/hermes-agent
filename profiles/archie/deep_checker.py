import json
import re

with open("output.json") as f:
    data = json.load(f)

title = data["title"]
meta_title = data["meta_title"]
meta_desc = data["meta_description"]
body = data["body_markdown"]

full_text = f"{title}\n{meta_title}\n{meta_desc}\n{body}"

print("=== CHECKING RULES ===")

# 1. Em-dashes
em_dashes = re.findall(r"—|--", full_text)
print("1. Em-dashes:", len(em_dashes))

# 4. Explicit connectors
connectors = ["furthermore", "in addition", "moreover", "that's why", "consequently", "thus", "additionally", "overall", "in conclusion"]
found_conn = [c for c in connectors if re.search(rf"\b{c}\b", full_text, re.I)]
print("4. Explicit connectors found:", found_conn)

# 5. Contrastive negation
negations = ["not only", "instead of", "rather than"]
found_neg = [n for n in negations if re.search(rf"\b{n}\b", full_text, re.I)]
print("5. Contrastive negations found:", found_neg)

# 9. Limits
print(f"9. Meta title length: {len(meta_title)} <= 60: {len(meta_title) <= 60}")
print(f"9. Meta desc length: {len(meta_desc)} <= 155: {len(meta_desc) <= 155}")

# 7. Twin sentences
paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]
for p in paragraphs:
    if p.startswith("#") or p.startswith("*"):
        continue
    sentences = re.split(r'(?<=[.!?])\s+', p)
    for i in range(len(sentences)-1):
        s1 = sentences[i].strip()
        s2 = sentences[i+1].strip()
        w1 = s1.split()[0].lower() if s1 else ""
        w2 = s2.split()[0].lower() if s2 else ""
        if w1 == w2 and len(w1) > 2:
            print(f"WARNING Twin start ({w1}):\n  S1: {s1}\n  S2: {s2}")

