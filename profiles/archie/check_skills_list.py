import json

with open('/opt/hermes/profiles/archie/.skills_prompt_snapshot.json') as f:
    data = json.load(f)

skills = data.get('skills', [])
for item in skills:
    if isinstance(item, dict):
        print("Skill item:", item.get('name'), item.get('skill_name'), item.get('path'))
        if item.get('skill_name') == 'avalanche-copywriting' or item.get('name') == 'avalanche-copywriting':
            print("FOUND CONTENT:")
            print(json.dumps(item, ensure_ascii=False, indent=2))
