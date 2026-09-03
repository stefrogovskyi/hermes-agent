import urllib.request
from bs4 import BeautifulSoup
import sys

url = "https://www.searates.com/blog/post/autonomous-trucks-in-2025-a-global-snapshot-of-deployment-use-cases-and-what-comes-next"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        title_el = soup.find('h1')
        title = title_el.get_text().strip() if title_el else "Autonomous trucks in 2025 a global snapshot of deployment use cases and what comes next"
        
        # Try finding post content container
        post_body = soup.find('div', class_='post-body') or soup.find('div', class_='blog-content') or soup.find('article') or soup.find('main')
        
        if not post_body:
            post_body = soup
            
        elements = post_body.find_all(['p', 'h2', 'h3', 'h4', 'ul', 'ol', 'li'])
        text_blocks = []
        for el in elements:
            # Avoid header/footer noise if possible
            txt = el.get_text().strip()
            if txt and len(txt) > 5:
                text_blocks.append(f"{el.name.upper()}: {txt}")
                
        print(f"TITLE: {title}")
        print("\n--- BODY TEXT ---")
        full_text = "\n\n".join([el.get_text().strip() for el in elements if el.get_text().strip()])
        print(full_text)
        
        with open("/opt/hermes/profiles/archie/original_article.txt", "w", encoding="utf-8") as f:
            f.write(f"Title: {title}\n\n{full_text}")
            
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
