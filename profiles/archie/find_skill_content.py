import json
import os

with open('/opt/hermes/profiles/archie/.skills_prompt_snapshot.json') as f:
    data = json.load(f)

print("Type of data:", type(data))
if isinstance(data, dict):
    print("Keys in snapshot:", list(data.keys()))
    skills = data.get('skills', [])
    for s in skills:
        print("Skill item keys:", list(s.keys()) if isinstance(s, dict) else type(s))
        if isinstance(s, dict) and 'avalanche' in str(s).lower():
            print("Avalanche item:", json.dumps(s, indent=2)[:500])

# Also search /opt/hermes or ~/.hermes for skill files
for root, dirs, files in os.walk('/opt/hermes'):
    for file in files:
        if 'avalanche' in file.lower() or 'copywriting' in file.lower():
            print("Found file:", os.path.join(root, file))
