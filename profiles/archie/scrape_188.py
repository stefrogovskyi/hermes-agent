import urllib.request
from bs4 import BeautifulSoup
import re

url = "https://www.searates.com/blog/post/mega-ships-comparison-ultra-deepwater-vs-ultra-large-vessels-ocean-depth-or-trade-scale"

req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
)

try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Save title
        title = soup.title.string if soup.title else "No title"
        print("TITLE:", title)
        
        # Remove script and style elements
        for script in soup(["script", "style", "header", "footer", "nav"]):
            script.extract()
            
        # Get text
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        with open('/opt/hermes/profiles/archie/article_188_original.txt', 'w') as f:
            f.write(f"Title: {title}\n\nURL: {url}\n\nHTML Content / Cleaned Text:\n{text}")
            
        print("Successfully scraped article! Length:", len(text))
except Exception as e:
    print("Scraping error:", e)
