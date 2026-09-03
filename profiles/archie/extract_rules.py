import glob, re

logs = glob.glob("/opt/hermes/profiles/archie/cache/terminal-output/*.log")
for l in sorted(logs):
    with open(l, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
        if "Правило 1" in text or "Rule 1" in text or "8-шаг" in text.lower():
            print("=== Found in", l)
            # Find snippet
            matches = [m.start() for m in re.finditer(r'Правило 1|Rule 1|11 правил', text)]
            for idx in matches[:2]:
                print(text[max(0, idx-100):min(len(text), idx+1500)])
                print("-" * 50)
