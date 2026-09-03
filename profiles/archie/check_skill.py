import json
with open('/opt/hermes/profiles/archie/.skills_prompt_snapshot.json') as f:
    data = json.load(f)
for k, v in data.items():
    if 'avalanche' in k or 'copywriting' in k:
        print('Key:', k)
        print('Length:', len(v))
        with open('avalanche_skill_body.txt', 'w') as f_out:
            f_out.write(v)
