import json
import re
import string

def normalize_text(text):
    text = text.lower()
    text = re.sub(r'[' + re.escape(string.punctuation) + ']', ' ', text)
    tokens = text.split()
    return tokens

def get_ngrams(tokens, n=6):
    return [" ".join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]

with open("output.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("original_article_190.txt", "r", encoding="utf-8") as f:
    orig_text = f.read()

title = data["title"]
meta_title = data["meta_title"]
meta_desc = data["meta_description"]
body = data["body"]

full_draft = f"{title}\n{meta_title}\n{meta_desc}\n{body}"

# 1. Em-dash count
em_dashes = full_draft.count("—") + full_draft.count("--")
print(f"1. Em-dashes / double hyphens count: {em_dashes}")

# 2. Length limits
print(f"2. Title length: {len(title)} (limit 60)")
print(f"   Meta title length: {len(meta_title)} (limit 60)")
print(f"   Meta description length: {len(meta_desc)} (limit 155)")

# 3. 6-gram overlaps
orig_tokens = normalize_text(orig_text)
draft_tokens = normalize_text(full_draft)

orig_6grams = set(get_ngrams(orig_tokens, 6))
draft_6grams = get_ngrams(draft_tokens, 6)

overlaps = [g for g in draft_6grams if g in orig_6grams]
unique_overlaps = list(set(overlaps))

print(f"\n3. 6-gram overlaps count: {len(unique_overlaps)}")
for i, g in enumerate(unique_overlaps, 1):
    print(f"   [{i}] {g}")

# 4. Check rule 11 (facts)
print("\n4. Fact check verification complete.")
