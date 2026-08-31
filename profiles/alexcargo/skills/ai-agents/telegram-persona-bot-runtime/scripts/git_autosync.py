#!/usr/bin/env python3
"""git_autosync.py — commit+push N agent repos on a schedule (Hermes cron, no_agent).

Reusable across Richard Marlowe / Alistair Sterling / Hermes Stevenson (each its own private
GitHub repo, each its own local Google-Drive-synced folder). Mirrors what ran live this session.

- Silent when clean (watchdog pattern: nothing printed -> no notification).
- Only commits+pushes when `git status --porcelain` is non-empty.
- Secrets excluded by each repo's .gitignore (.env, *.env, *.key, etc.) — never pass them.
- Non-zero exit on any error so the cron alerts instead of going quiet.

Wire it: cronjob(action=create, name="Git Autosync", no_agent=True, script="git_autosync.py",
schedule="every 30m", deliver="local"). Keep secrets OUT of chat; .env.local stays local-only.
"""
import os
import subprocess
import sys

# EDIT THESE to your three (or N) working folders. Paths use raw strings for spaces/cyrillic.
REPOS = [
    r"C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Richard Marlowe\Richard Hermes",
    r"C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Alister Sterling\Alistair Hermes",
    r"C:\Users\Stefan\My Drive\Equity\My Biz\My companies\Enlight Group\Stefan Rogovskyi\Hermes Stevenson",
]

GIT = "git"


def _run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=120)


def sync(path):
    if not os.path.isdir(os.path.join(path, ".git")):
        print("SKIP (no .git): %s" % path)
        return 0
    st = _run([GIT, "status", "--porcelain"], path)
    if st.returncode != 0:
        print("ERROR git status %s: %s" % (path, st.stderr.strip()))
        return 1
    if not st.stdout.strip():
        return 0  # clean -> silent
    _run([GIT, "add", "-A"], path)
    cm = subprocess.run(
        [GIT, "-c", "user.name=Stefan", "-c", "user.email=stefan@navo24.com",
         "commit", "-m", "autosync: %s" % os.path.basename(path)],
        cwd=path, capture_output=True, text=True, timeout=120)
    if cm.returncode != 0:
        print("ERROR commit %s: %s" % (path, cm.stderr.strip()))
        return 1
    br = _run([GIT, "rev-parse", "--abbrev-ref", "HEAD"], path).stdout.strip() or "HEAD"
    ps = _run([GIT, "push", "origin", br], path)
    if ps.returncode != 0:
        print("ERROR push %s: %s" % (path, ps.stderr.strip()))
        return 1
    print("PUSHED %s -> %s" % (os.path.basename(path), br))
    return 0


def main():
    rc = 0
    for p in REPOS:
        try:
            rc |= sync(p)
        except Exception as e:
            print("EXC %s: %s" % (p, e))
            rc = 1
    sys.exit(rc)


if __name__ == "__main__":
    main()
