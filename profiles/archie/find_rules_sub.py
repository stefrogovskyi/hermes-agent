import glob, re

files = glob.glob('/opt/hermes/profiles/archie/cache/delegation/live/*/*.log') + glob.glob('/opt/hermes/profiles/archie/cache/terminal-output/*.log')
for f in sorted(files, reverse=True):
    try:
        content = open(f, errors='ignore').read()
        if "Правило 1:" in content or "Rule 1:" in content or "11 правил" in content:
            idx = content.find("8-шагов")
            if idx == -1: idx = content.find("8 шагов")
            if idx == -1: idx = content.find("Правило 1")
            if idx != -1:
                print(f"=== FOUND IN {f} ===")
                print(content[idx:idx+3500])
                break
    except Exception as e:
        pass
