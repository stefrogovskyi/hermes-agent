with open('/opt/hermes/profiles/archie/cache/delegation/live/deleg_cf5c3d8c/task-0.log', 'r', encoding='utf-8') as f:
    text = f.read()

print(text[:3000])
