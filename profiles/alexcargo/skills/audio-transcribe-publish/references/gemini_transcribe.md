# Gemini free-tier transcription (verified 2026-07-27)

Best path for Stefan's audio jobs: **perpetual free tier, no Nous/LLM token cost**.
Model: `gemini-2.5-flash`. Key: `GEMINI_API_KEY` from `C:\Users\Stefan\AppData\Local\hermes\.env`.

## Inline recipe (chunk ≤20MB, audio/mp3)
```
import os, json, base64, urllib.request, urllib.error
BASE = r"C:\Users\Stefan\AppData\Local\hermes"
key = next(s.split("=",1)[1].strip().strip('"') for s in open(os.path.join(BASE,".env"),encoding="utf-8") if s.strip().startswith("GEMINI_API_KEY="))
b64 = base64.b64encode(open(chunk,"rb").read()).decode()
payload = {"contents":[{"parts":[
    {"text":"Транскрибируй это аудио на русском языке как стенографию. Только текст."},
    {"inline_data":{"mime_type":"audio/mp3","data":b64}}]}],  # NOTE audio/mp3 NOT audio/mpeg
    "generationConfig":{"temperature":0}}
url=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}"
req=urllib.request.Request(url,data=json.dumps(payload).encode(),method="POST")
req.add_header("Content-Type","application/json")
with urllib.request.urlopen(req,timeout=180) as r:
    txt=json.loads(r.read().decode())["candidates"][0]["content"]["parts"][0]["text"]
```

## Gotchas (cost real debugging time)
- **`audio/mpeg` → 404.** Gemini inline audio must be `audio/mp3`.
- **`gemini-2.0-flash` → 404 "no longer available".** Use `gemini-2.5-flash` (or `gemini-flash-latest`, `gemini-3.5-flash` also worked). Google retires old models.
- **File API `files.upload` is removed** from the deprecated `google.generativeai` package; prefer inline_data REST.
- Free limits: ~10–15 RPM, 1500 RPD. Sleep ~7s between chunks. On **429**, fall back (Whisper trial, or paid Gemini if `GEMINI_BILLING=true`) and **notify the user** which path ran.

## Why not MCP / AI Studio web UI
AI Studio (aistudio.google.com) is a web UI, not an MCP server — cannot be "connected via MCP".
Gemini API IS the AI Studio engine; call it directly via REST (above). Browser path only if CDP:9223 Chrome is alive + logged into Google.
