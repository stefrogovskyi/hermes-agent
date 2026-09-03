import json
from bs4 import BeautifulSoup

with open("/opt/hermes/profiles/archie/original_article.json", "r", encoding="utf-8") as f:
    data = json.load(f)

html = data.get("raw_html", "")
soup = BeautifulSoup(html, 'html.parser')

all_tags = soup.find_all(['h1', 'h2', 'h3', 'p', 'li'])
print(f"Total tags: {len(all_tags)}")
for t in all_tags[:25]:
    text = t.get_text(" ", strip=True)
    if len(text) > 10:
        print(f"[{t.name}] {text[:100]}")
