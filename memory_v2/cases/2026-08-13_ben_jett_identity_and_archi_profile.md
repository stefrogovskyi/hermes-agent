# Case: Ben Jett Identity Lock & Archi Standalone Profile Setup
**Date:** 2026-08-13  
**Domain:** agent_club / memory_systems  

## Context & Problem
1. **Ben Jett Identity Loss:** During profile reloads or fallback shifts, Ben Jett (`@benjettbot` / CMO & Growth Hacker) lost context regarding his company identity and role.
2. **New Agent Profile Request:** Stefan requested creating a dedicated standalone loop agent profile named **Archi** (`archie` profile) with its own Telegram bot token (`840067775:***`).

## Solution & Actions Taken
1. **Ben Jett Identity Lock:**
   - Verified and locked Ben Jett's `SOUL.md` and system prompts under `/opt/hermes/profiles/ben/`.
   - Explicitly defined Ben Jett as Chief Marketing Officer (CMO) & Growth Hacker for Navo / Navo24.
   - Ensured system prompts across `profiles/ben/` enforce persistent company identity to prevent future amnesia upon profile reinitialization.

2. **Archi Profile Creation:**
   - Created full isolated profile structure at `/opt/hermes/profiles/archie/` (SOUL.md, config.yaml, memory, skills).
   - Configured dedicated Telegram bot token for Archi, isolating its state and gateway loop from all other agents.
   - Connected Archi to the multi-agent cluster without falling back or overlapping with Hermes or other sub-agent tokens.

## Verification
- Verified profile directory structures and `SOUL.md` contents for `ben` and `archie`.
- Confirmed token isolation and profile independence across all 7 profiles in `/opt/hermes/profiles/`.
