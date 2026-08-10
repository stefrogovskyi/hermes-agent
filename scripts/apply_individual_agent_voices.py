import yaml, os

# 1. Update Hermes Stevenson in config.yaml
config_path = r'C:\Users\Stefan\AppData\Local\hermes\config.yaml'
with open(config_path, 'r', encoding='utf-8') as f:
    cfg = yaml.safe_load(f)

cfg.setdefault('tts', {})
cfg['tts']['provider'] = 'openai'
cfg['tts'].setdefault('openai', {})
cfg['tts']['openai']['model'] = 'gpt-4o-mini-tts'
cfg['tts']['openai']['voice'] = 'onyx'

with open(config_path, 'w', encoding='utf-8') as f:
    yaml.dump(cfg, f, allow_unicode=True, sort_keys=False)

print("Updated Hermes Stevenson voice to 'onyx' in config.yaml!")

# 2. Update agent env files
agent_voices = {
    r'C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Alister Sterling\Alistair Hermes\.env.local': 'fable',
    r'C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Richard Marlowe\Richard Hermes\.env.local': 'echo',
    r'C:\Users\Stefan\My Drive\Equity\My Biz\My companies\Enlight Group\Enlight Board\Callum Vance\Callum Vance Hermes\.env.local': 'ash',
    r'C:\Users\Stefan\My Drive\Equity\My Biz\My companies\Enlight Group\Enlight Board\Liz Harper\Liz Harper Hermes\.env.local': 'nova'
}

for env_p, voice_name in agent_voices.items():
    lines = []
    if os.path.exists(env_p):
        lines = open(env_p, encoding='utf-8', errors='ignore').readlines()
    
    out_lines = []
    has_voice = False
    for line in lines:
        if line.startswith('TTS_OPENAI_VOICE='):
            out_lines.append(f"TTS_OPENAI_VOICE={voice_name}\n")
            has_voice = True
        else:
            out_lines.append(line)
            
    if not has_voice:
        out_lines.append(f"TTS_OPENAI_VOICE={voice_name}\n")
        
    with open(env_p, 'w', encoding='utf-8') as f:
        f.writelines(out_lines)
        
    print(f"Updated voice to '{voice_name}' in {env_p}")

print("ALL INDIVIDUAL AGENT VOICES APPLIED SUCCESSFULLY!")
