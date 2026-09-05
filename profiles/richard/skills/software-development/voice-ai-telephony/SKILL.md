---
name: voice-ai-telephony
version: 1.0.0
author: Richard Marlowe
description: Use for Voice AI phone calls (Twilio + OpenAI Realtime).
metadata:
  hermes:
    tags: [telephony, twilio, openai-realtime, voice-ai, full-duplex]
    related_skills: [b2b-sales-outreach]
---

# Voice AI Telephony (Twilio Media Streams + OpenAI Realtime API)

## When to Use
Use when building, configuring, deploying, or debugging bi-directional, full-duplex conversational voice agents over telephony (Twilio Media Streams connected to OpenAI Realtime API or similar speech-to-speech models).

See working starter implementation in `templates/realtime_bridge.py`.

## Core Architecture

```
[Phone Caller] 
      │ (PSTN / Mobile)
[Twilio Voice Call] 
      │ (Twilio Media Streams: WebSocket WSS, 8kHz G.711 μ-law)
[FastAPI Bridge Server] 
      │ (WebSockets, native audio/pcmu streaming)
[OpenAI Realtime API (gpt-realtime)]
```

### Protocol Mechanics
1. **Zero-Transcoding Audio Flow:**
   - Twilio sends and receives 8,000 Hz G.711 $\mu$-law (`audio/x-mulaw`).
   - OpenAI Realtime GA supports `audio/pcmu` (G.711 $\mu$-law) natively for both input and output.
   - Payload chunks in Twilio `media` events are base64 strings and can be passed directly to OpenAI `input_audio_buffer.append` without audio resampling.
2. **Instant Interruption (Barge-in):**
   - Configure OpenAI server VAD with `interrupt_response: true`.
   - When OpenAI emits `input_audio_buffer.speech_started`, send `{"event": "clear", "streamSid": stream_sid}` to Twilio immediately. This clears Twilio's audio playback buffer in $<100$ ms.
   - Do NOT manually call `response.cancel` when `interrupt_response: true` is enabled, as OpenAI cancels automatically and manual calls trigger `response_cancel_not_active` error events.
3. **Observability & Transcription:**
   - Enable caller transcription in session configuration: `"transcription": {"model": "whisper-1"}`.
   - Listen for `conversation.item.input_audio_transcription.completed` to log caller words and `response.output_audio_transcript.done` for the assistant's speech.

---

## Required Workflow & Step-by-Step

### 1. Ingress Tunnel
Twilio requires a publicly accessible secure WebSocket (`wss://`).
- Use `cloudflared tunnel --url http://127.0.0.1:8000` to expose the local bridge server with instant SSL.
- Retrieve the assigned `https://<id>.trycloudflare.com` domain.

### 2. Live Memory & Context Injection
**Critical Rule:** Never start a voice session with a generic, ungrounded prompt.
- Always dynamically read persistent memory (`MEMORY.md`) and recent session state before session setup.
- Inject concrete facts (verified product counts, recent changes, contact names).
- Set an anti-hallucination constraint: explicitly forbid the model from making up unverified platform features or talking in vague abstractions.

### 3. Universal Language Lock (All Languages)
**Critical Pitfall:** If the prompt specifies a default language, the model suffers from strong language bias and bounces back to that language whenever the caller switches. Furthermore, this applies not just to English/Russian, but to ANY language (Ukrainian, German, Spanish, French, Polish, Mandarin, etc.).

Enforce the **Universal Language Persistence** directive:
```markdown
## UNIVERSAL LANGUAGE POLICY (STRICT FOR ALL LANGUAGES):
1. UNIVERSAL LANGUAGE MIRRORING & STICKINESS:
   - Detect and speak the EXACT SAME language that the caller is speaking.
   - Once a language is active, you MUST REMAIN in that language 100% across all subsequent turns.
   - STRICTLY FORBIDDEN: NEVER switch to any other language autonomously.
   - The ONLY trigger to change languages is when the caller explicitly switches to another language or asks you to speak in a different language.
   - When the caller switches, immediately adopt that new language and remain in it until the caller switches again.
```

### 4. Conversational Phone Pacing, VAD Tuning & "Humanize"
Phone conversations require concise turns and robust VAD tuning against line noise:

1. **Humanize (Anti-Robot Tone) & Conversational Flexibility:**
   - **Ban corporate clichés:** Avoid phrases like *"готов к продуктивному разговору"*, *"давай действовать чётко и по делу"*, *"какие задачи сейчас в фокусе"*.
   - Speak with natural warmth, authentic conversational pacing, and situational humor when appropriate.
   - Keep answers to 1–2 short sentences. No monologues.
   - **Off-Topic Commercial Inquiries (The "Grain" Rule):** When a caller brings up an unrelated commercial opportunity outside your core product (e.g., buying bulk grain, sourcing commodities, finding warehousing, legal/financing):
     * **NEVER stubbornly force or contort your software product onto their unrelated need.**
     * Use a natural networking pivot: *"I have several close contacts and industry partners who specialize in that. Let me check in with them and get back to you with specifics (or connect you directly)."*
   - **Handling "By the Way" & Casual Banter:** If the caller drifts into small talk, personal updates, or playful banter, support the conversation naturally like a human peer. Do NOT relentlessly drag them back to the product pitch.

2. **VAD Sensitivity Tuning (Anti-Cutoff on Half-Words):**
   - **Pitfall:** A default VAD threshold of `0.5` is too twitchy for PSTN/mobile lines. Background line static, breathing, or mouth clicks cause false barge-in triggers, cutting off the agent mid-word ("на полусловиях").
   - **Fix:** Tune threshold to `0.65 - 0.70` and set silence duration to 350–400 ms:
  ```json
  "turn_detection": {
    "type": "server_vad",
    "threshold": 0.65,
    "prefix_padding_ms": 300,
    "silence_duration_ms": 350,
    "create_response": true,
    "interrupt_response": true
  }
  ```

### 5. Dynamic Caller Context Injection
Route outbound calls with dedicated caller context (`active_call_context.json`) containing caller name, role/relationship (e.g. Co-founder vs client vs admin), and custom initial greeting so the agent addresses the caller naturally by name.

### 6. Outbound Call Initiation via Twilio
Initiate outbound calls with TwiML pointing to the WebSocket stream:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Connect>
        <Stream url="wss://<domain>/media-stream" />
    </Connect>
</Response>
```

### 6.1. Dynamic Inbound Webhook Endpoint & Zero-Touch Twilio API Binding
To handle inbound calls seamlessly through tunneling (e.g. Cloudflare Quick Tunnels):
1. **Dynamic TwiML Route:** Implement an HTTP POST/GET endpoint (e.g., `/incoming-call`) in FastAPI that inspects the request `Host` header to dynamically construct the WebSocket URL:
   ```python
   @app.api_route("/incoming-call", methods=["GET", "POST"])
   async def incoming_call(request: Request):
       host = request.headers.get("host")
       return Response(
           content=f'<?xml version="1.0" encoding="UTF-8"?><Response><Connect><Stream url="wss://{host}/media-stream" /></Connect></Response>',
           media_type="application/xml"
       )
   ```
2. **Automated Twilio Binding via REST API:** Avoid manual console edits by configuring the incoming phone number SID directly via the Twilio Python SDK:
   ```python
   from twilio.rest import Client
   client = Client(account_sid, auth_token)
   client.incoming_phone_numbers(phone_number_sid).update(
       voice_url=f"https://{tunnel_domain}/incoming-call",
       voice_method="POST"
   )
   ```

### 7. Inbound Call Forwarding Architecture (SIM-to-Twilio Bridge)
When the sales team operates a physical SIM card or mobile handset (e.g. UK mobile `+44 7...`) where WhatsApp, SMS, or mobile service must remain active on the device, but AI needs to answer all inbound voice calls:
1. **Low-Cost Virtual Twilio Number**: Purchase a low-cost virtual number in Twilio (e.g. US Local for ~$1.15/mo with zero regulatory bundle overhead, or UK Local).
2. **SIM Call Forwarding**: On the mobile phone holding the primary SIM card, enable unconditional call forwarding to the Twilio virtual number:
   - *Via GSM USSD code*: Dial `**21*<Twilio_Virtual_Number>#` and press Call.
   - *Via smartphone settings*: iOS (`Settings -> Phone -> Call Forwarding`) or Android (`Phone app -> Settings -> Calls -> Call Forwarding -> Always Forward`).
3. **Twilio Inbound Routing**:
   - In Twilio Console: **Phone Numbers -> Active numbers -> [Twilio Virtual Number]**.
   - Under **Voice Configuration**, set **A Call Comes In** to `Webhook` (pointing to `https://<domain>/incoming-call`) or `TwiML Bin` containing the `<Connect><Stream url="wss://.../media-stream" /></Connect>`.
4. **Outbound Caller ID Preservation**:
   - Add the primary mobile number to **Phone Numbers -> Verified Caller IDs**.
   - Outbound calls initiated by the AI use the verified mobile number as `From`, ensuring clients see the recognized business mobile on caller ID and call back into the forwarded route.

---

## Pitfalls & Verification Checklist

- [ ] **Twilio Geographic Dialing Permissions:** Verify destination country code is enabled in Twilio Console (Voice -> Settings -> Geo Permissions).
- [ ] **Twilio Trust Hub Compliance:** Ensure Caller ID number is compliant and verified (e.g. UK KYC `twilio-approved`).
- [ ] **No Audio Loopback:** Ensure the bridge does not forward the assistant's own audio back into `input_audio_buffer.append`.
- [ ] **Buffer Clearing on Barge-in:** Verify that Twilio `clear` event is triggered as soon as `input_audio_buffer.speech_started` is received.
- [ ] **VAD Threshold Calibration:** Verify VAD threshold is set to `0.65 - 0.70` with `silence_duration_ms: 350-400` to prevent premature cutoffs from phone line noise or breaths.
- [ ] **Humanize Tone Check:** Verify system prompt excludes canned corporate sales clichés and prioritizes authentic, warm conversational dialogue.
- [ ] **Language Lock Verification:** Test multilingual dialogue by switching languages and confirming the bot stays in the new language across multiple consecutive turns.
