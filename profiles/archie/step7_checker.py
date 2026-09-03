import json
import re

with open('/opt/hermes/profiles/archie/subagent1_output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

title = data['title']
meta_title = data['meta_title']
meta_description = data['meta_description']
body = data['body_markdown']

full_text = f"{title}\n{meta_title}\n{meta_description}\n{body}"

# Check em-dashes / en-dashes / double-hyphens
em_dashes = re.findall(r'[\u2014\u2013]|--', full_text)

# Check lengths
title_len = len(title)
meta_title_len = len(meta_title)
meta_desc_len = len(meta_description)

# N-gram overlap check against clean body
with open('/opt/hermes/profiles/archie/orig_article_357_raw.txt', 'r', encoding='utf-8') as f:
    orig_text = f.read()

def clean_words(text):
    text = re.sub(r'[^\w\s]', '', text.lower())
    return [w for w in text.split() if w]

def get_ngrams(words, n=6):
    return set([' '.join(words[i:i+n]) for i in range(len(words)-n+1)])

orig_words = clean_words(orig_text)
rewrite_words = clean_words(full_text)

orig_6grams = get_ngrams(orig_words, 6)
rewrite_6grams = get_ngrams(rewrite_words, 6)

overlaps = orig_6grams.intersection(rewrite_6grams)

print("=== PROGRAMMATIC STEP 7 CHECK ===")
print(f"1. Em-dash / En-dash count: {len(em_dashes)}")
print(f"2. Title Length: {title_len} chars (limit <= 60)")
print(f"3. Meta Title Length: {meta_title_len} chars (limit <= 60)")
print(f"4. Meta Description Length: {meta_desc_len} chars (limit <= 155)")
print(f"5. 6-gram Overlaps Count: {len(overlaps)}")
if overlaps:
    print("Overlaps found:")
    for o in overlaps:
        print("  -", o)

results = {
    "em_dash_count": len(em_dashes),
    "title_length": title_len,
    "meta_title_length": meta_title_len,
    "meta_desc_length": meta_desc_len,
    "ngram_overlap_count": len(overlaps),
    "overlaps": list(overlaps)
}

with open('/opt/hermes/profiles/archie/step7_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
