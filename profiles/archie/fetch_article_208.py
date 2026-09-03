import urllib.request
from bs4 import BeautifulSoup
import re

url = "https://www.searates.com/blog/post/how-to-prevent-freight-shipping-delays-effective-strategies-for-reliable-delivery"

req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
)

try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "header", "footer", "nav"]):
            script.extract()
            
        # Extract title
        title_tag = soup.find('h1')
        title = title_tag.get_text(strip=True) if title_tag else "No H1 title"
        print(f"TITLE: {title}\n")
        
        # Extract body text
        body = soup.find('article') or soup.find('main') or soup.find('div', class_=re.compile('post|content|blog', re.I)) or soup.body
        
        if body:
            # Get text or paragraphs/headings
            text = body.get_text(separator='\n', strip=True)
            print("=== CONTENT ===")
            print(text)
            with open('/opt/hermes/profiles/archie/orig_article_208.txt', 'w') as f:
                f.write(f"Title: {title}\n\n{text}")
        else:
            print("No body content found.")
except Exception as e:
    print(f"Error: {e}")
