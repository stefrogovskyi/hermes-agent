import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

def search_ddg(query):
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            soup = BeautifulSoup(html, 'html.parser')
            results = []
            for a in soup.find_all('a', class_='result__snippet'):
                results.append(a.get_text(strip=True))
            return results[:5]
    except Exception as e:
        print("DDG error:", e)
        return []

print("Query 1:", search_ddg("cargo vs freight differences logistics e-commerce"))
print("Query 2:", search_ddg("LCL cargo vs freight shipping commercial goods"))
