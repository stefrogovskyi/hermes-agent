import re

keywords = [
    "freight index market analytics",
    "container spot rate benchmarking",
    "historical freight tariffs",
    "ocean freight rate trends",
    "white-label freight index API",
    "supply chain rate forecasting"
]

with open("check_text.py") as f:
    code = f.read()

# Extract body and full text from check_text.py execution
from check_text import title, meta_title, meta_desc, body, full_text

print("--- KEYWORD CHECK ---")
for kw in keywords:
    count = full_text.lower().count(kw.lower())
    print(f"'{kw}': {count} occurrences")

print("\n--- RULE CHECKLIST ---")
print("1. Em-dashes / double-hyphens:", "—" not in full_text and "--" not in full_text)

# Check slop words and generic fluff
slop_words = [
    'delve', 'testament', 'crucial', 'seamless', 'landscape', 'tapestry',
    "today's world", 'vital', 'unlock', 'game-changer', 'revolutionize',
    'elevate', 'transform', 'empower', 'robust', 'paradigm', 'comprehensive',
    'fostering', 'cutting-edge', 'in conclusion', 'to summarize'
]
slop_matches = [w for w in slop_words if w in full_text.lower()]
print("2. AI Slop Words:", slop_matches if slop_matches else "None (PASSED)")

# Connectors check
connectors = ["that's why", "which is why", "that explains why", "this is why"]
connector_matches = [c for c in connectors if c in full_text.lower()]
print("6. Over-explaining Connectors:", connector_matches if connector_matches else "None (PASSED)")

# Contrastive negation check
# Search for "instead of", "X, not Y", "not X, but Y", "not X, Y"
neg_patterns = [
    r'\binstead of\b',
    r'\bnot [a-zA-Z0-9\s]+, but\b',
    r'\bnot [a-zA-Z0-9\s]+, [a-zA-Z0-9\s]+\b'
]
neg_count = 0
for pat in neg_patterns:
    matches = re.findall(pat, full_text, re.IGNORECASE)
    neg_count += len(matches)
print("7. Contrastive Negations count:", neg_count, "(Limit max 1)")

print("\n--- METRICS ---")
print("Title length:", len(title), "/ 60")
print("Meta-Title length:", len(meta_title), "/ 60")
print("Meta-Description length:", len(meta_desc), "/ 155")
