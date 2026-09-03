from bs4 import BeautifulSoup

with open("/opt/hermes/profiles/archie/raw_page.html") as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

h1 = soup.find('h1')
if not h1:
    print("No H1 found")
    exit(1)

parent = h1.parent
blog_container = parent
while parent and parent.name not in ['body', 'html']:
    text = parent.get_text()
    if "What’s new for week 47" in text:
        blog_container = parent
        break
    parent = parent.parent

nodes = []
for child in blog_container.find_all(['h1', 'h2', 'h3', 'p', 'li']):
    if child.find_parents(['header', 'nav', 'footer']):
        continue
    txt = child.get_text(separator=' ', strip=True)
    if txt and txt not in nodes:
        if not any(k in txt.lower() for k in ['cookie', 'all rights reserved', 'privacy policy', 'terms of use']):
            nodes.append(f"{child.name.upper()}: {txt}")

clean_text = "\n\n".join(nodes)
print("=== COMPLETE ARTICLE SOURCE ===")
print(clean_text)

with open("/opt/hermes/profiles/archie/original_article_clean.txt", "w") as f:
    f.write(clean_text)
