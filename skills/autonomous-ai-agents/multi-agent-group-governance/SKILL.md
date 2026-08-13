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

### 3. Cross-Profile Isolation Barrier
- **Sub-Agents:** Allowed to modify ONLY their own profile directory (`/opt/hermes/profiles/<self>/`) and own Kanban (`<self>-kanban`).
- **Strict Prohibition:** Sub-agents MUST NOT modify, scan, or run bulk edits across other agents' files, memories, skills, or Kanbans.
- **Orchestrator:** Only **Hermes Stevenson** (main profile) holds cross-profile orchestration authority.

### 4. Kanban Hosting & Persistence Standards
- **Hosting Target:** EXCLUSIVELY on Vercel (`https://<agent>-kanban.vercel.app`). NEVER host or deploy Kanbans on `aavalanche.com`.
- **Bidirectional Sync:** Drag-and-drop actions, timestamps (`moved_at`), and comments sync via `https://dev.aavalanche.com/kanban_api.php?agent=<agent>`.
- **Auto-Merge:** Client-side frontend auto-merges server cards with local cache on load to prevent stale state wiping.

### 5. Execution Timeout & Compression Guardrails
- **`request_timeout_seconds: 30`:** Hard 30-second model timeout to prevent long hanging loops during fallback switches.
- **`compression.threshold: 0.25`:** Auto-compresses context at 25% capacity (~25k-50k tokens) down to 15% to maintain 1-3s API response latency.
- **Timezone Standard:** All scheduled crons and time reports MUST follow Ukrainian time (`Europe/Kiev` / UTC+3).
