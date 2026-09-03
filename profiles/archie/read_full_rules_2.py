with open('/opt/hermes/profiles/archie/cache/delegation/live/deleg_cf5c3d8c/task-0.log', 'r', encoding='utf-8') as f:
    text = f.read()

# find "MANDATORY RULES:"
idx = text.find("MANDATORY RULES:")
if idx != -1:
    print(text[idx:idx+2500])
else:
    print(text[:2000])
