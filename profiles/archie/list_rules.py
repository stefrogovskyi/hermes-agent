import glob

for fname in glob.glob('/opt/hermes/profiles/archie/*.py'):
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    if 'Rule 11' in content or 'Rule 1:' in content:
        print(f"=== {fname} ===")
        for line in content.splitlines():
            if any(f"Rule {i}" in line or f"{i}." in line for i in range(1, 12)):
                if len(line.strip()) > 5 and ('em-dash' in line.lower() or 'fact' in line.lower() or 'cliche' in line.lower() or 'negation' in line.lower() or 'rule' in line.lower()):
                    print("  ", line.strip()[:120])
