import glob, re

for filepath in glob.glob("/opt/hermes/profiles/archie/cache/terminal-output/*.log"):
    with open(filepath) as f:
        text = f.read()
    if "Rule 11" in text or "11." in text or "Rule 10" in text:
        m = re.findall(r'(Rule 1:.*?Rule 11:[^\n]+)', text, re.DOTALL)
        if m:
            print(f"Match in {filepath}:")
            print(m[0])
            break
        m2 = re.findall(r'(1\. STRICT ZERO EM-DASHES.*?11\.[^\n]+)', text, re.DOTALL)
        if m2:
            print(f"Match 2 in {filepath}:")
            print(m2[0])
            break
