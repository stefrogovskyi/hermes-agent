import re

with open("/opt/hermes/profiles/archie/draft_article.md", "r", encoding="utf-8") as f:
    text = f.read()

body_start = text.find("# Article Content")
body = text[body_start + len("# Article Content"):].strip()

sections = re.split(r'\n(?=## )', body)
for s in sections:
    header = s.split('\n')[0]
    words = len(s.split())
    print(f"{header[:40]}: {words} words")

print(f"TOTAL BODY WORDS: {len(body.split())}")
