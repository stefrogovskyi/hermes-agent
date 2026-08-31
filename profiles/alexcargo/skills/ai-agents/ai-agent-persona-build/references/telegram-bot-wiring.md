# Telegram bot wiring — concrete recipes

Two proven ways to put a persona agent on Telegram. Pick per the build.

## A. Hermes gateway bot → answer AS the persona

Problem: bot is "connected" (gateway running, polling) but greets as the default
"Hermes Agent from Nous Research" and even hallucinates the OS. The gateway is
using its stock system prompt, not yours.

Mechanism (read from source, not guessed): `gateway/run.py` builds the session
system prompt via `_load_ephemeral_system_prompt()`, which returns
`os.getenv("HERMES_EPHEMERAL_SYSTEM_PROMPT")` if set, else
`cfg_get(cfg, "agent", "system_prompt", default="")`. So the persona goes in
`~/.hermes/config.yaml` under `agent.system_prompt`.

Steps:
1. Compress `system_prompt.md` into one line (no YAML multiline needed):
   ```
   hermes config set agent.system_prompt "You are <Name>, <role>. Owner: <owner>. Voice: ... Guardrails: ..."
   ```
   (Warning "not a recognized config key" is expected — the gateway still reads it.)
2. `hermes gateway restart`.
3. Verify in Telegram: send "Расскажи о себе". Then `hermes logs` should show
   `Sending response (NNN chars) to <chat_id>` — no "Blocked unauthorized user",
   no default-persona text, no OS hallucination.
4. If still default: try env `HERMES_EPHEMERAL_SYSTEM_PROMPT` or a `/skill <name>`
   load; the config key is per-gateway-startup and must be re-read after restart.

Auth gotcha: gateway drops unknown chats with `Blocked unauthorized user <id>`.
Pair the owner chat first (`hermes pairing list` / `hermes pairing approve
telegram <code>`). `/pair` may not exist — look for `/approve` via
`https://api.telegram.org/bot<TOKEN>/getMyCommands`.

## B. Standalone stdlib bot (`python telegram_bot.py`, long polling)

Use when the bot is a single persona (not the orchestrator) and you want it
decoupled from the gateway. No external deps — `urllib`, `json`, `threading`.

Golden rule — ONE process per bot:
- Telegram allows only one `getUpdates` stream per bot. Two runners ⇒
  `HTTP Error 409: Conflict`; replies flaky / dropped.
- A `terminal(background=true)` launch makes a deep `bash→bash→python` chain and
  spawns a venv-python + uv-python (2 procs = one bot, that's normal). Repeated
  launches accumulate orphans.
- Kill-all-then-one recipe (PowerShell / git-bash):
  ```powershell
  Get-CimInstance Win32_Process -Filter "Name='python.exe'" |
    Where-Object { $_.CommandLine -like '*BOT_SCRIPT*' } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
  ```
  In git-bash use `taskkill /F /PID <pid>` (single slash — `//F` is rejected).
  Wait, confirm ZERO processes, then launch exactly one.

Stub-mode pattern for placeholder keys (so the bot runs before real creds exist):
- Bot requires `TELEGRAM_BOT_TOKEN`, `NOUS_API_KEY` (LLM), `NAVO_API_KEY` (tools).
  With stubs, guard early instead of raising at startup:
  ```python
  nous_key = os.environ.get("NOUS_API_KEY", "")
  if not nous_key or nous_key.startswith("stub-"):
      return os.environ.get("RICHARD_STUB_MESSAGE", "Configuring…")
  ```
- Load `.env.local` manually at `__main__` (stdlib only, no python-dotenv):
  skip `#`/blank lines, split on first `=`, strip quotes, set only if unset.
- `navo_client.call_tool` still honestly raises `RuntimeError("NAVO_API_KEY not
  set")` on a real tool call — the bot's try/except turns that into a clean
  "hit a snag" reply. Real mode is untouched once real keys replace `stub-…`.
- Secrets in `.env.local`; repo `.gitignore` must contain `.env*` so the file is
  never committed. Verify with `git check-ignore .env.local`.

Verify recipe (temp script, auto-approved when filename starts `hermes-verify-`):
count bot processes == one chain; `git check-ignore .env.local` returns
the path; `.env.local` contains `stub-` (no real keys); stub self-test returns the
honest message. Do NOT spawn a second bot inside the checker — it inflates the
count and looks like a duplicate.
