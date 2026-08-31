# Bot / Agent Verification — in-process ping (no user, no getUpdates)

## Problem Stefan flagged
Hermes kept saying "write to him and tell me what he says" instead of verifying
the bot itself. Stefan: "ты же сам можешь его пинговать и посмотреть, что он
отвечает."

## Technique (verified working)
For a Telegram bot that is a plain .py loop (Richard, Liz, Alistair, Ben):
1. Locate the bot's .py (e.g. richard_bot.py).
2. In a separate python (hermes venv), import it WITHOUT running its main loop:
   ```python
   import importlib.util
   spec = importlib.util.spec_from_file_location("rb", r"<path>/richard_bot.py")
   rb = importlib.util.module_from_spec(spec); spec.loader.exec_module(rb)
   # many bots start the poll under `if __name__=="__main__"`, so importing
   # the module does NOT start the loop.
   print(rb.llm_chat([{"role":"user","content":"ping"}]))
   ```
3. Read the returned dict: `resp["choices"][0]["message"]["content"]` + the
   model/base the function actually used. THAT is the fact (which model/provider
   the bot runs on).

## CRITICAL — never call getUpdates manually
- Calling `getUpdates` on a live bot from a diagnostic script collides with the
  bot's own long-poll → `409 Conflict` → silences the bot's queue (bot goes mute).
  Seen with Richard and Liz.
- Diagnose ONLY via in-process calls (above). Never consume the bot's Telegram
  update queue for testing.

## Telegram gateway bots (Hermes/Liz via the gateway)
- Prefer the in-process import approach. If the bot is wired through Hermes
  gateway, import its agent module and call its chat/run function directly.
