import urllib.request
from bs4 import BeautifulSoup

url = "https://www.searates.com/blog/post/international-shipping-safety-lockouttagout-protocols-for-multi-national-compliance"

req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
)

with urllib.request.urlopen(req) as response:
    html = response.read().decode('utf-8')

soup = BeautifulSoup(html, 'html.parser')

# Try to find the blog post main content container
post_content = soup.find('div', class_='post-content') or soup.find('article') or soup.find('main') or soup.body

for element in post_content.find_all(['script', 'style', 'nav', 'header', 'footer', 'aside']):
    element.decompose()

text = post_content.get_text(separator='\n')
lines = [line.strip() for line in text.splitlines() if line.strip()]

cleaned_text = '\n'.join(lines)

with open('/opt/hermes/profiles/archie/article_325_clean.txt', 'w') as f:
    f.write(cleaned_text)

print("Clean article saved. Length:", len(cleaned_text))
print("Full Clean Text:")
print("========================================")
print(cleaned_text)
print("========================================")
