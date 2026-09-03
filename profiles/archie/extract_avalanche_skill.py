import json

with open('/opt/hermes/profiles/archie/.skills_prompt_snapshot.json') as f:
    data = json.load(f)

for k, v in data.items():
    if 'avalanche-copywriting' in k:
        print(f"=== KEY: {k} ===")
        content = "".join(v) if isinstance(v, list) else str(v)
        print(content)
