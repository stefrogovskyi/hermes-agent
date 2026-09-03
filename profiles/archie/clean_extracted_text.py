import re

with open("/opt/hermes/profiles/archie/original_post.txt") as f:
    text = f.read()

# Extract from "Maritime Logistics and Analytics: How to Convert PDF Reports into PowerPoint Presentations" down to author/comments/footer
match = re.search(r"(Maritime Logistics and Analytics: How to Convert PDF Reports into PowerPoint Presentations.*?)(?=Comments|Leave a comment|Recent Posts|Footer|\Z)", text, re.DOTALL)
if match:
    article_text = match.group(1)
    with open("/opt/hermes/profiles/archie/cleaned_article.txt", "w") as out:
        out.write(article_text)
    print("Article extracted successfully! Length:", len(article_text))
    print("--- SAMPLE ---")
    print(article_text[:1000])
    print("...")
    print(article_text[-1000:])
else:
    print("Could not match main article block.")
