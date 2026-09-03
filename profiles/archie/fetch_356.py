import urllib.request
import re
from bs4 import BeautifulSoup

url = 'https://www.searates.com/blog/post/searates-updates-week-34-2024'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
html = urllib.request.urlopen(req).read().decode('utf-8')

soup = BeautifulSoup(html, 'html.parser')
title = soup.find('h1').get_text(strip=True) if soup.find('h1') else 'Searates updates week 34 2024'
print('TITLE:', title)

# Try to locate the main body
main_div = soup.find('div', class_=re.compile(r'blog-single-main-content|blog-content|post-content'))
if not main_div:
    main_div = soup.find('main') or soup.body

# Save full HTML and extracted text
with open('/opt/hermes/profiles/archie/orig_article_356_raw.html', 'w', encoding='utf-8') as f:
    f.write(html)

paragraphs = []
for el in main_div.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'li']):
    txt = el.get_text(strip=True)
    if txt and len(txt) > 5:
        paragraphs.append(txt)

full_text = "\n\n".join(paragraphs)
print("EXTRACTED LENGTH:", len(full_text))

with open('/opt/hermes/profiles/archie/orig_article_356.txt', 'w', encoding='utf-8') as f:
    f.write(full_text)

print("\n--- SAMPLE CONTENT ---")
print(full_text[:2000])
