import urllib.request
import re
from bs4 import BeautifulSoup

url = "https://www.searates.com/blog/post/october-2024-development-release-empowering-business-users"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.extract()
            
        text = soup.get_text(separator='\n')
        # Clean up empty lines
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        print("=== ARTICLE TITLE ===")
        title = soup.find('h1')
        print(title.text if title else "No H1 found")
        
        print("\n=== ARTICLE BODY ===")
        print(text[:4000])
        
        with open("/opt/hermes/profiles/archie/original_article.txt", "w") as f:
            f.write(text)
except Exception as e:
    print("Error:", e)
