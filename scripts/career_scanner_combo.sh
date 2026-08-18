#!/bin/bash
# career_scanner_combo.sh — единый пре-ран для Career Scanner Daily:
# гарантированно запускает ОБА сканера, чтобы агенту не приходилось
# запускать check_dpworld_jobs.py самому (раньше это было в промпте и
# выполнялось нестабильно).
PY=/opt/hermes/hermes-agent/venv/bin/python3
[ -x "$PY" ] || PY=python3

echo "===== SCAN 1/2: Executive Careers Poller (22 companies) ====="
$PY /opt/hermes/scripts/executive_careers_poller.py
echo
echo "===== SCAN 2/2: DP World Oracle HCM Poller ====="
$PY /opt/hermes/scripts/check_dpworld_jobs.py
