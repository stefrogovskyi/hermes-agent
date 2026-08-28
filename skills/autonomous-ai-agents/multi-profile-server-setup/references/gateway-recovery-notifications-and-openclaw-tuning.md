# Gateway Shutdown / Restart Recovery Notification Pattern

## Problem
During background self-improvement reviews, context auto-compression, or systemd daemon recycling, the Hermes Gateway sends an active warning to the user:
`⚠️ Gateway shutting down / restarting — Your current task will be interrupted.`

When these restarts are internal maintenance routines rather than unrecoverable crashes, the user is left wondering whether the agent died or recovered.

## Solution & Architecture
1. **Shutdown State Ledger (`state/shutdown_notified_chats.json`):**
   When `_notify_active_sessions_of_shutdown` executes in `gateway/run.py`, serialize the active session keys into `shutdown_notified_chats.json`.
2. **Post-Startup Recovery Hook (`_notify_recovered_after_restart`):**
   During gateway initialization (after messaging platforms and adapters are marked `running`), trigger an asynchronous recovery task:
   - Check if `shutdown_notified_chats.json` exists.
   - If present, dispatch a concise confirmation message to each notified session/chat:
     `✅ Gateway успешно перезапущен и готов к работе.`
   - Unlink the state file once delivered.

## OpenClaw Timeout & Fast Model Fallback
- **Problem:** OpenClaw gateways throwing `Request timed out before a response was generated. Please try again, or increase agents.defaults.timeoutSeconds in your config.`
- **Fix:** In `~/.openclaw/openclaw.json`:
  - Increase `agents.defaults.timeoutSeconds` from 10s to 120s.
  - Increase `models.providers.*.timeoutSeconds` from 6s to 45s.
  - Prioritize ultra-fast high-throughput models (e.g. `openrouter/stealth/ox-alpha`) as primary.
