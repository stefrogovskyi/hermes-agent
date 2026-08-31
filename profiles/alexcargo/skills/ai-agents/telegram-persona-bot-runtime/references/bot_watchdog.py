#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
bot_watchdog.py — keep a stdlib Telegram persona bot alive 24/7.

Pattern (see telegram-persona-bot-runtime SKILL.md §7a):
  • Checks the LOCAL-disk pid-lock (NOT a OneDrive path — see §1a).
  • If the owning pid is dead/absent, relaunches the bot DETACHED (no console window).
  • SILENT when healthy (exits 0, prints nothing) so a Hermes `no_agent=True` cron
    delivers nothing unless it actually had to restart the bot (watchdog pattern).

Wire up:
  1. Copy the bot's lock logic to use %LOCALAPPDATA%\\hermes\\entities\\<entity>.lock
     (the bot and this watchdog MUST agree on the exact same lock path).
  2. Copy this file into %LOCALAPPDATA%\\hermes\\scripts\\ so cron finds it by name.
  3. cronjob(action=create, no_agent=True, script="<this>.py", schedule="every 10m")
  4. cronjob(action=run, ...) once to bring the bot up immediately.

Edit the three constants below for your entity.
"""
import os
import sys
import time
import subprocess

# --- EDIT THESE for your entity -------------------------------------------------
HERE = r"C:\path\to\bot\folder"          # folder containing the bot .py (may be OneDrive)
BOT_FILE = "alistair_bot.py"             # the bot script filename
LOCK_NAME = "alistair.lock"              # entity lock filename
# --------------------------------------------------------------------------------

# Lock lives on LOCAL disk (never OneDrive — cloud shim breaks O_EXCL atomicity, §1a).
_LOCK_DIR = os.path.join(os.environ.get("LOCALAPPDATA",
                         os.path.expanduser(r"~\AppData\Local")), "hermes", "entities")
LOCK = os.path.join(_LOCK_DIR, LOCK_NAME)
BOT = os.path.join(HERE, BOT_FILE)
LOG = os.path.join(HERE, os.path.splitext(BOT_FILE)[0] + "_run.log")


def pid_alive(pid):
    # Windows-safe: os.kill(pid,0) throws WinError 87, so use tasklist.
    try:
        out = subprocess.run(["tasklist", "/FI", "PID eq %d" % pid],
                             capture_output=True, text=True, timeout=15).stdout
        return str(pid) in out
    except Exception:
        return False


def running():
    if not os.path.exists(LOCK):
        return False
    try:
        pid = int(open(LOCK, encoding="utf-8").read().strip())
    except Exception:
        return False
    return pid_alive(pid)


def start():
    flags = 0x00000008 | 0x08000000  # DETACHED_PROCESS | CREATE_NO_WINDOW
    with open(LOG, "a", encoding="utf-8") as lf:
        subprocess.Popen([sys.executable, BOT], cwd=HERE,
                         stdout=lf, stderr=lf, creationflags=flags, close_fds=True)


if __name__ == "__main__":
    if running():
        sys.exit(0)  # healthy -> silent (cron delivers nothing)
    start()
    time.sleep(6)
    ok = running()
    print("[watchdog %s] bot was down -> restarted: %s"
          % (time.strftime("%Y-%m-%d %H:%M"), "OK" if ok else "FAILED"))
    sys.exit(0 if ok else 1)
