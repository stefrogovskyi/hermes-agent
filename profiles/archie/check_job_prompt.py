import json

with open('/opt/hermes/profiles/archie/cache/delegation/live/deleg_48336009/manifest.json', 'r') as f:
    d = json.load(f)
    with open('/opt/hermes/profiles/archie/extracted_goal.txt', 'w') as out:
        out.write(d['tasks'][0]['goal'])
