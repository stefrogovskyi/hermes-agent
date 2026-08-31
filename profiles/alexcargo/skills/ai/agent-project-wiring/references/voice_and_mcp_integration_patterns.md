# Voice, MCP, and Document Attachment Integration Patterns

This reference captures verified production patterns for Telegram persona bots (Alistair, Richard, Callum, Liz) and Hermes core tools.

---

## 1. OpenAI STT & TTS Upgrades for Natural Voice

To achieve fast, natural, human-sounding voice interaction without synthetic robot artifacts:

### Model Selection
* **Speech-to-Text (STT):** `gpt-4o-transcribe` (high accuracy, fast transcription, low noise sensitivity).
* **Text-to-Speech (TTS):** `gpt-4o-mini-tts` (generates natural human-like pacing and intonation in ~2.2s).

### Individual Agent Voice Assignments
Do NOT use a single default voice (like `echo`) for all agents. Assign distinct personas:
* **Hermes Stevenson (Chief Orchestrator):** `onyx` (deep, calm, authoritative male voice)
* **Alistair Sterling (PM):** `fable` (precise, structured British male voice)
* **Richard Marlowe (Sales):** `echo` (warm, confident, persuasive commercial male voice)
* **Callum Vance (Full-Stack Engineer):** `ash` (modern, clear, soft young male voice)
* **Elizabeth "Liz" Harper (CPO):** `nova` (warm, articulate, inspiring female voice)

---

## 2. Telegram Native Voice Bubble Delivery (`sendVoice`)

Sending an `.mp3` file via `sendDocument` attaches a file card instead of a native Telegram voice bubble.

### Requirements for Native Voice Memos
1. **Convert audio to Ogg Opus format:**
   ```bash
   ffmpeg -y -i input.mp3 -c:a libopus -b:a 32k output.ogg
   ```
2. **Send via `sendVoice` endpoint:**
   ```http
   POST https://api.telegram.org/bot<TOKEN>/sendVoice
   Content-Type: multipart/form-data; boundary=<BOUNDARY>
   ```
3. **Multipart Payload:**
   - Field `chat_id`: Target Telegram chat/group ID.
   - Field `voice`: Binary `.ogg` file bytes with `Content-Type: audio/ogg`.
   - Field `caption` (optional): Caption text with `parse_mode: HTML` or Markdown.

---

## 3. Navo24 Remote MCP Protocol (`Accept` Header Trap)

Navo24 MCP services (`mcp.schedulesmcp.com`, `mcp.trackingmcp.com`, `mcp.loadingmcp.com`) use Streamable Remote HTTP MCP transport.

### CRITICAL HEADER REQUIREMENT
```http
POST https://mcp.schedulesmcp.com/mcp
Content-Type: application/json
Accept: application/json, text/event-stream
Authorization: Bearer <NAVO_API_KEY>
x-api-key: <NAVO_API_KEY>
```
⚠️ **TRAP:** Omitting `Accept: application/json, text/event-stream` causes the server to return `HTTP 406 Not Acceptable`.

### JSON-RPC 2.0 Payload
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "compare_lanes",
    "arguments": { "origin": "CNSHA", "destination": "NLRTM" }
  },
  "id": 1
}
```
Responses arrive wrapped as Server-Sent Events (`data: {"result": {"content": [{"type": "text", "text": "..."}]}}`). Parse the `data: ` line as JSON.

---

## 4. SeaRates API v3.0 Direct Endpoints

* **Container Tracking:** `GET https://tracking.searates.com/tracking?api_key={KEY}&number={CONTAINER_OR_BL}`
* **Vessel Tracking:** `GET https://vessel-tracking.searates.com/vessel-tracking?api_key={KEY}&imo={IMO}`
* **Distance & Time:** `GET https://distance.searates.com/distance?api_key={KEY}&from={POL}&to={POD}`
* **World Sea Ports:** `GET https://ports.searates.com/ports?api_key={KEY}&search={QUERY}`

---

## 5. Consolidated Benchmark Reports & Attachments

When delivering audit/benchmark reports to Telegram groups:
1. **Never split reports into multiple text messages** (e.g. 5 containers per message).
2. **Send ONE single summary message** containing total count, operational findings, and actionable recommendations for engineering.
3. **Attach BOTH the HTML report AND 5-sheet Excel workbook (`ocean_tracking_comparison_*.xlsx`)** directly as document attachments via `sendDocument`.
