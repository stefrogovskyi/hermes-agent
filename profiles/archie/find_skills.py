import os

for root, dirs, files in os.walk('/opt/hermes'):
    for f in files:
        if f == 'SKILL.md' or 'avalanche' in f:
            print(os.path.join(root, f))
