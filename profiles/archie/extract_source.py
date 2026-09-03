from bs4 import BeautifulSoup

with open('raw_article.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

container = soup.find('div', class_='blog-single-main-content')
if not container:
    container = soup.find('div', class_='main-content')

title_el = soup.find('h1')
title = title_el.get_text(strip=True) if title_el else "The Quantum Leap in Logistics: A View From the Helm of SeaRates"

# Extract paragraphs, headings, blockquotes, etc.
elements = []
elements.append(f"# {title}\n")

for elem in container.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'ul', 'ol', 'blockquote']):
    text = elem.get_text(strip=True)
    if not text:
        continue
    # avoid duplicates or social links if any
    if elem.name == 'h2':
        elements.append(f"\n## {text}\n")
    elif elem.name == 'h3':
        elements.append(f"\n### {text}\n")
    elif elem.name in ['ul', 'ol']:
        for li in elem.find_all('li'):
            elements.append(f"- {li.get_text(strip=True)}")
    else:
        elements.append(text)

article_content = "\n\n".join(elements)

with open('source_article.txt', 'w', encoding='utf-8') as f:
    f.write(article_content)

print(f"Saved source_article.txt ({len(article_content)} chars)")
print("\n--- FULL SOURCE ARTICLE ---")
print(article_content)
