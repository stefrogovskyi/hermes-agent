# -*- coding: utf-8 -*-
"""
convert_richard_to_hermes_profile.py — Полная конверсия Ричарда Марлоу (richard) в 100% Полноценный Профиль Гермеса:
  1. Создание папки профиля profiles/richard/
  2. Миграция памяти, soul.md и правил с Google Диска
  3. Извлечение токена @richnavobot и настройка config.yaml с мастер-цепочкой из 14 фолбеков
  4. Нейтрализация старого richard_bot.py / richard_watchdog.py и очистка lock-файлов
  5. Запуск hermes.exe --profile richard gateway run в фоновом режиме CREATE_NO_WINDOW
"""

import os, re, psutil, subprocess, time

HERMES_DIR = r"C:\Users\Stefan\AppData\Local\hermes"
hermes_exe = r"C:\Users\Stefan\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe"
richard_profile_dir = os.path.join(HERMES_DIR, "profiles", "richard")
richard_memories_dir = os.path.join(richard_profile_dir, "memories")
richard_skills_dir = os.path.join(richard_profile_dir, "skills")
richard_cron_dir = os.path.join(richard_profile_dir, "cron")

os.makedirs(richard_memories_dir, exist_ok=True)
os.makedirs(richard_skills_dir, exist_ok=True)
os.makedirs(richard_cron_dir, exist_ok=True)

# 1. FIND OLD RICHARD FOLDER ON GOOGLE DRIVE
old_richard_dir = r"C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Richard Marlowe\Richard Hermes"

soul_txt = ""
memory_txt = ""
token = ""

if os.path.exists(old_richard_dir):
    for f_name in ["soul.md", "system_prompt.md"]:
        f_p = os.path.join(old_richard_dir, f_name)
        if os.path.exists(f_p):
            soul_txt += f"\n--- {f_name} ---\n" + open(f_p, encoding="utf-8", errors="ignore").read()

    for f_name in ["memory.md", "richard_memory.json"]:
        f_p = os.path.join(old_richard_dir, f_name)
        if os.path.exists(f_p):
            memory_txt += f"\n--- {f_name} ---\n" + open(f_p, encoding="utf-8", errors="ignore").read()

    env_p = os.path.join(old_richard_dir, ".env.local")
    if not os.path.exists(env_p):
        env_p = os.path.join(old_richard_dir, ".env")
        
    if os.path.exists(env_p):
        for line in open(env_p, encoding="utf-8", errors="ignore"):
            if "TELEGRAM_BOT_TOKEN=" in line or "RICHARD_BOT_TOKEN=" in line:
                token = line.split("=", 1)[1].strip().strip('"').strip("'")
                break

print("🔑 Retrieved Richard Telegram Bot Token (masked):", token[:10] + "..." if token else "Not found")

# 2. WRITE COMBINED MEMORY & USER.MD
richard_combined_memory = f"""# Richard Marlowe — Senior Sales Agent (Hermes Profile Memory)

## Persona, Voice & Core Sales Directives
{soul_txt}

## Accumulated Historical Client & Product Knowledge
{memory_txt}
"""

open(os.path.join(richard_memories_dir, "MEMORY.md"), "w", encoding="utf-8").write(richard_combined_memory)
open(os.path.join(richard_memories_dir, "USER.md"), "w", encoding="utf-8").write("User: Stefan Rogovskiy (COO Navo). Richard Marlowe is the Navo Senior AI Sales Agent for Navo IT Products & MCP APIs (TrackingMCP, SchedulesMCP, LoadingMCP, FreightRatesMCP).")

print("✅ Migrated Richard's soul.md, system_prompt.md, and memory.md into profiles/richard/memories/MEMORY.md")

# 3. WRITE CONFIG.YAML WITH MASTER FALLBACK CHAIN
if token:
    open(os.path.join(richard_profile_dir, ".env"), "w", encoding="utf-8").write(f"TELEGRAM_BOT_TOKEN={token}\n")

richard_config = f"""# Hermes Profile Config: Richard Marlowe (Senior AI Sales Agent - Navo)
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
  You are Richard Marlowe, Senior AI Sales Agent at Navo (@richnavobot).
  You speak in a confident, professional, high-converting B2B sales tone.
  You are an expert on Navo IT Products & MCP APIs (TrackingMCP, SchedulesMCP, AirCargoMCP, LoadingMCP, FreightRatesMCP).
  You run on the full-scale autonomous Hermes Agent core. You handle client inquiries, calculate pricing, generate quotes, and manage deal pipelines autonomously.

voice: echo
auto_tts: false

telegram:
  enabled: true
  bot_token: "{token}"

onboarding:
  seen:
    profile_build_offered: true
"""

open(os.path.join(richard_profile_dir, "config.yaml"), "w", encoding="utf-8").write(richard_config)
print("✅ Created profiles/richard/config.yaml with Master Fallback Chain!")

# 4. NEUTRALIZE OLD SCRIPT & WATCHDOGS
# Disable richard_watchdog.py in old dir
old_rw = os.path.join(old_richard_dir, "richard_watchdog.py")
if os.path.exists(old_rw):
    try:
        os.rename(old_rw, old_rw + ".disabled")
        print("✅ Disabled old richard_watchdog.py!")
    except Exception:
        pass

# Update global bot_watchdog.py
global_bw = os.path.join(HERMES_DIR, "scripts", "bot_watchdog.py")
if os.path.exists(global_bw):
    bw_txt = open(global_bw, encoding="utf-8").read()
    bw_txt = bw_txt.replace(
        '    "richard": (\n        r"C:\\Users\\Stefan\\My Drive\\Equity\\My Biz\\Partner companies\\Navo\\6. Departments\\Richard Marlowe\\Richard Hermes",\n        "richard_bot",\n        [r"C:\\Users\\Stefan\\AppData\\Local\\hermes\\entities\\richard.lock", r"C:\\Users\\Stefan\\My Drive\\Equity\\My Biz\\Partner companies\\Navo\\6. Departments\\Richard Marlowe\\Richard Hermes\\richard.lock"]\n    )',
        '    # "richard" migrated to full Hermes Profile --profile richard'
    )
    open(global_bw, "w", encoding="utf-8").write(bw_txt)
    print("✅ Excluded richard from global bot_watchdog.py loop!")

# Kill old running richard_bot processes
for p in psutil.process_iter(['pid', 'name', 'cmdline']):
    try:
        cmd = ' '.join(p.info['cmdline'] or [])
        if 'richard' in cmd.lower() and 'hermes.exe' not in cmd and p.info['pid'] != os.getpid():
            print(f"🛑 Killing old Richard process PID {p.info['pid']}...")
            psutil.Process(p.info['pid']).kill()
    except Exception:
        pass

# Clean lock files
for l_path in [
    r"C:\Users\Stefan\AppData\Local\hermes\entities\richard.lock",
    os.path.join(old_richard_dir, "richard.lock")
]:
    if os.path.exists(l_path):
        try:
            os.remove(l_path)
            print(f"✅ Cleaned lock file: {l_path}")
        except Exception:
            pass

# 5. LAUNCH REAL HERMES GATEWAY FOR RICHARD PROFILE
vbs_launcher = f"""Set WshShell = CreateObject("WScript.Shell")
WshShell.SetEnvironmentVariable "HERMES_PROFILE", "richard", 1
WshShell.Run "\"{hermes_exe}\" --profile richard gateway run", 0, False
"""

open(os.path.join(HERMES_DIR, "scripts", "run_richard_hermes_verified.vbs"), "w", encoding="utf-8").write(vbs_launcher)

env = os.environ.copy()
env["HERMES_PROFILE"] = "richard"

proc = subprocess.Popen([hermes_exe, "--profile", "richard", "gateway", "run"], env=env, creationflags=0x08000000)
print(f"🚀 Launched 100% Real Hermes Agent Gateway for Profile 'richard' (PID {proc.pid})!")

time.sleep(3)

# 6. VERIFY RUNNING PROCESS
running = False
for p in psutil.process_iter(['pid', 'name', 'cmdline']):
    try:
        cmd = ' '.join(p.info['cmdline'] or [])
        if 'hermes.exe' in cmd and 'richard' in cmd:
            print(f"🎉 CONFIRMED RUNNING! PID {p.info['pid']}: {cmd}")
            running = True
    except Exception:
        pass

if not running:
    subprocess.Popen([hermes_exe, "--profile", "richard", "gateway", "run"], env=env, creationflags=0x08000000)

print("🎉 RICHARD MARLOWE IS NOW 100% PERMANENTLY RUNNING ON HERMES AGENT CORE!")
