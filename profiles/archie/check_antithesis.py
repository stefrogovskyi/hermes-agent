import json, re

with open('draft.json') as f:
    data = json.load(f)

text = data['body_markdown']
sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip() and not s.startswith('#')]

for i, s in enumerate(sentences):
    if re.search(r'^\s*(where|while)\b', s, re.IGNORECASE):
        print(f"Sentence {i}: {s}")
