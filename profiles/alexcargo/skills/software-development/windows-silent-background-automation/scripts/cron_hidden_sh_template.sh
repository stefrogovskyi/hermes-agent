#!/bin/bash
# cron_hidden_sh_template.sh — hidden launcher for a Hermes no_agent .py cron script.
# Copy this file per cron job, set SCRIPT to the real .py, and point the cron
# job's `script:` at this .sh (relative name only; must live under ~/.hermes/scripts/).
#
# WHY: Hermes cron runs .py scripts via the uv base python, which re-execs a visible
# conhost even under CREATE_NO_WINDOW. Wrapping in .sh lets Hermes use the hidden
# bash path. CRITICAL: call the BASE python directly — do NOT call pythonw.exe or the
# venv python.exe, because in a uv-created venv those are uv-LAUNCHERS that re-exec
# the visible base console anyway (confirmed: conhost still grew 3->4 with pythonw).
# Read venv/pyvenv.cfg: if `home = .../uv/python/...` and `uv = 0.11.x`, it's a
# launcher — point BASE_PY at the real cpython under that home.
BASE_PY="C:/Users/Stefan/AppData/Roaming/uv/python/cpython-3.11-windows-x86_64-none/python.exe"
VENV="C:/Users/Stefan/AppData/Local/hermes/hermes-agent/venv"
SP="$VENV/Lib/site-packages"
export VIRTUAL_ENV="$VENV"
export PYTHONPATH="$(dirname "$0")/..:$SP"
SCRIPT="C:/Users/Stefan/AppData/Local/hermes/scripts/REPLACE_WITH_YOUR_SCRIPT.py"
"$BASE_PY" "$SCRIPT"
exit 0
