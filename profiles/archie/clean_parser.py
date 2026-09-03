import urllib.request
from bs4 import BeautifulSoup

url = 'https://www.searates.com/blog/post/hidden-costs-of-lcl-shipping-how-to-calculate-avoid-extra-fees'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8')

soup = BeautifulSoup(html, 'html.parser')

# Remove navigation, header, footer, scripts, styles
for tag in soup(['nav', 'header', 'footer', 'script', 'style', 'aside']):
    tag.decompose()

# Look for post content wrapper
post_body = soup.find('div', class_='post-body') or soup.find('div', class_='blog-post') or soup.find('article')

lines = []
if post_body:
    for elem in post_body.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'li', 'blockquote']):
        txt = elem.get_text(strip=True)
        if txt and len(txt) > 5:
            lines.append(f"{elem.name.upper()}: {txt}")
else:
    # find all headings and paragraphs in body
    for elem in soup.body.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'li', 'blockquote']):
        txt = elem.get_text(strip=True)
        if txt and len(txt) > 5:
            # exclude header navigation items
            if any(x in txt for x in ["Logistics Explorer", "Tracking System", "Container Tracking", "Vessel Tracking", "Ship Schedules", "Logistics Map", "Load Calculator", "Distance & Time", "Freight Index", "Rate Management System", "CO2 Calculator", "More tools", "Services", "Info", "Dimensions"]):
                continue
            lines.append(f"{elem.name.upper()}: {txt}")

full_article_text = "\n\n".join(lines)
print("Extracted lines count:", len(lines))

with open('/opt/hermes/profiles/archie/orig_article_clean.txt', 'w', encoding='utf-8') as f:
    f.write(full_article_text)

print("Saved clean article to /opt/hermes/profiles/archie/orig_article_clean.txt")
