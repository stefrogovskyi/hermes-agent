import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

def search_ddg(query):
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            results = []
            for a in soup.find_all('a', class_='result__snippet'):
                results.append(a.get_text(strip=True))
            return results[:5]
    except Exception as e:
        return [str(e)]

print("Query 1:", search_ddg("audio technology digital freight management logistics trends 2026"))
print("Query 2:", search_ddg("acoustic AI predictive maintenance fleet logistics"))
