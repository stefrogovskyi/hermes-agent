with open('/opt/hermes/profiles/archie/cache/terminal-output/out-1788160440-3216452-28a0.log', 'r') as f:
    text = f.read()

idx = text.find('strictly following all 11 Anti-AI Copywriting Rules:')
if idx != -1:
    print(text[idx:idx+2500])
