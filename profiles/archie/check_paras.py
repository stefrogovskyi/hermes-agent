import json, re

with open('draft.json') as f:
    data = json.load(f)

paras = [p.strip() for p in data['body_markdown'].split('\n\n') if p.strip()]

for i, p in enumerate(paras):
    if p.startswith('#'):
        print(f"Heading: {p}")
    else:
        s_count = len([s for s in re.split(r'(?<=[.!?])\s+', p) if s.strip()])
        print(f"Para {i} ({s_count} sentences): {p[:50]}...")
