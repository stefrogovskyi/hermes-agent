import json

with open('/tmp/final_article_data.json') as f:
    data = json.load(f)

print("Overlaps:", data['overlaps'])
