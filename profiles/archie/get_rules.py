import re

with open('/opt/hermes/profiles/archie/cache/terminal-output/out-1788309323-3652763-5580.log', 'r', encoding='utf-8') as f:
    text = f.read()

# Look for 'STRICT RULES TO FOLLOW' or '11 rules'
matches = [m.start() for m in re.finditer(r'STRICT RULES TO FOLLOW|11 rules|8-ШАГ', text)]
for idx in matches[:5]:
    print("--- MATCH ---")
    print(text[idx:idx+1500])

