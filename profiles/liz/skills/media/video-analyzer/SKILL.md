---
name: video-analyzer
description: "Use when analyzing video files or Telegram video notes."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [video, audio, vision, telegram, whisper, ffmpeg]
---

# Video & Video-Note Multimodal Analyzer Skill

Use this skill when processing, transcribing, and visually analyzing user video uploads (.mp4, .mov, .mkv, .webm) and Telegram video notes (кружочки).

## 🛠 Prerequisites
- `ffmpeg` + `ffprobe` in system PATH.
- `faster_whisper` (or OpenAI Whisper STT) installed in the environment.

## 🚀 Execution Pipeline

### 1. Extract Audio & Transcribe (Whisper)
```bash
# Extract audio track to MP3
ffmpeg -i /path/to/video.mp4 -vn -acodec libmp3lame /tmp/audio.mp3 -y

# Transcribe with faster-whisper / Whisper
python3 -c "
from faster_whisper import WhisperModel
model = WhisperModel('small', device='cpu', compute_type='int8')
segments, info = model.transcribe('/tmp/audio.mp3', beam_size=5)
for s in segments:
    print(f'[{s.start:.1f}s -> {s.end:.1f}s] {s.text}')
"
```

### 2. Extract Keyframes for Visual Analysis
```bash
mkdir -p /tmp/video_frames
# Extract 0.5 - 1 frame per second
ffmpeg -i /path/to/video.mp4 -vf "fps=0.5" /tmp/video_frames/frame_%02d.jpg -y
```

### 3. Multimodal Vision Inspection
Pass the extracted frames (`/tmp/video_frames/frame_01.jpg`, etc.) into `vision_analyze` tool to describe actions, objects, facial expressions, and scenes.
