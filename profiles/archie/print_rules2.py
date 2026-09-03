import json, glob

for p in glob.glob('cache/delegation/live/*/manifest.json'):
    with open(p) as f:
        data = json.load(f)
    goal = data['tasks'][0].get('goal', '')
    if '11 Anti-AI' in goal or '11 MUST' in goal or 'STRICT RULE' in goal:
        print(f"=== {p} ===")
        print(goal)
