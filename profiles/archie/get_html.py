import urllib.request
from bs4 import BeautifulSoup

url = "https://www.searates.com/blog/post/searates-updates-week-43-2024"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as response:
    html = response.read().decode('utf-8')

with open("full_page.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Saved full_page.html length:", len(html))
