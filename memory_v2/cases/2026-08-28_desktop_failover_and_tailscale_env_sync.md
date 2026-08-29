# Case: Desktop Failover Daemon & Tailscale Direct .env Sync Protocol

**Date:** 2026-08-28  
**Domain:** `agent_club` / `ops_infrastructure`  
**Profile:** All (Hermes, Richard, Harrison, Alistair, etc.)

## Context & Problem
1. When the primary desktop machine undergoes maintenance or stays offline, automated tasks and polling require a fallback failover daemon (`desktop_failover_daemon.py`).
2. `.env` files containing live API keys and secrets were previously at risk of being excluded or lost during Git sync (`git_autosync_hidden.sh`), since `.env` files are ignored in Git repositories to prevent credential leaks.

## Resolution & Implementation
1. **Desktop Failover Daemon:** Created `/opt/hermes/scripts/desktop_failover_daemon.py` which can be mirrored to Stefan's PC (`C:\Users\Stefan\hermes_failover_daemon.py`) and scheduled via Windows Startup (`shell:startup`) or Task Scheduler for automatic failover.
2. **Tailscale SSH Direct Sync:** Established direct SCP/SSH transport over Tailscale for `.env` files (`/opt/hermes/profiles/<agent>/.env`). Live secrets are synced securely between PC and VPS without touching Git.
3. **Career Scanner Grounded Rules:** Hardened `executive_careers_poller.py` output mandates to prohibit hallucinating vacancies, metrics, or altered URLs.

## Mandate
- `.env` changes must be synced via direct SSH/SCP over Tailscale (`Rule 13`).
- Executive Career Scanner outputs must be strictly grounded (`Rule 14`).
