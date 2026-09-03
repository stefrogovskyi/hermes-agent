import urllib.request
from bs4 import BeautifulSoup
import re

url = 'https://www.searates.com/blog/post/hidden-costs-of-lcl-shipping-how-to-calculate-avoid-extra-fees'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8')

soup = BeautifulSoup(html, 'html.parser')

# Find heading or article body
# Let's inspect headings and main text
print("--- HEADINGS ---")
for h in soup.find_all(['h1', 'h2', 'h3']):
    print(h.name, ':', h.get_text(strip=True))

print("\n--- PARAGRAPHS ---")
paras = [p.get_text(strip=True) for p in soup.find_all('p') if len(p.get_text(strip=True)) > 20]
for p in paras:
    print("-", p[:150])

# Let's save all clean body paragraphs to orig_clean.txt
with open('/opt/hermes/profiles/archie/orig_clean.txt', 'w', encoding='utf-8') as f:
    f.write("TITLE: " + (soup.find('h1').get_text(strip=True) if soup.find('h1') else "Hidden Costs of LCL Shipping") + "\n\n")
    # find container with paragraphs
    main_div = None
    for div in soup.find_all('div'):
        # count paragraphs inside div
        p_count = len(div.find_all('p'))
        if p_count > 5:
            main_div = div
            break
            
    if main_div:
        for elem in main_div.find_all(['h1', 'h2', 'h3', 'p', 'ul', 'ol']):
            if elem.name in ['ul', 'ol']:
                for li in elem.find_all('li'):
                    f.write(f"* {li.get_text(strip=True)}\n")
            else:
                f.write(f"{elem.get_text(strip=True)}\n\n")
    else:
        for p in paras:
            f.write(f"{p}\n\n")
