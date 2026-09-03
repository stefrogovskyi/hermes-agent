import json

with open('/opt/hermes/profiles/archie/.skills_prompt_snapshot.json') as f:
    data = json.load(f)

print("Type of data:", type(data))
if isinstance(data, dict):
    for k in data.keys():
        if 'avalanche' in k or 'copy' in k or 'blog' in k:
            print("Dict key:", k)
elif isinstance(data, list):
    for idx, item in enumerate(data):
        if isinstance(item, dict):
            for k, v in item.items():
                if 'avalanche' in str(v) or 'copywriting' in str(v):
                    print(f"List item {idx} key {k}: {v[:100] if isinstance(v, str) else v}")
