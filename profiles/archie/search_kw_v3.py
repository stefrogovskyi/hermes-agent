import urllib.request
import urllib.parse
import json

def fetch_search(query):
    # Using DuckDuckGo Lite or instant API
    url = "https://lite.duckduckgo.com/lite/"
    data = urllib.parse.urlencode({'q': query}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Content-Type': 'application/x-www-form-urlencoded'
    })
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            tds = soup.find_all('td', class_='result-snippet')
            return [td.get_text(strip=True) for td in tds[:5]]
    except Exception as e:
        return [str(e)]

print("Acoustic AI:", fetch_search("acoustic AI predictive maintenance logistics"))
print("Spatial audio logistics:", fetch_search("spatial audio training transport operations"))
