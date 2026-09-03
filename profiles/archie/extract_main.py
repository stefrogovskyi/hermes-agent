from bs4 import BeautifulSoup

with open('page.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Find main content container
# SeaRates blog posts usually have content in specific containers or tags
main = soup.find('div', class_='blog-content') or soup.find('div', class_='post-content') or soup.find('article') or soup.find('main')

if main:
    print("FOUND MAIN CONTAINER:")
    print(main.get_text(separator='\n', strip=True))
    with open('article_content.txt', 'w', encoding='utf-8') as f:
        f.write(main.get_text(separator='\n', strip=True))
else:
    print("NO MAIN CONTAINER FOUND, SEARCHING PARAGRAPHS:")
    paragraphs = [p.get_text(strip=True) for p in soup.find_all(['p', 'h1', 'h2', 'h3', 'li'])]
    text = '\n'.join(paragraphs)
    print(text[:2000])
    with open('article_content.txt', 'w', encoding='utf-8') as f:
        f.write(text)
