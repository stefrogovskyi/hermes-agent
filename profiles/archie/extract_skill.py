import json

with open('/opt/hermes/profiles/archie/.skills_prompt_snapshot.json') as f:
    data = json.load(f)

for item in data.get('skills', []):
    if item.get('skill_name') == 'avalanche-copywriting' or item.get('name') == 'avalanche-copywriting':
        print("Item keys:", item.keys())
        for k, v in item.items():
            if isinstance(v, str) and len(v) > 100:
                print(f"Key {k} length {len(v)}")
                with open(f'avalanche_content_{k}.txt', 'w') as out:
                    out.write(v)
