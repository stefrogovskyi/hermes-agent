from bs4 import BeautifulSoup
import re

with open("/opt/hermes/profiles/archie/raw_page.html") as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Look for blog post text container
# In SeaRates blog posts, content is often inside specific div classes
content_div = soup.find('div', class_=re.compile(r'post|article|content|entry', re.I))

# Let's extract paragraphs, headers, list items
paragraphs = []
for el in soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'li']):
    txt = el.get_text(strip=True)
    if txt and len(txt) > 3:
        # Avoid navigation/footer links
        if not any(banned in txt.lower() for banned in ['cookie', 'all rights reserved', 'privacy policy', 'terms of use', 'searates.com']):
            paragraphs.append(txt)

full_text = "\n\n".join(paragraphs)
print("Extracted paragraph count:", len(paragraphs))
print("Extracted text length:", len(full_text))
print("--- PREVIEW ---")
print(full_text[:3000])

with open("/opt/hermes/profiles/archie/extracted_article.txt", "w") as f:
    f.write(full_text)
