from bs4 import BeautifulSoup

with open("full_page.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

main_div = soup.find('div', class_=lambda c: c and 'blog-single-main-content' in c)

if main_div:
    # Print clean formatted text retaining structure
    lines = []
    for tag in main_div.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'ul', 'ol', 'li']):
        t = tag.get_text(strip=True)
        if t:
            if tag.name.startswith('h'):
                lines.append(f"\n### {t}\n")
            elif tag.name == 'li':
                lines.append(f"- {t}")
            elif tag.name == 'p':
                lines.append(f"{t}")
            else:
                lines.append(t)
    
    clean_text = "\n".join(lines)
    with open("article_326_original.txt", "w", encoding="utf-8") as f:
        f.write(clean_text)
    print("Successfully extracted article! Word count:", len(clean_text.split()))
    print("\n--- CONTENT PREVIEW ---")
    print(clean_text[:1500])
else:
    print("blog-single-main-content not found")
