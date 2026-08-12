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

### Diagnostics First (No Guesses)
- **Do NOT guess BotFather privacy settings**: Never claim `/setprivacy` or BotFather settings are the cause without inspecting local configs first.
- **Check `config.yaml` Settings**:
  - `require_mention: true|false`: Dictates whether `@botusername` or direct quote-reply is strictly required vs wake words.
  - `group_trigger_keywords`: List of declensions (e.g., `Алистер`, `Алистеру`). Ensure the case/form used in the message is listed.
  - `group_allow_from`: Ensure group chat ID or `*` is permitted.
- **Inspect Gateway Logs**: Check `profiles/<name>/logs/gateway.log` and `agent.log` for inbound message events, adapter filters, or `Blocked unauthorized user` / `no @mention` logs.

