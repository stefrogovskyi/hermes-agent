with open("raw_extracted.txt", "r", encoding="utf-8") as f:
    lines = [l.strip() for l in f.readlines()]

start = False
article_lines = []
for line in lines:
    if "Sustainability-Driven Innovations in Ro-Ro Shipping" in line and not start:
        start = True
    if start:
        if line in ["RECOMMENDED POSTS", "Explore SeaRates tools", "Subscribe to our newsletter", "Popular posts"]:
            break
        article_lines.append(line)

clean_text = "\n".join(article_lines)
with open("source_article.txt", "w", encoding="utf-8") as f:
    f.write(clean_text)

print("Final Source Article length:", len(clean_text))
print("LAST 300 CHARS:\n", clean_text[-300:])
