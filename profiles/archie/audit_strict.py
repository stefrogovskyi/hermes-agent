import json
import re

with open("test_full_check.py") as f:
    code = f.read()

loc = {}
exec(code, loc)

title = loc['title']
meta_title = loc['meta_title']
meta_description = loc['meta_description']
body = loc['body']

full_text = f"{title}\n{meta_title}\n{meta_description}\n{body}"

# AI Clichés list
cliches = [
    "delve", "delving", "testament", "beacon", "landscape", "pivotal", "game-changer",
    "seamless", "seamlessly", "tapestry", "nestled", "foster", "fostering", "crucial",
    "essential", "in summary", "in conclusion", "unwavering", "demystify", "navigating",
    "realm", "ever-evolving", "paramount", "cornerstone", "vibrant", "unlock", "revolves around",
    "leverage", "leveraging", "dive deep", "harness", "harnessing", "treasure trove"
]

found_cliches = []
for c in cliches:
    # word boundary match
    if re.search(r'\b' + re.escape(c) + r'\b', full_text, re.IGNORECASE):
        found_cliches.append(c)

print("AI Clichés found:", found_cliches)

# Contrastive negations / "instead of" / "rather than" / "not X, but Y"
negations = ["instead of", "rather than", "not only"]
found_negations = []
for n in negations:
    matches = re.findall(r'\b' + re.escape(n) + r'\b', full_text, re.IGNORECASE)
    if matches:
        found_negations.append((n, len(matches)))

print("Negations found:", found_negations)

# Overlap checks
o1 = "[Material]+[Form]+[Primary function/use]+[Key specs]+[Brand/Model/SKU]"
o2 = "Injection-molded polypropylene brackets for automotive dashboards, non-structural, 220×45×6 mm, SKU BRK-220"
o3 = "T-7 to T-5 days: Finalize commercial paperwork and send broker pre-advice."

print("Overlap 1 exact match:", o1 in full_text)
print("Overlap 2 exact match:", o2 in full_text)
print("Overlap 3 exact match:", o3 in full_text)

# Check sub-phrases of overlaps to ensure high dissimilarity
print("\nSub-phrase overlap checks:")
print("'[Material]+[Form]':", "[Material]+[Form]" in full_text)
print("'Injection-molded polypropylene brackets for automotive dashboards':", "Injection-molded polypropylene brackets for automotive dashboards" in full_text)
print("'Finalize commercial paperwork and send broker pre-advice':", "Finalize commercial paperwork and send broker pre-advice" in full_text)

