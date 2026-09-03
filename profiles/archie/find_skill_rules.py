import os, glob

for log in glob.glob("/opt/hermes/profiles/archie/cache/terminal-output/*.log"):
    try:
        with open(log) as f:
            content = f.read()
            if "Правило 1" in content or "11 правил" in content or "Rule 1" in content:
                print(f"Found in {log}")
                # print snippet
                idx = content.find("1. ")
                if idx != -1:
                    print(content[idx:idx+2000])
                    break
    except Exception as e:
        pass
