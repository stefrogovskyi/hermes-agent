import glob
import re

files = glob.glob('/opt/hermes/profiles/archie/cache/terminal-output/*.log') + glob.glob('/opt/hermes/profiles/archie/*.md')
for file in files:
    with open(file, 'r', errors='ignore') as f:
        content = f.read()
        if 'Правило 1' in content or 'Rule 1' in content or '1. Запрет em-dash' in content:
            print("Found 11 rules in", file)
            match = re.search(r'(1\. (?:Запрет|No em-dash).{200,3000})', content, re.DOTALL)
            if match:
                print("--- RULES MATCH ---")
                print(match.group(1)[:2500])
                break
