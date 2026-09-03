import json
import re

# Read Subagent 3 output file or full text
with open('/opt/hermes/profiles/archie/cache/delegation/subagent-summary-0-20260901_211627_280107.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract json
json_match = re.search(r'```json\s*(\{.*?\})\s*```', content, re.DOTALL)
if json_match:
    json_str = json_match.group(1)
else:
    json_str = content[content.find('{'):content.rfind('}')+1]

article_data = json.loads(json_str)

title = article_data["title"]
meta_title = article_data["meta_title"]
meta_description = article_data["meta_description"]
body = article_data["body_markdown"]

full_text = f"{title}\n{meta_title}\n{meta_description}\n{body}"

# 1. Dash check
em_dashes = full_text.count("—")
en_dashes = full_text.count("–")
double_hyphens = full_text.count("--")
total_dashes = em_dashes + en_dashes + double_hyphens

print(f"1. Dash check: em={em_dashes}, en={en_dashes}, double={double_hyphens}. Total={total_dashes}")

# 2. Meta lengths
print(f"2. Lengths:")
print(f"   Title: {len(title)} chars")
print(f"   Meta Title: {len(meta_title)} chars (max 60) -> {'OK' if len(meta_title) <= 60 else 'EXCEEDED'}")
print(f"   Meta Description: {len(meta_description)} chars (max 155) -> {'OK' if len(meta_description) <= 155 else 'EXCEEDED'}")

# 3. Banned AI clichés & connectors
banned_words = [
    "delve", "tapestry", "testament", "beacon", "landscape", "pivotal", 
    "game-changer", "fostering", "unlock", "seamless", "elevate", 
    "cutting-edge", "realm", "ever-evolving", "paramount", "spearhead", "boasts"
]
banned_connectors = [
    "furthermore", "moreover", "in addition", "crucially", "that's why", "ultimately", "importantly"
]

found_banned = [w for w in banned_words if re.search(rf"\b{w}\b", full_text, re.I)]
found_connectors = [c for c in banned_connectors if re.search(rf"\b{c}\b", full_text, re.I)]

print(f"3. Clichés found: {found_banned}")
print(f"   Connectors found: {found_connectors}")

# 4. N-gram 6-gram check
with open("/opt/hermes/profiles/archie/article_329_clean.txt", "r", encoding="utf-8") as f:
    orig_text = f.read()

def normalize(txt):
    txt = re.sub(r'[^\w\s]', ' ', txt.lower())
    return [w for w in txt.split() if w]

orig_words = normalize(orig_text)
rewrite_words = normalize(full_text)

orig_6grams = set(" ".join(orig_words[i:i+6]) for i in range(len(orig_words)-5))
rewrite_6grams = [" ".join(rewrite_words[i:i+6]) for i in range(len(rewrite_words)-5)]

matched_6grams = [g for g in rewrite_6grams if g in orig_6grams]

print(f"4. 6-gram overlaps count: {len(matched_6grams)}")
if matched_6grams:
    print("   Unique matches:")
    for m in set(matched_6grams):
        print("    -", m)

# Save verified json
verified_output = {
    "title": title,
    "meta_title": meta_title,
    "meta_description": meta_description,
    "body_markdown": body,
    "em_dash_count": total_dashes,
    "meta_title_len": len(meta_title),
    "meta_desc_len": len(meta_description),
    "banned_words": found_banned,
    "banned_connectors": found_connectors,
    "ngram_overlap_count": len(set(matched_6grams))
}

with open("/opt/hermes/profiles/archie/final_article_verified.json", "w", encoding="utf-8") as f:
    json.dump(verified_output, f, ensure_ascii=False, indent=2)

print("\nSaved final_article_verified.json")
