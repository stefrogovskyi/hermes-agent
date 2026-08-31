# Telegram Group Behavior — concrete recipe (persona bot in groups)

Condensed from a build where Richard Marlowe (richnavobot, Navo24 sales agent)
was deployed into a Telegram group: read-all context, reply selectively, no spam,
answer instantly. Reusable for any persona bot in groups.

## 1. Privacy (do this first)
- BotFather -> `/setprivacy` -> **Turn off**. Without this the bot only sees
  `/`-commands, replies-to-bot, and service messages — NOT the group context.
- WARNING: After toggling privacy, **remove the bot from the group and re-add it.**
  Telegram caches privacy at join time; it will not refresh otherwise.

## 2. Single-consumer rule (the constraint that breaks naive designs)
Telegram delivers each update to exactly ONE `getUpdates` consumer per token.
- Two long-polling processes on the same token -> `409 Conflict` (messages bounce,
  replies flaky). Kill-all-then-one. (See main skill 409 pitfall.)
- Realtime bot vs scheduled sweep on the same token = mutually exclusive. Pick one:
  - **Realtime** (user: "answer immediately, don't wait for the sweep") -> instant
    replies, single process, NO sweep. This is the usual default.
  - **Sweep-only** (batch reading e.g. every hour) -> no realtime bot running.
- Do NOT add a *second* bot just to read the group. The persona bot's own token
  is the only consumer it needs.

## 3. Reading only unseen messages (diff mechanics)
`getUpdates(offset = last_update_id + 1)`. Persist `last_update_id` in a state
file; each run fetches `update_id > last_seen`, filters by chat, then commits the
new max. `update_id` is global per bot (not per chat), so one pointer covers all
chats. Guarantees: no duplicates, no missed messages while the process is alive.
(For the realtime path the gateway handles this internally — no script needed.)

## 4. Gateway config (Hermes) for read-all / reply-selectively
```yaml
telegram:
  allowed_chats:
    - "-1001234567890"        # DM or specific group if you DO want to restrict
  group_allowed_chats:
    - "-1001234567890"
  require_mention: true            # only reply when directly addressed
  observe_unmentioned_group_messages: true  # see everything, reply selectively
```
- To allow the bot in ANY group (no chat_id filter), omit `allowed_chats` /
  `group_allowed_chats` restrictions (don't hardcode a single GROUP_CHAT_ID).
- `require_mention: true` + `observe_unmentioned_group_messages: true` = the
  "OpenClaw/Yuanbao-style" group behavior the docs describe.

## 5. .env pattern (secrets as env refs, never plaintext in chat/repo)
```
TELEGRAM_BOT_TOKEN=<bot token>      # the persona bot's ONLY token
STEFAN_CHAT_ID=330656040            # OWNER DM — private escalations only
BOT_USERNAME=richnavobot            # mention detection
ON_DOMAIN_KEYWORDS=логистика,фрахт,navo,tracking,rate,shipment,...
```
- `.env` is git-ignored; `.env.example` is committed with empty values.
- Token forwarded through a chat = leak risk; recommend BotFather `/revoke` +
  update `.env` after the session.

## 6. system_prompt.md personality additions (write into the prompt body)
- Persona touch: "A dash of British humour — sparingly. Dry, self-deprecating…
  only now and then; most replies stay straight."
- NON-WORK CHATTER block:
  - Respond only when addressed directly (mention / reply-to-bot). Never jump in.
  - Don't answer every poke — occasionally is fine, quiet is the right call.
  - Keep it 1–2 sentences, same tone.
  - Never spam groups; silence when not addressed is correct.
- Work messages (on-domain) follow full playbooks; humour is seasoning, not meal.
- Escalation: price-out-of-policy / contract / finance -> NO group reply, send
  digest to owner DM instead.

## 7. Verification (do before declaring done)
- `getMe` probe confirms the token maps to the right bot username.
- Send the owner a test DM via `sendMessage` to confirm the escalation channel.
- `fetch` against the live API returns `{"max_id":0,"messages":[]}` when the bot
  isn't yet in a group (correct, not an error).
- After adding the bot to a group + a test message: a realtime run should reply
  instantly; confirm exactly ONE process holds the token (no 409).
