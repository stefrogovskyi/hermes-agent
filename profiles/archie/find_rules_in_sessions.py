import glob, json, re

for fpath in glob.glob('/opt/hermes/profiles/archie/sessions/*.json'):
    with open(fpath) as f:
        txt = f.read()
        if '11 rules' in txt or '11 правил' in txt:
            matches = [m.start() for m in re.finditer(r'1\. NO EM-DASH|1\. ZERO EM-DASH|MANDATORY RULES|11 rules', txt)]
            for m in matches[:3]:
                print(f"=== MATCH IN {fpath} AT {m} ===")
                print(txt[m:m+1500])
                break
