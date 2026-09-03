import json

with open("/opt/hermes/profiles/archie/.skills_prompt_snapshot.json") as f:
    data = json.load(f)

for k in data.keys():
    print(k)
