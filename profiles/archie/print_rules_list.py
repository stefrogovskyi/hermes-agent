with open('/opt/hermes/profiles/archie/cache/terminal-output/out-1788160440-3216452-28a0.log', 'r') as f:
    text = f.read()

idx = text.find('STRICT MANDATORY RULES (DO NOT VIOLATE):')
if idx != -1:
    print(text[idx:idx+2500])
