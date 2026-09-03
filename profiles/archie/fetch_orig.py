import urllib.request
from bs4 import BeautifulSoup

url = 'https://www.searates.com/blog/post/harnessing-data-visualization-for-freight-efficiency'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Try to find specific article content container
        # SeaRates blogs often have post-content or article tags
        content_div = soup.find('div', class_='post-content') or soup.find('article') or soup.find('main')
        if not content_div:
            content_div = soup.body
            
        text = content_div.get_text(separator='\n')
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        
        print('TITLE:', soup.title.string if soup.title else '')
        print('TOTAL LINES:', len(lines))
        
        full_text = '\n'.join(lines)
        with open('/opt/hermes/profiles/archie/original_article.txt', 'w', encoding='utf-8') as f:
            f.write(full_text)
            
        print("Saved original_article.txt successfully")
except Exception as e:
    print('ERROR:', e)
