# Telegram Video Notes (Кружочки) & Multi-Daemon Bytecode Synchronization

## 1. Telegram Ingress for Video Notes (`video_note`)
In python-telegram-bot / Telegram Bot API:
- Standard video files arrive as `msg.video` with `filters.VIDEO`.
- Round video messages (video notes / кружочки) arrive as `msg.video_note` with `filters.VIDEO_NOTE`.
- **Pitfall:** If the message handler filter only specifies `filters.VIDEO`, Telegram drops all video notes before passing them to the agent event loop.
- **Fix in adapter.py:** Ensure `filters.VIDEO_NOTE` is present in the message filter chain, and check `msg.video or getattr(msg, "video_note", None)` when extracting media payloads.

## 2. Multi-Daemon Bytecode Cache Invalidation (`.pyc`)
- **Problem:** When editing shared platform plugins or core framework code in `/opt/hermes/hermes-agent/`, restarting only `hermes-default.service` leaves sub-agent daemons (`hermes-alistair`, `hermes-richard`, etc.) running stale Python bytecode in memory.
- **Fix Procedure:**
  ```bash
  # 1. Clear bytecode cache
  find /opt/hermes/hermes-agent -name "*.pyc" -delete
  # 2. Restart ALL cluster agent daemons simultaneously
  systemctl restart hermes-alistair hermes-archie hermes-ben hermes-callum hermes-default hermes-harrison hermes-liz hermes-richard
  ```

## 3. Video Analysis Pipeline
1. Extract audio track via `ffmpeg -i input.mp4 -vn -acodec libmp3lame /tmp/audio.mp3 -y`
2. Transcribe voice using `faster-whisper` (or Whisper STT).
3. Sample keyframes (`fps=0.5` or scene-detection) via `ffmpeg -i input.mp4 -vf "fps=0.5" /tmp/video_frames/frame_%02d.jpg -y`
4. Inspect visual frames using `vision_analyze`.
