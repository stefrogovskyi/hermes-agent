import json
import re

with open("final_verified_data.json", "r", encoding="utf-8") as f:
    revised_data = json.load(f)

with open("original_article.txt", "r", encoding="utf-8") as f:
    orig_text = f.read()

# 1. Em-dash check
full_text_to_check = revised_data["title"] + " " + revised_data["meta_title"] + " " + revised_data["meta_description"] + " " + revised_data["body_markdown"]
em_dashes = re.findall(r'[—–]|--', full_text_to_check)
print(f"1. Em-dashes count: {len(em_dashes)}")

# 2. Length limits check
title_len = len(revised_data["title"])
meta_title_len = len(revised_data["meta_title"])
meta_desc_len = len(revised_data["meta_description"])
print(f"2. Title length: {title_len} (max 60) -> {'OK' if title_len <= 60 else 'FAIL'}")
print(f"   Meta Title length: {meta_title_len} (max 60) -> {'OK' if meta_title_len <= 60 else 'FAIL'}")
print(f"   Meta Description length: {meta_desc_len} (max 155) -> {'OK' if meta_desc_len <= 155 else 'FAIL'}")

# 3. 6-gram overlap check
def clean_words(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text.lower())
    return [w for w in text.split() if w]

orig_words = clean_words(orig_text)
rev_words = clean_words(revised_data["body_markdown"])

orig_6grams = set()
for i in range(len(orig_words) - 5):
    orig_6grams.add(tuple(orig_words[i:i+6]))

overlaps = []
for i in range(len(rev_words) - 5):
    gram = tuple(rev_words[i:i+6])
    if gram in orig_6grams:
        overlaps.append(" ".join(gram))

print(f"3. 6-gram overlaps count: {len(overlaps)}")
if overlaps:
    print("   Overlaps detail:")
    for o in set(overlaps):
        print(f"   - '{o}'")

# Rule 11 manual re-verification
print("4. Rule 11 Verification:")
print("   - SOLAS: ", "FOUND (BAD)" if "solas" in full_text_to_check.lower() else "PASSED (NONE)")
print("   - IoT: ", "FOUND (BAD)" if "iot" in full_text_to_check.lower() else "PASSED (NONE)")
print("   - Pumps: ", "FOUND (BAD)" if "pumps" in full_text_to_check.lower() else "PASSED (NONE)")
print("   - Electrical: ", "FOUND (BAD)" if "electrical" in full_text_to_check.lower() else "PASSED (NONE)")
print("   - Saltwater: ", "FOUND (BAD)" if "saltwater" in full_text_to_check.lower() else "PASSED (NONE)")
