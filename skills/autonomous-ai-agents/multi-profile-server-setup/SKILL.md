---
name: multi-profile-server-setup
description: "Manage multi-profile Hermes systemd daemons and git sync."
version: 1.0.0
author: Hermes Curator
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [hermes, systemd, multi-profile, gateway, telegram, token-isolation, git-sync]
    related_skills: [hermes-agent]
---

# Multi-Profile Server Setup & Token Isolation

## When to Use
Use when configuring or troubleshooting multi-profile Hermes Agent instances running as systemd background services on Linux servers, or setting up Git workspace synchronization.

## Key Concepts & Architecture

1. **Systemd Services per Profile:**
   - Each Hermes profile (`default`, `richard`, `callum`, `alistair`, `ben`, `liz`) runs as an independent systemd daemon: `hermes-<profile>.service`.
   - Executable command: `hermes --profile <profile> gateway run`.

2. **Telegram Token Isolation:**
   - **Critical Pitfall:** When creating a new profile via `hermes profile create <name> --clone`, the new profile inherits `.env` containing `TELEGRAM_BOT_TOKEN` from the source profile.
   - Running two gateways with the same `TELEGRAM_BOT_TOKEN` causes Telegram API polling conflicts (`Conflict: terminated by other getUpdates request`).
   - **Fix:** Each profile must either have its own unique Telegram bot token in `/opt/hermes/profiles/<name>/.env` OR have Telegram polling disabled in `config.yaml`:
     ```yaml
     platforms:
       telegram:
         enabled: false
     ```

3. **Workspace Git Auto-Sync (`git_autosync_hidden.sh`):**
   - User workspace data (skills, scripts, memories, non-secret configs) across all profiles should be tracked via Git.
   - **Crucial `.gitignore` Rules:** Never track `.env`, `auth.json`, or SQLite databases (`*.db`, `*.db-wal`, `*.db-shm`) to prevent token leaks and binary database corruption:
     ```gitignore
     *.db
     *.db-journal
     *.db-wal
     *.db-shm
     *.pid
     *.lock
     *.log
     .env
     auth.json
     audio_cache/
     image_cache/
     sessions/
     logs/
     cache/
     state/
     hermes-agent/
     profiles/*/.env
     profiles/*/auth.json
     profiles/*/*.db*
     profiles/*/sessions/
     ```

4. **Remote Electron Gateway Access:**
   - Desktop Electron app connects to the remote server via Remote Gateway settings over SSH/Tailscale IP.
   - Closing the local laptop disconnects the Electron GUI client without interrupting 24/7 background agents on the server.

5. **Multi-Device File Indexing vs Replication (Hard Rule):**
   - **Constraint:** Do NOT attempt full file sync or replication from large remote workstations (5+ TB across PCs) onto a server with limited storage (e.g. 500 GB VPS).
   - **Pattern:** Use a **lightweight metadata & FTS5 index** (paths, filenames, extracted text) and fetch/transfer individual files **on-demand** over Tailscale / SMB / SSH when explicitly requested.

6. **Windows Remote Access & SMB Inspection over Tailscale:**
   - **Windows SMB Guest Access:** Windows 10/11 blocks anonymous SMB by default (`STATUS_ACCESS_DENIED`). To enable guest SMB access:
     ```powershell
     Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanWorkstation\Parameters" -Name "AllowInsecureGuestAuth" -Value 1 -Type DWord
     ```
   - **OpenSSH Server Setup (Windows):**
     ```powershell
     Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
     Start-Service sshd
     Set-Service -Name sshd -StartupType 'Automatic'
     New-NetFirewallRule -Name 'OpenSSH-Server-Inbound' -DisplayName 'OpenSSH Server' -Enabled True -Direction Inbound -Protocol TCP -LocalPort 22 -Action Allow
     ```
   - **Python Direct SMB Access:** Use `impacket.smbconnection.SMBConnection` with `conn.login("Guest", "")` to list SMB shares and paths over Tailscale without needing local mount points on Linux.
