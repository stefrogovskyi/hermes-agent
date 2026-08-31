# Telegram Persona Bot — Token Isolation & Gemini REST API Formatting

## 1. Token Isolation Trap (Main Orchestrator Token Hijacking)

### Problem:
If a persona bot script (e.g. `richard_bot.py` or `alistair_bot.py`) contains a fallback default string literal matching Hermes's main orchestrator bot token (`8682188433`), or loads parent `.env` before local `.env.local`, the sub-bot will poll Hermes's main Telegram token and **hijack the orchestrator's Telegram chat turn**. When Stefan messages Hermes Stevenson, Richard Marlowe will answer on Hermes's channel.

### Solution & Guardrails:
1. **Force-bind `BOT_TOKEN` in `.env.local`:**
   Each sub-bot MUST read its own token from its local `.env.local` file (`8846249306` for Richard, `8738625022` for Alistair, `8857115619` for Liz, `8548593141` for Callum, `8766104921` for Ben).
2. **In-Code Assertion Guardrail:**
   At bot startup, add an explicit check before `getUpdates`:
   ```python
   if BOT_TOKEN.startswith("8682188433"):
       raise RuntimeError("CRITICAL SAFETY BLOCK: Sub-bot attempted to use Hermes main bot token (8682188433)!")
   ```
3. **Watchdog Verification (`_verify_bot_token_safety`):**
   Ensure `bot_watchdog.py` scans each bot script before spawning it and blocks execution if `8682188433` is detected.

---

## 2. Google Gemini REST API Role Alternation (`generateContent`)

### Problem:
When calling Google Gemini REST API (`generateContent`), passing `system` messages as `user` or sending consecutive `user` role items in `contents` triggers:
`HTTP Error 400: Please ensure that roles alternate between user and model`

### Solution:
Pass the system prompt using `system_instruction`:
```python
payload = {
    "system_instruction": {"parts": [{"text": system_text}]},
    "contents": chat_contents  # Strictly alternating user <-> model
}
```
If consecutive messages have the same role, merge their text into a single `user` or `model` part.
