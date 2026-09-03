import json
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

def search_ddg(query):
    url = f"https://lite.duckduckgo.com/lite/"
    data = urllib.parse.urlencode({'q': query}).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data,
        headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            snippets = []
            for td in soup.find_all('td', class_='result-snippet'):
                snippets.append(td.get_text().strip())
            return snippets
    except Exception as e:
        return [str(e)]

q1 = search_ddg("TPM25 S&P Global container shipping trends")
q2 = search_ddg("ocean freight rate automation supply chain visibility 2025")

print("Q1 results:", q1[:3])
print("Q2 results:", q2[:3])
