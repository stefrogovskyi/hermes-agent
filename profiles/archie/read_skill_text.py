import json

with open('/opt/hermes/profiles/archie/.skills_prompt_snapshot.json') as f:
    data = json.load(f)

for k, v in data.items():
    if 'avalanche-copywriting' in str(k):
        print("KEY:", k)
        print("CONTENT:")
        if isinstance(v, dict):
            print(json.dumps(v, ensure_ascii=False, indent=2)[:3000])
        else:
            print(str(v)[:3000])
