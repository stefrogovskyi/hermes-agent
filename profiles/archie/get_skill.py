import json

with open('/opt/hermes/profiles/archie/.skills_prompt_snapshot.json') as f:
    data = json.load(f)

for k, v in data.items():
    if isinstance(v, dict):
        for sk_path, content in v.items():
            if 'avalanche-copywriting' in sk_path:
                print('TYPE:', type(content))
                print('CONTENT:', content)
