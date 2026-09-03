import json

data = json.load(open('.skills_prompt_snapshot.json'))
print(type(data))
if isinstance(data, dict):
    print("Keys:", list(data.keys())[:20])
elif isinstance(data, list):
    print("Length:", len(data))
    for item in data:
        if isinstance(item, dict) and ('avalanche' in str(item)):
            print("Found item:", item.get('name'), item.get('skill_name'))
