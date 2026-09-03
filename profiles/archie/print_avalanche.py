import json

with open('/opt/hermes/profiles/archie/.skills_prompt_snapshot.json') as f:
    data = json.load(f)

for sk in data.get('skills', []):
    if sk.get('skill_name') == 'avalanche-copywriting':
        print(json.dumps(sk, indent=2, ensure_ascii=False))
