---
name: multi-agent-group-governance
description: "Govern multi-agent Telegram groups, triggers and isolation."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [agents, telegram, groups, isolation, governance, orchestration]
---

# Multi-Agent Group & Profile Governance

Class-level skill defining execution rules, isolation barriers, and group chat trigger semantics for multi-agent clusters (Hermes, Richard, Callum, Alistair, Liz, Ben).

## When to Use
Use when configuring, orchestrating, or executing actions across multiple Telegram bot profiles or inside shared Telegram group chats.

## Core Rules & Directives

### 1. Group Chat Trigger Rules (Silence by Default)
All agent bots in Telegram group chats remain silent by default (`require_mention: true`).
An agent responds to **ANY group participant** (not just admins) ONLY under 3 conditions:
1. **Direct `@mention`:** e.g., `@richnavobot`, `@callumvancebot`, `@qubicpmbot`.
2. **Text Name Mention:** e.g., "Ричард", "Каллум", "Алистер".
3. **Direct `Reply`:** Quoting/replying to the bot's message by ANY participant.

**Bot-to-Bot Loop Shield:** Responses to other bots (`is_bot: true`) are blocked at the gateway level to prevent infinite chat loops.

### 2. Domain & Sales Isolation
- **Sales, Leads, & CRM:** Handled EXCLUSIVELY by **Richard Marlowe** (`@richnavobot`). Orchestrator and other sub-agents MUST NOT issue sales, lead, or CRM reports on Richard's behalf.

### 3. Cross-Profile Isolation Barrier & Tool Restrictions
- **Tool Disabling:** Leaf sub-agents MUST have `cronjob` and `skill_manage` disabled in their `config.yaml` (`tools.disabled: [cronjob, skill_manage]`). Only Hermes Orchestrator maintains cron and skill management authority.
- **Domain Boundaries & Automatic Reversion:** Sub-agents operate strictly within their baseline domain (Richard=Sales/CRM, Callum=Dev/Code, Alistair=Operations/OODA & alistair-kanban, Ben=PPC/SEO/Landing Marketing, Liz=HR/Team, Archie=Content Strategy & Copywriting). Alistair controls STRICTLY his own Kanban (`alistair-kanban`) and does NOT manage or control other agents' Kanbans or files. If asked about another domain, sub-agents redirect the user to the correct bot. Situational user requests are executed once for that turn, after which sub-agents automatically revert to baseline domain isolation.
- **Sub-Agents File Scope:** Allowed to modify ONLY their own profile directory (`/opt/hermes/profiles/<self>/`) and own Kanban (`<self>-kanban`).
- **Strict Prohibition:** Sub-agents MUST NOT modify, scan, or run bulk edits across other agents' files, memories, skills, or Kanbans.
- **Orchestrator:** Only **Hermes Stevenson** (main profile) holds cross-profile orchestration authority.

### 4. Windows Desktop GUI Profile Sync
- **Side Panel Profile Discovery:** The Hermes Desktop Electron app on Windows scans `C:\Users\<user>\AppData\Local\hermes\profiles\` to draw profile tabs in the UI.
- **Creating Profiles for Desktop GUI:** When a new profile (e.g., `archie`) is created on the server, a corresponding folder `AppData\Local\hermes\profiles\<name>` containing `SOUL.md` and `config.yaml` must exist on the local Windows PC so the profile appears in the Desktop App side menu.

### 4. Kanban Hosting & Persistence Standards
- **Hosting Target:** EXCLUSIVELY on Vercel (`https://<agent>-kanban.vercel.app`). NEVER host or deploy Kanbans on `aavalanche.com`.
- **Bidirectional Sync:** Drag-and-drop actions, timestamps (`moved_at`), and comments sync via `https://dev.aavalanche.com/kanban_api.php?agent=<agent>`.
- **Auto-Merge:** Client-side frontend auto-merges server cards with local cache on load to prevent stale state wiping.

### 5. Execution Timeout, Compression & Flood Control Guardrails
- **`request_timeout_seconds: 15`:** Hard 15-second model timeout per turn to prevent long hanging loops.
- **`compression.threshold: 0.20`:** Auto-compresses context at 20% capacity (~20k-40k tokens) down to 10% to guarantee 1-3s response latency.
- **Telegram Flood Control Cooldown:** Gateway daemons under `systemd` queue inbound messages during temporary Telegram API flood control limits (e.g. 68s cooldown) without dropping them.
- **Timezone Standard:** All scheduled crons and time reports MUST follow Ukrainian time (`Europe/Kiev` / UTC+3).
