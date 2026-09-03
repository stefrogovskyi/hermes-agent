import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

def search_ddg(query):
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    try:
        with urllib.request.urlopen(req) as resp:
            soup = BeautifulSoup(resp.read().decode("utf-8"), "html.parser")
            results = soup.find_all("a", class_="result__snippet")
            print(f"=== Results for: {query} ===")
            for r in results[:3]:
                print("-", r.get_text())
    except Exception as e:
        print("Search error:", e)

search_ddg("ocean container tracking freight rate alerts logistics software")
search_ddg("air cargo tracking api bulk booking export freight forwarder")
