---
name: audio-transcribe-publish
description: Transcribe large audio and publish text to a Google Doc.
---

# audio-transcribe-publish

Class-level workflow for: "here is a big audio file, transcribe it, then write X about it, then put it in this Google Doc."

## When to use
- User drops an `.mp3/.wav/.m4a/.mp4` (often >20MB; Telegram rejects >20MB so they put it on Desktop).
- They want (1) transcript, (2) a second LLM-generated piece from the transcript, (3) one/both inserted into a Google Doc at a known marker line.
## Pipeline (Windows host, venv python: C:\Users\Stefan\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe)
1. **Locate file** — `ls C:/Users/Stefan/Desktop/` filter audio extensions. (Telegram `read_file` of a >20MB voice fails — ask user to put it on disk.)
2. **Split if needed** — both Whisper (25MB/file) and Gemini (20MB inline) need chunks.
3. **Transcribe** — prefer Gemini 2.5-flash or Whisper API.
4. **Publish to Google Doc** — append text under marker line without deleting existing contents.
1. **Locate file** — `ls C:/Users/Stefan/Desktop/` filter audio extensions. (Telegram `read_file` of a >20MB voice fails — ask user to put it on disk.)
2. **Split if needed** — both Whisper (25MB/file) and Gemini (20MB inline) need chunks. A 212MB / 93-min mp3 ≈ 1 MB/min, so ~9-min segments (~21MB) fit Whisper's 25MB; for Gemini use ~8-min (≤20MB). Use ffmpeg (present via WinGet):
   `ffmpeg -y -ss START -i SRC -t 540 -c copy part_NN.mp3` (540s = 9 min). Loop by duration from `ffprobe -v error -show_entries format=duration -of json SRC`.
3. **Transcribe — PREFER GEMINI FREE TIER (Stefan standing rule: always free)** — `gemini-2.5-flash` via REST, NO token cost to Nous/LLM. See `references/gemini_transcribe.md` for the verified recipe. Key facts:
   - Model `gemini-2.5-flash` (free, permanent tier). **`gemini-2.0-flash` is DEAD — Google returns 404**; never use it.
   - Inline audio must be `mime_type: "audio/mp3"` — **NOT `audio/mpeg`** (Gemini rejects audio/mpeg with 404). Base64 the chunk, POST `contents[].parts[] = [{text: prompt},{inline_data:{mime_type:"audio/mp3", data:b64}}]`.
   - Free limits: ~10–15 RPM, 1500 RPD, ≤20MB/request. Stefan's volume (~1 rec/week, force-major ≤10/week) fits easily.
   - **Fallback contract**: if Gemini returns HTTP 429 (free limit hit), switch to Whisper (free trial, see below) OR paid Gemini if `GEMINI_BILLING=true` in .env — and NOTIFY the user which path was used (never silently bill).
   - Whisper key `VOICE_TOOLS_OPENAI_KEY` from `C:\Users\Stefan\AppData\Local\hermes\.env`.
   - **Whisper is NOT a monthly free allowance** — OpenAI gives a ONE-TIME trial credit that expires ~3 months after account creation; after that it is pay-as-you-go ($0.006/min). Do not tell the user "free forever" for Whisper. Gemini free tier is the genuinely perpetual free path.
4. **Derive piece** — load hermes `run_agent.AIAgent` (model tencent/hy3:free via Nous), feed transcript + the user's 2nd prompt (e.g. "reflect in first person, 500 words, cite Bible verses, deliberate minor punctuation errors"). Write result to file.
5. **Publish to Google Doc** — see `references/google_doc_insert.md`. Insert under the marker line; prepend `Дата: YYYY-MM-DD` and `Файл: <name>`. Never delete existing content. Verify by re-reading.

## Hard lessons (from 2026-07-27 run)
- **Whisper limit is 25MB/file** — split BEFORE transcribing. 9-min segments of a ~1MB/min file are safe.
- **Key source**: read `VOICE_TOOLS_OPENAI_KEY` from `C:\Users\Stefan\AppData\Local\hermes\.env` (NOT os.environ).
- **ffmpeg present** at `C:/Users/Stefan/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg.../bin/ffmpeg` — use directly, no pip.
- **Long tasks**: run split+transcribe in `terminal(background=true, notify_on_complete=true)`; never sleep in the main Telegram session.
- **Verify the doc write** — re-open and confirm text present/complete before reporting done. On failure record `Обработка не завершилась: <file>, <date>` in the doc per user spec.

## References
- `references/google_doc_insert.md` — Google Docs insert/append API calls + verification.
- `references/gemini_transcribe.md` — **preferred free-tier path**: verified Gemini 2.5-flash REST recipe, audio/mp3 gotcha, dead 2.0-flash, 429 fallback contract.
- `references/whisper_split_transcribe.py` — copy-ready split+transcribe+concat script (fallback only; Whisper is one-time trial, NOT monthly-free).
- `references/make_reflection.py` — copy-ready AIAgent reflection script.

## Anti-patterns
- Do NOT invent a transcript if the file is missing/unreadable — report the blocker, ask for a disk path.
- Do NOT paste the LLM piece from chat memory — regenerate it from the saved transcript for fidelity.
- Do NOT delete doc content to "make room" — only append.
