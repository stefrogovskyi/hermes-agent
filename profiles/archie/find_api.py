import json

with open('draft.json') as f:
    d = json.load(f)

full_text = (d['title'] + ' ' + d['meta_title'] + ' ' + d['meta_description'] + ' ' + d['body']).lower()

print("Full text snippet with API:")
for line in full_text.split('\n'):
    if 'api' in line:
        print(repr(line))
