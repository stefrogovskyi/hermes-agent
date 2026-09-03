import urllib.request
import re

url = "https://html.duckduckgo.com/html/?q=b2b+logistics+social+media+marketing"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    # Find all text inside result__snippet or result__body
    text_matches = re.findall(r'class="result__snippet[^">]*">(.*?)</a>', html, re.DOTALL)
    for t in text_matches[:5]:
        clean = re.sub(r'<[^>]+>', '', t).strip()
        print("MATCH:", clean)
except Exception as e:
    print("Error:", e)
