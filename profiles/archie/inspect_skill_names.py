import json

data = json.load(open('.skills_prompt_snapshot.json'))
skills = data.get('skills', [])
if isinstance(skills, list):
    for s in skills:
        print(s.get('name'))
elif isinstance(skills, dict):
    for k in skills:
        print(k)
