import re

with open('/opt/hermes/profiles/archie/cache/terminal-output/out-1788160440-3216452-28a0.log', 'r') as f:
    text = f.read()

matches = [m.start() for m in re.finditer(r'10\.', text)]
for idx in matches[:5]:
    print("=== MATCH 10 ===")
    print(text[idx-500:idx+1000])
