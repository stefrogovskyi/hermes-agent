import json

with open("/opt/hermes/profiles/archie/fixed_rewrite.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("=== TITLE ===")
print(data["title"])
print("\n=== META TITLE ===")
print(data["meta_title"])
print("\n=== META DESCRIPTION ===")
print(data["meta_description"])
print("\n=== BODY MARKDOWN ===")
print(data["body_markdown"])
