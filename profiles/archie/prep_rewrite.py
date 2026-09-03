with open('/opt/hermes/profiles/archie/clean_original_article.txt', 'r', encoding='utf-8') as f:
    source_text = f.read()

print(f"Source text size: {len(source_text)} chars")
