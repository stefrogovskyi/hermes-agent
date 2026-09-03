import urllib.request
from bs4 import BeautifulSoup

url = "https://www.searates.com/blog/post/searates-updates-week-18-2025"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

req = urllib.request.Request(url, headers=headers)
html = urllib.request.urlopen(req).read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

# Let's inspect the tags around "SeaRates Updates - Week 18, 2025"
h1 = soup.find("h1")
print("H1:", h1.get_text(strip=True) if h1 else "None")

# Find container holding h1 or post content
parent = h1.parent if h1 else None
while parent and parent.name != "body":
    text = parent.get_text(separator="\n", strip=True)
    if "Check our prior updates" in text:
        print("Found main content parent tag:", parent.name, parent.get('class'))
        with open("/tmp/article_exact_content.txt", "w") as f:
            f.write(text)
        print("=== EXACT CONTENT ===")
        print(text)
        break
    parent = parent.parent
