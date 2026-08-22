---
name: aeon-framework
description: "Use when managing the Aeon autonomous framework and CLI."
version: 1.0.0
author: Hermes Curator
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [aeon, autonomous-agents, github-actions, harness, unattended-execution, claude-code, codex]
    related_skills: [hermes-agent, multi-profile-server-setup, claude-code, codex]
---

# Aeon Autonomous Agent Framework

## When to Use
Use when deploying, configuring, troubleshooting, or integrating the **Aeon Autonomous Agent Framework** (`aeonfun/aeon`), managing `./aeon` CLI, GitHub Actions autonomous harnesses, packs, skills, and background unattended execution.

## Creator & Architecture Origin
- **Original Author:** Aaron Mars ([@aaronjmars](https://github.com/aaronjmars) / [aeon.fun](https://aeon.fun)).
- **Core Repository:** `https://github.com/aeonfun/aeon` (Template/Framework) and user forks (e.g. `stefrogovskyi/aeon`).
- **Core Philosophy:** *"The most autonomous agent framework. No approval loops. No babysitting. Configure once, forget forever."*

## Key Architectural Components

### 1. Dual Interface (`./aeon` CLI & Web Dashboard)
- **`./aeon` executable:**
  - Bare `./aeon` launches the local Next.js / React dashboard.
  - `./aeon <command>` delegates to the non-interactive TypeScript CLI (`apps/cli`).
  - Supported commands: `skills`, `secrets`, `runs`, `config`, `memory`, `strategy`, `soul`, `packs`, `mcp`, `sync`, `auth`.
- **Environment & Root Discovery:**
  - Honours `AEON_REPO_ROOT` environment variable for targeting external Aeon repositories from any working directory.

### 2. GitHub Actions Harness (Unattended Execution)
- Runs agent loops entirely in GitHub Actions workflows triggered by cron schedules, webhooks, or manual repository dispatches.
- Autonomous runners drive coding agents (Claude Code, OpenAI Codex, Grok) without requiring real-time human approval for intermediate steps.

### 3. Skills & Packs Ecosystem
- Skills and tool packs are managed declaratively in `aeon.yml`.
- CLI commands for skill lifecycle:
  ```bash
  ./aeon skills enable <name>
  ./aeon skills disable <name>
  ./aeon skills run <name>
  ./aeon packs install <owner/repo>
  ```

### 4. Telegram Integration Modes
- **Instant Mode (`apps/webhook`):**
  - Cloudflare Worker acting as a Telegram webhook.
  - Relays updates in ~1s via GitHub `repository_dispatch` to trigger the `Messages` workflow.
  - Required Worker secrets: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `TELEGRAM_ALLOWED_USER_ID`, `TELEGRAM_WEBHOOK_SECRET`, `GITHUB_REPO`, `GITHUB_TOKEN`.
- **Polling Mode:**
  - Fallback 5-minute cron checking Telegram via `getUpdates` (mutually exclusive with active webhooks).
- **Registration Command:**
  ```bash
  ./aeon telegram register
  ```

### 5. Deployment & Setup Procedures
1. **Prerequisites & CLI Setup:**
   - Node.js (v20+ / v22+), npm.
   - GitHub CLI (`gh`): install and authenticate non-interactively:
     ```bash
     echo "$GH_PAT_TOKEN" | gh auth login --with-token
     gh auth setup-git
     ```
2. **Repository Clone & Sync:**
   ```bash
   git clone https://github.com/<owner>/aeon.git /root/aeon
   cd /root/aeon
   git remote add upstream https://github.com/aeonfun/aeon.git
   git fetch upstream && git merge upstream/main --no-edit
   gh repo set-default <owner>/aeon
   ```
3. **Dependency Installation:**
   ```bash
   cd /root/aeon/apps/cli && npm install
   cd /root/aeon/apps/dashboard && npm install
   ```
4. **Secrets Provisioning (GitHub Secrets):**
   Set core credentials using `gh secret set` or `./aeon secrets set`:
   ```bash
   echo "$CLAUDE_OAUTH_OR_API_KEY" | gh secret set CLAUDE_CODE_OAUTH_TOKEN -R <owner>/aeon
   echo "$TELEGRAM_BOT_TOKEN" | gh secret set TELEGRAM_BOT_TOKEN -R <owner>/aeon
   echo "$TELEGRAM_CHAT_ID" | gh secret set TELEGRAM_CHAT_ID -R <owner>/aeon
   echo "$TELEGRAM_USER_ID" | gh secret set TELEGRAM_ALLOWED_USER_ID -R <owner>/aeon
   echo "$GH_PAT_TOKEN" | gh secret set GH_GLOBAL -R <owner>/aeon
   ```
5. **Telegram Command Menu Registration:**
   ```bash
   ./aeon telegram register
   # Dispatches .github/workflows/setup-commands.yml to register bot commands
   ```
6. **Running the Dashboard / CLI / Test Run:**
   - CLI commands: `cd /root/aeon && ./aeon <command>`
   - Trigger a skill: `./aeon skills run heartbeat` (or `gh workflow run aeon.yml -f skill=heartbeat -R <owner>/aeon`)
   - Dashboard: `cd /root/aeon && ./aeon` (defaults to port 5555).

## Pitfalls & Best Practices
- **gh Authentication:** Mutating commands (`./aeon secrets set`, `./aeon skills run`, etc.) fail immediately with an error if `gh auth status` is unauthenticated. Always run `gh auth setup-git` after token login.
- **Upstream Sync on Forks:** If `setup-commands.yml` is missing on older fork branches, `gh workflow run setup-commands.yml` returns 404. Fast-forward or merge `upstream/main` to your fork's `main` branch before registering.
- **Claude Code Authentication:** `CLAUDE_CODE_OAUTH_TOKEN` takes setup tokens generated via `claude setup-token` (`sk-ant-oat01-...`), whereas `ANTHROPIC_API_KEY` takes pay-per-token API keys. Set one or the other based on subscription type.
- **Repository Context:** Ensure `gh repo set-default <owner>/<repo>` is executed in the Aeon repo folder so CLI knows which target fork to inspect/dispatch to.
- **Pure Aeon vs Chatbot Gateway:** Pure Aeon uses GitHub Actions and headless worker harnesses; Telegram bots should be connected via `apps/webhook` dispatch or `./aeon` CLI triggers rather than treating the bot as an interactive conversational REPL only.
