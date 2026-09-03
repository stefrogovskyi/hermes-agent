import urllib.request
from bs4 import BeautifulSoup
import re

url = 'https://www.searates.com/blog/post/searates-updates-week-44-2024'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8')

soup = BeautifulSoup(html, 'html.parser')

# Find main content container
# SeaRates blog posts usually have specific structure
main = soup.find('main') or soup.find('div', class_=re.compile(r'blog|post|article', re.I)) or soup

# Let's clean up navigation, header, footer, comments, related posts
for elem in soup.find_all(['header', 'footer', 'nav', 'script', 'style', 'noscript']):
    elem.extract()

# Find article text or specific blog body
text_blocks = []
for p in soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'li']):
    t = p.get_text().strip()
    if t and len(t) > 3:
        # filter out repetitive header/footer items if any
        if "Logistics Explorer" in t or "Tracking System" in t or "Request an IT quote" in t:
            continue
        text_blocks.append(t)

clean_text = '\n\n'.join(text_blocks)
print("Extracted article text:\n", clean_text)

with open('original_article_clean.txt', 'w') as f:
    f.write(clean_text)
