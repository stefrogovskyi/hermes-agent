import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

query = "smart logistics workflow automation AI freight 2026"
url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')
        results = soup.find_all('a', class_='result__snippet')
        for r in results[:5]:
            print("-", r.get_text(strip=True))
except Exception as e:
    print("DDG search error:", e)
