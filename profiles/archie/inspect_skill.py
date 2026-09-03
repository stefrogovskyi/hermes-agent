import json

with open("/opt/hermes/profiles/archie/.skills_prompt_snapshot.json") as f:
    data = json.load(f)

skills = data.get("skills", [])
for item in skills:
    s_str = json.dumps(item)
    if "avalanche" in s_str:
        print("KEYS:", item.keys() if isinstance(item, dict) else type(item))
        print("STRING REPRESENTATION:")
        print(s_str[:2000])
