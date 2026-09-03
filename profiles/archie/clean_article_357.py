with open('/opt/hermes/profiles/archie/orig_article_357_raw.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Filter out standard navigation, header, footer lines
content_lines = []
capturing = False

for line in lines:
    l = line.strip()
    if 'TILOG – LOGISTIX 2024: Bangkok Conference Summary' in l:
        capturing = True
    if 'Subscribe to our newsletter' in l or 'SeaRates Blog' in l and capturing and len(content_lines) > 20:
        if 'SeaRates Blog' in l or 'Related posts' in l or 'Comments' in l or 'Leave a reply' in l:
            # Stop capturing at footer/comments
            pass
    if capturing:
        content_lines.append(l)

full_text = '\n'.join(content_lines)
print("=== ARTICLE EXTRACTED LINES ===")
print(len(content_lines))
print("=== FIRST 1000 CHARS ===")
print(full_text[:1000])
print("=== LAST 1000 CHARS ===")
print(full_text[-1000:])

with open('/opt/hermes/profiles/archie/orig_article_357.txt', 'w', encoding='utf-8') as f:
    f.write(full_text)
