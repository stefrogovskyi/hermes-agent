import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import re

query = "digital adoption in logistics freight management trends 2025"
url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"

req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
)

try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        snippets = []
        for a in soup.find_all('a', class_='result__snippet'):
            snippets.append(a.get_text())
        print("FOUND DDG RESULTS:", len(snippets))
        for s in snippets[:5]:
            print("- ", s)
except Exception as e:
    print("Search error:", e)
