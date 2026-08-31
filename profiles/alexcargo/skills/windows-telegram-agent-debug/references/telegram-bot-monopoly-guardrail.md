# Telegram Bot Monopoly Single-Instance Guardrail & Token Isolation

## 1. Single-Instance Monopoly Guardrail

When running self-hosted Telegram bots on Windows, orphan background processes (`pythonw.exe`) can accumulate when watchdog tasks, terminal commands, or background runner tools spawn sub-processes. Multiple instances polling Telegram on the same token cause perpetual `HTTP Error 409: Conflict` loops.

### Verified Single-Instance Guardrail Pattern:
```python
import os, sys, psutil, subprocess

def _kill_all_other_instances(script_name):
    my_pid = os.getpid()
    for p in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if p.info['pid'] == my_pid:
                continue
            cmd = ' '.join(p.info['cmdline'] or [])
            if script_name in cmd:
                try:
                    p.kill()
                except Exception:
                    pass
        except Exception:
            pass

def _acquire_lock():
    _kill_all_other_instances("richard_bot.py")
    import atexit
    try:
        open(LOCK_FILE, "w", encoding="utf-8").write(str(os.getpid()))
        atexit.register(lambda: os.path.exists(LOCK_FILE) and open(LOCK_FILE, encoding="utf-8").read().strip() == str(os.getpid()) and os.remove(LOCK_FILE))
    except Exception as e:
        print("[Bot] Lock write note: %s" % e)
```

## 2. Token Isolation & Unmasked .env.local Loading

Sub-bots must never inherit the main orchestrator's token (`8682188433`) from parent process environment variables.

### Verified Token Loader Pattern:
```python
def _get_clean_bot_token():
    env_local = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env.local")
    if os.path.exists(env_local):
        for line in open(env_local, encoding="utf-8", errors="ignore"):
            if line.strip().startswith("TELEGRAM_BOT_TOKEN="):
                t = line.split("=", 1)[1].strip().strip('"').strip("'")
                if t and not t.endswith("***"):
                    return t
    raise RuntimeError("Valid TELEGRAM_BOT_TOKEN not found in .env.local")

BOT_TOKEN = _get_clean_bot_token()

if BOT_TOKEN.startswith("8682188433"):
    raise RuntimeError("CRITICAL SAFETY BLOCK: Sub-bot attempted to use Hermes main bot token (8682188433)!")
```

## 3. Fast Long-Polling Timeout
Use `timeout=10` with `socket_timeout=15` for long polling so TCP socket connections never linger on Telegram's servers and avoid 409 conflict loops upon network blips.
