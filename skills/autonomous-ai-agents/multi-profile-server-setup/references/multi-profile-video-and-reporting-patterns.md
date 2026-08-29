# Multi-Profile Sync, Video Analysis & Report Formatting Guide

## 1. Telegram Video Notes (Кружочки) Pipeline & Multi-Profile Daemon Restart
- **Telegram Filter Requirement:** Ensure `filters.VIDEO_NOTE` and `msg.video_note` are explicitly handled in `adapter.py` alongside `filters.VIDEO`.
- **Multi-Profile Python Cache Pitfall:** When modifying core adapter/plugin files under `/opt/hermes/hermes-agent/`, all independent profile daemons (`hermes-default`, `hermes-alistair`, `hermes-richard`, `hermes-callum`, `hermes-liz`, `hermes-archie`, `hermes-ben`, `hermes-harrison`) keep stale bytecode in memory.
  - Fix: Always purge `find /opt/hermes/hermes-agent -name "*.pyc" -delete` and restart ALL systemd services together: `systemctl restart hermes-*`.
- **Multimodal Video Note Pipeline:**
  1. Extract audio via `ffmpeg -i video.mp4 -vn -acodec libmp3lame /tmp/audio.mp3 -y`
  2. Transcribe audio with `faster-whisper`
  3. Extract keyframes via `ffmpeg -i video.mp4 -vf "fps=0.5" /tmp/video_frames/frame_%02d.jpg -y`
  4. Inspect frames natively via `vision_analyze`

## 2. Real Bot Usernames Verification Pattern
- Never guess or extrapolate bot usernames (e.g. `@bennavobot` or `@alistair_navobot`).
- Query official `https://api.telegram.org/bot<TOKEN>/getMe` for each token in `/opt/hermes/profiles/*/.env`.

## 3. Visual & Russian-Language Report Standards (Stefan's Preference)
- **Zero Raw Logs:** Never send raw logs (`[SKIPPED_disabled]`, brackets, unparsed arrays) in Telegram DM cron reports.
- **Clean Structure:** 
  - Title with visual emoji (e.g. 🩺 **Ежедневный аудит и самолечение**, 📚 **Ежедневная индексация экосистемы**)
  - Timestamp (Kyiv timezone)
  - Key-value bullet points with clean agent roles and verified `@usernames`
  - Concise summary / action outcome at the bottom

## 4. High-Performance SQLite FTS5 Indexing Strategy
- Crawling entire workspace trees (including `venv`, `.git`, `cache`, `node_modules`, `data`) causes indexers to time out (>30s).
- **Optimized Batch Pattern:**
  1. Restrict index scope to high-signal directories: `/opt/hermes/skills`, `/opt/hermes/scripts`, `/opt/hermes/memories`, `/opt/hermes/profiles/*/skills`.
  2. Use SQLite parameter binding and `executemany()` for batch insertion with explicit connection timeouts (`sqlite3.connect(..., timeout=10.0)`).
  3. Index latency drops from 35s+ to ~1.2s while capturing all knowledge bases.
