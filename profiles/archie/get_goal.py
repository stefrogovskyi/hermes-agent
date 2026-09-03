import json
from pathlib import Path

manifests = list(Path("/opt/hermes/profiles/archie/cache/delegation").glob("**/manifest.json"))
for m in manifests:
    data = json.loads(m.read_text())
    tasks = data.get("tasks", [])
    for t in tasks:
        goal = t.get("goal", "")
        if "STRICT RULES TO FOLLOW" in goal:
            print("FOUND GOAL:")
            print(goal)
            break
