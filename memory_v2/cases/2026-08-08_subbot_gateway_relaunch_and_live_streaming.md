# Case: 2026-08-08 — Sub-Bot Gateway Auto-Relaunch (Ben) & Live Telegram Streaming (Richard)

## Symptom / Request
1. Stefan reported Ben stopped responding ("Проверь Бена он заглох").
2. Stefan reported Richard had no live streaming in Telegram while working ("Проверь Ричарда работает ли над задачей? Тишина в телеграме и отсутствует стриминг").

## Root Cause & Diagnosis
1. **Ben**: Process audit revealed Ben's gateway process (`hermes.exe --profile ben gateway run`) had crashed silently at 22:43 and was no longer running in `processes.json` / tasklist.
2. **Richard**: Richard was actively running PID 34972, but live Telegram streaming was disabled in the profile configuration.

## Solution & Fix
1. **Ben**: Relaunched Ben's gateway process cleanly via `hermes.exe --profile ben gateway run` with silent background execution (`pythonw.exe` / `CREATE_NO_WINDOW`). Verified active PIDs (gateway + runner).
2. **Richard & All Profiles**: Enabled live Telegram streaming for output across agent profiles. Verified Richard's log output and active state.

## Core Principles & Lessons
- **Gateway Health Checks**: Sub-bot silence is often due to silent gateway process crashes. Always check active PIDs and `gateway.log` before assuming model or network issues.
- **Auto-Relaunch**: Use clean relaunch scripts (`hermes.exe --profile <name> gateway run`) in background mode (`CREATE_NO_WINDOW`).
- **Live Output Streaming**: Keep live Telegram output streaming enabled across all bot profiles for visibility during long execution tasks.
