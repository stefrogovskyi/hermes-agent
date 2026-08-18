#!/bin/bash
# Обёртка: запускает вахтёра сессии через venv с telethon
exec /opt/hermes/hermes-agent/venv/bin/python3 /opt/hermes/scripts/odessa_session_watchdog.py
