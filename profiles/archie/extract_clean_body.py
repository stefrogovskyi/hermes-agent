import urllib.request
from bs4 import BeautifulSoup

url = "https://www.searates.com/blog/post/october-2024-development-release-empowering-business-users"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as response:
    html = response.read().decode('utf-8')

soup = BeautifulSoup(html, 'html.parser')

# Find the main article content container
# SeaRates blog articles usually have a specific article body container or div
article_body = soup.find('article') or soup.find('div', class_=lambda c: c and 'post' in c) or soup.find('main')

if article_body:
    text = article_body.get_text(separator='\n\n')
else:
    text = soup.get_text(separator='\n\n')

# Let's inspect the entire text length and save it
lines = [l.strip() for l in text.splitlines() if l.strip()]
full_clean = '\n\n'.join(lines)

print("Full clean text length:", len(full_clean))
print("--- FULL TEXT START ---")
print(full_clean)
print("--- FULL TEXT END ---")

with open("/opt/hermes/profiles/archie/article_clean.txt", "w") as f:
    f.write(full_clean)
