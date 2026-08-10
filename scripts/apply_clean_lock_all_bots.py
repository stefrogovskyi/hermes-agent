# -*- coding: utf-8 -*-
"""
apply_clean_lock_all_bots.py — Идеальный, устойчивый PID-лок для всех 5 ботов.
"""

import os, sys, re

bots = {
    "richard": (r"C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Richard Marlowe\Richard Hermes", "richard_bot.py", "richard.lock"),
    "alistair": (r"C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Alister Sterling\Alistair Hermes", "alistair_bot.py", "alistair.lock"),
    "callum": (r"C:\Users\Stefan\My Drive\Equity\My Biz\My companies\Enlight Group\Enlight Board\Callum Vance\Callum Vance Hermes", "callum_vance_bot.py", "callum.lock"),
    "liz": (r"C:\Users\Stefan\My Drive\Equity\My Biz\My companies\Enlight Group\Enlight Board\Liz Harper\Liz Harper Hermes", "liz_harper_bot.py", "liz.lock"),
    "ben": (r"C:\Users\Stefan\My Drive\Equity\My Biz\My companies\Enlight Group\Avalanche Agency\Team\Ben Jett\Ben Jett Hermes", "ben_jett_bot.py", "ben.lock")
}

print("=== 🚀 ВНЕДРЕНИЕ ИДЕАЛЬНОГО PID-ЛОКА ДЛЯ ВСЕХ 5 БОТОВ ===")

for name, (bdir, script_file, lock_name) in bots.items():
    path = os.path.join(bdir, script_file)
    if not os.path.exists(path):
        continue
        
    text = open(path, encoding="utf-8", errors="ignore").read()
    
    clean_lock_code = f'''LOCK_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "{lock_name}")

def _is_bot_running_pid(pid):
    if not pid or pid == os.getpid():
        return False
    try:
        import psutil
        if psutil.pid_exists(pid):
            p = psutil.Process(pid)
            cmd = " ".join(p.cmdline() or [])
            if "{script_file}" in cmd:
                return True
    except Exception:
        pass
    return False

def _acquire_lock():
    if os.path.exists(LOCK_FILE):
        try:
            old_pid = int(open(LOCK_FILE, encoding="utf-8").read().strip())
            if _is_bot_running_pid(old_pid):
                print("[{name.capitalize()}] Bot process %d is already running — exiting duplicate." % old_pid)
                sys.exit(0)
        except Exception:
            pass
    import atexit
    open(LOCK_FILE, "w", encoding="utf-8").write(str(os.getpid()))
    atexit.register(lambda: os.path.exists(LOCK_FILE) and open(LOCK_FILE, encoding="utf-8").read().strip() == str(os.getpid()) and os.remove(LOCK_FILE))'''

    text = re.sub(
        r'LOCK_FILE = .*?def _acquire_lock\(\):.*?(?=\n\n# |\ndef |\nclass |HISTORY_FILE)',
        clean_lock_code.strip() + "\n\n",
        text,
        flags=re.DOTALL
    )
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
        
    print(f"✅ В боте {name.upper()} обновлен чистый PID-лок!")
