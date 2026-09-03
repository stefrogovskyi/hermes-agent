import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

def search_ddg(query):
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            results = []
            for a in soup.find_all('a', class_='result__snippet'):
                results.append(a.get_text(strip=True))
            return results[:3]
    except Exception as e:
        return [f"Error: {e}"]

queries = [
    "SIL Barcelona 2025 logistics trends",
    "green logistics Industry 4.0 supply chain 2025",
    "digital freight forwarding technology trends 2025"
]

for q in queries:
    print(f"=== QUERY: {q} ===")
    res = search_ddg(q)
    for r in res:
        print(" -", r)
