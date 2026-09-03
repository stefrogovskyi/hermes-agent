import json

data = json.load(open('.skills_prompt_snapshot.json'))
print("Keys:", list(data.keys()))
for k, v in data.items():
    if 'avalanche' in str(v):
        print("Found avalanche in key/val:", k)
