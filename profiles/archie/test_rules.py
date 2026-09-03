import json
import re

with open("output.json", "r") as f:
    data = json.load(f)

title = data["title"]
meta_title = data["meta_title"]
meta_desc = data["meta_description"]
body = data["body"]

full_text = f"{title}\n{meta_title}\n{meta_desc}\n{body}"

print("=== CHECKING RULES ===")

# Rule 1: Dash check
dashes_found = []
if "—" in full_text: dashes_found.append("Em-dash (—)")
if "–" in full_text: dashes_found.append("En-dash (–)")
if "--" in full_text: dashes_found.append("Double hyphen (--)")
if " - " in full_text: dashes_found.append("Spaced hyphen ' - '")
print("Rule 1 (Dashes):", "FAIL: " + str(dashes_found) if dashes_found else "PASS")

# Rule 4: Explicit connectors
forbidden_connectors = [
    "furthermore", "in addition", "moreover", "however", "therefore",
    "consequently", "on the other hand", "additionally", "overall", "in conclusion",
    "besides", "thus", "hence", "nonetheless", "nevertheless", "what's new", "finally"
]
connectors_found = []
for c in forbidden_connectors:
    if re.search(r'\b' + re.escape(c) + r'\b', full_text, re.IGNORECASE):
        connectors_found.append(c)
print("Rule 4 (Connectors):", "FAIL: " + str(connectors_found) if connectors_found else "PASS")

# Rule 5: Contrastive negation check
# e.g. "not X, but Y", "not only X, but Y", "not X but Y"
negations = re.findall(r'\bnot\b[^.!?]*\bbut\b', full_text, re.IGNORECASE)
print("Rule 5 (Contrastive Negation count):", len(negations), negations)

# Rule 9: Metadata constraints
print("Rule 9 (Meta Title Len):", len(meta_title), "<= 60:", len(meta_title) <= 60)
print("Rule 9 (Meta Desc Len):", len(meta_desc), "<= 155:", len(meta_desc) <= 155)

# Check Trend Keywords
trend_keywords = [
    "container loading optimization",
    "air cargo tracking integration",
    "tracking history API",
    "freight index route calculation",
    "iOS mobile logistics access",
    "parcel tracking API"
]
for tk in trend_keywords:
    found = tk.lower() in full_text.lower()
    print(f"Trend keyword '{tk}':", "FOUND" if found else "MISSING")

