import urllib.request
from bs4 import BeautifulSoup
import json

url = "https://www.searates.com/blog/post/maritime-logistics-and-analytics-how-to-convert-pdf-reports-into-powerpoint-presentations"
req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
)

try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
            
        text = soup.get_text(separator='\n')
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        print("TITLE:", soup.title.string if soup.title else "")
        print("--- CONTENT START ---")
        print(text[:5000])
        print("--- CONTENT END ---")
        
        with open("/opt/hermes/profiles/archie/original_post.txt", "w") as f:
            f.write(text)
            
except Exception as e:
    print("Error:", e)
