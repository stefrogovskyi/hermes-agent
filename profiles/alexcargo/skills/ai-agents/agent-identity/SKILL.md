---
name: agent-identity
description: Read persona files before answering identity questions.
version: 1.0.0
author: autonomous curator
license: MIT
platforms: [linux, macos, windows]
---

# Agent Identity Inspection

When the user asks about an agent/entity/persona, DO NOT answer from memory alone.
Read the live identity files first.

## Canonical source

Google Drive is source of truth. Drive root: `C:\Users\Stefan\My Drive\`

## Known entity folders

- **Richard Marlowe:** `Equity\My Biz\Partner companies\Navo\6. Departments\Richard Marlowe\Richard Hermes`
- **Liz Harper:** `Equity\My Biz\My companies\Enlight Group\Enlight Board\Liz Harper\Liz Harper Hermes`
- **Alistair Sterling:** `Equity\My Biz\Partner companies\Navo\6. Departments\Alister Sterling\Alistair Hermes`
- **Ben Jett:** `Equity\My Biz\My companies\Enlight Group\Avalanche Agency\Team\Ben Jett\Ben Jett Hermes`

Build absolute paths by prefixing with `C:\Users\Stefan\My Drive\`.

## Required files (read in this order)

1. `soul.md` — persona, character, voice, boundaries, non-negotiables
2. `system_prompt.md` — compiled system prompt for the LLM core
3. `AGENTS.md` — operational manual: roles, commands, integrations, architecture

## Workflow

1. Locate the entity folder under `C:\Users\Stefan\My Drive\...`
2. Read `soul.md`, `system_prompt.md`, `AGENTS.md` from that folder
3. Answer from the files, citing specifics. Do not invent facts not present in the files.

## Pitfalls

- Do NOT answer agent questions from memory alone — memory is high-level; files are source of truth.
- Do NOT search only local non-synced paths — Google Drive (`C:\Users\Stefan\My Drive\...`) is the canonical store for all four identities (Richard, Liz, Alistair, Ben).
- Do NOT guess roles/titles/partners — if the file says Chief People Officer, do not say CPO/Product.
- Cloned Agent Architecture: Cloned agents are isolated, standalone Python processes (`bot.py`) in their own folders with separate `.env.local` keys, individual Telegram tokens, and isolated task trackers (`tasktracker_store.json`). They operate as specialized leaf nodes or sub-orchestrators, with Hermes Stevenson acting as the Chief Orchestrator.
- Do NOT return generic summaries when the user asked for concrete bullet points; keep fidelity to file structure.

## Related

- `google-workspace` — only if Drive access/auth needs repair.
- `memory-recall` — for cross-session facts, not persona specifics.
