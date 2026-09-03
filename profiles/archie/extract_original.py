import urllib.request
from bs4 import BeautifulSoup

url = "https://www.searates.com/blog/post/truck-towing-service-in-germany-costs-assistance-emergency-guide"

req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
)

with urllib.request.urlopen(req) as response:
    html = response.read().decode('utf-8')

soup = BeautifulSoup(html, 'html.parser')

main_div = soup.find('div', class_='blog-single-main-content')

if not main_div:
    print("Error: blog-single-main-content not found")
else:
    # Extract clean text line by line
    lines = []
    for elem in main_div.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'li', 'td', 'tr']):
        text = elem.get_text(strip=True)
        if text and text not in lines:
            if elem.name in ['h1', 'h2', 'h3', 'h4']:
                lines.append(f"\n## {text}\n")
            elif elem.name == 'li':
                lines.append(f"- {text}")
            else:
                lines.append(text)
                
    full_text = "\n\n".join(lines)
    
    with open("/opt/hermes/profiles/archie/original_article.txt", "w", encoding="utf-8") as f:
        f.write(full_text)
        
    print("Successfully extracted original article!")
    print(f"Total length: {len(full_text)} characters.")
    print("\n--- FULL TEXT ---\n")
    print(full_text)
