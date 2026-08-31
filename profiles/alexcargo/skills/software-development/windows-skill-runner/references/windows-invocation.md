# Running skill helper scripts on Windows (Hermes desktop)

## Problem
On the Windows host the terminal's `python3` alias is shadowed by the
Microsoft Store stub. Running it prints:
```
Python was not found; run without arguments to install from the
Microsoft Store, or disable this shortcut from Settings > Apps > Advanced
app settings > App execution aliases.
```
`uv` is on PATH (`/c/Users/Stefan/AppData/Local/hermes/bin/uv`), but:
```
uv pip install --python /c/.../venv/Scripts/python.exe <pkg>
```
fails with: `error: No virtual environment or system Python installation found
for path ...; run uv venv to create an environment`. uv does not accept a raw
`.exe` path as a target environment.

## Working recipe (tested 2026-07-23)
1. Locate the real interpreter (NOT the Store stub):
   ```bash
   which python
   # -> /c/Users/Stefan/AppData/Local/hermes/hermes-agent/venv/Scripts/python
   ```
   Use that `.exe` path directly.
2. Install deps with the interpreter, not uv:
   ```bash
   "/c/Users/Stefan/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe" \
     -m pip install youtube-transcript-api
   ```
3. Run the helper (MSYS paths like `/c/Users/...` work; also fine to pass the
   script path with forward slashes):
   ```bash
   VENV_PY="/c/Users/Stefan/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe"
   SCRIPT="C:/Users/Stefan/AppData/Local/hermes/skills/media/youtube-content/scripts/fetch_transcript.py"
   "$VENV_PY" "$SCRIPT" "URL" --text-only --timestamps
   ```

## Note
The venv path is stable for this Hermes install; re-derive it with `which python`
if the layout ever changes. This pattern applies to ANY skill that ships a
Python helper script on this host, not just youtube-content.
