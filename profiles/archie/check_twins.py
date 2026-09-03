import json, re

with open('draft.json') as f:
    data = json.load(f)

text = data['body_markdown']
lines = text.split('\n')
text_lines = [l for l in lines if not l.startswith('#') and l.strip()]
plain_body = ' '.join(text_lines)

sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', plain_body) if s.strip()]

twins = []
for i in range(len(sentences) - 1):
    w1 = [w.lower().strip(',.!"\'()') for w in sentences[i].split()[:2]]
    w2 = [w.lower().strip(',.!"\'()') for w in sentences[i+1].split()[:2]]
    if len(w1) >= 2 and len(w2) >= 2 and w1 == w2:
        twins.append((sentences[i], sentences[i+1]))

print("Parallel twin sentences found:", len(twins))
for t1, t2 in twins:
    print("1:", t1)
    print("2:", t2)
