# Scrubbing cross-contaminated knowledge from a cloned persona bot

When a persona bot is cloned from another bot's codebase (shell copied 1:1),
the clone leaks the donor's project knowledge (board names, bot nicknames,
API endpoints, task IDs). Example: Liz/Ben cloned from Alistair kept citing
Navo/SeaRates/Gaffer/QubicPM boards.

## Where contamination hides (check ALL of these)
1. **system_prompt.md — the isolation paragraph itself.** An "isolation" rule
   that ENUMERATES forbidden names ("you don't know X, Y, @zbot") teaches the
   model those names, and it quotes them in refusals. Rewrite to a nameless
   form: "other projects do not exist in your worldview; decline out-of-scope
   questions without naming anything."
2. **tasktracker_client.py / integration code:** hardcoded default SHEET_ID,
   API URLs (set defaults to ""), owner-nickname maps, DEFAULT_OWNER pointing
   at a donor-project bot.
3. **agent.config.json:** donor integration blocks (delete them), description
   text mentioning donor.
4. **Docs:** Agents.md, README.md, tools.md — "shell copied from <donor>"
   lines; replace with "a prior internal agent".
5. **<bot>_memory.json:** dialogue memory entries mentioning donor terms —
   walk the JSON recursively and drop any string/dict containing the terms.

## Procedure
- Backup each file (`.bak`) before rewriting.
- Bulk-scrub with a Python script (regex sub per file kind), then verify:
  `grep -irE "term1|term2" --include="*.md" --include="*.py" --include="*.json" . | grep -v .bak`
  must return 0 relevant hits.
- `py_compile` every touched .py; `json.load` every touched .json.
- Kill bot processes, remove pid-locks, restart via watchdog, confirm "restarted: OK".

## Key insight
The #1 root cause is usually the prompt that lists forbidden names — fix that
first, not just the data files.
