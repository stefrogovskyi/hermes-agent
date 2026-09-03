import glob

files = glob.glob('/opt/hermes/profiles/archie/cache/terminal-output/*.log') + glob.glob('/opt/hermes/profiles/archie/*.py') + glob.glob('/opt/hermes/profiles/archie/*.json')
for file in files:
    try:
        with open(file, 'r', errors='ignore') as f:
            content = f.read()
            if 'Правило 1' in content or '1. Запрет em-dash' in content or 'Rule 1' in content:
                print("FOUND RULES IN:", file)
                idx = content.find('1. ')
                if idx != -1:
                    print(content[idx:idx+2500])
                    break
    except Exception as e:
        pass
