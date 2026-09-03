import json
import re

with open('/opt/hermes/profiles/archie/final_draft.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('/opt/hermes/profiles/archie/article_full_text.txt', 'r', encoding='utf-8') as f:
    orig_text = f.read()

title = data['title']
meta_title = data['meta_title']
meta_description = data['meta_description']
body = data['body_markdown']

full_combined = f"{title}\n{meta_title}\n{meta_description}\n{body}"

print("=== PROGRAMMATIC CHECK RESULTS ===")

# 1. Em-dashes
em_dashes = full_combined.count("—") + full_combined.count("--")
print(f"1. Em-dash count (— or --): {em_dashes} (Target: 0)")

# 2. Length limits
print(f"2. Title length: {len(title)} chars (Target: <= 60)")
print(f"   Meta Title length: {len(meta_title)} chars (Target: <= 60)")
print(f"   Meta Description length: {len(meta_description)} chars (Target: <= 155)")

# 3. Contrastive negation check
not_count = len(re.findall(r'\bnot\b', body, re.IGNORECASE))
instead_count = len(re.findall(r'\binstead of\b', body, re.IGNORECASE))
print(f"3. Negation occurrences ('not': {not_count}, 'instead of': {instead_count})")

# 4. 6-gram overlap check
def get_ngrams(text, n=6):
    words = re.findall(r'\b\w+\b', text.lower())
    return set(zip(*[words[i:] for i in range(n)]))

orig_ngrams = get_ngrams(orig_text, 6)
body_ngrams = get_ngrams(body, 6)

overlaps = orig_ngrams.intersection(body_ngrams)

# Exempt proper names / carrier / industry terms
exempt_terms = {"uniqode", "digital", "business", "card", "credibly"}

non_exempt_overlaps = []
for gram in overlaps:
    phrase = " ".join(gram)
    if not any(term in phrase for term in exempt_terms):
        non_exempt_overlaps.append(phrase)

print(f"4. 6-gram overlap count (excluding exemptions): {len(non_exempt_overlaps)}")
if non_exempt_overlaps:
    print("   Non-exempt overlaps:", non_exempt_overlaps)
else:
    print("   ZERO non-exempt 6-gram overlaps found!")

# 5. Cliché / AI vocabulary check
ai_words = ["delve", "testament", "tapestry", "pivotal", "paramount", "beacon", "game-changer", "seamless", "robust", "foster", "elevate", "streamline"]
found_ai_words = [w for w in ai_words if re.search(r'\b' + w + r'\b', full_combined, re.IGNORECASE)]
print(f"5. Banned AI words found: {found_ai_words}")

pass_all = (em_dashes == 0) and (len(title) <= 60) and (len(meta_title) <= 60) and (len(meta_description) <= 155) and (len(non_exempt_overlaps) == 0) and (len(found_ai_words) == 0)
print(f"\nFINAL VERDICT: {'PASS - ALL CHECKS PASSED' if pass_all else 'NEEDS CORRECTION'}")
