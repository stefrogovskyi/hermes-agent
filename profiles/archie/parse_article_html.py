import urllib.request
from bs4 import BeautifulSoup

url = "https://www.searates.com/blog/post/october-2024-development-release-empowering-business-users"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as response:
    html = response.read().decode('utf-8')

soup = BeautifulSoup(html, 'html.parser')

# Let's find all H1, H2, H3, P, UL, OL tags inside body
body = soup.find('body')
content_elements = []

for elem in body.find_all(['h1', 'h2', 'h3', 'p', 'ul', 'ol']):
    # skip headers/footers/nav if inside them
    if elem.find_parent(['nav', 'header', 'footer']):
        continue
    txt = elem.get_text(separator=' ').strip()
    if txt and len(txt) > 2 and not txt.startswith('Categories') and not txt.startswith('All\n'):
        content_elements.append(txt)

full_article = '\n\n'.join(content_elements)
print("Extracted article length:", len(full_article))
print(full_article)

with open("/opt/hermes/profiles/archie/article_clean.txt", "w") as f:
    f.write(full_article)
