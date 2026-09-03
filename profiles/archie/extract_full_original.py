from bs4 import BeautifulSoup

with open("raw_page.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

main_div = soup.find('div', {'class': lambda x: x and 'blog-single-main-content' in x}) or soup.find('article')

if main_div:
    text = main_div.get_text(separator='\n', strip=True)
else:
    text = soup.get_text(separator='\n', strip=True)

with open("original_article.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("Saved original_article.txt, length:", len(text))
print("Full content:")
print("="*50)
print(text)
print("="*50)
