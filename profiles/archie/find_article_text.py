from bs4 import BeautifulSoup
import re

with open("/opt/hermes/profiles/archie/raw_page.html") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# Look for text or JSON embedded in scripts (like __NEXT_DATA__ or Nuxt or window.__INITIAL_STATE__)
script_tags = soup.find_all("script")
for s in script_tags:
    if s.string and ("week 50" in s.string.lower() or "searates updates" in s.string.lower()):
        print("FOUND IN SCRIPT! Length:", len(s.string))
        with open("/opt/hermes/profiles/archie/script_data.json", "w") as sf:
            sf.write(s.string)

# Look for article text
for div in soup.find_all(['div', 'article', 'section']):
    text = div.get_text(separator="\n", strip=True)
    if "week 50" in text.lower() and len(text) > 300:
        print(f"FOUND IN DIV ({div.name}, class={div.get('class')}): length={len(text)}")
        print(text[:500])
        print("="*40)
