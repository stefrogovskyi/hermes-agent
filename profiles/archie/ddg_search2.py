import urllib.request
import urllib.parse
import json

def ddg_json(query):
    url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return data.get('RelatedTopics', [])
    except Exception as e:
        return [str(e)]

print("DDG JSON result:", ddg_json("colocation data center logistics")[:3])
