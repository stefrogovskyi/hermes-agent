import json
import re

# Load JSON output from subagent 1
with open('/opt/hermes/profiles/archie/final_output.json', 'r') as f:
    data = json.load(f)

title = data.get('title', '')
meta_title = data.get('meta_title', '')
meta_desc = data.get('meta_description', '')
body = data.get('body_markdown', '')

print(f"Title ({len(title)} chars): {title}")
print(f"Meta Title ({len(meta_title)} chars): {meta_title}")
print(f"Meta Description ({len(meta_desc)} chars): {meta_desc}")

# 1. Em-dash check
full_text = f"{title}\n{meta_title}\n{meta_desc}\n{body}"
em_dash_count = full_text.count('—') + full_text.count('--')
print(f"Em-dash count: {em_dash_count}")

# 2. Length limits
# Title max 60, Meta title max 60, Meta desc max 155
print(f"Title len check: {'OK' if len(title) <= 60 else 'EXCEEDED'}")
print(f"Meta title len check: {'OK' if len(meta_title) <= 60 else 'EXCEEDED'}")
print(f"Meta desc len check: {'OK' if len(meta_desc) <= 155 else 'EXCEEDED'}")

# 3. 6-gram overlap check against original source
with open('/opt/hermes/profiles/archie/cache/web/www.searates.com-904b8cc18b.md', 'r') as f:
    orig_text = f.read()

def clean_words(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text.lower())
    return [w for w in text.split() if w]

orig_words = clean_words(orig_text)
body_words = clean_words(body)

orig_6grams = set()
for i in range(len(orig_words) - 5):
    orig_6grams.add(tuple(orig_words[i:i+6]))

overlaps = []
for i in range(len(body_words) - 5):
    gram = tuple(body_words[i:i+6])
    if gram in orig_6grams:
        overlaps.append(" ".join(gram))

print(f"Total 6-gram overlaps count: {len(overlaps)}")
print("Overlaps list:")
for o in set(overlaps):
    print(" -", o)
