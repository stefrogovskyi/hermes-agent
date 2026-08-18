# Case: Alistair PM Team Roster Synchronization & Model Upgrade

**Date**: 2026-08-02  
**Domain**: `agent_club` / `business`  
**Cross-ref**: `domains/life_domains.md#agent_club`

## Symptom
Alistair Sterling (`@qubicpmbot`) hallucinated fictional team member names (e.g. "George", "Maria") in conversation. Additionally, Stefan corrected his official role to **Co-founder & COO Navo** and requested adding Evgeny Karavan (Tech Support Manager) and purging unacquainted personnel (Liz Harper) from Alistair's memory.

## Root Cause & Fix
1. **Model Upgrade**: Alistair was using `poolside/laguna-s-2.1:free` which had high hallucination rates on names. Upgraded `ALISTAIR_MODEL` to `google/gemma-4-31b-it:free` in `Alister Sterling\Alistair Hermes\.env.local`.
2. **Memory & Prompt Cleanup**:
   - Cleaned `alistair_memory.json` to purge fictional names and remove Liz Harper.
   - Updated `system_prompt.md` and `AGENTS.md` across all agents to list Stefan as **Co-founder, COO Navo** and added Evgeny Karavan (Technical Support Manager).
3. **Restart**: Force-restarted Alistair via `bot_watchdog.py`.

## Lesson Learned
Small/free LLM models used in agent runtimes can hallucinate entity names when answering about team structures. Upgrading to higher-parameter models (e.g., Gemma 4 31B) alongside explicit system prompt rosters prevents memory corruption and hallucination.
