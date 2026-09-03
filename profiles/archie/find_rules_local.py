import glob, re

for fpath in glob.glob('/opt/hermes/profiles/archie/*'):
    if fpath.endswith('.py') or fpath.endswith('.md'):
        with open(fpath, errors='ignore') as f:
            txt = f.read()
            if 'EM-DASH' in txt and 'RULE' in txt:
                print(f"=== {fpath} ===")
                for line in txt.splitlines():
                    if any(k in line for k in ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.', '11.']):
                        print(line[:120])
