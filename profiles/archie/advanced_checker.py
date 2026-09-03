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

# Rule 1: Dash check
dashes = [c for c in full_text if ord(c) in [8211, 8212, 8213]] or re.findall(r'--', full_text)
print("Rule 1 (Em-dashes/En-dashes/Double hyphens):", "FAIL" if dashes else "PASS", dashes)

# Rule 2 & 6: Sentences check
sentences = [s.strip() for s in re.split(r'[.!?]\s+', body) if s.strip()]
print(f"Total Sentences in Body: {len(sentences)}")

# Rule 3: Explicit Connectors
connectors = ["that's why", "which is why", "furthermore", "moreover", "in addition", "however", "consequently", "therefore", "as a result", "thus"]
found_conn = [c for c in connectors if re.search(r'\b' + re.escape(c) + r'\b', full_text, re.IGNORECASE)]
print("Rule 3 (Explicit Connectors):", "FAIL" if found_conn else "PASS", found_conn)

# Rule 4: Contrastive Negation
negations = ["instead of", "rather than", ", not "]
found_neg = [n for n in negations if n in full_text.lower()]
print("Rule 4 (Contrastive Negation):", f"Count={len(found_neg)}", "PASS" if len(found_neg) <= 1 else "FAIL", found_neg)

# Rule 9: AI Vocab
banned_words = [
    "delve", "seamless", "seamlessly", "tapestry", "game-changer", "gamechanger", "game changer", 
    "testament", "fast-paced", "vital role", "leverage", "paradigm shift", "beacon", 
    "not only", "revolutionize", "revolutionizes", "revolutionizing", "revolution",
    "foster", "intertwined", "realm", "landscape", "unwavering", "in conclusion", "to sum up"
]
found_banned = [w for w in banned_words if re.search(r'\b' + re.escape(w) + r'\b', full_text, re.IGNORECASE)]
print("Rule 9 (Banned AI Vocabulary):", "FAIL" if found_banned else "PASS", found_banned)

# Rule 10: Lengths
print(f"Rule 10 (Meta Title Length): {len(meta_title)} chars (Max 60) ->", "PASS" if len(meta_title) <= 60 else "FAIL")
print(f"Rule 10 (Meta Desc Length): {len(meta_desc)} chars (Max 155) ->", "PASS" if len(meta_desc) <= 155 else "FAIL")

# Trend Keywords check
trend_kws = [
    "cellular IoT fleet tracking",
    "global asset visibility",
    "multi-network roaming",
    "remote SIM provisioning"
]

print("\n=== TREND KEYWORDS CHECK ===")
for kw in trend_kws:
    present = kw.lower() in full_text.lower()
    print(f"Keyword '{kw}':", "PRESENT" if present else "MISSING")

