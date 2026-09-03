import json

with open('/opt/hermes/profiles/archie/cache/delegation/live/deleg_0703394d/manifest.json') as f:
    m = json.load(f)

print(json.dumps(m, indent=2, ensure_ascii=False))
