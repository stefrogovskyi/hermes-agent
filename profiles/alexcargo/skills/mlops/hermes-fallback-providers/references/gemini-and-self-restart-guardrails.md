# Gemini API & Self-Restart Guardrails

## 1. Gemini API 400 INVALID_ARGUMENT (Unmatched Function Calls)

### Symptom
`Gemini API Error: HTTP 400 (INVALID_ARGUMENT): Please ensure that function call turn comes immediately after a user turn or after a function response turn.`

### Cause
In Google Gemini API:
1. Every `model` turn containing `functionCall` parts MUST be followed immediately by a `user` turn containing matching `functionResponse` parts for those function calls.
2. If tool execution was interrupted (e.g. SIGTERM / process restart) or if a user sent a new text prompt before tool results were recorded in `state.db`, the history has a `model` `functionCall` turn followed directly by a human text `user` turn.
3. Gemini API rejects this history with HTTP 400 `INVALID_ARGUMENT`.

### Fix
In `agent/gemini_native_adapter.py`, `_sanitize_gemini_contents` parses `contents` before sending to Gemini:
- If a `model` turn contains `functionCall` parts and the next turn is missing matching `functionResponse` parts, it synthesizes a `user` turn with dummy `functionResponse` parts (`{"output": "[Function execution interrupted or omitted]"}`) followed by an `[INTERRUPTED_RESPONSE_PLACEHOLDER]` model turn before any human user turn.
- Ensures strict `user` -> `model` role alternation and first-turn `user` role.

---

## 2. Self-Restart Self-Killing Loop (`SIGTERM` / `-15`)

### Symptom
Running `systemctl restart hermes-default` or `hermes gateway restart` inside a foreground tool turn kills the active process mid-turn with `SIGTERM` (`exit_code: -15`).
Upon restart, the gateway sees an interrupted turn, re-opens the session transcript, and enters an endless repair/hallucination loop.

### Fix
In `tools/terminal_tool.py`, synchronous self-restart commands (`systemctl restart hermes`, `service hermes restart`, `hermes gateway restart`) are intercepted:
- Executed as a detached delayed background command (`nohup bash -c 'sleep 2 && <command>' >/dev/null 2>&1 &`).
- Returns `{"output": "Self-restart scheduled in 2 seconds in background...", "exit_code": 0}` immediately.
- The active turn completes cleanly and sends its reply before systemd restarts the daemon.

---

## 3. Systemd Resilience & Master Ecosystem Key File

### Systemd Auto-Restart Policy
- In `/etc/systemd/system/hermes-*.service`, set `StartLimitIntervalSec=0` under `[Unit]` and `RestartSec=2s` under `[Service]`.
- Systemd will NEVER lock out or give up restarting an agent service on repeated crashes.

### Systemd Timer Watchdog (`hermes-self-heal.timer`)
- Runs `/opt/hermes/scripts/ecosystem_self_heal_audit.py` every 60 seconds at OS level via `hermes-self-heal.service` (oneshot).
- Independent of Python agent runtime: checks all 6 services, journalctl 409 conflicts, and network deadlocks.

### Master Key & Config File
- Path (Linux VPS): `/opt/hermes/MASTER_ECOSYSTEM_KEYS_AND_CONFIGS.txt`
- Path (Windows PC): `C:\Users\Stefan\AppData\Local\hermes\MASTER_ECOSYSTEM_KEYS_AND_CONFIGS.txt`
- Contains all environment variables, API keys, bot tokens, OAuth credentials (Google Workspace, Make.com, Surge, Vercel), database paths, service names, profile names, systemd service configurations, SSH/Tailscale details, and emergency recovery procedures.
