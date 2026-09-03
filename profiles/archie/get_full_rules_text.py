import glob

files = glob.glob('/opt/hermes/profiles/archie/cache/delegation/live/deleg_*/task-0.log')
for fpath in files:
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        txt = f.read()
        if '11 rules' in txt or 'RULES:' in txt or '1. NO EM-DASH' in txt:
            pos = txt.find('1. NO EM-DASH')
            if pos != -1:
                print(f"=== FOUND IN {fpath} ===")
                print(txt[pos-50:pos+2500])
                break
