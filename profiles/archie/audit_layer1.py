import re
from collections import defaultdict

with open('/opt/hermes/profiles/archie/source.txt') as f:
    original = f.read()

with open('/opt/hermes/profiles/archie/draft.txt') as f:
    draft = f.read()

def tokenize(text):
    # normalize words for n-gram comparison
    words = re.findall(r'\b[\w\.\@\-]+\b', text.lower())
    return words

orig_words = tokenize(original)
draft_words = tokenize(draft)

print(f"Original word count: {len(orig_words)}")
print(f"Draft word count: {len(draft_words)}")

# Check 6-grams or longer overlaps
orig_6grams = set()
for i in range(len(orig_words) - 5):
    orig_6grams.add(" ".join(orig_words[i:i+6]))

matches = []
for i in range(len(draft_words) - 5):
    gram = " ".join(draft_words[i:i+6])
    if gram in orig_6grams:
        matches.append((i, gram))

print("\n--- 6+ Word Overlaps Found ---")
for idx, m in matches:
    print(f"Index {idx}: {m}")

# Also check for longer overlaps or character-level / word-level exact phrase matches
def get_ngrams(words, n):
    return [" ".join(words[i:i+n]) for i in range(len(words)-n+1)]

# Let's inspect all n-gram matches for n=4, 5, 6, 7...
for n in [4, 5, 6, 7, 8]:
    o_grams = set(get_ngrams(orig_words, n))
    d_grams = [g for g in get_ngrams(draft_words, n) if g in o_grams]
    print(f"Matching {n}-grams count: {len(d_grams)}")
    if d_grams:
        for g in set(d_grams):
            print(f"   {n}-gram: {g}")
