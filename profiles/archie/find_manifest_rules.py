import json
from pathlib import Path

logs = list(Path("/opt/hermes/profiles/archie/cache/delegation").glob("**/*.log"))

for l in logs:
    txt = l.read_text(encoding="utf-8", errors="ignore")
    if "1. NO EM-DASH" in txt or "1. Запрет em-dash" in txt or "Правило 1" in txt:
        print(f"FOUND IN {l}")
        # find where rules start
        idx = txt.find("1.")
        while idx != -1:
            snippet = txt[idx:idx+1500]
            if "11." in snippet or "10." in snippet:
                print(snippet)
                break
            idx = txt.find("1.", idx+1)
        break
