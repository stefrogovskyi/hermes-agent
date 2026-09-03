import json

with open("/opt/hermes/profiles/archie/extracted_original.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("TITLE:", data["title"])
print("--- FULL TEXT ---")
for i, item in enumerate(data["items"]):
    print(f"{i+1}. [{item['tag'].upper()}] {item['text']}")
