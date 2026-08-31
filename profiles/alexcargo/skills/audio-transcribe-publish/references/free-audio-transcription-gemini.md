# Free audio transcription: Gemini free tier vs Whisper trial

## Decision for Stefan (2026-07-27): ALWAYS transcribe on the FREE Gemini package.
Use case: ~1 recording/week, force-major up to ~10/week (easily fits free tier).

## Working recipe (verified)
- Model: `gemini-2.5-flash` (FREE tier, permanent — NOT a trial).
- Endpoint: `POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$GEMINI_API_KEY`
- Body: `{"contents":[{"parts":[{"text":"Транскрибируй это аудио на русском языке как стенографию. Только текст."},{"inline_data":{"mime_type":"audio/mp3","data":<base64>}}]}],"generationConfig":{"temperature":0}}`
- Inline audio limit: ~20 MB per request. Split longer files with ffmpeg
  (`-ss`/`-t` 9-min segments ~17 MB at 128 kbps) BEFORE base64.
- `GEMINI_API_KEY` lives in `hermes/.env` (len ~53).

## CRITICAL: which models are DEAD vs ALIVE (Google rotates aggressively)
- `gemini-2.0-flash` -> **404 "no longer available"** (Google killed it). Do NOT use.
- ALIVE free (verified 2026-07-27): `gemini-2.5-flash`, `gemini-flash-latest`,
  `gemini-3.5-flash`. `gemini-2.5-flash` is the stable pick.
- If Google later 404s 2.5-flash, fall back to `gemini-flash-latest` (alias)
  or `gemini-3.5-flash`.

## Gemini free tier limits (relevant to volume)
- ~10-15 RPM, 1500 RPD, inline audio <=20 MB.
- 10 recordings/week (~11 chunks each = 110 req/week) = ~7% of daily limit.
- Upside vs Whisper: permanent free, no card, no expiry.

## Whisper via OpenAI API is NOT "free monthly"
- OpenAI gives a ONE-TIME free trial credit ($5, OR $18 legacy) that EXPIRES
  ~3 months after account creation. After that Whisper is PAY-AS-YOU-GO
  ($0.006/min). There is NO recurring free monthly quota.
- The earlier `Standard recording 1.mp3` (93 min) transcription used Whisper
  and may already have drawn from trial credit or billed — not a guaranteed free path.
- Therefore: do NOT rely on Whisper as the "free" option. Use it only as an
  explicit fallback if Gemini free is exhausted AND the user accepts billing,
  OR swap to paid Gemini (`GEMINI_BILLING=true`).

## MCP note
- Google AI Studio is a WEB UI, not an MCP server — cannot "connect via MCP".
- The Gemini API above IS the same engine; call it directly (REST), not via UI.
- Browser path (AI Studio chat) only works if Chrome CDP :9223 is live + logged in.
