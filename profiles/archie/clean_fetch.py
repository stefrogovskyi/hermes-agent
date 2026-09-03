import urllib.request
import json
from bs4 import BeautifulSoup

url = 'https://www.searates.com/blog/post/how-data-driven-reporting-improves-supply-chain-efficiency'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8')

soup = BeautifulSoup(html, 'html.parser')

h1 = soup.find('h1')
title = h1.get_text(strip=True) if h1 else ""

# Find main content block
# SeaRates blog post body usually sits inside a specific container or after h1
post_body = []
if h1:
    # grab all sibling or parent elements under the article container
    parent = h1.parent
    while parent and parent.name not in ['article', 'main', 'body'] and not ('container' in parent.get('class', [])):
        parent = parent.parent
    
    # Extract headers and paragraphs inside parent
    for elem in parent.find_all(['h2', 'h3', 'h4', 'p', 'ul', 'ol']):
        txt = elem.get_text(strip=True)
        if txt and not txt.startswith("Tools") and not txt.startswith("Services") and not txt.startswith("Logistics Explorer"):
            if elem.name in ['ul', 'ol']:
                for li in elem.find_all('li'):
                    post_body.append(f"- {li.get_text(strip=True)}")
            else:
                post_body.append(txt)

clean_text = "\n\n".join(post_body)

data = {
    "title": title,
    "url": url,
    "body": clean_text
}

with open("/opt/hermes/profiles/archie/clean_article.json", "w", encoding="utf-8") as f:
    json.dumps(data)
    f.write(json.dumps(data, ensure_ascii=False, indent=2))

print("Clean Title:", title)
print("Clean Text Length:", len(clean_text))
print("\nFirst 500 chars:\n", clean_text[:500])
