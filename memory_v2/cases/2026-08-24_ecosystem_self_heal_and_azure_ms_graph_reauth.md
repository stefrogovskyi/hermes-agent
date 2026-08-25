# Case: Ecosystem Self-Healing Script Upgrade, Token Isolation Audit & Azure MS Graph Re-Auth

**Date:** 2026-08-24  
**Domain:** `agent_club` / `ops_infrastructure`  
**Status:** SUCCESS  

## Context
During ecosystem health checks on server `stefan1`, multiple architectural tasks required validation and automation:
1. Dynamic discovery of agent services (including new profiles like Aeon) in the automated self-healing script.
2. Verification of strict token isolation and userbot security across all 9 Hermes profiles.
3. Microsoft Azure App Registration renewal for `Navo Booking` and MS Graph API email authentication for Richard (`navo24.com`).

## Solutions & Architecture
1. **Dynamic Self-Healing Script (`ecosystem_self_heal_audit.py`):**
   - Upgraded `/opt/hermes/scripts/ecosystem_self_heal_audit.py` (run via `hermes-self-heal.timer`) from hardcoded service lists to dynamic globbing of `/etc/systemd/system/hermes-*.service` and `openclaw-*.service`.
   - Identified and revived `hermes-aeon.service`, switching it to `enabled` and starting it cleanly.

2. **Token Isolation & Userbot Verification:**
   - Scanned all 9 profile `.env` files. Verified 100% token isolation: no sub-agent uses the main Hermes bot token (`8682188433`).
   - Verified `stefan_userbot.session` file security (`chmod 600`) and confirmed no impersonation violations.

3. **Azure MS Graph & Navo Booking Re-Authentication:**
   - Registered/renewed client secrets for Azure App Registration `Navo Booking` (Client ID: `fb397420-6419-4113-b501-960b2135941e`) under `navo24.com`.
   - Verified MS Graph OAuth token flow for Richard's B2B CRM and email outreach via `dr.reenforce@gmail.com` and `contact@navo24.com`.

## Cross-References
- Principle: `/opt/hermes/memory_v2/principles/stefan_rules.md`
- Domain: `/opt/hermes/memory_v2/domains/ops_infrastructure.md`
