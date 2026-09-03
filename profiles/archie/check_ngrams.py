import re

with open("/opt/hermes/profiles/archie/exact_article.txt") as f:
    orig_text = f.read()

from process_and_verify import body_markdown, title

def normalize_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    words = text.split()
    return words

orig_words = normalize_text(orig_text)
rewrite_words = normalize_text(f"{title} {body_markdown}")

def get_ngrams(words, n=6):
    return set(tuple(words[i:i+n]) for i in range(len(words)-n+1))

orig_6grams = get_ngrams(orig_words, 6)
rewrite_6grams = get_ngrams(rewrite_words, 6)

overlap = orig_6grams.intersection(rewrite_6grams)

print(f"Total 6-gram overlaps found: {len(overlap)}")
for g in overlap:
    phrase = " ".join(g)
    print(f"  Overlap: '{phrase}'")
