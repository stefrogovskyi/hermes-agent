import json

data = json.load(open('.skills_prompt_snapshot.json'))
skills = data.get('skills', {})
for s in skills:
    if 'avalanche' in s.get('name', ''):
        print("Skill Name:", s.get('name'))
        print("Body:", s.get('body'))
