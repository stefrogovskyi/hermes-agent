with open('/opt/hermes/profiles/archie/clean_original_article.txt', 'r', encoding='utf-8') as f:
    text = f.read()

start_marker = "Advanced Transport Management with Logistics Map & Virtual Office"
idx = text.find(start_marker)

if idx != -1:
    article_body = text[idx:]
    # Remove footer elements if any
    footer_idx = article_body.find("Subscribe to our newsletter")
    if footer_idx != -1:
        article_body = article_body[:footer_idx]
else:
    article_body = text

print("Extracted Article Body Length:", len(article_body))
print("\n=== ARTICLE BODY START ===")
print(article_body)
print("=== ARTICLE BODY END ===")

with open('/opt/hermes/profiles/archie/article_body.txt', 'w', encoding='utf-8') as f:
    f.write(article_body)
