import urllib.request
from bs4 import BeautifulSoup

url = "https://www.searates.com/blog/post/searates-updates-week-42-2024"
req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
)

with urllib.request.urlopen(req) as response:
    html = response.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

# Let's inspect paragraphs and headings
paragraphs = []
for p in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'li']):
    txt = p.get_text().strip()
    if txt and len(txt) > 5:
        paragraphs.append(txt)

full_text = '\n\n'.join(paragraphs)

# Find where "Sophia Shkuro" or "What’s new for week 42" starts
pos = full_text.find("What’s new for week 42")
if pos != -1:
    content = full_text[pos:]
else:
    pos2 = full_text.find("Your ongoing assistance")
    if pos2 != -1:
        content = full_text[pos2:]
    else:
        content = full_text

# Truncate at end footer
end_pos = content.find("Subscribe to our channel")
if end_pos != -1:
    content = content[:end_pos]

end_pos2 = content.find("Related posts")
if end_pos2 != -1:
    content = content[:end_pos2]

print("=== ARTICLE FULL TEXT ===")
print(content)

with open("article_328_clean.txt", "w", encoding="utf-8") as f:
    f.write("Title: SeaRates updates week 42 2024\n")
    f.write(f"URL: {url}\n\n")
    f.write(content)
