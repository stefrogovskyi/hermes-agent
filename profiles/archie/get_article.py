import urllib.request
import re
from bs4 import BeautifulSoup

url = "https://www.searates.com/blog/post/searates-updates-week-5-2025"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        
        # Try finding post content container
        post_content = soup.find("div", class_=re.compile("post|blog|content|article", re.I))
        if not post_content:
            post_content = soup.body
            
        text = post_content.get_text(separator="\n")
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        
        full_text = "\n".join(lines)
        print("TITLE:", soup.title.string if soup.title else "No title")
        print("\n--- CONTENT LENGTH ---", len(full_text))
        
        with open("/opt/hermes/profiles/archie/article_original_294.txt", "w", encoding="utf-8") as f:
            f.write(full_text)
            
        # Also let's print relevant main body lines
        print("\n--- FIRST 50 LINES ---")
        print("\n".join(lines[:50]))
except Exception as e:
    print("Error:", e)
