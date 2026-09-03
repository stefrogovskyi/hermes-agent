import glob

logs = glob.glob('/opt/hermes/profiles/archie/cache/terminal-output/*.log')
for l in logs:
    with open(l) as f:
        txt = f.read()
        if "11 rules" in txt or "11 Anti-AI Copywriting Rules" in txt or "11 ПРАВИЛ" in txt:
            for line in txt.splitlines():
                if "1." in line and "EM-DASH" in line:
                    print(l)
                    idx = txt.find(line)
                    print(txt[idx:idx+3000])
                    break
