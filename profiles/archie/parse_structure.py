import requests
from bs4 import BeautifulSoup

url = "https://www.searates.com/blog/post/efficient-shipping-choose-heavy-lift-or-project-cargo-bonus-checklist"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

resp = requests.get(url, headers=headers)
soup = BeautifulSoup(resp.text, 'html.parser')

# Let's inspect headings and main tags
headings = soup.find_all(['h1', 'h2', 'h3'])
print("HEADINGS:")
for h in headings:
    print(h.name, "->", h.get_text(strip=True))

# Look for divs with specific classes or blog-post content
print("\n--- POSS BUBBLES ---")
for d in soup.find_all('div'):
    classes = d.get('class', [])
    class_str = " ".join(classes) if isinstance(classes, list) else str(classes)
    if 'post' in class_str or 'blog' in class_str or 'content' in class_str or 'text' in class_str:
        t = d.get_text(strip=True)
        if len(t) > 300:
            print(f"DIV class='{class_str}' len={len(t)}")
