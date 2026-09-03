import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

queries = [
    "container tracking API shipping lines 2025",
    "air cargo tracking freight logistics trends",
    "multi carrier logistics software updates"
]

for q in queries:
    print(f"\n--- Search: {q} ---")
    url = 'https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(q)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        results = [a.get_text(strip=True) for a in soup.find_all('a', class_='result__snippet')]
        for r in results[:3]:
            print(" -", r)
    except Exception as e:
        print(" Error:", e)
