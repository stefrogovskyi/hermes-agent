import urllib.request
import urllib.parse
import json

# Let's search Wikipedia or DuckDuckGo API or Bing API / Serper / etc.
# DDG instant answer API:
for q in ["container tracking API", "demurrage and detention logistics", "vessel tracking API"]:
    url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(q)}&format=json"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(f"Query: {q}")
            print("Abstract:", data.get("AbstractText"))
            print("Related:", [r.get("Text") for r in data.get("RelatedTopics", []) if "Text" in r][:2])
    except Exception as e:
        print(f"Error {q}: {e}")
