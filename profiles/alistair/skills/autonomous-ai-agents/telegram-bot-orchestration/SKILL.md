---
name: telegram-bot-orchestration
description: Use when orchestrating multi-agent bots in Telegram groups.
version: 1.0.0
author: Alistair
license: MIT
metadata:
  hermes:
    tags: [telegram, multi-agent, bots, loop-prevention, group-chat]
    related_skills: [hermes-agent, autonomous-ai-agents]
---

# Telegram Bot Orchestration & Multi-Agent Group Chats

## When to Use
Use when configuring or participating as an agent in shared Telegram group chats with other AI bots (e.g. Alistair, Callum, Richard) to prevent infinite ping-pong loops and manage routing rules.

## Multi-Agent Trigger Rules

When multiple bots coexist in a Telegram group chat:
- **Mention Enforcement**: `require_mention: true` should be configured in platform settings.
- **Trigger Words**: Explicit trigger words (e.g., bot name declensions "Алистер", "Каллум", "Ричард") allow addressing bots without `@username`.
- **Quote-Reply Handling**: Telegram quote-replies (replying directly to a message) bypass `require_mention` on most platform adapters because they are treated as direct thread participation.

## Mandatory Human Interaction Rules in Groups

System-wide mandatory rules for human interaction in group chats across all bot profiles (Orchestrator, Alistair, Richard, Callum, Ben, Liz):
1. **Response Triggers**: Respond to a human ONLY when:
   - (a) Directly tagged via `@username`.
   - (b) Directly replied to (Telegram Reply) on a message from the bot.
   - (c) Addressed by name in the text.
2. **Tone & Brevity**: Respond concisely, politely, and strictly to the point of the question.
3. **Inter-Human Silence**: If humans are conversing with each other without addressing the bot — maintain complete **SILENCE** and do not interject.
4. **Quote-Replies Tagging Others**: If a user replies (Quote-Reply) to a bot's message but explicitly addresses another team member or bot via `@mention` (e.g. `@colleague @otherbot что с этим?`), the bot must not take over the task or answer in depth. If triggered by the platform adapter on the quote-reply, keep the response strictly to acknowledging routing/hand-off to the tagged parties without interfering in their domain.

## Mandatory Bot-to-Bot Interaction Rules in Groups

System-wide mandatory rules established by Stefan Rogovskiy for bot-to-bot interaction across all bot profiles (Orchestrator, Alistair, Richard, Callum, Ben, Liz):
1. **Direct Tagging Only**: Respond to another bot ONLY if it addressed you directly via your personal `@tag` (`@qubicpmbot`, `@richnavobot`, etc.).
2. **Initiating Contact**: Initiate communication with another bot using their `@tag` and a clear task description ONLY upon receiving a direct order from Stefan.
3. **Default Behavior**: In ALL OTHER CASES — completely **IGNORE** messages from other bots (to eliminate infinite loops/ping-ponging).

## Company & Sub-Agent Domain Segregation (Strict Cross-Entity Taboo)
When sub-agents operate across different organizations or distinct client spaces (e.g. Navo vs Enlight):
- **Zero Cross-Company Leakage**: In one company's public, group, or team channels (e.g., Navo chats), NEVER mention, tag, or reference agents, staff, or projects belonging to another company (e.g. Enlight agents such as Ben or Liz).
- **Public Visibility Boundary**: Restrict mentioned personas strictly to the authorized roster for that specific organization (e.g. in Navo: Stefan Rogovskiy, Alistair, Richard, Callum, Alex Shatunov, Gaffer).
- **Enforcement**: Embed strict negative constraints in `SOUL.md` and persistent memory so the model never generates cross-company colleague references in group conversations.

## Preventing Agent-to-Agent Ping-Pong Loops

### The Problem
When Agent A replies to Agent B, Telegram tags Agent B in a quote-reply. Agent B's gateway sees the quote-reply as direct engagement and triggers Agent B. If Agent B responds with a polite confirmation ("Принято! 👍" or "На связи!"), Agent A receives a quote-reply and responds back, creating an infinite loop.

### Inter-Bot Tagging Rules
- **Actionable Tagging Only**: When communicating in shared group chats, bots must only `@mention` another bot if an explicit response or action is required from that bot.
- **No Non-Actionable Tags**: Avoid tagging other bots in informational/status messages or acknowledgments to prevent accidental automated triggers.
- **Group-Specific Custom Rules**: Certain group chats (e.g., *Navo Agents*) may enforce strict routing where bots respond exclusively to direct `@mentions`, direct replies/quotes to their own messages, or explicit name mentions.

### Prevention Protocol
1. **Identify Acknowledgments**: Recognize when an incoming message is a closing acknowledgment, emoji, status echo, system redirect ("Redirected current run..."), or non-actionable response from another bot or automated process (e.g., "Принято! 👍", "🤝", "На связи!").
2. **Break the Chain**: Do **NOT** send a follow-up polite acknowledgment, emoji, or echo reply.
3. **Actionable Check**: Only respond if the incoming message contains a new task, question, explicit instruction, or code/architecture work addressed to this agent.
4. **Clean Exit / Minimal Output**: Conclude the turn quietly (or with minimal non-conversational character like `.`) when an output is required by the platform runner, avoiding emoji/phrase echo loops that trigger further quote-replies.

## Troubleshooting Group Silence & Mention Failures
For detailed step-by-step log analysis and common fallacies, see `references/telegram_group_troubleshooting.md`.

### Diagnostics First (No Guesses)
- **Never attribute unhandled group messages to BotFather `/setprivacy`**: Users often have privacy disabled. Check local `config.yaml` (`require_mention`, `mention_patterns`, `allowed_chats`) and `gateway.log` / `agent.log` first before making claims about Telegram platform settings. Blaming `/setprivacy` when the user has already disabled group privacy causes user frustration.
- **Configuring Name Triggers with `require_mention: true`**:
  - Always use `telegram.mention_patterns` in `config.yaml` as a list of regex patterns (e.g., `['\\bалистер[а-я]*\\b', '\\balistair\\b', '\\balister\\b', '\\bалик\\b']`).
  - **Do NOT include `(?i)` in `mention_patterns`**: The gateway automatically compiles all patterns with `re.IGNORECASE`. Adding embedded `(?i)` flags causes Python regex syntax errors (`global flags not at the start of the expression`), breaking pattern matching and resulting in complete silence on name triggers.
  - Avoid setting `require_mention: false` in active group chats: without filtering, the bot receives all background messages and risks chiming into conversations between humans directed at third parties.
- **Script-Based Cron Jobs & Model Drift**:
  - For recurring jobs that run deterministic reporting scripts (e.g. API benchmarks, status checkers, exports), configure the cron job with `no_agent: true`.
  - This prevents scheduler aborts due to model drift guardrails (`Skipped to prevent unintended spend: global inference config drifted since this job was created`) when default inference models are upgraded.
- **Autonomous Asynchronous API Polling**:
  - When querying external carrier/tracking APIs that resolve asynchronously (e.g. returning HTTP 202 `TRACKING_IN_PROGRESS` or `AUTO_CANT_FIND_INFO`), never leave the waiting burden on the user.
  - Automatically spin up a background poller via `terminal(background=True, notify_on_complete=True)` to query the endpoint every 10–15s and deliver the completed report the moment the background resolution finishes.
- **Strict User Intent & No Unrequested Task Execution**: Never schedule, execute, or report unrequested cron jobs or task pipelines based on background context templates or stale prompts. Only act on explicit user instructions given in their current turn.
- **Immediate Cron Deletion on User Request**: When the user requests stopping or deleting automated messages/crons to groups, remove the job immediately via `cronjob(action='remove')` and verify across all ecosystem profiles that no other jobs target the group destination.
- **Conciseness on Demand**: When the user asks for a concise answer (e.g., "Ответь кратко"), respond directly in 1-3 short sentences without unnecessary background narration or fluff.
- **Check `config.yaml` Settings**:
  - `require_mention: true|false`: Dictates whether `@botusername` or direct quote-reply is strictly required. When `require_mention: true` is set, text wake-words in `group_trigger_keywords` may be gated depending on platform adapter rules.
  - `group_trigger_keywords`: List of declensions (e.g., `Алистер`, `Алистеру`). Ensure all required case/declension forms are listed.
  - `group_allow_from`: Ensure group chat ID or `*` is permitted.
- **Inspect Gateway Logs**: Check `profiles/<name>/logs/gateway.log` and `agent.log` for inbound message events, adapter filters, or `no @mention` logs.

