import urllib.request
import json
from bs4 import BeautifulSoup

url = 'https://www.searates.com/blog/post/how-data-driven-reporting-improves-supply-chain-efficiency'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8')

soup = BeautifulSoup(html, 'html.parser')

# Let's inspect all tags and text
h1 = soup.find('h1')
print("H1:", h1.get_text(strip=True) if h1 else None)

# Print all H2, H3, P tags on page
elems = soup.find_all(['h1', 'h2', 'h3', 'p', 'li'])
clean_lines = []
for e in elems:
    txt = e.get_text(strip=True)
    if txt and len(txt) > 20: # skip menu items
        clean_lines.append(f"<{e.name}> {txt}")

print("\nSample lines (total " + str(len(clean_lines)) + "):")
for line in clean_lines[:30]:
    print(line)

