# Case: Richard Sub-Bot Token Isolation & Watchdog Preflight Validation

## Symptom
Richard Marlowe Telegram bot (`@richnavobot`) stopped responding to user messages and briefly inherited the main Hermes agent bot token (`8682188433`), leading to Hermes answering messages intended for Richard inside Richard's chat context.

## Hypothesis vs Fact
- **Hypothesis**: The Telegram API credentials for Richard expired or were rejected by Telegram servers.
- **Fact**: The sub-bot launcher environment fell back to default `TELEGRAM_BOT_TOKEN` (Hermes main token) when Richard's process crashed, causing `richard_bot.py` to register under the Hermes token instead of Richard's dedicated token (`8846249306`).

## Root Cause
Lack of explicit preflight validation on sub-bot token identity prior to process initialization. When environmental variable resolution fell back to the root configuration, the sub-bot process launched under the primary agent's token.

## Fix
1. Explicit token check and hard-coded token isolation inside sub-bot wrappers (Richard token: `8846249306`).
2. `bot_watchdog.py` preflight check: before polling or invoking `getMe` / `getUpdates`, verify `bot.id == expected_bot_id` to prevent cross-bot token bleed.
3. Added hard error exit if `TELEGRAM_BOT_TOKEN == HERMES_BOT_TOKEN` inside any sub-bot process.

## Key Lesson / Principle
Sub-bots MUST NEVER fall back to the primary Hermes agent token. Every sub-bot launcher must enforce strict token isolation and perform a preflight identity check against its designated Telegram bot ID before processing incoming messages.
