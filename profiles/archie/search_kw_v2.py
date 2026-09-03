import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

def search_ddg_v2(query):
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            results = []
            for res in soup.find_all('div', class_='result__body'):
                title = res.find('a', class_='result__a')
                snippet = res.find('a', class_='result__snippet')
                t_text = title.get_text(strip=True) if title else ""
                s_text = snippet.get_text(strip=True) if snippet else ""
                results.append(f"{t_text}: {s_text}")
            return results[:5]
    except Exception as e:
        return [str(e)]

print("Query 1:", search_ddg_v2("acoustic monitoring predictive maintenance fleet transport"))
print("Query 2:", search_ddg_v2("spatial audio VR training logistics operations"))
