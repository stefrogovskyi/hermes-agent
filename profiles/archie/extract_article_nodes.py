import json
from bs4 import BeautifulSoup

with open("/opt/hermes/profiles/archie/original_article.json", "r", encoding="utf-8") as f:
    data = json.load(f)

html = data.get("raw_html", "")
soup = BeautifulSoup(html, 'html.parser')

# Find main content region: look for elements after H1 or in article body
h1 = soup.find('h1')
content_nodes = []
if h1:
    curr = h1.parent
    # find all p, h2, h3, ul, ol inside curr or subsequent siblings
    for el in curr.find_all(['p', 'h2', 'h3', 'h4', 'ul', 'ol', 'li']):
        t = el.get_text(" ", strip=True)
        if len(t) > 15:
            content_nodes.append(t)

print(f"Total nodes found: {len(content_nodes)}")
full_article_text = "\n\n".join(content_nodes)
print("\n--- SAMPLE CONTENT ---\n")
print(full_article_text[:2000])

with open("/opt/hermes/profiles/archie/extracted_original.txt", "w", encoding="utf-8") as f:
    f.write(full_article_text)
