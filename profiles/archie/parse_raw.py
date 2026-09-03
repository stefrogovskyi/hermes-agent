from bs4 import BeautifulSoup

with open("raw_page.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# Find scripts, json, or paragraphs
print("Paragraphs count:", len(soup.find_all('p')))
for p in soup.find_all('p'):
    print("P:", p.get_text(strip=True))

print("\nDivs with post or content:")
for div in soup.find_all(['div', 'section', 'article']):
    cls = " ".join(div.get('class', []))
    id_ = div.get('id', '')
    if any(k in cls.lower() or k in id_.lower() for k in ['post', 'content', 'body', 'article', 'text', 'entry']):
        txt = div.get_text(separator=' ', strip=True)
        if len(txt) > 100:
            print(f"[{cls} / {id_}] len={len(txt)}: {txt[:300]}...")
