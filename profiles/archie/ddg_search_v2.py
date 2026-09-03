import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote("international logistics supply chain technology trends 2026")
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    for div in soup.find_all('div', class_='result__body'):
        title = div.find('a', class_='result__a')
        snippet = div.find('a', class_='result__snippet')
        if title and snippet:
            print("TITLE:", title.get_text(strip=True))
            print("SNIPPET:", snippet.get_text(strip=True))
            print("-" * 40)
