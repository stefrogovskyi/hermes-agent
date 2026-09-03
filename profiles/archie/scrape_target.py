import json
import urllib.request
from bs4 import BeautifulSoup

url = 'https://www.searates.com/blog/post/trump-tariffs-in-april-2025-new-era-of-trade-war-risks-for-the-global-supply-chain'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    # Target blog container or main content
    blog_body = soup.find('div', class_='blog-post') or soup.find('article') or soup.find('div', id='blog-content') or soup.find('body')
    
    title = soup.find('h1').get_text().strip() if soup.find('h1') else 'Trump tariffs in april 2025 new era of trade war risks for the global supply chain'
    
    # Extract structural elements
    elements = []
    for el in blog_body.find_all(['h1', 'h2', 'h3', 'p', 'ul', 'ol', 'li']):
        text = el.get_text().strip()
        if text and text not in elements:
            elements.append(text)
            
    full_text = "\n\n".join(elements)
    
    data = {
        "url": url,
        "title": title,
        "full_text": full_text,
        "elements": elements
    }
    
    with open("extracted_original.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    with open("extracted_original_raw.txt", "w", encoding="utf-8") as f:
        f.write(f"Title: {title}\n\n{full_text}")
        
    print(f"Scraped successfully. Title: {title}. Length: {len(full_text)} chars.")
except Exception as e:
    print(f"Error scraping: {e}")
