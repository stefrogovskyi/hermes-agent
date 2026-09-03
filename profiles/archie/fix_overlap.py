import json

with open("/opt/hermes/profiles/archie/fixed_rewrite.json", "r", encoding="utf-8") as f:
    data = json.load(f)

body = data["body_markdown"]

# Replace the overlapping sentence
old_phrase = "Predictive route optimization offers predictive insights that help logistics teams prepare for upcoming conditions."
new_phrase = "Forecast tools give logistics teams advance visibility to adapt before changing transit conditions impact delivery schedules."

if old_phrase in body:
    body = body.replace(old_phrase, new_phrase)
    print("Replaced overlapping phrase successfully!")
else:
    print("Old phrase not found, searching similar pattern...")
    import re
    body = re.sub(r'Predictive route optimization offers predictive insights that help logistics teams prepare for upcoming conditions\.', new_phrase, body)

data["body_markdown"] = body

with open("/opt/hermes/profiles/archie/fixed_rewrite.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Updated fixed_rewrite.json")
