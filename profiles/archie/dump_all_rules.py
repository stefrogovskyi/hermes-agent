import re

with open('/opt/hermes/profiles/archie/cache/terminal-output/out-1788160440-3216452-28a0.log', 'r') as f:
    text = f.read()

matches = [m.start() for m in re.finditer(r'EM-DASH BAN', text)]
for idx in matches:
    print("--- MATCH ---")
    print(text[max(0, idx-50):idx+2500])
