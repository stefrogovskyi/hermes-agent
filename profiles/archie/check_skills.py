import json

with open('/opt/hermes/profiles/archie/.skills_prompt_snapshot.json') as f:
    data = json.load(f)

skills = data.get('skills', {})
for k in skills.keys():
    print(k)
