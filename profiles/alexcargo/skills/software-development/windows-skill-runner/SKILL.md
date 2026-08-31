---
name: windows-skill-runner
description: Run Python helper scripts shipped inside Hermes skills on the Windows (Hermes desktop) host. Use whenever a skill's SKILL.md says to run `uv run python3 scripts/foo.py` or `python3 <script>` and you are on this Windows machine — the bare `python3` alias is broken and `uv pip --python <exe>` fails to detect the venv. Covers the working interpreter path, dependency install, and MSYS-path gotchas.
platforms: [windows]
---

# Windows Skill Runner

## When to use
Any skill (youtube-content, ocr-and-documents, songsee, jupyter-live-kernel,
etc.) asks you to execute a bundled Python helper. On this Windows Hermes host
the naive invocation fails. Reach for this skill first.

## The trap (why the obvious command fails)
1. `python3` in the terminal resolves to the **Microsoft Store stub**, not a
   real interpreter. Running it prints:
   ```
   Python was not found; run without arguments to install from the
   Microsoft Store, or disable this shortcut from Settings > Apps > Advanced
   app settings > App execution aliases.
   ```
2. `uv` IS on PATH (`/c/Users/Stefan/AppData/Local/hermes/bin/uv`), but
   `uv pip install --python /c/.../venv/Scripts/python.exe <pkg>` FAILS with:
   `error: No virtual environment or system Python installation found for path ...`
   uv does not accept a raw `.exe` path as a target environment.

## The fix (tested 2026-07-23, used to run youtube-content's fetch_transcript.py)
1. Find the REAL interpreter (NOT the Store stub):
   ```bash
   which python
   # -> /c/Users/Stefan/AppData/Local/hermes/hermes-agent/venv/Scripts/python
   ```
   Use that `.exe` path directly in every command.
2. Install the skill's deps with the interpreter itself — not uv:
   ```bash
   "/c/Users/Stefan/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe" \
     -m pip install <pkg>
   ```
3. Run the helper (MSYS paths like `/c/Users/...` and forward-slash
   `C:/Users/...` script paths both work):
   ```bash
   VENV_PY="/c/Users/Stefan/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe"
   SCRIPT="C:/Users/Stefan/AppData/Local/hermes/skills/media/youtube-content/scripts/fetch_transcript.py"
   "$VENV_PY" "$SCRIPT" "URL" --text-only --timestamps
   ```

## Pitfalls
- Do NOT `uv run python3 <script>` and do NOT `python3 <script>` — both hit the
  Store stub.
- Do NOT `uv pip install --python <venv-exe>` — uv can't see that as an env.
  Use `<venv-exe> -m pip install` instead.
- The `which python` result is the stable, supported interpreter for this
  Hermes install. Re-derive it (don't hardcode) if layout ever changes.

## See also
- `references/windows-invocation.md` — full error transcripts + recipe.
- `hermes-agent-skill-authoring` — when authoring a new skill that ships a
  Python helper, note the Windows invocation in the skill's Setup section.
