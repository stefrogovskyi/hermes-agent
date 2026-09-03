import json, glob

for p in glob.glob('cache/delegation/live/*/task-0.log'):
    with open(p) as f:
        text = f.read()
    if '1. ABSOLUTE' in text or 'Rule 1:' in text or 'Rule 11' in text:
        print(f"=== {p} ===")
        lines = text.split('\n')
        for line in lines:
            if any(f"{i}." in line or f"Rule {i}" in line for i in range(1, 12)):
                print(line[:300])
