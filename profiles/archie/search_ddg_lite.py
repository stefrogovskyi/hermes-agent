import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

def search_ddg_lite(query):
    url = "https://lite.duckduckgo.com/lite/"
    data = urllib.parse.urlencode({'q': query}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    try:
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        for td in soup.find_all('td', class_='result-snippet'):
            results.append(td.get_text().strip())
        return results[:5]
    except Exception as e:
        return [f"Error: {e}"]

q1 = search_ddg_lite("shipping container home design 2026 trends")
q2 = search_ddg_lite("repurposed shipping containers commercial pop-up spaces")

print("--- Query 1 ---")
for r in q1:
    print("-", r)

print("\n--- Query 2 ---")
for r in q2:
    print("-", r)
