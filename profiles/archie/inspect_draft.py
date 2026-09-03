import json

with open('/opt/hermes/profiles/archie/rewrite_draft.json') as f:
    data = json.load(f)

print('Title:', len(data['title']), repr(data['title']))
print('Meta Title:', len(data['meta_title']), repr(data['meta_title']))
print('Meta Description:', len(data['meta_description']), repr(data['meta_description']))
print('\n--- BODY ---')
print(data['body'])
