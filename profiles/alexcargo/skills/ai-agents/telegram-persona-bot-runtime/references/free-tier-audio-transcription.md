# Free-tier audio transcription — Gemini vs Whisper (contract + gotchas)

Stefan's standing rule (2026-07-27/28): **transcribe audio ALWAYS on the FREE
Gemini package**, never Whisper-by-default, never paid API. Volume ~1
recording/week, force-major up to 10/week.

## Gemini free tier (the real free path)
- **Permanent free tier** (not a trial): ~10–15 RPM, **1500 RPD**, inline audio
  ≤20 MB per request. No card. Stable until Google changes policy.
- Model: **`gemini-2.5-flash`** (verified live + transcribes Russian audio
  2026-07-28). `gemini-flash-latest` and `gemini-3.5-flash` also work.
- **`gemini-2.0-flash` was KILLED by Google** → returns `404 Not Found`. Do
  NOT hardcode it. If a Gemini call 404s, the model name expired — pick a
  current one from `GET https://generativelanguage.googleapis.com/v1beta/models`.
- Inline audio payload: `{"inline_data": {"mime_type": "audio/mp3", "data": <b64>}}`
  (NOT `audio/mpeg` — that 404s). Base64 the file; split files >20 MB into
  ~9-min chunks via ffmpeg (`-ss/-t -c copy`, ~17 MB@128kbps).
- Key: `GEMINI_API_KEY` from Hermes `.env`.
- Fallback on 429 (free limit hit): notify Stefan explicitly which path was
  used — Whisper OR paid Gemini (`GEMINI_BILLING=true`) — never silently bill.

## Whisper API — NOT a recurring free tier (correction)
- OpenAI Whisper API is **pay-as-you-go ($0.006/min)** after a **one-time free
  trial credit** ($5, no card, OR older $18) that **expires ~3 months after
  account creation**. There is **NO monthly free quota**.
- Do NOT tell the user "Whisper is free / hasn't charged" — that was a mistaken
  claim this session. After the trial lapses, calls bill to the card on file.
- Safe use: only as an explicit, NOTIFIED fallback when Gemini free is exhausted,
  and only if Stefan has agreed to the spend. Prefer flagging and waiting for a
  decision over silent Whisper billing.

## Working script (this host)
`C:\Users\Stefan\AppData\Local\hermes\scripts\gemini_transcribe.py`
- Splits into ≤20 MB chunks, transcribes each via `gemini-2.5-flash`, concatenates.
- On 429: switches to Whisper (if no `GEMINI_BILLING`) or paid Gemini, and prints
  `FALLBACK_USED=<method>` so Hermes can report the switch to Stefan.

## Gotcha: Google generativeai SDK deprecated
`pip install google-generativeai` installs but is END-OF-LIFE (FutureWarning,
`files.upload` removed). Use **raw REST** (`urllib`/requests) against
`generativelanguage.googleapis.com/v1beta/...` — no SDK needed.
