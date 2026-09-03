import json, re

with open('draft.json') as f:
    data = json.load(f)

text = data['body_markdown']
sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip() and not s.startswith('#')]

print("Total sentences:", len(sentences))
for i, s in enumerate(sentences):
    for word in ['not', 'instead', 'rather', 'but']:
        if re.search(r'\b' + word + r'\b', s, re.IGNORECASE):
            print(f'Sentence {i}: {s}')
