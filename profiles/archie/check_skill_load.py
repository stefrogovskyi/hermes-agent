import json
import subprocess
import sys

def get_skill():
    try:
        with open('/opt/hermes/profiles/archie/.skills_prompt_snapshot.json') as f:
            data = json.load(f)
        for k, v in data.items():
            if isinstance(v, dict):
                for sk_path, content in v.items():
                    if 'avalanche-copywriting' in sk_path:
                        return content
    except Exception as e:
        print("Snapshot error:", e)
    
    # Try searching system skill files
    cmd = ["find", "/opt/hermes", "-name", "SKILL.md", "-o", "-name", "*.md"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    for p in res.stdout.splitlines():
        if 'avalanche-copywriting' in p or 'copywriting' in p:
            try:
                with open(p) as f:
                    c = f.read()
                    if '8-ШАГ' in c or '8-STEP' in c or 'EM-DASH' in c or 'em-dash' in c or '11' in c or 'Anti-AI' in c:
                        return c
            except:
                pass
    return None

skill_content = get_skill()
print("SKILL LENGTH:", len(skill_content) if skill_content else "NOT FOUND")
if skill_content:
    print("SKILL PREVIEW:", skill_content[:500])
