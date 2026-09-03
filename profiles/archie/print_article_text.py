import json

data = json.load(open('/opt/hermes/profiles/archie/extracted_clean_article.json'))
print("=== TITLE ===")
print(data['title'])
print("\n=== BODY ===")
print(data['body'])
