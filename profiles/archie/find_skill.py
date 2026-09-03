import json, glob, os

snapshot_path = '/opt/hermes/profiles/archie/.skills_prompt_snapshot.json'
if os.path.exists(snapshot_path):
    with open(snapshot_path) as f:
        data = json.load(f)
    print("Keys in snapshot:", list(data.keys()))

files = glob.glob('/opt/hermes/**/SKILL.md', recursive=True) + glob.glob('/opt/hermes/**/*avalanche*', recursive=True)
print("Matching files:", files)
