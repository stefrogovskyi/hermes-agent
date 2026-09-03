from bs4 import BeautifulSoup
import re

with open('/tmp/raw_article.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Find all paragraphs or content divs that contain actual article text
# Let's search for tags or specific classes
for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'ul', 'ol']):
    text = tag.get_text(strip=True)
    if len(text) > 30 and not any(nav_word in text.lower() for nav_word in ['cookie', 'copyright', 'searates.com', 'all rights reserved', 'use our real-time']):
        print(f"[{tag.name}] {text}")
