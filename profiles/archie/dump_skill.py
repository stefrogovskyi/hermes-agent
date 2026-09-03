import json

with open('/opt/hermes/profiles/archie/.skills_prompt_snapshot.json') as f:
    data = json.load(f)

skills = data.get('skills', {})
print("Skills type:", type(skills))
if isinstance(skills, dict):
    for k, v in skills.items():
        if 'avalanche' in k.lower() or 'avalanche' in str(v).lower():
            print("Found in dict key:", k)
            with open('avalanche_skill_dump.txt', 'w') as out:
                out.write(json.dumps(v, indent=2, ensure_ascii=False))
elif isinstance(skills, list):
    for item in skills:
        if 'avalanche' in str(item).lower():
            print("Found in list item:", item.get('name') or item.get('skill_name'))
            with open('avalanche_skill_dump.txt', 'w') as out:
                out.write(json.dumps(item, indent=2, ensure_ascii=False))
