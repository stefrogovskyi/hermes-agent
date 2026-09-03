from bs4 import BeautifulSoup

with open("/opt/hermes/profiles/archie/raw_page.html") as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Find all headings and paragraphs in post body
blog_nodes = []
for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'li', 'span', 'div']):
    # check if tag has direct text
    if tag.name in ['h1', 'h2', 'h3', 'h4', 'p', 'li']:
        txt = tag.get_text(strip=True)
        if txt and ("Week 47" in txt or "Tracking System" in txt or "Ship Schedules" in txt or "Air Cargo" in txt or "Parcel Tracking" in txt or "Logistics Explorer" in txt or "Rate Management" in txt or "Distance & Time" in txt or "CO2 Calculator" in txt or "We appreciate" in txt or "What’s new" in txt):
            blog_nodes.append(f"<{tag.name}> {txt}")

# Deduplicate while preserving order
seen = set()
unique_nodes = []
for node in blog_nodes:
    if node not in seen:
        seen.add(node)
        unique_nodes.append(node)

article_str = "\n".join(unique_nodes)
print("=== EXTRACTED ARTICLE NODES ===")
print(article_str)

with open("/opt/hermes/profiles/archie/article_clean.txt", "w") as f:
    f.write(article_str)
