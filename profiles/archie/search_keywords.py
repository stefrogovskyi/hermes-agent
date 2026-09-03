import urllib.request
import urllib.parse
import json
from bs4 import BeautifulSoup

def ddg_search(query):
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req) as resp:
            soup = BeautifulSoup(resp.read(), 'html.parser')
            results = []
            for a in soup.find_all('a', class_='result__snippet'):
                results.append(a.get_text())
            return results[:5]
    except Exception as e:
        return [str(e)]

if __name__ == "__main__":
    print("Search 1:", ddg_search("supply chain cybersecurity IT support trends"))
    print("Search 2:", ddg_search("logistics supply chain cyber attack risk mitigation"))
