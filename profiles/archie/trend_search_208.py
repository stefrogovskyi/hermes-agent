import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

def ddg_search(query):
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req) as resp:
            soup = BeautifulSoup(resp.read().decode('utf-8'), 'html.parser')
            results = []
            for a in soup.find_all('a', class_='result__snippet'):
                results.append(a.get_text(strip=True))
            return results[:5]
    except Exception as e:
        return [str(e)]

res1 = ddg_search("prevent freight shipping delays supply chain visibility 2026")
res2 = ddg_search("freight shipping delay mitigation carrier performance TMS tracking")
print("Query 1:", res1)
print("Query 2:", res2)
