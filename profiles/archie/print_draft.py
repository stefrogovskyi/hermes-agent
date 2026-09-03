import json

with open('/opt/hermes/profiles/archie/draft.json') as f:
    data = json.load(f)

print("TITLE:", data['title'])
print("META TITLE:", data['meta_title'])
print("META DESCRIPTION:", data['meta_description'])
print("BODY LENGTH:", len(data['body_markdown']))
print("=== BODY ===")
print(data['body_markdown'])
