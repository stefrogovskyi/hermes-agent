import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

url = "https://html.duckduckgo.com/html/?q=container+shipping+rates"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a')
        print("Found links count:", len(links))
        for a in links[:10]:
            print(a.get_text().strip(), "-->", a.get('href'))
except Exception as e:
    print(e)
