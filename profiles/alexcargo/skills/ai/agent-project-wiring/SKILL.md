---
name: agent-project-wiring
description: >
  Scaffold and wire a full AI-agent project end-to-end: persona/ops/tool files,
  a stdlib REST client, a Telegram bot with admin/client chat_id routing, a
  Make.com automation blueprint, a self-pruning memory.md + weekly cron steward,
  Hermes skill registration with linked references to LIVE files, and a private
  GitHub repo as source of truth. Use when building any durable agent that must
  run across chat/voice/email and remember across sessions.
---

# SKILL — Agent Project Wiring (class-level)

Reusable pattern for building a durable, multi-channel AI agent that persists
memory and version-controls itself. Distilled from the Richard Marlowe / Navo build.

## Project file skeleton (the agent's "brain")
Keep these in ONE project folder (ideally git-synced):
- `soul.md` — persona: values, voice, tone samples, what NOT to do.
- `Agents.md` — roles, product/domain knowledge, competitive intel, playbooks, KPIs, guardrails.
- `tools.md` — exact tool/API call contracts + JSON examples (MCP/REST/webhook).
- `system_prompt.md` — compiled system prompt (persona + knowledge + tools focus).
- `agent.config.json` — machine-readable: channels, integrations, tool list, memory auto-load + self-inventory, guardrails.
- `memory.md` — LIVE, curated working memory (see references/self-pruning-memory.md).
- `SKILL.md` — this skill's entry; registers the agent in Hermes.

## Register in Hermes with LINKED REFERENCES to live files (key trick)
The skill copy lives in `~/AppData/Local/hermes/skills/<cat>/<name>/`, but its
`references/*.md` should POINT at the live project files (not duplicate them), so
edits to the project propagate to the agent on next activation. See
references/hermes-linked-refs.md. On activation the skill reads `memory.md` FIRST,
then `soul.md`.

## Channel wiring
- **Telegram bot (stdlib-only)**: admin/client routing by `chat_id` — Stefan's
  id → operations-console mode (build/audit), anyone else → sales/client mode.
  Two system prompts selected by id. See references/telegram-admin-routing.md.
  See references/voice_and_mcp_integration_patterns.md for STT/TTS voice upgrades (`gpt-4o-transcribe` / `gpt-4o-mini-tts`), native `.ogg` voice bubble sending (`sendVoice`), Navo24 MCP `Accept` headers, and SeaRates API endpoints.
- **Make.com (preferred over n8n)** when the user has Make experience: blueprint
  = `gateway:CustomWebHook` → `http:ActionSendData` (LLM or API) →
  `telegram:sendMessage`. NOTE: blueprint exports MODULE STRUCTURE only; API
  keys/connections are NOT exported — recreate them once on import. See
  references/make-blueprint.md.
- **Retell voice**: SIP trunking, <800 ms, bind same LLM; escalate legal/
  financial to human.

## Tooling without dependencies
- A stdlib-only REST client (`urllib`) works inside the execute_code sandbox with
  no `pip install` — useful for live API calls from chat.
- Verify changed `.py`/`.json` files: write a temp `hermes-verify-*.py` in
  `%TEMP%`, run it (mock network where possible), then DELETE it. This satisfies
  the ad-hoc verification requirement without leaving cruft.

## Self-pruning memory (keep the agent light)
`memory.md` is rewritten weekly by a cron "steward" that keeps high-signal
facts and drops stale ones (target < ~150 lines). Forgetting dead facts is GOOD.
See references/self-pruning-memory.md.

## Version control (source of truth)
Mirror the project to a PRIVATE GitHub repo; that repo is the source of truth.
`git init` in the local (OneDrive) folder, remote = private repo, branch `main`.
`.gitignore`: `.env`, `*.env`, `__pycache__/`, `*.log`, `.idea/`, `.vscode/`,
`.DS_Store`. NEVER commit real API keys — use env vars. After any edit:
`git add -A && git commit && git push`. See references/github-sync.md.

## Guardrails to bake in
- Don't promise out-of-scope capabilities.
- Don't fabricate data (e.g. container ETA) — say "no carrier data".
- Don't spam/pressure; don't disclose confidential info outside NDA.
- Escalate legal/financial/contract/signing to a human.

## Overlap note
Adjacent to bundled `hermes-agent-skill-authoring` (SKILL.md format/validator)
and `software-development` skills — those cover the skill FILE; this skill covers
the full agent PROJECT + channel + memory + VCS wiring beyond the skill file.
Curator may consolidate.
