import re

with open("original_post.txt", "r", encoding="utf-8") as f:
    orig_text = f.read()

from test_fix import result_json

full_rewrite = f"{result_json['title']}\n{result_json['meta_title']}\n{result_json['meta_description']}\n{result_json['body_md']}"

def normalize_words(text):
    text_clean = re.sub(r'[^\w\s]', ' ', text.lower())
    return [w for w in text_clean.split() if w]

orig_words = normalize_words(orig_text)
rewrite_words = normalize_words(full_rewrite)

orig_6grams = set()
for i in range(len(orig_words) - 5):
    orig_6grams.add(" ".join(orig_words[i:i+6]))

matches = []
for i in range(len(rewrite_words) - 5):
    gram = " ".join(rewrite_words[i:i+6])
    if gram in orig_6grams:
        matches.append(gram)

print(f"6-gram matches count: {len(matches)}")
for m in set(matches):
    print(" -", m)
