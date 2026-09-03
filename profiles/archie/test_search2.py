import urllib.request
from bs4 import BeautifulSoup
import urllib.parse

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

query = "container shipment tracking multi-carrier visibility"
url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req) as resp:
        soup = BeautifulSoup(resp.read(), 'html.parser')
        results = soup.find_all('a', class_='result__snippet')
        print("Found results count:", len(results))
        for r in results[:5]:
            print("-", r.get_text(strip=True))
except Exception as e:
    print("Error:", e)
