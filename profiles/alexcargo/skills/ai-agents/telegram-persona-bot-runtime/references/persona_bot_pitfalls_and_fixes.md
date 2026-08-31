# Persona Bot Runtime Pitfalls & Verified Fixes

## 1. Token Isolation Guardrail
- **The Trap:** If `_load_env()` searches `AppData\Local\hermes\.env` or if fallback code has hardcoded token strings from another bot (e.g. main orchestrator token `8682188433`), the persona bot process will poll the main orchestrator's token and hijack its Telegram identity.
- **The Fix:** Ensure each persona bot script (`richard_bot.py`, `alistair_bot.py`) sources `TELEGRAM_BOT_TOKEN` EXCLUSIVELY from its own local `.env.local` file and hardcodes its own dedicated token fallback. Add an explicit runtime guardrail assertion:
  ```python
  if BOT_TOKEN.startswith("8682188433"):
      raise RuntimeError("CRITICAL SAFETY BLOCK: Persona bot attempted to use Hermes main token!")
  ```

## 2. Lock File Stale PID Recovery
- **The Trap:** When `_acquire_lock()` reads a stale PID from `.lock` that is no longer running, a naive `psutil.pid_exists` check or failing to handle non-running PIDs causes new bot instances to see the lock file, print "duplicate process running", and immediately exit with `sys.exit(0)`.
- **The Fix:** If the old PID in `.lock` is dead or doesn't match a running `bot.py` process, `_acquire_lock()` must remove the stale lock file and acquire the lock cleanly instead of exiting:
  ```python
  def _acquire_lock():
      if os.path.exists(LOCK_FILE):
          try:
              old_pid = int(open(LOCK_FILE, encoding="utf-8").read().strip())
              if _is_bot_running_pid(old_pid):
                  if old_pid == os.getpid():
                      return
                  sys.exit(0)
              else:
                  os.remove(LOCK_FILE)
          except Exception:
              pass
  ```

## 3. Google Gemini REST API Role Alternation (HTTP 400 Fix)
- **The Trap:** Google Gemini REST API (`generateContent`) rejects payloads with consecutive `user` roles or `system` messages inside `contents`, returning `HTTP Error 400: Please ensure that roles alternate between user and model`.
- **The Fix:** Pass the system prompt in `system_instruction: {"parts": [{"text": system_prompt}]}` and merge consecutive messages of the same role in `contents` before sending the request:
  ```python
  payload = {
      "system_instruction": {"parts": [{"text": system_text}]},
      "contents": chat_contents
  }
  ```
