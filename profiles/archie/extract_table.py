from bs4 import BeautifulSoup

with open('/tmp/raw_article.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

tables = soup.find_all('table')
print(f"Found {len(tables)} tables.")
for idx, t in enumerate(tables):
    print(f"--- TABLE {idx+1} ---")
    rows = t.find_all('tr')
    for r in rows:
        cols = [c.get_text(strip=True) for c in r.find_all(['th', 'td'])]
        print(" | ".join(cols))
