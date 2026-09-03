import glob, re

logs = glob.glob('/opt/hermes/profiles/archie/cache/terminal-output/*.log')
for l in logs:
    with open(l) as f:
        txt = f.read()
        m = re.search(r'(1\. (?:STRICT ZERO|ABSOLUTE|NO) EM-DASH.*?(?=11\.).*?11\.[^\n]+)', txt, re.DOTALL | re.IGNORECASE)
        if m:
            print("MATCH IN", l)
            print(m.group(0))
            break
