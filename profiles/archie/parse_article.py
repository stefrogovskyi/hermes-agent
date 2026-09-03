import urllib.request
from bs4 import BeautifulSoup

url = 'https://www.searates.com/blog/post/searates-updates-week-35-2024'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

with urllib.request.urlopen(req) as response:
    html = response.read().decode('utf-8')

soup = BeautifulSoup(html, 'html.parser')

# Let's inspect headings, paragraphs, and post-specific tags
article_tag = soup.find('article') or soup.find('main') or soup.find('div', class_=lambda c: c and 'blog' in c and 'detail' in c)

if not article_tag:
    # Look for headers like h1, h2, h3, p
    print("No article tag found, printing all h1, h2, h3, p...")
    for elem in soup.find_all(['h1', 'h2', 'h3', 'p', 'li']):
        text = elem.get_text(strip=True)
        if text:
            print(f"{elem.name}: {text}")
else:
    for elem in article_tag.find_all(['h1', 'h2', 'h3', 'p', 'li']):
        text = elem.get_text(strip=True)
        if text:
            print(f"{elem.name}: {text}")
