import urllib.request
import re
from bs4 import BeautifulSoup

url = "https://www.searates.com/blog/post/how-to-future-proof-your-logistics-career"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

with urllib.request.urlopen(req, timeout=15) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

soup = BeautifulSoup(html, 'html.parser')

h1_el = soup.find('h1')
h1_text = h1_el.get_text().strip() if h1_el else "How to Future-Proof Your Logistics Career"

content_div = soup.find('div', class_='blog-single-main-content')

if not content_div:
    print("Error: blog-single-main-content div not found")
else:
    # Clean up tags or extract structured paragraphs and headings
    blocks = []
    for tag in content_div.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'ul', 'ol']):
        txt = tag.get_text().strip()
        # Filter out social sharing or author metadata if needed
        if txt and not txt.startswith("Share") and not txt.startswith("By SeaRates"):
            blocks.append(txt)
            
    full_article = "\n\n".join(blocks)
    print(f"H1 Title: {h1_text}")
    print(f"Extracted article length: {len(full_article)} chars")
    print("\n--- FULL ARTICLE TEXT ---")
    print(full_article)
    
    with open("/opt/hermes/profiles/archie/original_article.txt", "w", encoding="utf-8") as f:
        f.write(f"# {h1_text}\n\n{full_article}")
