import json

with open('.skills_prompt_snapshot.json') as f:
    data = json.load(f)

print("Keys:", list(data.keys()))
for k, v in data.items():
    print(k, type(v))
