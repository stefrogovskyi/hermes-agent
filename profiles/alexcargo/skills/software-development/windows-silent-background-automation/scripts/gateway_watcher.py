#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
gateway_watcher.py - silent watchdog for the Hermes gateway (NO black windows).

Launched via pythonw (windowless) or a scheduled-task/cron. Does NOT touch a
live gateway directly - it only checks liveness and relaunches the gateway
hidden (pythonw, CREATE_NO_WINDOW) when the process is gone, EVEN if the
Hermes Desktop GUI is open.

Liveness check uses ctypes (OpenProcess on the pid in gateway_state.json) -
NEVER shells out to powershell.exe / tasklist (those spawn a visible conhost
every loop tick). Lock file guards against duplicate instances.

Alerts Stefan in Telegram if Telegram stays disconnected > TG_DOWN_S.
"""
import os
import time
import json
import ctypes
import subprocess
import urllib.request
import urllib.error

HERMES_HOME = os.environ.get("HERMES_HOME") or os.path.expanduser(
    r"~\\AppData\\Local\\hermes"
)
STATE = os.path.join(HERMES_HOME, "gateway_state.json")
ENV = os.path.join(HERMES_HOME, ".env")
LOCK = os.path.join(HERMES_HOME, "scripts", "gateway_watcher.lock")
LOG = os.path.join(HERMES_HOME, "scripts", "gateway_watcher.log")

# BASE pythonw (NOT venv/uv-launcher - that re-execs a conhost)
PY_EXE = r"C:\Users\Stefan\AppData\Roaming\uv\python\cpython-3.11-windows-x86_64-none\pythonw.exe"
GATEWAY_CMD = [PY_EXE, "-m", "hermes_cli.main", "gateway", "run"]

CHECK_INTERVAL_S = 30
TG_DOWN_S = 120
ALERT_COOLDOWN_S = 600

kernel32 = ctypes.windll.kernel32


def _pid_alive(pid):
    h = kernel32.OpenProcess(0x0400, False, pid)  # PROCESS_QUERY_INFORMATION
    if h:
        kernel32.CloseHandle(h)
        return True
    return False


def gateway_process_alive():
    """Authoritative: gateway writes its own pid into gateway_state.json."""
    try:
        with open(STATE, encoding="utf-8") as f:
            d = json.load(f)
        pid = d.get("pid")
        if pid and _pid_alive(int(pid)):
            return True
    except Exception:
        pass
    return False


def _acquire_lock():
    try:
        if os.path.exists(LOCK):
            try:
                old = int(open(LOCK, encoding="utf-8").read().strip() or "0")
            except Exception:
                old = 0
            if old and _pid_alive(old):
                return False
            try:
                os.remove(LOCK)
            except Exception:
                pass
    except Exception:
        pass
    try:
        open(LOCK, "w", encoding="utf-8").write(str(os.getpid()))
        return True
    except Exception:
        return False


def _release_lock():
    try:
        if os.path.exists(LOCK) and open(LOCK, encoding="utf-8").read().strip() == str(os.getpid()):
            os.remove(LOCK)
    except Exception:
        pass


def log(msg):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] {msg}\n")
    except Exception:
        pass


def _read_env(key):
    try:
        with open(ENV, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith(key + "="):
                    return line.split("=", 1)[1].strip().strip('"')
    except Exception:
        pass
    return os.environ.get(key, "")


def send_alert(text):
    token = _read_env("TELEGRAM_BOT_TOKEN")
    chat = _read_env("STEFAN_CHAT_ID") or "330656040"
    if not token:
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = json.dumps({"chat_id": chat, "text": text}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req, timeout=15)
    except Exception as e:
        log(f"alert send failed: {e}")


def restart_gateway(reason):
    log(f"RESTART gateway ({reason})")
    try:
        flags = 0x00000008 | 0x08000000  # DETACHED | CREATE_NO_WINDOW
        subprocess.Popen(
            GATEWAY_CMD, cwd=HERMES_HOME,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            creationflags=flags, close_fds=True,
        )
        log("gateway restart command issued")
    except Exception as e:
        log(f"gateway restart FAILED: {e}")


def gateway_state_info():
    try:
        st = os.stat(STATE)
        mtime = st.st_mtime
    except Exception:
        return None, None, None, None
    try:
        with open(STATE, encoding="utf-8") as f:
            d = json.load(f)
    except Exception:
        return "unreadable", None, mtime, None
    state = d.get("gateway_state")
    tg = (d.get("platforms") or {}).get("telegram", {}).get("state")
    return state, tg, mtime, d


def main():
    if not _acquire_lock():
        return
    try:
        last_alert = 0
        tg_down_since = None
        log("watcher started")
        while True:
            try:
                state, tg, mtime, d = gateway_state_info()
                now = time.time()
                need_restart = False
                reason = ""
                if not gateway_process_alive():
                    need_restart = True
                    reason = "no gateway run process"
                if not need_restart:
                    if tg == "connected":
                        tg_down_since = None
                    else:
                        if tg_down_since is None:
                            tg_down_since = now
                        down_for = now - tg_down_since
                        if down_for > TG_DOWN_S:
                            if now - last_alert > ALERT_COOLDOWN_S:
                                send_alert(
                                    f"⚠️ Hermes: Telegram {tg or 'down'} "
                                    f"{int(down_for)}s. Gateway перезапускаю."
                                )
                                last_alert = now
                                log(f"TELEGRAM down {int(down_for)}s -> alert sent")
                            need_restart = True
                            reason = reason or f"telegram {tg}"
                if need_restart:
                    restart_gateway(reason)
                    tg_down_since = None
                    time.sleep(20)
                else:
                    time.sleep(CHECK_INTERVAL_S)
            except Exception as e:
                log(f"loop error: {e}")
                time.sleep(CHECK_INTERVAL_S)
    finally:
        _release_lock()


if __name__ == "__main__":
    main()
