import urllib.request
import urllib.parse
import json

query = "sea freight distance transit time estimation keywords"
url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json"

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    data = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    print("Related topics:")
    for topic in data.get("RelatedTopics", [])[:5]:
        if "Text" in topic:
            print("-", topic["Text"])
except Exception as e:
    print("Error:", e)
