with open('/opt/hermes/profiles/archie/cache/terminal-output/out-1788160440-3216452-28a0.log') as f:
    text = f.read()

idx = text.find("Rule 1: ZERO EM-DASHES")
if idx != -1:
    print(text[idx:idx+3500])
else:
    idx2 = text.find("STRICT 11 RULES TO FOLLOW")
    print(text[idx2:idx2+3500])
