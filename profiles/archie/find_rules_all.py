import os, glob

for filepath in glob.glob("/opt/hermes/profiles/archie/**/*.log", recursive=True) + glob.glob("/opt/hermes/profiles/archie/**/*.md", recursive=True):
    try:
        with open(filepath) as f:
            content = f.read()
            if "Rule 11" in content or "Правило 11" in content or "11." in content:
                idx = content.find("Rule 1")
                if idx == -1:
                    idx = content.find("1. ZERO EM-DASHES")
                if idx != -1:
                    print(f"=== FOUND IN {filepath} ===")
                    print(content[idx:idx+3500])
                    break
    except Exception as e:
        pass
