---
name: video-shorts-maker
description: "Use when creating Reels/Shorts with burned-in subtitles."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [video, reels, shorts, tiktok, subtitles, whisper, ffmpeg]
---

# Video Shorts, Reels & Subtitles Maker Skill

Use this skill when converting videos into engaging 9:16 vertical Shorts/Reels with burned-in dynamic subtitles (Hormozi / MrBeast style).

## 🛠 Features
1. **Audio Extraction & Word-Level Timing:** Extracts speech timestamps using `faster-whisper`.
2. **Dynamic ASS Subtitle Styling:** High-contrast yellow/white text with dark stroke and shadow.
3. **9:16 Vertical Formatting:** Auto-scales to 1080x1920 with high visual fidelity.
4. **Hardcoded Burn-in:** Fast `ffmpeg` encoding directly into Telegram-ready MP4.

## 🚀 Execution Script
```bash
python3 /opt/hermes/scripts/make_shorts_with_subtitles.py --input /path/to/video.mp4 --output /path/to/output_shorts.mp4
```
