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

# Print all h1, h2, h3 and paragraphs
output = []
for el in soup.find_all(['h1', 'h2', 'h3', 'p', 'li']):
    txt = el.get_text().strip()
    if txt and len(txt) > 20: # skip short nav items
        output.append(f"<{el.name}>: {txt}")

clean_text = "\n\n".join(output)

with open('/opt/hermes/profiles/archie/article_188_body.txt', 'w') as f:
    f.write(clean_text)

print("Saved body. Total entries:", len(output))
