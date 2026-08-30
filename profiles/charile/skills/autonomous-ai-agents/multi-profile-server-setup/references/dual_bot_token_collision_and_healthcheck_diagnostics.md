# Dual-Bot Token Conflict Resolution & Health Check Diagnostics

## 1. Dual-Process Bot Token Collision (Conflict: HTTP 409)
### The Problem
When two distinct process daemons attempt to connect to the Telegram Bot API using the exact same `TELEGRAM_BOT_TOKEN` simultaneously (e.g. native `aeon-bridge.service` and a lingering `hermes-aeon.service`), the following breakdown occurs:
1. **Telegram Ingress Thrashing:** Both long-polling HTTP listeners terminate each other's connections (`HTTP Error 409: Conflict`).
2. **Spurious Gateway Shutdown Notices:** The Hermes gateway interprets the repeated 409 conflict as an unrecoverable adapter error and pushes a `"⚠️ Gateway shutting down — Your current task will be interrupted"` alert into the user's Telegram DM.
3. **Interactive Self-Termination Prompts:** When the user asks *"What is this?"*, the autonomous Hermes profile attempts to remediate the collision by issuing `systemd-run --on-active=4s systemctl disable --now hermes-<profile>.service`, which triggers an interactive Command Approval prompt (**Allow Once / Session / Always / Deny**).

### Prevention & Fix Procedure
1. **Decommission Hermes profile daemon for native/external framework agents:**
   ```bash
   systemctl stop hermes-<profile>.service
   systemctl disable hermes-<profile>.service
   ```
2. **Neutralize `.env` token in deactivated Hermes profile:**
   Set `TELEGRAM_BOT_TOKEN=DISABLED_USE_NATIVE_<FRAMEWORK>` in `/opt/hermes/profiles/<profile>/.env` to permanently prevent accidental reconnects.
3. **Restart the designated native bridge daemon:**
   ```bash
   systemctl enable <framework>-bridge.service
   systemctl restart <framework>-bridge.service
   ```

---

## 2. 3-Level Robust Agent Health Check (Anti-False-Positive Protocol)
### Why `systemctl is-active` Fails (Silent Hang Detection)
A service status of `Active: running` only verifies that the OS process has not crashed. It fails to detect when the Python async event loop is trapped in an internal reconnect cycle due to `httpx.ReadTimeout` or network drops (e.g. `[Telegram] Telegram network error (attempt 4/10), reconnecting in 40s`).

### The 3-Level Audit Routine:
1. **Level 1 — OS Process (Systemd):**
   `systemctl is-active hermes-<profile>.service` must return `active`.
2. **Level 2 — Telegram Ingress & Webhook Queue:**
   Invoke `https://api.telegram.org/bot<TOKEN>/getWebhookInfo` to verify:
   - `pending_update_count == 0` (messages are being consumed in real-time, not queueing up).
   - No conflicting active webhook URL if long-polling is used.
3. **Level 3 — Journalctl Log Analysis:**
   Inspect `journalctl -u hermes-<profile>.service -n 50 --no-pager` for:
   - No recent `TimedOut` / `ReadTimeout` reconnect loops.
   - No `Blocked unauthorized user` warnings.
   - No `Restart-loop breaker` / `Exit code 1/FAILURE` restarts.
