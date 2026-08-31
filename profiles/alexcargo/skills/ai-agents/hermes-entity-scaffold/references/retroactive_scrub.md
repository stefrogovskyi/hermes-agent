# Retroactive knowledge scrub — make a deployed bot FORGET sibling projects

Use when a bot is already live and the user says "let X forget everything about
Navo / SeaRates / Gaffer / <sibling project>" (Liz/Ben 2026-07-25). The bot keeps
citing forbidden names because they are embedded in its files, not just memory.

## Where leaked names hide (grep ALL of these, per entity folder)
Bot folder e.g. `…\Enlight Group\…\<Entity> Hermes\`:
- `system_prompt.md` — the #1 culprit: an isolation clause that LISTS the
  forbidden entities. The bot reads the list and quotes it back in refusals.
- `<entity>_memory.json` — dialogue History; a past exchange may contain the
  leaked names verbatim.
- `tasktracker_client.py` — `SHEET_ID` / `SALESLOOP_URL` hardcoded DEFAULTS (the
  `os.environ.get("X", "<real value>")` fallbacks), `OWNER_MAP` sibling handles,
  docstrings/comments mentioning "канбан Гаффера / SalesLoop", `DEFAULT_OWNER`.
- `agent.config.json` — an integrations block (e.g. `"salesloop": {…}`).
- `Agents.md`, `tools.md`, `README.md` — provenance + integration prose.

## Scrub procedure (one execute_code / heredoc python pass)
1. **Backup** each file (`shutil.copy(p, p+".bak")`) before editing.
2. **system_prompt.md**: regex-replace the entire enumerated isolation paragraph
   with the GENERIC depersonalized clause (see SKILL step 6). This is the fix
   that actually stops the quoting behavior.
3. **memory json**: recursively walk dict/list; DROP any string value (or dict/
   list item containing one) matching
   `re.compile(r"navo|searates|gaffer|qubic|lxxmng|salesloop|richnavobot|thegaffermcp", re.I)`.
   Guard `searates` if the owner's real company is SeaRates.com — use
   `searates(?!\.com)` so you don't wipe legit CEO bio lines.
4. **tasktracker_client.py**:
   - `os.environ.get("SALESLOOP_URL", "https://salesloop.fly.dev/…")` → default `""`
   - `os.environ.get("GOOGLE_SHEETS_ID", "<id>")` → default `""`
   - delete sibling OWNER_MAP lines; set `DEFAULT_OWNER` to the entity's own
     owner (e.g. `@benjett`), never a sibling handle
   - obfuscate comments/docstrings ("канбан Гаффера" → "внешний канбан (отключён)")
5. **agent.config.json**: `json.load`, pop the integration block
   (`strip("salesloop")`), `json.dump` with `ensure_ascii=False, indent=2`.
6. **docs**: replace `(Navo PM)` provenance with "предыдущего внутреннего агента",
   strip SalesLoop/@handle lines.

## Verify before done
- Re-grep all working files (exclude `*.bak`) for the bad-word set → expect the
  only survivors to be intentional (`SALESLOOP_URL` env-var NAME, the `if b ==
  "salesloop": b="stub"` guard). Zero prose/name hits.
- `py_compile` every edited `.py` — WITH a Windows literal path, not an MSYS
  `/c/...` path (py_compile chokes on the mangled path and reports a false
  "No such file").
- Restart the entity via its watchdog (`rm entities/<e>.lock; python
  <scripts>\<e>_watchdog.py`) so it reloads clean state; confirm "restarted: OK".
- Watch for `U+200B`/zero-width chars if you author replacement comments via a
  patch tool — they trigger `SyntaxError: invalid non-printable character`.
  Re-patch to plain ASCII if the lint flags it.
