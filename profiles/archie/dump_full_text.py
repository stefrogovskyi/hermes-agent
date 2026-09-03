from bs4 import BeautifulSoup

with open('/opt/hermes/profiles/archie/post_raw.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Print title
h1 = soup.find('h1')
print("TITLE:", h1.get_text(strip=True) if h1 else "")

# Find main content
# In SeaRates blog posts, text is usually in div.blog-post or div.post-content or similar
main_div = soup.find('div', class_='blog-post') or soup.find('div', class_='post-body') or soup.body

# Let's extract all structured content under article/main
for elem in main_div.find_all(['h2', 'h3', 'p', 'ul', 'ol']):
    # skip menu items
    text = elem.get_text(separator=' ', strip=True)
    if 'ToolsServicesReferences' in text or 'Choose language' in text or 'RECOMMENDED POSTS' in text:
        continue
    if len(text) > 5:
        print(f"[{elem.name.upper()}] {text}")
