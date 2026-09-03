import urllib.request
from bs4 import BeautifulSoup

url = "https://www.searates.com/blog/post/searates-updates-week-49-2024"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as response:
    html = response.read().decode('utf-8')

soup = BeautifulSoup(html, 'html.parser')

# Print all paragraphs, headers, lists
paragraphs = soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'li'])
content_lines = []
for p in paragraphs:
    t = p.get_text(strip=True)
    if t and len(t) > 3:
        content_lines.append(f"<{p.name}> {t}")

print("\n".join(content_lines[:100]))

with open("/opt/hermes/profiles/archie/extracted_content.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(content_lines))
