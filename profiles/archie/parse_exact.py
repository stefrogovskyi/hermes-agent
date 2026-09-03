with open("/opt/hermes/profiles/archie/original_post.txt") as f:
    text = f.read()

# Let's find where the blog post title appears in the body
start_marker = "Maritime Logistics and Analytics: How to Convert PDF Reports into PowerPoint Presentations\nShipping insights\nAug 28, 2024"
if start_marker in text:
    start_pos = text.find(start_marker)
    # End before the standard header/footer repetition
    end_marker = "Choose language:"
    end_pos = text.find(end_marker, start_pos)
    if end_pos != -1:
        article_body = text[start_pos:end_pos].strip()
    else:
        article_body = text[start_pos:start_pos+5000].strip()
else:
    article_body = text

with open("/opt/hermes/profiles/archie/exact_article.txt", "w") as out:
    out.write(article_body)

print("Exact article length:", len(article_body))
print("=== ARTICLE BODY ===")
print(article_body)
