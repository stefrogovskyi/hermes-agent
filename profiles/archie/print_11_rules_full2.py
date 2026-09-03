with open('/opt/hermes/profiles/archie/cache/terminal-output/out-1788160440-3216452-28a0.log', 'r') as f:
    text = f.read()

idx = text.find('Mandatory Rules:')
while idx != -1:
    print("--- FOUND AT ---", idx)
    print(text[idx:idx+1500])
    idx = text.find('Mandatory Rules:', idx+1)
