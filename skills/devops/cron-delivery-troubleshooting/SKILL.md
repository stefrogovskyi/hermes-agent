---
name: cron-delivery-troubleshooting
description: Fix cron jobs firing at wrong time or twice.
category: devops
tags:
  - cron
  - scheduler
  - timezone
  - duplicates
  - hermes
---

# Cron Delivery Troubleshooting

## When to Use
- User asks "why did this scheduled message arrive at <odd time>?"
- User reports a cron/scheduled delivery arriving twice.
- After any server timezone change or Hermes migration between machines.

Diagnose and fix scheduled jobs that arrive at the wrong wall-clock time, arrive twice, or arrive at odd hours (early morning "ghost" deliveries). Applies to Hermes cron jobs but the method generalizes.

## Symptom A: job fires at wrong local time

Root cause seen in production: **server timezone changed (e.g. UTC+3 → UTC)**. The scheduler logs `next_run_at offset changed (3:00:00 -> 0:00:00). Recomputing cron run to preserve local wall-clock intent` — it preserves the numeric hour, which now means a different local time for the user.

Diagnosis steps:
1. `date; timedatectl` — confirm current server TZ.
2. `grep "offset changed" /opt/hermes/logs/agent.log*` — lists EVERY affected job with timestamps. One TZ shift hits many jobs; audit them all, not just the one the user complained about.
3. Fix by shifting cron expressions in UTC: `cronjob(action='update', job_id=..., schedule='0 <utc_hour> * * *')` where utc_hour = desired_local_hour − utc_offset.
4. Only fix user-facing jobs with wall-clock intent; leave TZ-agnostic maintenance jobs (every Nh, night syncs) alone. Report the before/after table to the user in their local time.

## Symptom B: job delivered twice (or at an unexplained extra time)

Do NOT stop at the first plausible explanation. In production the "7:30 AM mystery delivery" had TWO causes stacked: a TZ shift on the VPS **and** a duplicate job on another machine doing catch-up delivery.

Checklist, in order:
1. **Count deliveries in the primary scheduler's log**: `grep -c "Job '<id>': delivered" /opt/hermes/logs/agent.log*`. If the primary log shows exactly one delivery per day, the duplicate comes from OUTSIDE this scheduler.
2. **Check system-level cron/timers on the same host**: `crontab -l`, `/etc/cron.d/`, `systemctl list-timers`.
3. **Check OTHER MACHINES running the same stack** (old installs are the classic source). Enumerate hosts with `tailscale status`, then inspect each: Windows path is `%LOCALAPPDATA%\hermes\cron\jobs.json`; discovery via `ssh user@host "type <path> | findstr /i <jobname>"`.
4. **Smoking gun for catch-up deliveries**: `last_run_at` in the duplicate's jobs.json at an odd hour (e.g. 07:30 local) = the machine was asleep at scheduled time, woke, and fired the missed run. This explains "why did this arrive in the morning" questions.
5. Disable the duplicate, keep exactly one owner: set `enabled: false, state: "paused", paused_reason: "duplicate of <primary_job_id>; disabled by Hermes <date>"` in the remote jobs.json, upload, then **verify by re-downloading and reading back**.

## Windows-over-SSH pitfalls (editing remote jobs.json)

- Complex PowerShell one-liners over ssh break on quoting (`$_` mangling, `2>NUL` → out-file errors). Don't fight it: **scp the file down, edit with local python3 json, scp back, re-download to verify**. Fast and deterministic.
- Simple `dir /b`, `type ... | findstr /i x` cmd.exe commands DO work over ssh; use them for discovery.
- `schtasks /query ... | findstr` inside a powershell wrapper fails on `2>NUL`; run it via plain cmd if needed.

## Reporting rule (Stefan)

When the true cause turns out different/bigger than an earlier explanation you gave, explicitly correct the earlier answer ("my morning explanation was correct but incomplete") — don't silently move on.

## Common Pitfalls & Cross-Platform Quirks

### 1. Windows vs Linux Cron Execution Failures
- **Hardcoded Linux Paths (`/opt/hermes/...`):** Scripts executing on Windows (e.g. desktop node during failover/sync) will crash with `FileNotFoundError`.
  - **Fix:** Use dynamic detection:
    ```python
    if os.name == "nt":
        DEFAULT_HOME = os.path.expandvars(r"%LOCALAPPDATA%\hermes")
    else:
        DEFAULT_HOME = "/opt/hermes"
    HERMES_HOME = os.environ.get("HERMES_HOME", DEFAULT_HOME)
    ```
- **Windows Console Encoding (`UnicodeEncodeError` on emojis):** Windows PowerShell/cmd defaults to `cp1252`/`cp866`, crashing python scripts when outputting emojis (`📊`, `🕒`, `✅`).
  - **Fix:** Force UTF-8 reconfigure at script startup:
    ```python
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    ```

### 2. Cron Report Formatting & User Legibility
- Always deliver reports in Russian.
- Suppress raw logs/traces; format with structured emoji indicators, summary bullet points, and human-readable schedules (converting UTC cron expressions to Kyiv time `UTC+3`).
- **NO HTML TAGS IN NOTIFICATIONS (STRICT):**
  - Never use HTML formatting tags (`<b>`, `<code>`, `<i>`, `<pre>`, `<a>`) in cron prompts, notifications, or output scripts.
  - Always use pure Telegram-compatible Markdown (`**bold**`, `` `code` ``, `*italic*`, `[links](url)`) and emojis.
- **Silent Background Maintenance vs User Delivery (`deliver: local` vs `deliver: origin`):**
  - High-frequency or purely synchronization maintenance tasks (e.g. 6-hour Google Sheet registry updates) must use `deliver: "local"` to prevent spamming Telegram chat with technical confirmation strings like `Successfully synced N entries`.
  - Only dedicated user-facing summary briefings (e.g. evening digest at 22:00 Kyiv) should use `deliver: "origin"`.

### 3. Model Drift Guard (`RuntimeError: global inference config drifted`)
- In Hermes Agent v0.20+, scheduled jobs carry an internal `model_snapshot` and `provider_snapshot`.
- When the global default model in `config.yaml` is changed (e.g. `gemini-3.7-flash` -> `gemini-3.8-flash`), unpinned jobs that lack explicit model overrides will be skipped at execution time with:
  `RuntimeError: Skipped to prevent unintended spend: global inference config drifted since this job was created...`
- **Resolution Checklist on Model Tier Changes:**
  1. Inspect all `jobs.json` files across `/opt/hermes/cron/jobs.json` and all profiles in `/opt/hermes/profiles/*/cron/jobs.json`.
  2. For every job inheriting the default model (`model: null`), synchronize `model_snapshot` and `provider_snapshot` to match the exact new active model string (e.g. `google/gemini-3.8-flash`, provider `gemini`).
  3. Jobs explicitly pinned to a specific engine (e.g. Archie blogwriting on `claude-sonnet-5`) must have their `model_snapshot` pinned to that same engine.

### 4. Spurious Burst Deliveries via `catch_up_occurrences`
- **Root Cause:** When heavy file system, git operations (e.g. `git-filter-repo`, history rewrites), or time drifts occur, Hermes schedulers across profiles may perceive the timestamps as a reboot or missed interval lag.
- Hermes creates temporary `catch_up_occurrences` files in `/opt/hermes/cron/` and profile cron directories, causing a rapid-fire "burst" execution of all jobs at once.
- **Prevention & Fix:**
  1. In all `jobs.json` definitions, explicitly declare `"catch_up": false` for recurring jobs unless historical replay is strictly intended.
  2. If burst triggers occur, immediately purge all `catch_up_occurrences` files:
     ```bash
     find /opt/hermes -name "catch_up_occurrences" -delete
     ```
  3. Ensure jobs have `"catch_up": false` written across all cluster profiles.

### 5. Git Sanitization, Secret Leaks & Safe Remote Updates
- When scrubbing sensitive files or large assets across Git history using `git-filter-repo` (e.g. after GitHub Secret Scanning flags leaked API keys):
  1. Always create a safety bundle first: `git bundle create /tmp/pre_filter.bundle --all`.
  2. Prepare targeted path list (`--paths-from-file /tmp/paths.txt`) to strip credentials, `.env`, tokens, and heavy binary backups (`*.tar.gz`).
  3. Execute `git-filter-repo --invert-paths --paths-from-file ... --force` (using the virtualenv binary if not in global PATH).
  4. Remember `git-filter-repo` unsets remotes for safety: re-add origin (`git remote add origin <URL>`) and reset tracking branch (`git branch --set-upstream-to=origin/master master`).
  5. Force-push rewritten clean history: `git push origin master --force`.
  6. **Prevent Spurious Catch-up Storms:** History rewrites alter commit hashes and file timestamps, triggering schedulers into replaying missed intervals. Immediately purge `catch_up_occurrences` files and verify `"catch_up": false` on all jobs.

### 6. Desktop PC Silent Background Tasks (Zero Windows Popups)
- **Problem:** Running scheduled background scripts on a user's active Windows desktop (e.g. MS To-Do sync, local file dumpers) via PowerShell or cmd.exe spawns black console windows that steal focus or blink on screen.
- **Solution & Workflow:**
  1. Wrap script executions in a VBScript with `WindowStyle = 0`:
     ```vbscript
     Set WshShell = CreateObject("WScript.Shell")
     WshShell.Run "powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File ""C:\Path\To\script.ps1""", 0, False
     ```
  2. In Windows Task Scheduler, register tasks as hidden and point the action to `wscript.exe "C:\Path\To\run_silent.vbs"`.
  3. When triggering from Linux over SSH/Tailscale, call `wscript.exe` rather than direct `powershell.exe` to guarantee zero UI interruption.
  4. **UTF-8 BOM Trap over SSH:** When PowerShell writes JSON using `Set-Content -Encoding UTF8`, it prepends a UTF-8 BOM (`\ufeff`). When python reads it over SSH (`cat` / `type`), `json.loads` crashes with `Unexpected UTF-8 BOM (decode using utf-8-sig)`. Always strip BOM (`if s.startswith('\ufeff'): s = s[1:]`) or decode with `utf-8-sig`.

### 7. Proactive Model Discovery & Health Audit Radar
- Do not restrict fallback model health checks to static arrays.
- Actively scan discovery endpoints across all configured cluster keys:
  - Google Gemini API (`generativelanguage.googleapis.com/v1beta/models`)
  - NVIDIA NIM (`integrate.api.nvidia.com/v1/models`)
  - Nous Research Portal (`inference-api.nousresearch.com/v1/models`)
  - OpenRouter Free Catalog (`openrouter.ai/api/v1/models`)
  - Gonka24 API (`api.gonka24.com/v1/models`)
- Dynamically ping newly detected models with a lightweight probe. Automatically integrate successful `HTTP 200` responders into the active fallback chain and surface them in the morning audit report.



