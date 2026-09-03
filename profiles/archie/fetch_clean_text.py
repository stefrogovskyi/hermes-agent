import urllib.request
from bs4 import BeautifulSoup
import re

url = "https://www.searates.com/blog/post/tpm-2025-conference-summary"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as response:
    html = response.read().decode('utf-8')

soup = BeautifulSoup(html, 'html.parser')

# Find the div or article containing the blog post
# Let's inspect class names or look for the header/content
post_body = None
for div in soup.find_all(['div', 'article', 'section']):
    # check if title "TPM 2025" or similar is inside
    text = div.get_text()
    if "TPM 2025" in text or "Trans-Pacific Maritime" in text or "Long Beach" in text:
        # Check if it contains paragraphs
        ps = div.find_all('p')
        if len(ps) >= 3:
            post_body = div
            break

if post_body:
    # Extract h1, h2, h3, p, ul, ol
    elements = post_body.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'ul', 'ol'])
    lines = []
    for el in elements:
        t = el.get_text().strip()
        if t and not t.startswith("Choose language") and not "Logistics Explorer" in t and not "Sign in" in t:
            lines.append(t)
    
    # Deduplicate while preserving order
    clean_lines = []
    for line in lines:
        if line not in clean_lines and len(line) > 10:
            clean_lines.append(line)
            
    full_text = "\n\n".join(clean_lines)
    print("EXTRACTED ARTICLE CONTENT:")
    print("-----------------------------------")
    print(full_text)
    print("-----------------------------------")
    
    with open("/opt/hermes/profiles/archie/extracted_clean_original.txt", "w", encoding="utf-8") as f:
        f.write(full_text)
else:
    print("Could not find article body container.")
