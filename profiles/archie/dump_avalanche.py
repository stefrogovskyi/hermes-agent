import json

with open('/opt/hermes/profiles/archie/.skills_prompt_snapshot.json') as f:
    data = json.load(f)

skills = data.get('skills', [])
for s in skills:
    if isinstance(s, dict):
        if 'avalanche-copywriting' in s.get('skill_name', '') or 'avalanche-copywriting' in s.get('name', '') or 'avalanche' in str(s.get('path', '')):
            print("FOUND SKILL:")
            print(s.get('content', s.get('body', s)))
