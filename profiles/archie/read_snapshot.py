import json

with open("/opt/hermes/profiles/archie/.skills_prompt_snapshot.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data.get("skills", []):
    if "avalanche-copywriting" in str(item):
        print("Type:", type(item))
        if isinstance(item, dict):
            print("Keys:", list(item.keys()))
            print("Name:", item.get("skill_name") or item.get("name") or item.get("path"))
            print("Content sample:", str(item.get("content") or item.get("body") or item)[:1000])
