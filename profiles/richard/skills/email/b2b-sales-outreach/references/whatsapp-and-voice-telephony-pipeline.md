# WhatsApp Gateway & Twilio Voice Telephony Architecture (+44 7360 065904)

Comprehensive guide for operating Richard Marlowe's British phone number `+44 7360 065904` across WhatsApp Multi-Device Gateway and Twilio Outbound/Inbound Voice.

---

## 1. Verbatim Draft Approval Rule (Anti-Drift Mandate)

- **Strict Approval Discipline**: When Stefan approves an inbound lead notification card (`«Да»`, `«Отправляй»`, `«OK»`), the agent MUST send **strictly and verbatim the exact draft text** presented in the notification card, word for word.
- **No Unsolicited Language Switching or Rewriting**: NEVER unilaterally translate or rewrite an English draft into Russian (or vice versa) upon receiving an approval confirmation. If a different text is required, Stefan explicitly specifies the new text (e.g. `«Отправь: [...]»`).

---

## 2. WhatsApp Multi-Device Gateway Setup (Baileys)

- **Dedicated Service**: Runs as a lightweight Node.js daemon (`/opt/hermes/profiles/richard/services/whatsapp-gateway/index.js`) on port `3060`.
- **Browser Identity**: `["Ubuntu", "Chrome", "124.0.0.0"]` to prevent pairing rejection.
- **Session Auth**: Managed in `auth_info_richard/`. If status is logged out (401), stale credential files are cleanly wiped to allow instant re-pairing.
- **Silent Watchdog Delivery Semantics**:
  * In cron watcher scripts with `no_agent=True` and `deliver='origin'` (e.g. `whatsapp_inbound_triage.py`), the script MUST emit output ONLY when new actionable events exist.
  * **Non-empty stdout = deliver message to chat**; **empty stdout (silent exit 0) = no delivery**.
  * NEVER print *"No new events"* or log lines to stdout during silent ticks, as the scheduler delivers any non-empty stdout directly to Telegram.
- **Inbound Message Triage**:
  * Inbound messages are captured via `messages.upsert` and appended to `inbound_events.jsonl`.
  * Cron/watchdog script (`whatsapp_inbound_triage.py`) polls every minute and dispatches Telegram notification cards with client context and Richard's prepared B2B draft.
- **Outbound Endpoints**:
  * `POST http://localhost:3060/send-message`: Sends clean text messages (`{"phone": "...", "message": "..."}`).
  * `POST http://localhost:3060/send-voice`: Sends native WhatsApp PTT voice notes (`mimetype: 'audio/ogg; codecs=opus'`, `ptt: true`).

---

## 3. Native PTT Voice Note Generation

- **Format**: OGG container with Opus audio encoding at 24kHz/32kbps mono:
  ```bash
  ffmpeg -y -i input.mp3 -c:a libopus -b:a 32k -vbr on -application voip output.ogg
  ```
- **Voice Configurations**:
  * British English: `edge-tts --voice en-GB-RyanNeural`
  * Russian: `edge-tts --voice ru-RU-DmitryNeural`

---

## 4. Twilio Voice Telephony & UK Verified Caller ID

- **Caller ID**: `+44 7360 065904` (SID: `PN637a106ac9f7c9b55afe339b111a430e`).
- **Voice Engine**: Polly Neural British Voice (`Polly.Brian-Neural` / `Polly.Arthur-Neural`).
- **Compliance & Trust Hub**: Outbound PSTN calling requires an active/approved Customer Profile in Twilio Trust Hub (`BU37e8e804822f5918634848e30241c4ab` approved).
- **International Dialing Permissions (Geo-Permissions)**:
  * Twilio blocks international calls to many country codes (including Ukraine `UA` / `+380`) by default.
  * To enable dialing, update via Twilio Voice API:
    ```python
    client.voice.v1.dialing_permissions.bulk_country_updates.create(
        update_request=json.dumps([{
            "iso_code": "UA",
            "low_risk_numbers_enabled": True,
            "high_risk_special_numbers_enabled": False,
            "high_risk_tollfraud_numbers_enabled": False
        }])
    )
    ```

---

## 5. Full-Duplex Conversational Voice AI Architecture (Twilio Media Streams + OpenAI Realtime)

For live, natural phone conversations with instant interruptions (<100ms barge-in), zero robotic monologues, and human pacing:

### A. End-to-End Audio Pipeline
```
[User Phone] 
     ▲
     │ (8kHz G.711 mu-law / PCMU over PSTN)
     ▼
[Twilio Media Streams]
     ▲
     │ WebSocket (base64 audio chunks)
     ▼
[Cloudflare Tunnel / WSS Gateway] (cloudflared tunnel --url http://127.0.0.1:8000)
     ▲
     │ FastAPI WebSocket (/media-stream)
     ▼
[realtime_voice_bridge.py]
     ▲
     │ Native WebSocket (wss://api.openai.com/v1/realtime?model=gpt-realtime)
     ▼
[OpenAI Realtime GA Engine (gpt-realtime)]
```

### B. Critical Protocol Specifications (OpenAI Realtime GA)
1. **Model & Endpoint**:
   - Model name: `gpt-realtime` or `gpt-realtime-mini`.
   - URL: `wss://api.openai.com/v1/realtime?model=gpt-realtime`.
   - **DO NOT SEND `OpenAI-Beta: realtime=v1`**: The GA endpoint rejects this beta header with `beta_api_shape_disabled`. Use standard `Authorization: Bearer <KEY>`.
2. **Native PCMU Format (Zero Transcoding)**:
   - Twilio sends 8kHz G.711 mu-law audio chunks in `event: media`, payload `base64`.
   - Configure OpenAI Realtime to use `audio/pcmu` for both input and output:
     ```json
     {
       "type": "session.update",
       "session": {
         "type": "realtime",
         "instructions": "<Persona prompt>",
         "audio": {
           "input": {
             "format": {"type": "audio/pcmu"},
             "turn_detection": {
               "type": "server_vad",
               "threshold": 0.5,
               "prefix_padding_ms": 300,
               "silence_duration_ms": 250,
               "create_response": true,
               "interrupt_response": true
             }
           },
           "output": {
             "format": {"type": "audio/pcmu"},
             "voice": "ash"
           }
         }
       }
     }
     ```
   - Input audio append: `{"type": "input_audio_buffer.append", "audio": payload}`.
   - Output audio delta: OpenAI sends `response.output_audio.delta` (not `response.audio.delta`). Stream directly to Twilio:
     ```json
     {
       "event": "media",
       "streamSid": stream_sid,
       "media": {"payload": data["delta"]}
     }
     ```

### C. Barge-in & Interruption Handling (<100ms Latency)
When the user speaks while the AI is talking:
1. OpenAI emits event: `input_audio_buffer.speech_started`.
2. The bridge immediately sends a `clear` command to Twilio:
   ```json
   {"event": "clear", "streamSid": stream_sid}
   ```
   This flushes Twilio's audio playback queue instantly so the caller hears silence on their phone within 50–100ms.
3. Send `{"type": "response.cancel"}` to OpenAI to stop token and audio generation.

### D. Conversational Prompt Rules for Phone Calls
- **Brevity Mandate**: 1–2 short sentences per turn. Never speak in long paragraphs or monologue.
- **Natural conversational pacing**: Listen first, acknowledge briefly, ask a targeted question.
- **Bilingual flexibility**: Default to Russian with Stefan, switch seamlessly to English if the user switches.

---

## 6. Weekly Sales Testimonials Email Loop

- **Schedule**: Every Monday at 08:00 AM Kyiv (`0 5 * * 1` UTC).
- **Recipients**: `To: sales@navo24.com`, `CC: stefan@navo24.com, lxxmng@navo24.com`.
- **Content Rotation**: Dynamically rotates quotes (Buffett, Bezos, Gates, Godin, Ziglar) and 3 random focus questions across all 5 products, customer support speed, D&D demurrage savings, and developer MCP tools.
