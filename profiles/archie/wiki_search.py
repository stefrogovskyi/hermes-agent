import urllib.request
import json

# Let's search Wikipedia API for shipping container architecture / cargotecture keywords
url = "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=shipping+container+architecture+repurposing&format=json"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    res = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
    data = json.loads(res)
    print("Wikipedia Search Results:")
    for item in data['query']['search']:
        print(f"- {item['title']}: {item['snippet']}")
except Exception as e:
    print("Wiki error:", e)
