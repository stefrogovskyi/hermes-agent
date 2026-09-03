import urllib.request
import re
from bs4 import BeautifulSoup
import json

url = "https://www.searates.com/blog/post/how-to-future-proof-your-logistics-career"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')
        
        title_el = soup.find('h1')
        title = title_el.get_text().strip() if title_el else "How to future proof your logistics career"
        
        main = soup.find('div', class_=re.compile(r'blog-single-main-content|blog-post|content'))
        if not main:
            main = soup.body
        
        elements = main.find_all(['p', 'h2', 'h3', 'h4', 'ul', 'ol', 'li'])
        extracted = []
        for el in elements:
            txt = el.get_text().strip()
            if len(txt) > 15 and "SeaRates.com" not in txt and "All rights reserved" not in txt:
                extracted.append(txt)
                
        full_text = "\n\n".join(extracted)
        
        print(f"Title: {title}")
        print(f"Extracted Length: {len(full_text)} chars")
        print("\nFirst 1000 chars:\n", full_text[:1000])
        
        with open("/opt/hermes/profiles/archie/original_article.txt", "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n{full_text}")
            
except Exception as e:
    print(f"Error fetching article: {e}")
