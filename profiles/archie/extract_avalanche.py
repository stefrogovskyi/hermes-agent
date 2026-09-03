import json

with open('/opt/hermes/profiles/archie/.skills_prompt_snapshot.json') as f:
    data = json.load(f)

for k, v in data.items():
    if 'avalanche-copywriting' in k:
        print("KEY:", k)
        print("VALUE:", v)

