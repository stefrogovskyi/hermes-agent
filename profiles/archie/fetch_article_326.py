import urllib.request
import re
from bs4 import BeautifulSoup

url = "https://www.searates.com/blog/post/searates-updates-week-43-2024"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Try finding main content
        article = soup.find('article') or soup.find('div', class_=re.compile(r'post|content|blog', re.I))
        if article:
            text = article.get_text(separator='\n', strip=True)
        else:
            text = soup.get_text(separator='\n', strip=True)
        
        print("Fetched text length:", len(text))
        with open("article_326_raw.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print("Saved raw text.")
except Exception as e:
    print("Error:", e)
