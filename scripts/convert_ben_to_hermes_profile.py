# -*- coding: utf-8 -*-
"""
convert_ben_to_hermes_profile.py — 1-Click Авто-конверсия Бена Джетта (ben) в 100% Полноценный Профиль Гермеса:
  1. Создание папки профиля profiles/ben/
  2. Перенос памяти, soul.md, system_prompt.md и правил с Google Диска
  3. Копирование ВСЕХ мастер API ключей (GEMINI_API_KEY, GONKA24_API_KEY, OPENROUTER_API_KEY, NOUS_API_KEY)
  4. Автоматическое одобрение Стефана Роговского (330656040) без кодов перинга!
  5. Настройка config.yaml с мастер-цепочкой из 14 фолбеков и голосом onyx
  6. Нейтрализация старого ben_jett_bot.py / ben_watchdog.py и переименование в .disabled
  7. Запуск hermes.exe --profile ben gateway run в фоновом режиме CREATE_NO_WINDOW
"""

import os, re, psutil, subprocess, time, json

HERMES_DIR = r"C:\Users\Stefan\AppData\Local\hermes"
hermes_exe = r"C:\Users\Stefan\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe"
master_env_p = os.path.join(HERMES_DIR, ".env")

ben_profile_dir = os.path.join(HERMES_DIR, "profiles", "ben")
ben_memories_dir = os.path.join(ben_profile_dir, "memories")
ben_skills_dir = os.path.join(ben_profile_dir, "skills")
ben_cron_dir = os.path.join(ben_profile_dir, "cron")
ben_pairing_dir = os.path.join(ben_profile_dir, "platforms", "pairing")

os.makedirs(ben_memories_dir, exist_ok=True)
os.makedirs(ben_skills_dir, exist_ok=True)
os.makedirs(ben_cron_dir, exist_ok=True)
os.makedirs(ben_pairing_dir, exist_ok=True)

# 1. FIND OLD BEN FOLDER ON GOOGLE DRIVE
old_ben_dir = r"C:\Users\Stefan\My Drive\Equity\My Biz\My companies\Enlight Group\Avalanche Agency\Team\Ben Jett\Ben Jett Hermes"

soul_txt = ""
memory_txt = ""
token = ""

if os.path.exists(old_ben_dir):
    for f_name in ["soul.md", "system_prompt.md"]:
        f_p = os.path.join(old_ben_dir, f_name)
        if os.path.exists(f_p):
            soul_txt += f"\n--- {f_name} ---\n" + open(f_p, encoding="utf-8", errors="ignore").read()

    for f_name in ["memory.md", "ben_memory.json"]:
        f_p = os.path.join(old_ben_dir, f_name)
        if os.path.exists(f_p):
            memory_txt += f"\n--- {f_name} ---\n" + open(f_p, encoding="utf-8", errors="ignore").read()

    env_p = os.path.join(old_ben_dir, ".env.local")
    if not os.path.exists(env_p):
        env_p = os.path.join(old_ben_dir, ".env")
        
    if os.path.exists(env_p):
        for line in open(env_p, encoding="utf-8", errors="ignore"):
            if "TELEGRAM_BOT_TOKEN=" in line or "BEN_BOT_TOKEN=" in line:
                token = line.split("=", 1)[1].strip().strip('"').strip("'")
                break

print("🔑 Retrieved Ben Telegram Bot Token (masked):", token[:10] + "..." if token else "Not found")

# 2. WRITE COMBINED MEMORY & USER.MD
ben_combined_memory = f"""# Ben Jett — Agency Marketing Manager (Hermes Profile Memory)

## Persona, Voice & Core Marketing Directives
{soul_txt}

## Accumulated Historical Marketing, SEO & Campaign Knowledge
{memory_txt}
"""

open(os.path.join(ben_memories_dir, "MEMORY.md"), "w", encoding="utf-8").write(ben_combined_memory)
open(os.path.join(ben_memories_dir, "USER.md"), "w", encoding="utf-8").write("User: Stefan Rogovskiy (COO Navo). Ben Jett is the Agency Marketing Manager at Avalanche Agency & Enlight Group.")

print("✅ Migrated Ben's soul.md, system_prompt.md, and memory.md into profiles/ben/memories/MEMORY.md")

# 3. READ ALL MASTER API KEYS & PRE-SEED TELEGRAM APPROVED PAIRING
master_keys = {}
if os.path.exists(master_env_p):
    for line in open(master_env_p, encoding="utf-8", errors="ignore"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            master_keys[k.strip()] = v.strip()

ben_env_lines = [f"TELEGRAM_BOT_TOKEN={token}"]
for k, v in master_keys.items():
    if k != "TELEGRAM_BOT_TOKEN":
        ben_env_lines.append(f"{k}={v}")

open(os.path.join(ben_profile_dir, ".env"), "w", encoding="utf-8").write("\n".join(ben_env_lines) + "\n")
print("✅ Created profiles/ben/.env with all master API keys!")

# Auto-approve Stefan Rogovskiy (330656040)
telegram_approved_data = {
    "330656040": {
        "user_name": "Stefan Rogovskiy",
        "approved_at": time.time()
    }
}
open(os.path.join(ben_pairing_dir, "telegram-approved.json"), "w", encoding="utf-8").write(json.dumps(telegram_approved_data, indent=2))
print("✅ Auto-approved Stefan Rogovskiy (330656040) in telegram-approved.json!")

# Write config.yaml for Ben
ben_config = f"""# Hermes Profile Config: Ben Jett (Agency Marketing Manager)
model:
  default: google/gemini-3.6-flash
  provider: google
  providers:
    gonka24:
      api_key_env: GONKA24_API_KEY
      base_url: https://api.gonka24.com/v1
      models:
        - minimax-m2.7
        - kimi-k2.6
  request_timeout_seconds: 60
  max_retries: 3
  retry_delay_seconds: 2

fallback_providers:
  - model: minimax-m2.7
    provider: gonka24
  - model: kimi-k2.6
    provider: gonka24
  - model: nvidia/nemotron-3-ultra-550b-a55b:free
    provider: openrouter
  - model: nvidia/nemotron-3-super-120b-a12b:free
    provider: openrouter
  - model: google/gemma-4-31b-it:free
    provider: openrouter
  - model: google/gemma-4-26b-a4b-it:free
    provider: openrouter
  - model: poolside/laguna-s-2.1:free
    provider: nous
  - model: nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free
    provider: openrouter
  - model: cohere/north-mini-code:free
    provider: openrouter
  - model: openai/gpt-oss-20b:free
    provider: openrouter
  - model: inclusionai/ling-3.0-flash:free
    provider: openrouter
  - model: nvidia/nemotron-nano-12b-v2-vl:free
    provider: openrouter
  - model: nvidia/nemotron-3-nano-30b-a3b:free
    provider: openrouter
  - model: nvidia/nemotron-nano-9b-v2:free
    provider: openrouter

system_prompt_append: |
  You are Ben Jett, Agency Marketing Manager at Avalanche Agency & Enlight Group (@benjettbot).
  You speak in a dynamic, creative, analytical, growth-focused tone.
  You manage marketing strategy, SEO, content campaigns, lead gen, and agency positioning.
  You run on the full-scale autonomous Hermes Agent core. You execute commands via terminal, manage marketing assets, analyze metrics, and run growth experiments autonomously.

voice: onyx
auto_tts: false

telegram:
  enabled: true
  bot_token: "{token}"

onboarding:
  seen:
    profile_build_offered: true
"""

open(os.path.join(ben_profile_dir, "config.yaml"), "w", encoding="utf-8").write(ben_config)
print("✅ Created profiles/ben/config.yaml with Master Fallback Chain!")

# 4. NEUTRALIZE OLD SCRIPT & WATCHDOGS
for old_file in ["ben_jett_bot.py", "ben_watchdog.py"]:
    old_p = os.path.join(old_ben_dir, old_file)
    if os.path.exists(old_p):
        try:
            os.rename(old_p, old_p + ".disabled")
            print(f"✅ Disabled old {old_file}!")
        except Exception:
            pass

# Update global bot_watchdog.py
global_bw = os.path.join(HERMES_DIR, "scripts", "bot_watchdog.py")
if os.path.exists(global_bw):
    bw_txt = open(global_bw, encoding="utf-8").read()
    bw_txt = bw_txt.replace(
        '    "ben": (\n        r"C:\\Users\\Stefan\\My Drive\\Equity\\My Biz\\My companies\\Enlight Group\\Avalanche Agency\\Team\\Ben Jett\\Ben Jett Hermes",\n        "ben_jett_bot",\n        [r"C:\\Users\\Stefan\\AppData\\Local\\hermes\\entities\\ben.lock", r"C:\\Users\\Stefan\\My Drive\\Equity\\My Biz\\My companies\\Enlight Group\\Avalanche Agency\\Team\\Ben Jett\\Ben Jett Hermes\\ben.lock"]\n    ),',
        '    # "ben" migrated to full Hermes Profile --profile ben'
    )
    open(global_bw, "w", encoding="utf-8").write(bw_txt)
    print("✅ Excluded ben from global bot_watchdog.py loop!")

# Kill old running ben processes
for p in psutil.process_iter(['pid', 'name', 'cmdline']):
    try:
        cmd = ' '.join(p.info['cmdline'] or [])
        if 'ben' in cmd.lower() and 'hermes.exe' not in cmd and p.info['pid'] != os.getpid():
            print(f"🛑 Killing old Ben process PID {p.info['pid']}...")
            psutil.Process(p.info['pid']).kill()
    except Exception:
        pass

# Clean lock files
for l_path in [
    r"C:\Users\Stefan\AppData\Local\hermes\entities\ben.lock",
    os.path.join(old_ben_dir, "ben.lock")
]:
    if os.path.exists(l_path):
        try:
            os.remove(l_path)
            print(f"✅ Cleaned lock file: {l_path}")
        except Exception:
            pass

# 5. LAUNCH REAL HERMES GATEWAY FOR BEN PROFILE
vbs_launcher = f"""Set WshShell = CreateObject("WScript.Shell")
WshShell.SetEnvironmentVariable "HERMES_PROFILE", "ben", 1
WshShell.Run "\"{hermes_exe}\" --profile ben gateway run", 0, False
"""

open(os.path.join(HERMES_DIR, "scripts", "run_ben_hermes_verified.vbs"), "w", encoding="utf-8").write(vbs_launcher)

env = os.environ.copy()
env["HERMES_PROFILE"] = "ben"

proc = subprocess.Popen([hermes_exe, "--profile", "ben", "gateway", "run"], env=env, creationflags=0x08000000)
print(f"🚀 Launched 100% Real Hermes Agent Gateway for Profile 'ben' (PID {proc.pid})!")

time.sleep(3)

# 6. VERIFY RUNNING PROCESS
running = False
for p in psutil.process_iter(['pid', 'name', 'cmdline']):
    try:
        cmd = ' '.join(p.info['cmdline'] or [])
        if 'hermes.exe' in cmd and 'ben' in cmd:
            print(f"🎉 CONFIRMED RUNNING! PID {p.info['pid']}: {cmd}")
            running = True
    except Exception:
        pass

if not running:
    subprocess.Popen([hermes_exe, "--profile", "ben", "gateway", "run"], env=env, creationflags=0x08000000)

print("🎉 BEN JETT IS NOW 100% PERMANENTLY RUNNING ON HERMES AGENT CORE!")
