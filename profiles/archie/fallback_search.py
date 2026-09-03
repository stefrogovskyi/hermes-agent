import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import json

def ddg_search(query):
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            results = []
            for a in soup.find_all('a', class_='result__snippet'):
                results.append(a.get_text().strip())
            return results[:5]
    except Exception as e:
        return [str(e)]

print("DDG SEARCH 1:")
print(ddg_search("counterparty management digital logistics virtual office"))
print("\nDDG SEARCH 2:")
print(ddg_search("SeaRates counterparties virtual office vendor carrier management"))
