import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

def search(q):
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})
    resp = urllib.request.urlopen(req)
    soup = BeautifulSoup(resp.read(), 'html.parser')
    snippets = []
    for div in soup.find_all('div', class_='result__body'):
        title = div.find('a', class_='result__a')
        snippet = div.find('a', class_='result__snippet')
        if title and snippet:
            snippets.append(f"{title.get_text()} - {snippet.get_text()}")
    return snippets

print("Query 1:", search("maritime digital compliance regulations 2026 sanctions KYC")[:3])
print("Query 2:", search("ocean freight cybersecurity NIS2 MARPOL EEXI compliance software")[:3])
