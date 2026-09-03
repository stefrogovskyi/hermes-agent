import urllib.request
import re
from bs4 import BeautifulSoup

url = "https://www.searates.com/blog/post/searates-updates-week-42-2024"
req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
)

with urllib.request.urlopen(req) as response:
    html = response.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

# Find main content container
# On SeaRates blog posts, post content is usually in specific tags or container
post_content = soup.find('div', class_=re.compile('post-content|blog-post|content|entry-content', re.I))

if not post_content:
    # fallback: search for text starting with "What’s new for week 42" or "Sophia Shkuro"
    text = soup.get_text(separator='\n')
else:
    text = post_content.get_text(separator='\n')

lines = [line.strip() for line in text.splitlines() if line.strip()]

# Filter lines to keep only main article text
start_idx = 0
end_idx = len(lines)

for i, l in enumerate(lines):
    if "Your ongoing assistance" in l or "What’s new for week 42" in l or "Sophia Shkuro" in l:
        start_idx = i
        break

for i in range(start_idx, len(lines)):
    if "Subscribe to our channel" in lines[i] or "Search by blog" in lines[i] or "Related posts" in lines[i] or "Comments" in lines[i]:
        end_idx = i
        break

article_lines = lines[start_idx:end_idx]
article_text = '\n'.join(article_lines)

print("--- EXTRACTED ARTICLE TEXT ---")
print(article_text)

with open("article_328_original.txt", "w", encoding="utf-8") as f:
    f.write("Title: SeaRates updates week 42 2024\n")
    f.write(f"URL: {url}\n\n")
    f.write(article_text)
