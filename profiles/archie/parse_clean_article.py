import urllib.request
from bs4 import BeautifulSoup
import re

url = 'https://www.searates.com/blog/post/advanced-transport-management-with-logistics-map-virtual-office'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

with urllib.request.urlopen(req) as response:
    html = response.read().decode('utf-8')

soup = BeautifulSoup(html, 'html.parser')

# Find the main container or article
# On SeaRates blog, article is usually inside a specific blog container
content_div = soup.find('div', class_=re.compile(r'post|article|content|blog', re.I))

# Let's inspect paragraphs and headings in the main body
lines = []
for el in soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'li']):
    txt = el.get_text(strip=True)
    if txt and len(txt) > 5:
        # Filter out common nav items
        if txt in ["All", "Shipping & Logistics", "Cases", "Offers", "Ports & Routes", "Innovations", "Education", "Trade & Markets", "Shipping insights", "Events", "Archive", "Categories", "Like", "Share", "Subscribe"]:
            continue
        lines.append(txt)

# Deduplicate consecutive duplicates while preserving order
clean_lines = []
for line in lines:
    if not clean_lines or clean_lines[-1] != line:
        clean_lines.append(line)

full_article_text = "\n\n".join(clean_lines)

print("Full Extracted Article Length:", len(full_article_text))
print("\n--- EXTRACTED TEXT START ---")
print(full_article_text[:3000])
print("...\n--- EXTRACTED TEXT END ---")

with open('/opt/hermes/profiles/archie/clean_original_article.txt', 'w', encoding='utf-8') as f:
    f.write(full_article_text)
