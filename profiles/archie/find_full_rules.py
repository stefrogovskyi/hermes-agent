import glob, os, re

files = glob.glob('/opt/hermes/profiles/archie/**/*.log', recursive=True) + \
        glob.glob('/opt/hermes/profiles/archie/**/*.txt', recursive=True) + \
        glob.glob('/opt/hermes/profiles/archie/**/*.md', recursive=True) + \
        glob.glob('/opt/hermes/profiles/archie/**/*.py', recursive=True)

for path in files:
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if "1. EM-DASH BAN" in content or "1. EM-DASH" in content or "Rule 1: EM-DASH" in content:
                m = re.search(r'(1\. EM-DASH.*?(?:11\..*?\n|\n\n))', content, re.DOTALL)
                if m:
                    print("FOUND IN:", path)
                    print(m.group(1))
                    break
    except Exception as e:
        pass
