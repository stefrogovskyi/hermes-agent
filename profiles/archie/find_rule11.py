import re

with open('/opt/hermes/profiles/archie/cache/terminal-output/out-1788160440-3216452-28a0.log', 'r') as f:
    text = f.read()

# Find occurrences of 1. EM-DASH BAN or similar where 11. is present
matches = [m.start() for m in re.finditer(r'11\.\s+FAIR|11\.\s+NO INVENTED|11\.\s+ЗАПРЕТ|11\.\s+FACTUAL', text)]
for idx in matches:
    print("=== MATCH 11 ===")
    start = max(0, idx - 2000)
    print(text[start:idx+500])
