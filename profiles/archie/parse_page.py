from bs4 import BeautifulSoup
import re

with open('/opt/hermes/profiles/archie/page.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Find the main container for blog post content
# Usually in searates blog posts, content is inside blog-post-content or post-content or div with class containing post
post_body = soup.find('div', class_=re.compile(r'post|blog|content', re.I))

# Let's extract all text from article or post container
candidates = soup.find_all(['div', 'article', 'section'])
best_text = ""
for c in candidates:
    # Look for elements containing the text "SeaRates Updates" or "What’s new"
    if "What’s new" in c.text or "Announcements:" in c.text:
        t = c.get_text(separator='\n')
        if len(t) > len(best_text) and len(t) < 50000:
            best_text = t

print("Best text length:", len(best_text))

# Let's clean up lines
lines = [l.strip() for l in best_text.splitlines() if l.strip()]
cleaned_text = '\n'.join(lines)

with open('/opt/hermes/profiles/archie/original_article.txt', 'w', encoding='utf-8') as f:
    f.write(cleaned_text)

print("--- TEXT PREVIEW ---")
print(cleaned_text[:2000])
