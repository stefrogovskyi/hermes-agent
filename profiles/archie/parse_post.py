import urllib.request
import re
from bs4 import BeautifulSoup

url = "https://www.searates.com/blog/post/driving-innovation-in-transportation-with-advanced-fleet-management-solutions"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

with urllib.request.urlopen(req) as response:
    html = response.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    
    # Let's find title and post body
    h1 = soup.find('h1')
    print("H1 Title:", h1.text if h1 else "No H1 found")
    
    # Print all paragraph text or specific post container
    # Let's search for tags or classes
    divs = soup.find_all(['div', 'section', 'article'])
    for d in divs:
        # Check if contains significant text and heading
        if d.find('h1') or ('post' in str(d.get('class', '')).lower()):
            text = d.get_text(separator='\n', strip=True)
            if len(text) > 300:
                print("--- FOUND CONTAINER ---")
                print(text[:1500])
                with open('/opt/hermes/profiles/archie/original_article_clean.txt', 'w', encoding='utf-8') as f:
                    f.write(text)
                break
