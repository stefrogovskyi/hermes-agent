import urllib.request
import re
from bs4 import BeautifulSoup

url = "https://www.searates.com/blog/post/full-searates-guide-cargo-vs-freight-explore-differences-benefits"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove nav, header, footer, scripts, styles
        for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'form', 'iframe']):
            tag.decompose()
            
        # Find post main body
        body_container = soup.find('div', class_=re.compile(r'post|content|blog|article', re.I)) or soup.find('main') or soup.body
        
        paragraphs = []
        for el in body_container.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'li']):
            txt = el.get_text(strip=True)
            if txt and len(txt) > 2:
                paragraphs.append(txt)
                
        text_content = "\n\n".join(paragraphs)
        
        with open("/opt/hermes/profiles/archie/article_329_clean.txt", "w", encoding="utf-8") as f:
            f.write(text_content)
            
        print(f"Successfully extracted {len(text_content)} characters.")
        print("First 500 chars:\n", text_content[:500])

except Exception as e:
    print("Error fetching URL:", e)
