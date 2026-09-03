import urllib.request
import re
import json
from bs4 import BeautifulSoup

url = 'https://www.searates.com/blog/post/how-data-driven-reporting-improves-supply-chain-efficiency'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find article main content
        title = ""
        h1 = soup.find('h1')
        if h1:
            title = h1.get_text(strip=True)
            
        # Try finding post content container
        article_elem = soup.find('article') or soup.find('div', class_=re.compile(r'blog-post|post-content|article-content|blog-detail', re.I))
        
        if not article_elem:
            article_elem = soup.body
            
        text_blocks = []
        for elem in article_elem.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'ul', 'ol']):
            if elem.name in ['ul', 'ol']:
                for li in elem.find_all('li'):
                    text_blocks.append(f"- {li.get_text(strip=True)}")
            else:
                txt = elem.get_text(strip=True)
                if txt:
                    text_blocks.append(txt)
                    
        full_text = "\n\n".join(text_blocks)
        
        out = {
            "url": url,
            "title": title,
            "body": full_text
        }
        
        with open("/opt/hermes/profiles/archie/extracted_article.json", "w", encoding="utf-8") as f:
            json.dumps(out)
            f.write(json.dumps(out, ensure_ascii=False, indent=2))
            
        print("Successfully extracted article. Title:", title)
        print("Length of body:", len(full_text))

except Exception as e:
    print("Error fetching article:", e)
