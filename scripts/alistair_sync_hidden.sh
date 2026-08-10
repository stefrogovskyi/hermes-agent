#!/bin/bash
# Скрытая обёртка: BASE python (не uv-launcher) -> без чёрного окна.
BASE_PY="C:/Users/Stefan/AppData/Roaming/uv/python/cpython-3.11-windows-x86_64-none/python.exe"
VENV="C:/Users/Stefan/AppData/Local/hermes/hermes-agent/venv"
SP="$VENV/Lib/site-packages"
export VIRTUAL_ENV="$VENV"
export PYTHONPATH="$(dirname "$0")/..:$SP"
SCRIPT="C:/Users/Stefan/AppData/Local/hermes/scripts/alistair_sync.py"
"$BASE_PY" "$SCRIPT"
exit 0
