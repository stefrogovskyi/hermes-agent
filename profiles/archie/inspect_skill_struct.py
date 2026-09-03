import json

data = json.load(open('.skills_prompt_snapshot.json'))
skills = data.get('skills')
print(type(skills))
if isinstance(skills, list) and len(skills) > 0:
    print(skills[0].keys() if isinstance(skills[0], dict) else type(skills[0]))
    print(json.dumps(skills[0], indent=2)[:500])
