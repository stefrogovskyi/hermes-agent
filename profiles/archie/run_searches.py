import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

queries = [
    "TPM 2025 container shipping trends S&P Global",
    "Trans-Pacific ocean freight rate automation 2025",
    "supply chain transparency AI logistics 2025"
]

for query in queries:
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )
    print(f"\n=== Query: {query} ===")
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            results = soup.find_all('a', class_='result__snippet')
            for r in results[:3]:
                print("-", r.get_text().strip())
    except Exception as e:
        print("Error:", e)
