with open('/opt/hermes/profiles/archie/cache/delegation/live/deleg_c083a1ce/task-0.log', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

idx = text.find('11 ПРАВИЛ')
if idx != -1:
    print(text[idx:idx+4000])
else:
    print(text[:4000])
