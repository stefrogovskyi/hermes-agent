import json

with open('/opt/hermes/profiles/archie/rewrite_draft.json') as f:
    data = json.load(f)

print(json.dumps(data, indent=2))
