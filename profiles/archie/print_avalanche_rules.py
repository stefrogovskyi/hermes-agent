import json

with open('.skills_prompt_snapshot.json') as f:
    data = json.load(f)

for k, v in data.items():
    if 'avalanche' in str(k):
        print("=== KEY ===", k)
        if isinstance(v, list):
            for line in v:
                print(line)
        elif isinstance(v, dict):
            print(json.dumps(v, indent=2))
