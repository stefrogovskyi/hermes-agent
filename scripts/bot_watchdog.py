
# === TOKEN ISOLATION GUARDRAIL ===
HERMES_MAIN_TOKEN_PREFIX = "8682188433"

def _verify_bot_token_safety(bot_name, bot_script_path):
    """Проверяет, что скрипт бота не использует главный токен Гермеса."""
    if os.path.exists(bot_script_path):
        script_txt = open(bot_script_path, encoding='utf-8', errors='ignore').read()
        if HERMES_MAIN_TOKEN_PREFIX in script_txt:
            print(f"[Watchdog GUARDRAIL ERROR] {bot_name} contains main Hermes token {HERMES_MAIN_TOKEN_PREFIX}! Blocking start.")
            return False
    return True


# -*- coding: utf-8 -*-
"""
bot_watchdog.py — Строгий реальный сторожевой заслон всей экосистемы ботов (Richard, Alistair, Callum, Liz, Ben).
Проверяет НЕ ТОЛЬКО PID в Task Manager, но и Выполняет РЕАЛЬНЫЙ СМЫСЛОВОЙ ТЕСТ ГЕНЕРАЦИИ (run_agent('ping')).
При любой ошибке или задержке — моментально реанимирует бота!
"""

import os, sys, time, json, subprocess, psutil

HERMES_DIR = r"C:\Users\Stefan\AppData\Local\hermes"
LOG_FILE = os.path.join(HERMES_DIR, "bot_watchdog.log")

bot_configs = {
    # "liz" migrated to full Hermes Profile --profile liz,
    # "ben" migrated to full Hermes Profile --profile ben
    # "callum" migrated to full Hermes Profile --profile callum
    # "alistair" migrated to full Hermes Profile --profile alistair,
    # "richard" migrated to full Hermes Profile --profile richard
}

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] [Watchdog] {msg}"
    print(formatted, flush=True)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
    except Exception:
        pass

def restart_bot(name, bot_dir, bot_mod):
    target_script = f"{bot_mod}.py"
    killed_count = 0
    
    # 1. Kill ALL processes matching the script name on the entire system
    for p in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmd = ' '.join(p.info['cmdline'] or [])
            if target_script in cmd:
                log(f"Killing process {name} (PID {p.info['pid']})...")
                psutil.Process(p.info['pid']).kill()
                killed_count += 1
        except Exception:
            pass

    # 2. Clean up lock files
    lock_paths = bot_configs[name][2]
    for lock_p in lock_paths:
        if os.path.exists(lock_p):
            try:
                os.remove(lock_p)
            except Exception:
                pass

    # 3. Verify safety guardrail
    script_path = os.path.join(bot_dir, f"{bot_mod}.py")
    if not _verify_bot_token_safety(name, script_path):
        log(f"❌ CANNOT START {name.upper()}: Failed token safety guardrail check!")
        return

    # 4. Spawn single clean process
    pythonw_exe = r"C:\Users\Stefan\AppData\Roaming\uv\python\cpython-3.11-windows-x86_64-none\pythonw.exe"
    if not os.path.exists(pythonw_exe):
        pythonw_exe = sys.executable.replace("python.exe", "pythonw.exe")

    p = subprocess.Popen(
        [pythonw_exe, script_path],
        cwd=bot_dir,
        creationflags=0x08000000
    )
    log(f"🚀 RESTARTED BOT {name.upper()} SILENTLY VIA PYTHONW (PID {p.pid})")
    time.sleep(2)


def test_and_heal_bots():
    log("=== STARTING REAL SEMANTIC LLM HEALTH CHECK FOR ALL 5 BOTS ===")
    
    for name, (bot_dir, mod_name, lock_paths) in bot_configs.items():
        need_restart = False
        
        # 1. Check PID across possible lock paths
        pid = None
        found_alive = False
        for lock_p in lock_paths:
            if os.path.exists(lock_p):
                try:
                    pid = int(open(lock_p, encoding="utf-8").read().strip())
                    if psutil.pid_exists(pid):
                        found_alive = True
                        break
                except Exception:
                    pass
                    
        if not found_alive:
            log(f"❌ {name.upper()} PID is DEAD or missing lock")
            need_restart = True

        # 2. Check Real LLM Response (if PID alive)
        if not need_restart:
            try:
                sys.path.insert(0, bot_dir)
                env_p = os.path.join(bot_dir, ".env.local")
                if os.path.exists(env_p):
                    for line in open(env_p, encoding="utf-8", errors="ignore"):
                        if line.strip() and not line.startswith("#") and "=" in line:
                            k, v = line.split("=", 1)
                            os.environ[k.strip()] = v.strip().strip('"').strip("'")

                mod = __import__(mod_name)
                sys_prompt = getattr(mod, f"{name.upper()}_SYSTEM", "")
                
                t0 = time.time()
                res = mod.run_agent("ping test", system=sys_prompt)
                t1 = time.time()

                res_str = res.get("content", "") if isinstance(res, dict) else str(res)

                if not res_str or "режиме настройки" in res_str or "lost the line" in res_str or "не подключён" in res_str:
                    log(f"⚠️ {name.upper()} RETURNED STENCIL ERROR: '{res_str[:60]}'")
                    need_restart = True
                else:
                    log(f"✅ {name.upper()} SEMANTIC TEST PASSED ({t1-t0:.2f}s)! Sample: '{res_str[:50]}'")
            except Exception as e:
                log(f"❌ {name.upper()} SEMANTIC TEST FAILED: {e}")
                need_restart = True

        if need_restart:
            restart_bot(name, bot_dir, mod_name)

if __name__ == "__main__":
    test_and_heal_bots()
