from bs4 import BeautifulSoup

with open("/opt/hermes/profiles/archie/raw_page.html") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

div = soup.find("div", class_="blog-single-main-content")
if not div:
    div = soup.find("div", class_="container")

# Extract clean text
text = div.get_text(separator="\n", strip=True)

print("=== ORIGINAL ARTICLE TEXT ===")
print(text)

with open("/opt/hermes/profiles/archie/original_article.txt", "w") as f:
    f.write(text)
