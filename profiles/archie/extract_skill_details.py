import json
with open('.skills_prompt_snapshot.json') as f:
    data = json.load(f)
for k, v in data.items():
    if 'avalanche' in str(k):
        print("FOUND KEY:", k)
        print("="*40)
        print(v)
