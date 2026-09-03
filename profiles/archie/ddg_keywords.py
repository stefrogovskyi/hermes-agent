import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import json

def ddg_search(query):
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            results = []
            for a in soup.find_all('a', class_='result__snippet'):
                results.append(a.get_text())
            return results[:5]
    except Exception as e:
        return [str(e)]

res1 = ddg_search("TILOG LOGISTIX 2024 Bangkok digital supply chain")
res2 = ddg_search("ASEAN logistics digital tools supply chain trends 2024 2025")

print("RES 1:", res1)
print("RES 2:", res2)

keywords = [
    "digital supply chain logistics ASEAN",
    "TILOG LOGISTIX Bangkok trade exhibition",
    "smart warehousing material handling IT solutions",
    "freight management digital logistics platforms"
]

with open('/opt/hermes/profiles/archie/keywords.json', 'w', encoding='utf-8') as f:
    json.dump({'keywords': keywords, 'ddg_1': res1, 'ddg_2': res2}, f, ensure_ascii=False, indent=2)
