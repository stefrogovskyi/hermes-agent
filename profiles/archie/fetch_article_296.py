import urllib.request
from bs4 import BeautifulSoup

url = 'https://www.searates.com/blog/post/enhancing-freight-shipping-software-efficiency-with-paraphrasing-tools-and-grammar-solutions'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
req = urllib.request.Request(url, headers=headers)
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    
    # Save full text to file
    with open('/opt/hermes/profiles/archie/article_296_raw.txt', 'w', encoding='utf-8') as f:
        f.write(soup.get_text())
        
    print('TITLE:', soup.title.string if soup.title else 'No title')
    
    # Find blog content div if present
    post_div = soup.find('div', class_='blog-post') or soup.find('div', class_='post-content') or soup.find('article')
    if post_div:
        print('FOUND POST DIV:')
        print(post_div.get_text(separator='\n', strip=True)[:2000])
    else:
        print('FULL TEXT SNIPPET:')
        print(soup.get_text(separator='\n', strip=True)[:2000])
except Exception as e:
    print('Error:', e)
