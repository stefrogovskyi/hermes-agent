import glob, re

for path in glob.glob('/opt/hermes/profiles/archie/**/*.py', recursive=True) + glob.glob('/opt/hermes/profiles/archie/**/*.md', recursive=True):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
            if "Rule 11" in c or "Правило 11" in c:
                matches = re.findall(r'(\d+[\.\)]\s*.*)', c)
                if len(matches) >= 8:
                    print(f"=== {path} ===")
                    for m in matches[:15]:
                        print(m)
    except:
        pass
