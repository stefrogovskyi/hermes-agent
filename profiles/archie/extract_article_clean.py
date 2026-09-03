from bs4 import BeautifulSoup

with open('/opt/hermes/profiles/archie/article_344_raw.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Find the main heading or article text
text_blocks = []
h1 = soup.find('h1')
if h1:
    text_blocks.append(f"TITLE: {h1.get_text().strip()}")

# Extract paragraphs, lists, headings after h1 or in the blog container
# Let's inspect all tags inside body in order
body = soup.find('body')
if body:
    # Find h1 index or element
    found_h1 = False
    for elem in body.descendants:
        if elem.name == 'h1':
            found_h1 = True
        if found_h1:
            if elem.name in ['p', 'h2', 'h3', 'ul', 'ol', 'li'] and elem.get_text().strip():
                # Avoid duplicate nested text
                if not any(child.name in ['p', 'h2', 'h3', 'ul', 'ol', 'li'] for child in elem.children):
                    txt = elem.get_text().strip()
                    if txt and txt not in text_blocks:
                        text_blocks.append(txt)

full_post = "\n\n".join(text_blocks)
print(full_post)

with open('/opt/hermes/profiles/archie/article_344_final_extracted.txt', 'w', encoding='utf-8') as f:
    f.write(full_post)
