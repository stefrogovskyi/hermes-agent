---
name: telegram-group-agent
description: "Configure an AI agent (a persona bot like Richard Marlowe, or any Telegram bot) to monitor and selectively participate in a Telegram group via HOURLY BATCH polling — NOT realtime. Covers the single-token architecture (no extra watcher bots), the getUpdates diff cursor, BotFather privacy mode, token batching to save tokens, and selective-response logic. Use when a user wants an agent added to a Telegram group to read full context and reply only on @mention or on-domain content, reading batched (e.g. once/hour) instead of streaming every message."
platforms: [linux, macos, windows]
---

# Telegram Group Agent — Batch Monitoring Setup

## When to use
- User wants to add an AI agent/bot to a Telegram group.
- Goal: agent sees group context but does NOT reply to every message; replies only on @mention or on-topic (on-domain) content.
- User wants the agent active in ANY group it's added to (no hardcoded chat_id filter).
- User says "don't spawn extra bots" — that's the correct instinct; see principle below.
- **Realtime vs batch — ASK, don't assume.** The original design here was HOURLY BATCH
  polling to save tokens. But a user may instead demand INSTANT replies ("if they ask a
  question he should answer right away, not wait for the hourly sweep"). In that case use a
  REALTIME long-polling bot on the agent's single token. Either is fine — BUT the two
  CANNOT coexist on one token (see the hard principle below: one token = one getUpdates
  consumer → a 409 conflict if two pollers run). Confirm which the user wants before
  building; the batch cron and the realtime bot are mutually exclusive consumers. If the
  user flips from batch to realtime mid-build, PAUSE/DELETE the hourly cron first.

## Core architecture principle (HARD — learned the hard way)
**One bot = one Telegram token = one consumer of `getUpdates`.**
- Do NOT create a separate "watcher" bot. Reuse the agent's OWN single token.
  (A user pushed back hard on spawning an extra group-watcher bot; the single
  agent token is sufficient and preferable — fewer entities, less confusion.)
- If you ALSO run a realtime gateway (e.g. Hermes messaging gateway) on that same
  token, the two consumers collide: the gateway eats the updates and the poller
  sees nothing. Resolution: the group-reading bot must NOT have its token wired
  into a realtime gateway; it is the sole consumer of its updates.
- **409 Conflict is the symptom of two consumers on one token.** If a `getUpdates` call
  returns HTTP 409, something else is ALSO long-polling that token (a second copy of the
  bot, a realtime gateway, a leftover daemon). Kill ALL python processes matching the bot
  and launch EXACTLY ONE copy. A "2-process chain" (python + its venv child) is ONE bot,
  not a conflict — only count distinct `commandline` matches, and watch for a 2nd chain.
- Two DIFFERENT tokens = two independent update queues = no conflict. (So an
  orchestrator's DM token and the agent's group token coexist fine; the
  orchestrator need not be in the group at all.)
- Corollary: to "read the group hourly, not realtime," just don't run a realtime
  consumer on that token and poll it on a cron instead.

## The diff mechanism (read ONLY unseen messages)
Telegram `update_id` is GLOBAL per bot (not per chat). Use it as a cursor:
1. Persist `last_update_id` in a state file (`group_state.json`).
2. Poll: `getUpdates(offset = last_update_id + 1, timeout=0, limit=100)`.
3. Page through ALL results (loop until empty or < 100 returned) — never stop at
   one batch, or you drop messages.
4. Filter: optional `chat_id` (only if restricting to one group) and
   `update_id > last_update_id`; SKIP updates with no `message`/`edited_message`
   key (callback queries, etc.).
5. After processing, set `last_update_id = max(update_id)` and COMMIT (write state).
   If you skip commit, the next poll redelivers the same messages.
6. To be active in ANY group, DROP the chat_id filter (read all chats the bot is
   in). `update_id` being global means one cursor covers every chat.

Coverage guarantee: N hourly polls × persisted cursor = full coverage, no
duplicates, no loss — AS LONG AS the polling process stays alive. Telegram retains
accumulated updates ~24h (and ~100 in queue); if the poller is down >24h, older
queued updates are dropped (SPOF). For hard guarantees, run the poller on a
VPS/Modal, not a desktop that sleeps.

## Privacy mode (BotFather) — REQUIRED for full context
The bot receives ONLY @mentions/edited messages unless Privacy Mode is OFF.
- BotFather → `/setprivacy` → **Turn off** for any bot that must see full group
  context. Without this, "read all group context" is impossible.

## Selective response logic (let the agent decide)
**STEFAN'S HARD RULE (2026-07-28, Richard Marlowe): the bot is SILENT by default.**
Do NOT key the reply on generic on-domain keywords (container / freight / tracking / ETA) —
that makes it answer every logistics question in the group, which Stefan explicitly rejected
("he must NOT reply to every message"). Reply ONLY when:
- (a) explicit @mention (`@richnavobot` / `@richard`),
- (b) addressed by name/variant (ричард, richard, richie, ричи, рич — NOT bare "rich" inside
      other text). IMPORTANT: for Russian bot names like Алистер, use declension-matching regexes
      with word boundaries `\b(алистер[а-я]*|alistair[a-z]*)\b` so the bot triggers when users write
      "Алистера", "Алистеру", "Алистером", "Алистере", etc.
- (c) it is a reply to one of the bot's OWN messages, OR
- (d) context makes it CLEAR the message is about THIS agent's SALES or CLIENTS
      (e.g. for Richard: navo, navo24, trackingmcp, schedulesmcp, loadingmcp, freightratesmcp,
       продаж, клиент, демо, тариф, прайс, цен, заказ, подключ, free tier, trial, коммерч).
      A statement about a client/demo counts (no `is_question` requirement).
Mentions of OTHER bots (`@thegaffermcp_bot`) and generic logistics ("как отследить контейнер",
"какой фрахт до Шанхая") → SILENT.
The exact filter code lives in `telegram-bot-polling-ops` Root-cause #4 (with SALES_TERMS list
and the test matrix). If you are building a DIFFERENT agent, apply the same shape: silent by
default, address-or-clear-commercial-intent as the only triggers — never "any on-domain keyword".
- ESCALATES to owner via DM digest (never replies in-group) for: price outside
  rate card, large contract, any financial/legal ask (per agent guardrails).
- ANSWERS ALL participants (no admin-only gating) unless the user wants otherwise.
- Voice/tone per the agent's own system_prompt / agent.config.json.

## Where the LLM step lives
A plain cron/scheduler job can't "decide" — it just runs a script. To make the
agent actually decide (reply vs silence, compose the reply, escalate), wire the
poller into an agentic cron: the cron collects the diff via `fetch`, applies the
agent's judgment via system_prompt, posts via `send`, escalates via `digest`, then
`commit`s the cursor. Template prompt in references/cron_prompt.md.

## Security
- Store the bot token ONLY as an env reference in a local `.env` (gitignored).
  Never inline in code or commit.
- If the user PASTES a live token in chat: save it to local `.env`, confirm via
  `getMe` (returns username+id), and WARN the user to revoke+reissue the token in
  BotFather afterward (tokens sent over chat are exposed). Do NOT echo the token
  back in chat.
- `STEFAN_CHAT_ID` (owner chat id) is needed for escalations; reading + replying
  in groups works without it, but digests won't deliver.

## Verification (ad-hoc, no live API — do this before claiming done)
Mock `api()` and assert the logic WITHOUT network or token:
- Synthetic `getUpdates` batches: some updates with NO `message` key, spanning
  multiple chat ids, with update_ids 1..150.
- Assert: only message-bearing updates captured; non-message updates skipped;
  BOTH chats read (no group_id filter); diff (second poll with last_id=max returns
  empty); partial diff (last_id=50 → only id>50); commit persists; missing token
  exits non-zero; send/digest hit correct targets.
- Run the mock, then delete the temp test file. See scripts/verify_sweep.py
  (self-contained harness) and references/verification.md.

## Files in this skill
- scripts/telegram_group_sweep.py — reusable, parameterized poller (fetch/commit/send/digest).
- scripts/verify_sweep.py — mock-based logic verification harness (no network).
- templates/.env.example — env layout.
- references/telegram_notes.md — Windows venv-python gotcha, getUpdates cursor details, privacy mode.
- references/telethon_user_client_routing.md — Telethon user-client scanner, local terminal login security (avoiding in-chat code invalidation), and Google Maps avoidance routing.
- references/cron_prompt.md — template agentic cron prompt that wraps the poller.

## Realtime bot variant (Richard Marlowe's actual live setup)
The batch design above is ONE valid consumer. Richard instead runs as a **realtime
long-polling bot on the single token** (Stefan's hard requirement: "if they ask, he should
answer right away, not wait for the hourly sweep"). When flipping batch→realtime, PAUSE/DELETE
the hourly cron first (two consumers on one token = 409 / duplicate replies). Runtime hardening
for that realtime bot lives in the `telegram-persona-bot-runtime` skill: Windows-safe PID-lock
(prevents the duplicate-bot duplicate-reply bug), `sendChatAction` typing ticker,
`reply_to_message` context injection, tiered `u:/g:/gu:` memory, and Nous-inference key sourcing
so the bot answers "like the orchestrator" without an OpenRouter key. Also: **Stefan tests
Richard in PM as a CLIENT (sales mode), NOT an admin console** — don't route his chat_id to a
build/audit mode. Persona must come from a loaded `system_prompt.md`, never hardcoded, so edits
take effect without code changes.

## Operational notes (Windows / MSYS — cost real time this session)
- Cyrillic+space paths break `py_compile <abs>` ("No such file") and `rg`/`search_files`
  ("IO error"). FIX: `cd` into the dir, then use RELATIVE paths (`py_compile richard_bot.py`,
  `read_file` instead of content-search).
- `sendChatAction(action="typing")` auto-clears after ~5s — keep a background ticker (every
  ~4s) alive during an LLM call so "Typing…" stays visible for 10–20s responses.
- Privacy OFF is cached at group-join time: after `/setprivacy` Turn off, REMOVE+RE-ADD the
  bot or it still sees only @mentions.
- 409 = two consumers on one token. Kill all matching python, confirm ONE chain (2 procs =
  python+venv child = one bot), launch exactly one copy.
