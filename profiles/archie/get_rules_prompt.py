import glob
import re

files = glob.glob('/opt/hermes/profiles/archie/cache/terminal-output/*.log')
for file in files:
    with open(file, 'r', errors='ignore') as f:
        content = f.read()
        if 'Правило 1:' in content or 'Rule 1:' in content or 'em-dash' in content:
            idx = content.find('8-ШАГОВОМУ')
            if idx != -1:
                print("FOUND AT INDEX", idx, "in", file)
                print(content[idx:idx+3500])
                break
