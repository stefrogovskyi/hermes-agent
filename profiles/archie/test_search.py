import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

query = "supply chain trends 2025 logistics digital transformation"
url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

try:
    with urllib.request.urlopen(req) as resp:
        soup = BeautifulSoup(resp.read().decode('utf-8'), 'html.parser')
        results = soup.find_all('a', class_='result__snippet')
        for r in results[:5]:
            print("-", r.get_text(strip=True))
except Exception as e:
    print("Search error:", e)
