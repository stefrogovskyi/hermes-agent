---
name: telegram-group-sweep
description: >-
  Put an AI agent into a Telegram working group WITHOUT realtime chatter and
  WITHOUT spawning extra bots. Covers the getUpdates diff mechanism (read only
  unseen fragments, hourly), the per-TOKEN conflict rule, the minimal-bot-footprint
  preference, and the cron/sweep architecture. Use whenever a user wants an agent
  (sales/support/ops) to monitor a group, react to mentions or on-domain content,
  and stay silent otherwise.
---

# Telegram Group Sweep (agent-in-group, hourly, diff-only)

Design pattern for letting an agent live in a Telegram group: see the WHOLE
context, read it on a schedule (not realtime), react only when useful, and never
proliferate bots. Captured from the Richard-Marlowe group-sweep session
(2026-07-23, Stevenson orchestrator).

## When to use
- User wants an agent to "be in the group", "watch the chat", "read context".
- User says: hourly batch read, not every message; react only to mentions or
  relevant content; don't add more bots to the group.
- Avoid for: realtime conversational bots (use the gateway instead).

## Core requirements (durable user preferences)
1. **Whole context** → BotFather `/setprivacy` → Turn off (Privacy Mode OFF),
   else the bot only sees its own @mentions.
2. **Hourly, not realtime** → read accumulated context once/hour (24 sweeps/day).
   Saves tokens; "достаточно раз в час".
3. **Diff-only** → read ONLY unseen fragments; never re-read seen content.
4. **React sparingly** → reply on @mention or genuinely-useful on-domain content;
   otherwise silence. Escalate price-out-of-pricing / contracts / finance.
5. **Minimal bot footprint** → ONE bot in the group. Do NOT add a separate
   "watcher" bot. User: "я не хочу плодить в группе ботов".

## The diff mechanism (read-only-unseen)
Telegram `getUpdates` returns each update to exactly ONE consumer of a token.
Track a persistent `last_update_id` and request:

```python
getUpdates(offset = last_update_id + 1, timeout=0, limit=100)
```

- `offset` = 1 + highest `update_id` already processed.
- Loop (page by 100) until empty → harvests everything accumulated.
- Filter by `chat_id` and `update_id > last_seen`. Update `last_update_id` only
  after committing the read.
- 24 hourly sweeps/day → full coverage, no duplicates, nothing lost (process alive).

## CRITICAL RULE (got wrong once — encode it)
**The realtime conflict is per-TOKEN, not per-GROUP.**
- One token's updates → one consumer at a time.
- So: never run BOTH a realtime gateway AND an hourly sweep on the same token.
- But a separate token = separate queue. An agent with its OWN token and NO
  realtime gateway on it can run the sweep alone — sole consumer, no conflict.
- CONCLUSION (user-corrected over-engineering): do NOT create a "group watcher"
  bot. Configure the agent ITSELF to sweep hourly. One bot in the group.

## Anti-pattern rejected (do not repeat)
- ✗ Spawning `hermes_group_watcher` (second bot) to read hourly while leaving the
  agent out.
- ✓ The agent's own token runs the sweep; the orchestrator only creates the cron
  and watches escalations, does NOT join the group.

## Minimal script shape (stdlib only, no pip)
- `fetch` → getUpdates diff → print JSON `{max_id, messages[]}`.
- `commit --max-id N` → persist `last_update_id`.
- `send --chat C --text T` → post as the agent.
- `digest --text T` → escalate to owner DM via same token.
- Env: `BOT_TOKEN`, `GROUP_CHAT_ID`, `STEFAN_CHAT_ID`, `BOT_USERNAME`.
- Dry-run with missing env must exit non-zero (e.g. 2) so cron catches it.

## Decision tree
1. Agent has its own token, no realtime gateway on it? → sweep on that token. DONE.
2. Same agent must ALSO do realtime DM? → use a SEPARATE token for the group sweep
   (group token ≠ DM token), never mix on one token.
3. Orchestrator needs to watch the group? → does NOT join; reads agent digests.

## SPOF / reliability
- Telegram retains accumulated updates ~24h (and ~100 in the immediate queue).
- Process down >24h → old queue lost. For 100% reliability run on VPS/Modal.
  On Windows Desktop it works while the Hermes process is alive.
- Persist `last_update_id` in a state file so restarts resume the diff cleanly.

## Cron
`every 1h` → run the sweep for each agent token. Per-agent state file keeps
diffs independent.

See `references/telegram_group_hourly_sweep.md` for a fuller annotated version
(decision tree, SPOF detail, script skeleton).
