import json

with open('draft.json') as f:
    data = json.load(f)

print(json.dumps(data, indent=2))
