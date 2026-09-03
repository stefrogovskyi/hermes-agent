import glob, re

files = glob.glob('/opt/hermes/profiles/archie/**/*.*', recursive=True)
for f in files:
    if f.endswith('.py') or f.endswith('.md') or f.endswith('.log') or f.endswith('.txt'):
        try:
            content = open(f, errors='ignore').read()
            if "Правило 1:" in content or "Rule 1:" in content:
                print(f"=== MATCH: {f} ===")
                for line in content.splitlines():
                    if any(k in line for k in ["Правило 1", "Правило 2", "Правило 3", "Правило 4", "Правило 5", "Правило 6", "Правило 7", "Правило 8", "Правило 9", "Правило 10", "Правило 11", "Rule 1", "Rule 11"]):
                        print("  ", line[:150])
        except Exception as e:
            pass
