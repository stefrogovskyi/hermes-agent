import os, json

print("Searching for skill content...")
for root, dirs, files in os.walk('/opt/hermes'):
    for f in files:
        if f.endswith('.md') or f.endswith('.json'):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    if 'contrastive negation' in content.lower():
                        print('Found in:', path)
            except Exception as e:
                pass
