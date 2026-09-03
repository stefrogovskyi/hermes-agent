import re

with open('/opt/hermes/profiles/archie/source.txt') as f:
    orig_text = f.read()

with open('/opt/hermes/profiles/archie/draft.txt') as f:
    draft_text = f.read()

# Clean up punctuation except spaces to compare exact word sequences
def clean_words(text):
    return re.findall(r'\b\w+\b', text)

orig_w = clean_words(orig_text)
draft_w = clean_words(draft_text)

def find_overlaps(min_len=5):
    orig_grams = {}
    for i in range(len(orig_w) - min_len + 1):
        gram = " ".join(orig_w[i:i+min_len]).lower()
        orig_grams[gram] = i

    found = []
    i = 0
    while i < len(draft_w) - min_len + 1:
        max_gram = ""
        max_l = 0
        for l in range(min_len, len(draft_w) - i + 1):
            gram = " ".join(draft_w[i:i+l]).lower()
            if gram in " ".join(orig_w).lower():
                max_gram = gram
                max_l = l
            else:
                break
        if max_l >= min_len:
            found.append((i, max_l, max_gram, " ".join(draft_w[i:i+max_l])))
            i += max_l
        else:
            i += 1
    return found

print("--- OVERLAPS (>= 5 words) ---")
for idx, length, gram_lower, gram_orig in find_overlaps(5):
    print(f"Length {length}: '{gram_orig}'")
