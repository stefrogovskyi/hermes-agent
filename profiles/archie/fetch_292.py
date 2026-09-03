import urllib.request
from bs4 import BeautifulSoup

url = 'https://www.searates.com/blog/post/how-proration-can-help-your-international-logistics-startup'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract article content
    # Look for blog text or main body
    for script in soup(["script", "style", "header", "footer", "nav"]):
        script.decompose()
        
    text = soup.get_text(separator='\n')
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    clean_text = '\n'.join(lines)
    
    with open('/opt/hermes/profiles/archie/original_article_292.txt', 'w', encoding='utf-8') as f:
        f.write(clean_text)
    print(f'Successfully fetched {len(clean_text)} characters')
    print('Sample:')
    print(clean_text[:1500])
except Exception as e:
    print('Error:', e)
