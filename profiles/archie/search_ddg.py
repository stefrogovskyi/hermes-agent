import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

def search_ddg(query):
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            results = []
            for a in soup.find_all('a', class_='result__snippet'):
                results.append(a.get_text(strip=True))
            return results[:5]
    except Exception as e:
        print(f"DDG search error: {e}")
        return []

print("=== Search 1: air cargo tracking mobile logistics ===")
print(search_ddg("air cargo tracking mobile logistics"))

print("=== Search 2: container tracking API carrier integrations ===")
print(search_ddg("container tracking API carrier integrations"))
