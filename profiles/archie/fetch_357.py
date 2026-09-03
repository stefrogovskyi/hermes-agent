import urllib.request
from bs4 import BeautifulSoup
import json

url = 'https://www.searates.com/blog/post/tilog-logistix-2024-bangkok-conference-summary'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Try to find main content article body
        article_body = soup.find('article') or soup.find('div', class_='blog-post') or soup.find('div', class_='content')
        
        # Remove scripts and styles
        for script in soup(['script', 'style', 'nav', 'header', 'footer']):
            script.decompose()
            
        text = soup.get_text(separator='\n')
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        cleaned = '\n'.join(lines)
        
        title = soup.title.string if soup.title else 'Tilog logistix 2024 bangkok conference summary'
        
        print('=== TITLE ===')
        print(title)
        print('=== CONTENT SAMPLE ===')
        print(cleaned[:1000])
        
        with open('/opt/hermes/profiles/archie/orig_article_357_raw.txt', 'w', encoding='utf-8') as f:
            f.write(cleaned)
            
        # Also let's extract the main article text specifically
        main_text = ""
        # Look for article container in SeaRates blog structure
        main_div = soup.find('div', {'class': lambda x: x and ('post' in x or 'article' in x or 'content' in x)})
        if main_div:
            main_text = main_div.get_text(separator='\n')
        else:
            main_text = cleaned
            
        with open('/opt/hermes/profiles/archie/orig_article_357_clean.txt', 'w', encoding='utf-8') as f:
            f.write(main_text)

except Exception as e:
    print('Error:', e)
