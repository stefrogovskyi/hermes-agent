from bs4 import BeautifulSoup

with open("/opt/hermes/profiles/archie/raw_page.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Find all paragraphs or specific blog content div
for tag in soup.find_all(['nav', 'header', 'footer', 'aside', 'script', 'style']):
    tag.decompose()

# Look for post content
post_div = soup.find('div', class_='blog-post') or soup.find('div', class_='post-content') or soup.find('div', class_='entry-content') or soup.find('main')

if not post_div:
    print("Post div not found directly, looking at all H1/H2/H3 and P tags in body")
    post_div = soup.body

lines = []
for el in post_div.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'li']):
    t = el.get_text(strip=True)
    if t and len(t) > 10:
        lines.append(f"{el.name.upper()}: {t}")

print("Total elements:", len(lines))
with open("/opt/hermes/profiles/archie/extracted_lines.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("Saved extracted_lines.txt")
print("\n".join(lines[:30]))
