import json

with open("article_final.json", "r", encoding="utf-8") as f:
    d = json.load(f)

print(d["body"])
