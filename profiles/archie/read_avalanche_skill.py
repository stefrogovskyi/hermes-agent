import json

with open('/opt/hermes/profiles/archie/.skills_prompt_snapshot.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

skills = data.get('skills', {})
print("Skills keys type:", type(skills))
if isinstance(skills, dict):
    for k in skills:
        if 'avalanche' in k or 'copywriting' in k:
            print("FOUND SKILL KEY:", k)
            print("CONTENT:\n", str(skills[k])[:2000])
elif isinstance(skills, list):
    for item in skills:
        if 'avalanche' in str(item):
            print("FOUND IN SKILL LIST:", str(item)[:1000])
