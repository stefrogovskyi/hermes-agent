import json
import os

snapshot_path = '/opt/hermes/profiles/archie/.skills_prompt_snapshot.json'
if os.path.exists(snapshot_path):
    with open(snapshot_path) as f:
        data = json.load(f)
    print("Keys in snapshot:", data.keys())
    for k, v in data.items():
        if isinstance(v, dict):
            for sk_path, content in v.items():
                if 'avalanche' in sk_path or 'copywriting' in sk_path:
                    print('PATH:', sk_path)
                    print(content[:1000])
