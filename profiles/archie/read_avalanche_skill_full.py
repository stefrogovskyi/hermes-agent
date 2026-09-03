import json

with open('/opt/hermes/profiles/archie/.skills_prompt_snapshot.json') as f:
    data = json.load(f)

skills = data.get('skills', [])
for item in skills:
    name = item.get('skill_name') or item.get('name') or item.get('frontmatter_name')
    if name and 'avalanche-copywriting' in name:
        print("KEYS:", item.keys())
        for k, v in item.items():
            print(f"=== {k} ===")
            print(str(v)[:2000])
