from bs4 import BeautifulSoup
import json
import re

with open("full_page.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Check script tags for JSON-LD or initial state data
scripts = soup.find_all('script')
for s in scripts:
    if s.string and ('articleBody' in s.string or 'SeaRates Updates' in s.string):
        print("Found matching script tag!")
        print(s.string[:500])

# Find all headings and paragraphs in body
elements = []
for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'ul', 'ol', 'li', 'div']):
    # check if class contains post, text, blog, description, etc.
    cls = " ".join(tag.get('class', []))
    id_ = tag.get('id', '')
    if any(k in cls.lower() or k in id_.lower() for k in ['post', 'blog', 'article', 'content', 'description', 'text']):
        # check text
        t = tag.get_text(separator=' ', strip=True)
        if len(t) > 50 and t not in elements:
            elements.append(f"[{cls} | {id_}] {t[:200]}")

print("Candidate elements:", len(elements))
for e in elements[:15]:
    print(e)
