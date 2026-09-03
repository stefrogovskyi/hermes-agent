import json

summary_path = '/opt/hermes/profiles/archie/cache/delegation/subagent-summary-0-20260828_083647_264433.txt'
with open(summary_path, 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('```json')
end = text.find('```\n\n***')
if start != -1 and end != -1:
    json_str = text[start+7:end].strip()
    data = json.loads(json_str)
    print('Title:', data['title'])
    print('Meta Title:', data['meta_title'])
    print('Meta Description:', data['meta_description'])
    print('Body Length:', len(data['body']))
    with open('/opt/hermes/profiles/archie/rewrite_draft.json', 'w', encoding='utf-8') as out:
        json.dump(data, out, ensure_ascii=False, indent=2)
    print('Saved to /opt/hermes/profiles/archie/rewrite_draft.json')
else:
    print('Could not find json block')
