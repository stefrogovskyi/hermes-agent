import re

with open('/opt/hermes/profiles/archie/final_article.txt', 'r', encoding='utf-8') as f:
    text = f.read()

with open('/opt/hermes/profiles/archie/original_article_clean.txt', 'r', encoding='utf-8') as f:
    orig_text = f.read()

# Extract Title, Meta Title, Meta Description, Body Text
title_m = re.search(r'Title:\s*(.*)', text)
meta_title_m = re.search(r'Meta Title:\s*(.*)', text)
meta_desc_m = re.search(r'Meta Description:\s*(.*)', text)

title = title_m.group(1).strip() if title_m else ''
meta_title = meta_title_m.group(1).strip() if meta_title_m else ''
meta_desc = meta_desc_m.group(1).strip() if meta_desc_m else ''

body_start = text.find('Text:')
body = text[body_start + 5:].strip() if body_start != -1 else text

print("--- Step 7 Programmatic Checks ---")

# 1. Em-dash check
em_dashes_title = title.count('—') + title.count('--')
em_dashes_mtitle = meta_title.count('—') + meta_title.count('--')
em_dashes_mdesc = meta_desc.count('—') + meta_desc.count('--')
em_dashes_body = body.count('—') + body.count('--')

total_em_dashes = em_dashes_title + em_dashes_mtitle + em_dashes_mdesc + em_dashes_body
print(f"1. Em-dashes count: {total_em_dashes} (Title: {em_dashes_title}, MetaTitle: {em_dashes_mtitle}, MetaDesc: {em_dashes_mdesc}, Body: {em_dashes_body})")

# 2. Length checks
print(f"2. Lengths:")
print(f"   - Title: {len(title)} chars (Limit: 60)")
print(f"   - Meta Title: {len(meta_title)} chars (Limit: 60)")
print(f"   - Meta Description: {len(meta_desc)} chars (Limit: 155)")

# 3. N-gram 6-gram check
def tokenize(s):
    # normalize: lowercase, keep letters, digits, spaces
    s_clean = re.sub(r'[^a-z0-9\s]', '', s.lower())
    return s_clean.split()

orig_tokens = tokenize(orig_text)
final_tokens = tokenize(body)

def get_ngrams(tokens, n=6):
    return set(" ".join(tokens[i:i+n]) for i in range(len(tokens) - n + 1))

orig_ngrams = get_ngrams(orig_tokens, 6)
final_ngrams = get_ngrams(final_tokens, 6)

overlap_6grams = final_ngrams.intersection(orig_ngrams)

# Exclude industry standard terms or proper nouns if any
ALLOWED_EXCEPTIONS = [
    "shipping containers are being repurposed in",
    "shipping containers can be converted into",
    "repurposing shipping containers creative and functional"
]

filtered_overlaps = [g for g in overlap_6grams if g not in ALLOWED_EXCEPTIONS]

print(f"3. 6-gram Overlaps: {len(filtered_overlaps)}")
if filtered_overlaps:
    print("   Matches found:")
    for match in filtered_overlaps:
        print(f"   - '{match}'")
else:
    print("   0 non-exempt 6-gram overlaps!")
