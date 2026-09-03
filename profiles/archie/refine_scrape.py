import urllib.request
from bs4 import BeautifulSoup
import json

url = "https://www.searates.com/blog/post/big-guide-how-to-use-ship-schedules-manage-shipments-by-points-vessels-and-ports"

req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
)

html = urllib.request.urlopen(req).read().decode('utf-8')
soup = BeautifulSoup(html, 'html.parser')

# Look for post content container
post_container = soup.find('div', class_=lambda c: c and 'post' in c) or \
                 soup.find('article') or \
                 soup.find('main')

title = ""
h1 = soup.find('h1')
if h1:
    title = h1.get_text(strip=True)

# Find all paragraphs, headings, list items inside post container or body
elements = []
if post_container:
    for tag in post_container.find_all(['p', 'h2', 'h3', 'h4', 'ul', 'ol']):
        txt = tag.get_text(" ", strip=True)
        if txt and len(txt) > 20:
            # exclude header/footer nav
            if not any(nav_word in txt.lower() for nav_word in ['logistics explorer', 'container tracking', 'ship schedules tool', 'sign in', 'privacy policy', 'terms of service', 'copyright']):
                elements.append(txt)

cleaned_text = "\n\n".join(elements)

print(f"Title: {title}")
print(f"Cleaned text length: {len(cleaned_text)}")
print("\nFirst 1000 chars:\n")
print(cleaned_text[:1000])

with open("/opt/hermes/profiles/archie/original_article.json", "w", encoding="utf-8") as f:
    json.dump({"title": title, "text": cleaned_text, "raw_html": html}, f, ensure_ascii=False, indent=2)
