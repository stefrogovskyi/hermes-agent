import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

def search_ddg(query):
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode("utf-8")
            soup = BeautifulSoup(html, "html.parser")
            results = []
            for res in soup.find_all("div", class_="result__body"):
                title_elem = res.find("a", class_="result__a")
                snippet_elem = res.find("a", class_="result__snippet")
                title = title_elem.get_text().strip() if title_elem else ""
                snippet = snippet_elem.get_text().strip() if snippet_elem else ""
                results.append(f"{title}: {snippet}")
            return results[:5]
    except Exception as e:
        return [str(e)]

print("Query 1:", search_ddg("container tracking API freight updates 2025"))
print("Query 2:", search_ddg("air cargo tracking integration logistics 2025"))
