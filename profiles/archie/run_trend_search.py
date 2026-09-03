import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

def search_ddg(query):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    url = 'https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            results = []
            for a in soup.find_all('a', class_='result__snippet'):
                results.append(a.get_text(strip=True))
            return results[:5]
    except Exception as e:
        print(f"Error for {query}: {e}")
        return []

queries = [
    "future proof logistics career supply chain skills 2026",
    "logistics automation AI workforce skills digital transformation",
    "supply chain management certifications CSCP CLTD career advancement"
]

trend_keywords = []
for q in queries:
    print(f"\nSearching: {q}")
    snippets = search_ddg(q)
    for s in snippets:
        print("- ", s)

