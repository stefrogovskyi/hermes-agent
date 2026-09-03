import urllib.request
from bs4 import BeautifulSoup

url = 'https://www.searates.com/blog/post/searates-updates-week-39-2024'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

# Let's find post body specifically
# Look for blog post main area
for nav in soup.find_all(['nav', 'header', 'footer', 'aside']):
    nav.decompose()

# Extract main paragraphs / headings
post_text = []
for p in soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'li']):
    txt = p.get_text(strip=True)
    if txt and txt not in post_text:
        # filter out generic site nav items if any
        if not any(x in txt for x in ['Categories', 'Archive', 'All Rights Reserved', 'Privacy Policy', 'Cookie']):
            post_text.append(txt)

clean_body = "\n\n".join(post_text)
print(clean_body)

with open('/opt/hermes/profiles/archie/orig_clean_335.txt', 'w', encoding='utf-8') as f:
    f.write(clean_body)
