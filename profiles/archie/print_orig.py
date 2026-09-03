import json

with open("article_original.json", "r", encoding="utf-8") as f:
    data = json.load(f)

text = data["content"]
print("=== FULL ARTICLE ORIGINAL TEXT ===")
print(text)
