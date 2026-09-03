import urllib.request
import urllib.parse
import json
import re

def search_ddg(query):
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
            links = re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', html, re.S)
            clean = [re.sub(r'<[^>]+>', '', l).strip() for l in links]
            return clean[:5]
    except Exception as e:
        return [str(e)]

if __name__ == '__main__':
    print("Search 1:", search_ddg("hidden costs LCL shipping charges"))
    print("Search 2:", search_ddg("how to calculate LCL volumetric weight extra fees"))
