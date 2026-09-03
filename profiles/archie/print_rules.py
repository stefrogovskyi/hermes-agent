with open('/opt/hermes/profiles/archie/cache/terminal-output/out-1788160440-3216452-28a0.log') as f:
    txt = f.read()

idx = txt.find("1. STRICT ZERO EM-DASHES")
if idx != -1:
    print(txt[idx:idx+3500])
