import urllib.request
from bs4 import BeautifulSoup

url = "https://www.searates.com/blog/post/driving-innovation-in-transportation-with-advanced-fleet-management-solutions"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

with urllib.request.urlopen(req) as response:
    html = response.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    # Find all p tags
    ps = soup.find_all('p')
    print(f"Total <p> tags: {len(ps)}")
    for i, p in enumerate(ps):
        print(f"--- P {i} ---")
        print(p.get_text(strip=True))

    # Also check headings h1, h2, h3, h4
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4'])
    print(f"\nTotal Headings: {len(headings)}")
    for h in headings:
        print(f"<{h.name}>: {h.get_text(strip=True)}")
