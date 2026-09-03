import json
import re

with open("verified_final_article.json", "r", encoding="utf-8") as f:
    article = json.load(f)

with open("original_article.txt", "r", encoding="utf-8") as f:
    orig_text = f.read()

def clean_words(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text.lower())
    return [w for w in text.split() if w]

orig_words = clean_words(orig_text)
rev_words = clean_words(article["body_markdown"])

orig_6grams = set()
for i in range(len(orig_words) - 5):
    orig_6grams.add(tuple(orig_words[i:i+6]))

print("Draft word count:", len(rev_words))
print("Original word count:", len(orig_words))

matched_grams = []
for i in range(len(rev_words) - 5):
    gram = tuple(rev_words[i:i+6])
    if gram in orig_6grams:
        matched_grams.append((i, " ".join(gram)))

print(f"Total matched 6-gram locations: {len(matched_grams)}")
for idx, g in matched_grams[:20]:
    context = " ".join(rev_words[max(0, idx-3):min(len(rev_words), idx+9)])
    print(f"At word {idx}: '{g}'")
    print(f"   Context: ...{context}...")
