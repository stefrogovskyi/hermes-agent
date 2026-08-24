# Case: 3-Level Sub-Agent Health Check Protocol & Harrison Recovery

**Date:** 2026-08-22  
**Domain:** `agent_club` / `ops_infrastructure`  
**Status:** SUCCESS  

## Context
Stefan noted that Harrison Croft (@harrisoncroftbot) was inactive and not responding on Telegram. However, an earlier automated health check had reported Harrison as healthy because `systemctl is-active hermes-harrison` returned `active`.

## Cause
`systemctl is-active` only verifies that the daemon process exists at the OS level. It does not detect silent network polling hangs (`httpx.ReadTimeout`, unhandled Telegram long-polling socket freezes, or accumulated `pending_update_count`).

## Solution
1. **Immediate fix:** Restarted `hermes-harrison.service` via `systemctl restart`. The bot resumed active processing immediately.
2. **Systemic protocol:** Formulated and adopted the Mandatory 3-Level Sub-Agent Health Check:
   - **Level 1 (OS Level):** `systemctl is-active hermes-<agent>` (verifies process existence).
   - **Level 2 (Telegram API Level):** Perform `getMe` and `getWebhookInfo` / `getUpdates` API calls (verifies bot token responsiveness and checks if `pending_update_count` is piling up).
   - **Level 3 (Journalctl Level):** Inspect `journalctl -u hermes-<agent>` for `ReadTimeout`, `TimedOut`, `Blocked unauthorized user`, or infinite restart loops.

## Cross-References
- Principle: `/opt/hermes/memory_v2/principles/stefan_rules.md` (Rule #11)
- Domain: `/opt/hermes/memory_v2/domains/ops_infrastructure.md`
