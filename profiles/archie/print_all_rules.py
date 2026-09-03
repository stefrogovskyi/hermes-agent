import re

with open("/opt/hermes/profiles/archie/cache/terminal-output/out-1788160440-3216452-28a0.log") as f:
    text = f.read()

# Let's search for "11 rules" or "RULE 1".."RULE 11" or numbered list 1..11
m = re.search(r"(1\. ZERO EM-DASHES.*?11\. [^\n]+)", text, re.DOTALL)
if not m:
    m = re.search(r"(1\. NO EM-DASH.*?11\. [^\n]+)", text, re.DOTALL)

if m:
    print(m.group(1))
else:
    # Find any block with 1..11
    matches = re.findall(r"1\..*?11\..*?\n", text, re.DOTALL)
    if matches:
        print(matches[0][:3000])
