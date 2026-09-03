import json

with open('.skills_prompt_snapshot.json') as f:
    data = json.load(f)

for skill in data.get('skills', []):
    print("Skill:", skill.get('name') or skill.get('skill_name'))
    if 'avalanche' in str(skill).lower():
        print("Found avalanche!")
        print(json.dumps(skill, ensure_ascii=False, indent=2))
