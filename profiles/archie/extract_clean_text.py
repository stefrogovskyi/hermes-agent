import urllib.request
import re
from bs4 import BeautifulSoup

url = "https://www.searates.com/blog/post/driving-innovation-in-transportation-with-advanced-fleet-management-solutions"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

with urllib.request.urlopen(req) as response:
    html = response.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    # Locate the article content
    # Look for the main title and paragraphs
    h1 = soup.find('h1')
    title = h1.text.strip() if h1 else ""
    
    # Extract article body text
    # Let's find paragraphs and headings following h1
    content_parts = []
    if h1:
        content_parts.append(f"# {title}\n")
        
        # Traverse parent container or siblings
        parent = h1.find_parent('div') or h1.find_parent('article') or soup
        # Get all headings and paragraphs in parent
        elements = parent.find_all(['h2', 'h3', 'h4', 'p', 'ul', 'ol'])
        for el in elements:
            # Skip header/nav elements if any
            txt = el.get_text(strip=True)
            if txt and not any(nav_word in txt.lower() for nav_word in ['logistics explorer', 'tracking system', 'container tracking', 'rate management', 'co2 calculator']):
                if el.name.startswith('h'):
                    content_parts.append(f"\n## {txt}\n")
                elif el.name in ['ul', 'ol']:
                    for li in el.find_all('li'):
                        content_parts.append(f"- {li.get_text(strip=True)}")
                else:
                    content_parts.append(txt)

    full_text = "\n\n".join(content_parts)
    print("Full text length:", len(full_text))
    print("=== ARTICLE FULL TEXT ===")
    print(full_text)
    
    with open('/opt/hermes/profiles/archie/original_article_extracted.txt', 'w', encoding='utf-8') as f:
        f.write(full_text)
