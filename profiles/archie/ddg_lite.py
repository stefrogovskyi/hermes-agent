import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

query = "heavy truck towing Germany roadside assistance cost"
url = f"https://lite.duckduckgo.com/lite/"
data = urllib.parse.urlencode({'q': query}).encode('utf-8')

req = urllib.request.Request(
    url, 
    data=data,
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
)

try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    tds = soup.find_all('td', class_='result-snippet')
    for td in tds[:5]:
        print("-", td.get_text(strip=True))
except Exception as e:
    print("Search error:", e)
