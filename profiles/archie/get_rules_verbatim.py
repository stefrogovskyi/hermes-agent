import json
from pathlib import Path

logs = list(Path("/opt/hermes/profiles/archie/cache/delegation").glob("**/*.log")) + list(Path("/opt/hermes/profiles/archie/cache/delegation").glob("**/*.json"))

for l in logs:
    try:
        txt = l.read_text(encoding="utf-8")
        if "Правило 1:" in txt or "Rule 1:" in txt:
            print(f"FOUND IN {l}:")
            idx = txt.find("Правило 1:") if "Правило 1:" in txt else txt.find("Rule 1:")
            print(txt[idx:idx+3500])
            break
    except Exception:
        pass
