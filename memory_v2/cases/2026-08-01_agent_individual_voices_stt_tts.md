# Case: Individual Voice Assignment for Agent Club & OpenAI STT/TTS Setup

**Date:** 2026-08-01
**Domain:** `agent_club`, `ai_infra`

## Symptom / Problem
The agent bots (Hermes, Alistair, Richard, Liz CPO, Callum Vance) were using default/shared voice settings (`echo`). Stefan requested distinct, persona-matched voices for each agent and verified native voice message delivery in Telegram.

## Root Cause
- Voice configurations in `config.yaml` and `.env.local` files were using a single default voice.
- Telegram voice memos require Opus encoded `.ogg` files (`audio/ogg; codecs=opus`) sent via Telegram Bot API `sendVoice` endpoint, otherwise Telegram displays them as regular audio attachments instead of voice bubbles.

## Fix / Implementation
1. **Configured STT and TTS Models**:
   - Set `STT_OPENAI_MODEL=gpt-4o-transcribe` (or `whisper-1`) in `config.yaml` and `.env.local`.
   - Set `TTS_OPENAI_MODEL=gpt-4o-mini-tts` in `config.yaml` and `.env.local`.
2. **Assigned Distinct Persona Voices**:
   - **Hermes Stevenson**: `onyx` (deep, authoritative male voice)
   - **Alistair Sterling**: `fable` (expressive, articulate British male voice)
   - **Richard Marlowe**: `echo` / `alloy` / `fable`
   - **Liz CPO**: `nova` / `alloy` (warm, professional female voice)
   - **Callum Vance / Ben**: `ash` / `coral`
3. **Telegram Voice Memo Delivery**:
   - Converted `.mp3` output from TTS API to `.ogg` (Opus) using `ffmpeg`:
     `ffmpeg -i sample.mp3 -c:a libopus -b:a 32k -vbr on sample.ogg`
   - Sent using each bot's individual Telegram bot token via `sendVoice` API endpoint:
     `https://api.telegram.org/bot<TOKEN>/sendVoice`

## Reflection / Key Lesson
- Voice bubbles on Telegram require `.ogg` (libopus codec) sent to `sendVoice`. Sending `.mp3` to `sendDocument` or `sendAudio` results in standard audio attachments.
- Each agent must use its own bot token when sending voice memos so the message appears directly from that persona.
