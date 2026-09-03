import urllib.request
import re
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []

    def handle_data(self, d):
        self.text.append(d)

    def get_data(self):
        return ''.join(self.text)

url = 'https://www.searates.com/blog/post/searates-updates-week-21-2025'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8')
        
        # Save raw HTML first
        with open("raw_page.html", "w", encoding="utf-8") as f:
            f.write(html)
            
        s = MLStripper()
        s.feed(html)
        text = s.get_data()
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        full_text = '\n'.join(lines)
        
        print("FETCHED RAW TEXT LENGTH:", len(full_text))
        
        with open("original_raw.txt", "w", encoding="utf-8") as f:
            f.write(full_text)
            
except Exception as e:
    print(f"Error: {e}")
