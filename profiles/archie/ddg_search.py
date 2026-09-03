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
                results.append(a.get_text().strip())
            return results[:5]
    except Exception as e:
        print(f"DDG search error: {e}")
        return []

kw1 = ddg_search("freight data visualization analytics trends 2026")
kw2 = ddg_search("logistics performance dashboard real time visibility")
print("Search Results 1:", kw1)
print("Search Results 2:", kw2)

keywords = ["real-time freight analytics", "supply chain control tower", "logistics telemetry dashboards", "predictive route optimization", "cargo capacity heatmaps", "carrier performance metrics"]
print("Selected keywords:", keywords)
with open("/opt/hermes/profiles/archie/keywords.json", "w", encoding="utf-8") as f:
    json.dump(keywords, f, ensure_ascii=False)
