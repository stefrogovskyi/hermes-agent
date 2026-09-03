import re
from audit import original_text, rewrite_text

# Check every 6-gram in rewrite against original
def get_ngrams(text, n=6):
    words = re.findall(r'\b\w+\b', text.lower())
    ngrams = []
    for i in range(len(words) - n + 1):
        ngrams.append((" ".join(words[i:i+n]), i, words[i:i+n]))
    return ngrams

orig_words = re.findall(r'\b\w+\b', original_text.lower())
orig_set = set()
for i in range(len(orig_words) - 5):
    orig_set.add(" ".join(orig_words[i:i+6]))

rewrite_ngrams = get_ngrams(rewrite_text, 6)
matching_6grams = []
for gram, idx, word_list in rewrite_ngrams:
    if gram in orig_set:
        matching_6grams.append((idx, gram))

print(f"Total matching 6-grams: {len(matching_6grams)}")
for idx, gram in matching_6grams:
    print(f"  [{idx}] {gram}")

