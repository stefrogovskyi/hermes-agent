import urllib.request
from bs4 import BeautifulSoup

url = "https://www.searates.com/blog/post/driving-innovation-in-transportation-with-advanced-fleet-management-solutions"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

with urllib.request.urlopen(req) as response:
    html = response.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    # Get title
    h1 = soup.find('h1').get_text(strip=True)
    
    # We can iterate through headings and paragraphs in order
    article_lines = [f"# {h1}\n"]
    
    # Get author and date info if needed
    # Body starts around P 31 up to P 107
    ps = soup.find_all('p')
    
    # Let's inspect elements under the main blog container
    # Or simply traverse all H2, H3, P in document order
    container = soup.find('h1').parent
    while container and container.name not in ['div', 'article', 'main']:
        container = container.parent
        
    elements = container.find_all(['h2', 'h3', 'p', 'ul', 'ol'])
    
    for el in elements:
        text = el.get_text(strip=True)
        if not text:
            continue
        if text.startswith("RECOMMENDED POSTS") or text.startswith("Choose language"):
            break
        if el.name == 'h2':
            article_lines.append(f"\n## {text}\n")
        elif el.name == 'h3':
            article_lines.append(f"\n### {text}\n")
        elif el.name in ['ul', 'ol']:
            for li in el.find_all('li'):
                article_lines.append(f"- {li.get_text(strip=True)}")
        else:
            # Skip menu items / buttons
            if any(k in text.lower() for k in ['logistics explorer', 'tracking system', 'container tracking', 'vessel tracking', 'ship schedules', 'logistics map', 'load calculator', 'distance & time', 'freight index', 'rate management', 'co2 calculator', 'explore more opportunities with searates']):
                continue
            article_lines.append(text)

    clean_article = "\n\n".join(article_lines)
    print("Clean article length:", len(clean_article))
    with open('/opt/hermes/profiles/archie/article_full_text.txt', 'w', encoding='utf-8') as f:
        f.write(clean_article)
    print("Saved to /opt/hermes/profiles/archie/article_full_text.txt")
