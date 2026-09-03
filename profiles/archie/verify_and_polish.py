import re, json

with open("/opt/hermes/profiles/archie/article_draft.md", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Em-dashes check
em_dashes = text.count("—") + text.count("–") + text.count("--")
print(f"Em-dashes / en-dashes / double-hyphens count: {em_dashes}")

# 2. Extract Title, Meta Title, Meta Description, Body
title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
title = title_match.group(1).strip() if title_match else ""

meta_title_match = re.search(r"\*\*Meta Title:\*\*\s*(.+)$", text, re.MULTILINE)
meta_title = meta_title_match.group(1).strip() if meta_title_match else title

meta_desc_match = re.search(r"\*\*Meta Description:\*\*\s*(.+)$", text, re.MULTILINE)
meta_desc = meta_desc_match.group(1).strip() if meta_desc_match else ""

print(f"Title ({len(title)} chars): {title}")
print(f"Meta Title ({len(meta_title)} chars): {meta_title}")
print(f"Meta Description ({len(meta_desc)} chars): {meta_desc}")

# Check limits
title_ok = len(title) <= 60
meta_title_ok = len(meta_title) <= 60
meta_desc_ok = len(meta_desc) <= 155

print(f"Title <= 60: {title_ok}")
print(f"Meta Title <= 60: {meta_title_ok}")
print(f"Meta Description <= 155: {meta_desc_ok}")

# Read original article text directly from saved JSON or task log
with open("/opt/hermes/profiles/archie/cache/delegation/live/deleg_a8606d7f/manifest.json") as f:
    manifest = json.load(f)

orig_text = ""
if "context" in manifest:
    orig_text = manifest["context"]
elif "tasks" in manifest and "context" in manifest["tasks"][0]:
    orig_text = manifest["tasks"][0]["context"]

def tokenize(s):
    s_clean = re.sub(r"[^\w\s]", "", s.lower())
    return s_clean.split()

tokens_orig = tokenize(orig_text)
tokens_draft = tokenize(text)

def get_ngrams(tokens, n):
    return set(tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1))

ngrams_orig = get_ngrams(tokens_orig, 6)
ngrams_draft = get_ngrams(tokens_draft, 6)

overlapping = ngrams_orig.intersection(ngrams_draft)
print(f"Overlapping 6-grams count: {len(overlapping)}")
for g in overlapping:
    print("  Overlap:", " ".join(g))
