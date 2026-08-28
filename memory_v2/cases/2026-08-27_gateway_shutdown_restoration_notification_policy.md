# Case: Gateway Shutdown & Restoration Notification Policy

**Date:** 2026-08-27  
**Domain:** `agent_club` / `ops_infrastructure`  
**Profile:** All (Hermes, Harrison, Richard, Archie, Callum, Ben, Alistair, Liz)

## Context & Problem
During background service operations, system reboots, or maintenance, agent gateways (e.g. Richard, Harrison) send "Gateway Shutdown" notifications to Stefan via Telegram. However, after internal restart or recovery completed, no follow-up notification was sent, leaving Stefan unsure if the gateway came back online.

## Resolution / Policy
Stefan instructed:
"Если они мне пишут 'Gateway Shutdown' и это какие-то их внутренние процессы, то пусть также мне сообщают, что успешно восстановлены, коротко"

## Mandate for Agents
1. When a gateway/service sends a "Gateway Shutdown" message prior to a restart/maintenance, it must log or schedule a recovery check.
2. Upon successful restoration and health check validation, the bot/agent MUST send a concise Telegram message: "Шлюз успешно восстановлен" (Gateway successfully restored).
3. Rule recorded as Rule 12 in `memory_v2/principles/stefan_rules.md`.
