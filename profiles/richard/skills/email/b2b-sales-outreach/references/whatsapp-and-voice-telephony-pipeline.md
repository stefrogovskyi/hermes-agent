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
- **Interactive TwiML Flow**:
  ```xml
  <Response>
      <Gather input="speech" timeout="3" speechTimeout="auto" action="/handle-response">
          <Say voice="Polly.Brian-Neural" language="en-GB">
              Hello. This is Richard Marlowe, Senior Sales Manager calling from Navo24 in London...
          </Say>
      </Gather>
  </Response>
  ```
- **Compliance Requirement**: Outbound PSTN calling requires an active/approved Customer Profile in Twilio Trust Hub.

---

## 5. Weekly Sales Testimonials Email Loop

- **Schedule**: Every Monday at 08:00 AM Kyiv (`0 5 * * 1` UTC).
- **Recipients**: `To: sales@navo24.com`, `CC: stefan@navo24.com, lxxmng@navo24.com`.
- **Content Rotation**: Dynamically rotates quotes (Buffett, Bezos, Gates, Godin, Ziglar) and 3 random focus questions across all 5 products, customer support speed, D&D demurrage savings, and developer MCP tools.
