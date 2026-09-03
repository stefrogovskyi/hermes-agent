import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

query = "digital supply chain workflow automation AI freight 2026"
url = f"https://lite.duckduckgo.com/lite/"
data = urllib.parse.urlencode({'q': query}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')
        snippets = soup.find_all('td', class_='result-snippet')
        for s in snippets[:5]:
            print("-", s.get_text(strip=True))
except Exception as e:
    print("DDG lite error:", e)
