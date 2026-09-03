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

# Find all elements after H1 inside the main body
content_elements = []

# Get the container holding H1
current = h1
# Move up to container level if needed, or find siblings/children
parent = h1.parent

# Let's collect h1, h2, h3, p, li, ul, ol under the main post wrapper
post_parts = []
# Find all elements in document that come after H1 in DOM order
for elem in h1.find_all_next(['h2', 'h3', 'h4', 'p', 'ul', 'ol']):
    # Stop if we hit footer or comments or related posts
    classes = " ".join(elem.get('class', []))
    id_attr = elem.get('id', '')
    if 'footer' in classes or 'related' in classes or 'comment' in classes or 'sidebar' in classes:
        break
        
    if elem.name in ['ul', 'ol']:
        items = [f"- {li.get_text(strip=True)}" for li in elem.find_all('li') if li.get_text(strip=True)]
        if items:
            post_parts.append("\n".join(items))
    elif elem.name in ['h2', 'h3', 'h4']:
        txt = elem.get_text(strip=True)
        if txt and not txt.startswith("Related") and not txt.startswith("Leave a"):
            post_parts.append(f"\n## {txt}\n")
    elif elem.name == 'p':
        txt = elem.get_text(strip=True)
        # check if it's social share or copyright
        if txt and not txt.startswith("Share") and not txt.startswith("©") and not txt.startswith("SeaRates"):
            post_parts.append(txt)

article_body = "\n\n".join(post_parts)

result = {
    "title": title,
    "url": url,
    "language": "English",
    "body": article_body
}

with open("/opt/hermes/profiles/archie/extracted_clean_article.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("Title:", title)
print("Total characters:", len(article_body))
print("\nArticle content sample:\n")
print(article_body[:1000])
