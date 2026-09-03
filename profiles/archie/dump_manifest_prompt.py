import json, glob

for path in glob.glob("/opt/hermes/profiles/archie/cache/delegation/**/manifest.json", recursive=True):
    with open(path) as f:
        data = json.load(f)
        for t in data.get("tasks", []):
            g = t.get("goal", "")
            if "Rule 1:" in g or "1. " in g or "em-dash" in g:
                if "Rule 11" in g or "Rule 10" in g:
                    print("=== MANIFEST GOAL ===")
                    print(g[:3000])
                    print("="*40)
                    break
