import json

with open('/opt/hermes/profiles/archie/article_rewrite_step4.json') as f:
    data = json.load(f)

print("TITLE:", data['title'])
print("META TITLE:", len(data['meta_title']), data['meta_title'])
print("META DESC:", len(data['meta_description']), data['meta_description'])
print("\nBODY:\n", data['body'])
