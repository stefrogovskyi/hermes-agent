import urllib.request
from bs4 import BeautifulSoup

url = "https://www.searates.com/blog/post/driving-innovation-in-transportation-with-advanced-fleet-management-solutions"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

with urllib.request.urlopen(req) as response:
    html = response.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    h1 = soup.find('h1')
    title = h1.get_text(strip=True) if h1 else ""
    
    article_lines = [f"# {title}\n"]
    
    # Traverse all elements after h1 in the body
    started = False
    for el in soup.find_all(['h1', 'h2', 'h3', 'p', 'ul', 'ol']):
        if el == h1:
            started = True
            continue
        if not started:
            continue
            
        text = el.get_text(strip=True)
        if not text:
            continue
            
        if "RECOMMENDED POSTS" in text or "Choose language:" in text:
            break
            
        # Filter out navigation p tags
        if any(nav in text for nav in ["Tools", "Services", "References", "Company", "Admin", "Logistics Explorer", "Tracking System", "Container Tracking", "Vessel Tracking", "Ship Schedules", "Logistics Map", "Load Calculator", "Distance & Time", "Freight Index", "Rate Management System", "CO2 Calculator"]):
            continue
            
        if el.name == 'h2':
            article_lines.append(f"\n## {text}\n")
        elif el.name == 'h3':
            article_lines.append(f"\n### {text}\n")
        elif el.name in ['ul', 'ol']:
            for li in el.find_all('li'):
                article_lines.append(f"- {li.get_text(strip=True)}")
        else:
            article_lines.append(text)

    clean_article = "\n\n".join(article_lines)
    print("Clean article length:", len(clean_article))
    with open('/opt/hermes/profiles/archie/article_full_text.txt', 'w', encoding='utf-8') as f:
        f.write(clean_article)
    print("Saved to /opt/hermes/profiles/archie/article_full_text.txt")
