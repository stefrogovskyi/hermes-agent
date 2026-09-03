import urllib.request
import json

url = "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=ISO+7010+safety+sign+hazardous+area&format=json"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        for item in data['query']['search']:
            print(item['title'], "-", item['snippet'])
except Exception as e:
    print("Error:", e)
