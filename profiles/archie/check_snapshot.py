import json

data = json.load(open('.skills_prompt_snapshot.json'))
for key, val in data.items():
    if 'avalanche-copywriting' in key:
        print("KEY:", key)
        if isinstance(val, dict):
            print(val.get('description', ''))
            print(val.get('instructions', ''))
        elif isinstance(val, list):
            for item in val:
                if isinstance(item, dict):
                    print(item.get('content', '')[:2000])
