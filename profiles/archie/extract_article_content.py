from bs4 import BeautifulSoup
import re

with open('/opt/hermes/profiles/archie/page.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Let's find article text or main container
# SeaRates blog post text usually resides in div with post content or blog-post classes
content_divs = soup.find_all('div', class_=re.compile(r'blog|post|article|content', re.I))

# Alternatively, find h1, h2, h3 and p tags inside the main section
main_sec = soup.find('article') or soup.find('main') or soup.body

paragraphs = []
for el in main_sec.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'li']):
    txt = el.get_text().strip()
    # Filter out footer/nav links
    if not txt:
        continue
    if any(ignore in txt.lower() for ignore in ['cookie', 'copyright', 'privacy policy', 'terms of service', 'logistics explorer', 'container tracking', 'all rights reserved']):
        continue
    paragraphs.append((el.name, txt))

# Deduplicate consecutive identical texts
cleaned = []
prev = None
for tag, txt in paragraphs:
    if txt != prev:
        cleaned.append(f"[{tag.upper()}] {txt}" if tag.startswith('h') else txt)
        prev = txt

full_article = "\n\n".join(cleaned)

with open('/opt/hermes/profiles/archie/original_article.txt', 'w', encoding='utf-8') as f:
    f.write(full_article)

print(f"Extracted article length: {len(full_article)} chars.")
print("\n--- EXTRACTED CONTENT ---")
print(full_article[:2500])
