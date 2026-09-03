import urllib.request
import re
from bs4 import BeautifulSoup

url = "https://www.searates.com/blog/post/sustainability-driven-innovations-in-ro-ro-shipping"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove scripts, styles
        for s in soup(['script', 'style', 'nav', 'footer', 'header']):
            s.decompose()
            
        # Try finding main content or post content
        post_body = soup.find('div', class_=re.compile('post|article|content|blog', re.I))
        if not post_body:
            post_body = soup.body
            
        text = post_body.get_text(separator='\n') if post_body else soup.get_text(separator='\n')
        
        # Clean up lines
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        clean_text = '\n'.join(lines)
        
        print("LENGTH:", len(clean_text))
        print("PREVIEW:\n", clean_text[:1000])
        
        with open("raw_extracted.txt", "w", encoding="utf-8") as f:
            f.write(clean_text)
            
except Exception as e:
    print("ERROR:", e)
