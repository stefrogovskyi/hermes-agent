import json, re

with open("draft.json") as f:
    data = json.load(f)

text = f"{data['title']} {data['meta_title']} {data['meta_description']} {data['body']}".lower()

patterns = ["not ", "rather than", "instead of", "but "]
for p in patterns:
    matches = re.findall(p, text)
    print(f"Pattern '{p}': {len(matches)} matches")

for line in text.split('\n'):
    if any(p in line for p in ["not", "rather", "instead", "but"]):
        print(f"Line: {line}")
