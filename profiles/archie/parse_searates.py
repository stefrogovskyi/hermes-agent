import urllib.request
from bs4 import BeautifulSoup

url = "https://www.searates.com/blog/post/sil-barcelona-2025-conference-summary"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
html = urllib.request.urlopen(req).read().decode('utf-8')

soup = BeautifulSoup(html, 'html.parser')

print("H1 tags:", [h.get_text(strip=True) for h in soup.find_all('h1')])
print("H2 tags:", [h.get_text(strip=True) for h in soup.find_all('h2')])

# Look for paragraphs or post content
paragraphs = [p.get_text(strip=True) for p in soup.find_all('p') if p.get_text(strip=True)]
print(f"Found {len(paragraphs)} paragraphs:")
for i, p in enumerate(paragraphs):
    print(f"[{i}] {p}")

