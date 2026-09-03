import json

with open("result.json", "r", encoding="utf-8") as f:
    d = json.load(f)

print("=== TITLE ===")
print(d["title"])
print("=== META TITLE ===")
print(d["meta_title"])
print("=== META DESC ===")
print(d["meta_description"])
print("=== BODY ===")
print(d["body"])
