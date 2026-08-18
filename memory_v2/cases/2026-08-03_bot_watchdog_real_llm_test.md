# Case: Bot Watchdog — Real LLM E2E Verification for All 5 Bots

## Summary
- **Date**: 2026-08-03
- **Domain**: agent_club
- **Context**: Autonomous monitoring of Telegram agent bots (Hermes, Richard, Liz, Alistair, Ben).

## Symptom / Challenge
- Monitoring scripts that only verified process HTTP `getUpdates` or API ping missed internal bot failures (e.g. LLM routing error, key expiration, stencil error responses).
- Users messaged Liz or Ben and received template/error messages despite the watchdog reporting "Healthy".

## Solution & Rule from Stefan
- **Rule**: Test ALL 5 bots (Hermes, Richard, Liz, Alistair, Ben) using a **REAL LLM test message**.
- Updated `bot_watchdog.py` to:
  1. Pass a test prompt directly into each bot's LLM generation chain.
  2. Verify that the response is generated dynamically by the model (non-empty, non-stencil, exit code 0).
  3. Auto-restart any bot failing the real LLM generation test.

## Key Lesson
- Health checks for LLM agents must test the LLM inference path, not just socket connectivity or process existence.
