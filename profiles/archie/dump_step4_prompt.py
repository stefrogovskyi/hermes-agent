import json, glob

for path in glob.glob("/opt/hermes/profiles/archie/cache/delegation/**/manifest.json", recursive=True):
    with open(path) as f:
        data = json.load(f)
        for t in data.get("tasks", []):
            g = t.get("goal", "")
            if "8-step" in g.lower() or "rewrite" in g.lower() or "avalanche" in g.lower():
                print("=== GOAL ===")
                print(g[:2000])
                print("="*40)
