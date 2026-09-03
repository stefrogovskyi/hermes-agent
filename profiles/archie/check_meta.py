import json

with open('draft.json') as f:
    data = json.load(f)

title = data['title']
meta_title = data['meta_title']
meta_description = data['meta_description']

print(f"Title ({len(title)} chars): {title}")
print(f"Meta Title ({len(meta_title)} chars): {meta_title}")
print(f"Meta Description ({len(meta_description)} chars): {meta_description}")

assert len(title) <= 60
assert len(meta_title) <= 60
assert len(meta_description) <= 155
print("All metadata limits satisfied perfectly!")
