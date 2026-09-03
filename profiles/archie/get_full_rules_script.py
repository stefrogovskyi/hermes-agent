import re

with open('/opt/hermes/profiles/archie/cache/terminal-output/out-1788160440-3216452-28a0.log', 'r') as f:
    text = f.read()

matches = re.findall(r'(RULES|Mandatory Rules|STRICT MANDATORY RULES|CRITICAL RULES):.*?(?=\n\n|\Z)', text, re.DOTALL)
for m in matches[:5]:
    print(m)
    print("="*40)

# Also search for "1. ", "2. ", ..., "11. "
m2 = re.search(r'1\.\s+STRICT.*?(?=8-step|\Z)', text, re.DOTALL)
if m2:
    print("FOUND RULES BLOCK:")
    print(m2.group(0)[:3000])
