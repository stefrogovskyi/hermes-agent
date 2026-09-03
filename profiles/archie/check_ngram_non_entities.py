import re
import json

with open('/opt/hermes/profiles/archie/original_article_clean.txt', 'r') as f:
    orig_text = f.read()

with open('/opt/hermes/profiles/archie/final_article.json', 'r') as f:
    data = json.load(f)

body = data['body_markdown']

def extract_prose(text):
    lines = text.splitlines()
    prose_lines = [l for l in lines if not l.strip().startswith('-') and not l.strip().startswith('#') and l.strip()]
    return " ".join(prose_lines)

orig_prose = extract_prose(orig_text)
rewrite_prose = extract_prose(body)

def normalize_and_tokenize(text):
    text_clean = re.sub(r'[^\w\s]', ' ', text.lower())
    tokens = text_clean.split()
    return tokens

orig_tokens = normalize_and_tokenize(orig_prose)
rewrite_tokens = normalize_and_tokenize(rewrite_prose)

orig_6grams = set(tuple(orig_tokens[i:i+6]) for i in range(len(orig_tokens)-5))
rewrite_6grams = [tuple(rewrite_tokens[i:i+6]) for i in range(len(rewrite_tokens)-5)]

matching = [ " ".join(g) for g in rewrite_6grams if g in orig_6grams ]

print("PROSE MATCHING 6-GRAMS COUNT:", len(matching))
for m in matching:
    print(" - PROSE MATCH:", m)
