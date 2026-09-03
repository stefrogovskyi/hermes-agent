from bs4 import BeautifulSoup

with open("/opt/hermes/profiles/archie/page.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

main_content = soup.find('div', class_='blog-single-main-content')
if not main_content:
    print("blog-single-main-content not found")
else:
    title_el = soup.find('div', class_='blog-single-title') or soup.find('h1')
    title_text = title_el.get_text(strip=True) if title_el else ""
    
    # Extract clean text line by line or paragraph by paragraph
    lines = []
    for elem in main_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'p', 'ul', 'ol', 'li']):
        text = elem.get_text(" ", strip=True)
        if text and text not in lines:
            # Avoid duplicate parent/child text
            lines.append(text)
            
    full_text = "\n\n".join(lines)
    print("=== TITLE ===")
    print(title_text)
    print("\n=== BODY ===")
    print(full_text[:2000])
    
    with open("/opt/hermes/profiles/archie/article_217_clean.txt", "w", encoding="utf-8") as f:
        f.write(f"Title: {title_text}\n\n{full_text}")
