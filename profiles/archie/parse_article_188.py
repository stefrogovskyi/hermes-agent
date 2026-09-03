import urllib.request
from bs4 import BeautifulSoup

url = "https://www.searates.com/blog/post/mega-ships-comparison-ultra-deepwater-vs-ultra-large-vessels-ocean-depth-or-trade-scale"

req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
)

with urllib.request.urlopen(req) as response:
    html = response.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    
    # Try finding main article container
    article = soup.find('article') or soup.find('div', class_=lambda c: c and ('post' in c or 'blog' in c or 'content' in c))
    
    if article:
        content = article.get_text('\n', strip=True)
    else:
        content = soup.get_text('\n', strip=True)

with open('/opt/hermes/profiles/archie/article_188_clean.txt', 'w') as f:
    f.write(content)

print("Saved clean content. Lines:", len(content.splitlines()))
