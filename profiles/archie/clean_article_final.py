with open("/opt/hermes/profiles/archie/clean_article.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Trim text after "Related Articles" or "Popular Posts" or footer links if present
stop_markers = [
    "Related Posts", "Related Articles", "Popular Posts", "Leave a Reply", "Comments", "Tools\nServices", "Logistics Explorer"
]

for marker in stop_markers:
    if marker in text:
        text = text.split(marker)[0]

text = text.strip()

with open("/opt/hermes/profiles/archie/extracted_article.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("TOTAL EXTRACTED CHARS:", len(text))
print("--- FULL TEXT ---")
print(text)
