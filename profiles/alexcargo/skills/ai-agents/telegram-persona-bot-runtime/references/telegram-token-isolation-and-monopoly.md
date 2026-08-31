# Telegram Sub-Bot Token Isolation, Monopoly Enforcement & Gemini REST API Rules

## 1. Token Isolation & Sub-Bot Override
When launching persona sub-bots from parent processes (like Hermes gateway or Python runners):
- `os.environ["TELEGRAM_BOT_TOKEN"]` from the parent process can pollute the child process or be inherited.
- Sub-bot `.env.local` parser MUST explicitly override `TELEGRAM_BOT_TOKEN` in `os.environ` with the sub-bot's own token from its local directory, and ignore any parent `TELEGRAM_BOT_TOKEN`.
- Never hardcode dummy tokens containing asterisks (e.g. `8846249306:***`) in code defaults as string constants — always read the unmasked token from `.env.local`.

## 2. Monopoly Single-Instance Enforcement
- In addition to checking PID lock files (`richard.lock`), `_acquire_lock()` or bot startup MUST scan system processes via `psutil.process_iter()` and terminate any duplicate process running the same script (`target_script.py`) on the host.
- Multiple background instances polling the same Telegram token cause perpetual HTTP 409 Conflict loops, making the bot completely deaf/silent to user messages.

## 3. Gemini REST API Formatting (`system_instruction`)
- In Google Gemini REST API (`generateContent`), system prompts must be passed in `system_instruction: {"parts": [{"text": system_text}]}`, NOT as `role: "system"` inside `contents`.
- Passing `role: "system"` inside `contents` causes HTTP 400 bad request error ("roles must alternate").

## 4. Voice / Auto-TTS Rule
- Never enable `auto_tts: true` or auto-spoken readout in `config.yaml` without explicit user request.
- Spoken audio synthesis is strictly prohibited unless the user explicitly requests it ("ответь голосом", "озвучь").
