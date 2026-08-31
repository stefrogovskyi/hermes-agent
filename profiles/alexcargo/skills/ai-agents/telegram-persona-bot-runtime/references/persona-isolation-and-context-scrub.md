# Isolating a cloned persona bot + scrubbing leaked shared context

When a persona bot is cloned "1:1 from another bot's shell" (e.g. Liz/Ben cloned
from Alistair/Richard), it inherits the source bot's data surfaces. Symptom:
the bot answers with **another project's data** (foreign kanban, task IDs,
@nicknames) or keeps *naming* forbidden projects even while refusing them.

## Root-cause insight (the counter-intuitive one)

An "isolation" system prompt that **enumerates the forbidden entities by name**
TEACHES the bot those names. Example that backfired:

> "ты НЕ знакома с Navo, SeaRates, Ричардом (@richnavobot), Алистером
>  (@qubicpmbot), Гаффером (@thegaffermcp_bot), @lxxmng…"

The bot then cheerfully quotes "Navo / SeaRates / Gaffer / @lxxmng" in its
refusals. **Fix: rewrite the isolation block to be name-free** — "other
projects/trackers do not exist in your world; if a question is out of scope, say
so WITHOUT naming anything." Never list the forbidden names in the prompt.

## All surfaces that must be scrubbed (grep every one)

A clone leaks through MORE than memory. Scrub each of these:

1. `*_memory.json` — dialog memory; delete any entry matching the bad terms
   (walk dict values + list items recursively).
2. `system_prompt.md` — the isolation/identity block (see insight above).
3. `tasktracker_client.py` — **hardcoded defaults** are the sneakiest leak:
   `SHEET_ID = os.environ.get("GOOGLE_SHEETS_ID", "<source-bot's-sheet-id>")`
   `SALESLOOP_URL = os.environ.get(..., "https://…fly.dev/…")`
   and an owner-nickname map (`"alistair": "@qubicpmbot"`, `DEFAULT_OWNER =
   "@thegaffermcp_bot"`). Blank the defaults to `""`; drop foreign nick rows;
   repoint `DEFAULT_OWNER` to the bot's own owner.
4. `agent.config.json` — remove foreign integration blocks (e.g. a `salesloop`
   section) and any description referencing the source project.
5. `Agents.md`, `README.md`, `tools.md` — prose mentions.

Verification grep (exclude the backups you create):
```
grep -irE "navo|gaffer|qubic|<nicks>|salesloop\.fly|richnavobot" \
  --include="*.md" --include="*.py" --include="*.json" . | grep -v ".bak"
```
Legit env-var NAMES (`SALESLOOP_API_KEY`, `'salesloop'` backend guard) are fine
to keep if the code path is disabled by the blanked default — filter them out of
the grep rather than deleting working guards.

## Safe edit procedure

- Back up each file (`shutil.copy(p, p+".bak")`) before editing.
- Do bulk regex edits in ONE python heredoc (stdlib json+re) rather than many
  patch calls — clone files are large and repetitive.
- `py_compile` every edited `.py`; `json.load` every edited `.json`.
- Restart the bot cleanly: kill its `python.exe` (match on `<bot>_bot.py` in the
  command line), delete its stale lock (`entities/<name>.lock`), then run the
  bot's watchdog which re-launches it detached+windowless.

## Pitfall: invisible chars from heredoc/patch

A comment typed into a patch picked up a U+200B zero-width space →
`SyntaxError: invalid non-printable character U+200B`. If a fresh comment line
trips a syntax error, retype it as plain ASCII.
