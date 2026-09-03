import json, re
with open('candidate.json') as f:
    data = json.load(f)
body = data['body_markdown']
sentences = re.split(r'[.!?]\s+', body)
ing_starters = [s for s in sentences if re.match(r'^\s*[*#-]*\s*[A-Z][a-z]+ing\b', s)]
for s in ing_starters:
    print('-', s)
