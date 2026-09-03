with open('/opt/hermes/profiles/archie/cache/terminal-output/out-1788160440-3216452-28a0.log') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'11 Anti-AI Copywriting Rules|8-step|8-ШАГОВ', text)]
for m in matches[:5]:
    print("--- MATCH ---")
    print(text[m-200:m+2500])
