import urllib.request
from bs4 import BeautifulSoup
import sys

url = 'https://www.searates.com/blog/post/the-future-of-shipping-embracing-smarter-workflows'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove nav, header, footer, scripts
        for tag in soup(['nav', 'header', 'footer', 'script', 'style']):
            tag.decompose()
            
        title = soup.find('h1')
        title_text = title.get_text(strip=True) if title else 'No H1 found'
        print(f"TITLE: {title_text}\n")
        
        # Find article or post container
        post_div = soup.find('div', class_='blog-post-content') or soup.find('div', class_='post-content') or soup.find('article') or soup
        
        text_elements = []
        for elem in post_div.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'li']):
            txt = elem.get_text(strip=True)
            if txt and len(txt) > 2:
                text_elements.append(f"<{elem.name}> {txt}")
                
        print("\n".join(text_elements))
except Exception as e:
    print(f"Error fetching article: {e}", file=sys.stderr)
