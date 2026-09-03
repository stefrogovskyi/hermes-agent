import urllib.request
from bs4 import BeautifulSoup

url = "https://www.searates.com/blog/post/searates-updates-week-41-2024"
req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
)

html = urllib.request.urlopen(req).read().decode('utf-8')
soup = BeautifulSoup(html, 'html.parser')

for tag in soup.find_all(['h1', 'h2', 'h3', 'p', 'li']):
    t = tag.get_text(strip=True)
    if len(t) > 10 and not any(k in t for k in ["Logistics Explorer", "CO2 Calculator", "Rate Management System", "Sign in", "Ship Schedules"]):
        print(f"[{tag.name}] {t}")
