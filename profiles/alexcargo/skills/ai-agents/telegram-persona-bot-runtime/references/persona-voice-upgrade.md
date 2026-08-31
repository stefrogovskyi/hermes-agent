# Persona bot voice upgrade (Whisper in + TTS out)

## Why this exists
A persona bot that "behaves differently from the orchestrator on voice" usually
has ONE of two root causes — both silent until you actually send a voice note:

1. **No voice-input branch.** The receive loop reads only `msg.get("text","")`.
   A voice/audio message has empty `text`, so the bot does nothing (or errors).
2. **Undefined system prompt var.** The agent is built with
   `ephemeral_system_prompt=LIZ_SYSTEM` but `LIZ_SYSTEM` was never defined →
   `NameError` at agent creation → "brain" never initialises, bot falls back to
   stub text. (This is exactly what happened to Liz Harper before the fix.)

## Minimal portable implementation (stdlib only, mirrors Richard Marlowe)
Key lives in the SAME `.env.local` as the bot token (never os.environ — see
telegram-409-gateway-autospawn.md). Voice label per agent (Liz=alloy,
Richard=onyx, Hermes=echo).

```python
OPENAI_BASE = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")

def _openai_key():
    for f in (os.path.join(BOT_DIR, ".env.local"), os.path.join(HERE, ".env.local")):
        if os.path.exists(f):
            for line in open(f, encoding="utf-8"):
                if line.strip().startswith("OPENAI_API_KEY="):
                    k = line.strip().split("=",1)[1].strip().strip('"')
                    return k if (k and not k.startswith("stub-")) else ""
    return ""

def _dl_telegram_file(token, file_id):
    info = tg_request("getFile", token, {"file_id": file_id})
    path = info.get("result",{}).get("file_path")
    if not path: return None
    with urllib.request.urlopen("https://api.telegram.org/file/bot%s/%s" % (token, path), timeout=60) as r:
        return r.read()

def transcribe(token, file_id):
    key = _openai_key()
    if not key: return None
    data = _dl_telegram_file(token, file_id)
    if not data: return None
    boundary = "----b"
    parts = [("--%s\r\n"%boundary).encode(),
             b'Content-Disposition: form-data; name="model"\r\n\r\n', b"whisper-1\r\n",
             ("--%s\r\n"%boundary).encode(),
             b'Content-Disposition: form-data; name="file"; filename="audio.ogg"\r\n',
             b"Content-Type: audio/ogg\r\n\r\n", data,
             ("\r\n--%s--\r\n"%boundary).encode()]
    req = urllib.request.Request(OPENAI_BASE+"/audio/transcriptions", data=b"".join(parts), method="POST")
    req.add_header("Authorization","Bearer %s"%key)
    req.add_header("Content-Type","multipart/form-data; boundary=%s"%boundary)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode("utf-8")).get("text","")
    except Exception as e:
        log("whisper err: %s"%e); return None

def speak(token, chat_id, text, voice="alloy"):
    key = _openai_key()
    if not key:
        tg_send_message(token, chat_id, text); return
    text = text[:4096]
    body = json.dumps({"model":"tts-1","input":text,"voice":voice,"response_format":"opus"}).encode()
    req = urllib.request.Request(OPENAI_BASE+"/audio/speech", data=body, method="POST")
    req.add_header("Authorization","Bearer %s"%key); req.add_header("Content-Type","application/json")
    try: audio = urllib.request.urlopen(req, timeout=60).read()
    except Exception as e:
        log("tts err: %s"%e); tg_send_message(token, chat_id, text); return
    boundary="----b"
    parts=[("--%s\r\n"%boundary).encode(),
           b'Content-Disposition: form-data; name="chat_id"\r\n\r\n', str(chat_id).encode(),
           ("\r\n--%s\r\n"%boundary).encode(),
           b'Content-Disposition: form-data; name="voice"; filename="reply.ogg"\r\n',
           b"Content-Type: audio/ogg\r\n\r\n", audio,
           ("\r\n--%s--\r\n"%boundary).encode()]
    req = urllib.request.Request("https://api.telegram.org/bot%s/sendVoice"%token, data=b"".join(parts), method="POST")
    req.add_header("Content-Type","multipart/form-data; boundary=%s"%boundary)
    try: urllib.request.urlopen(req, timeout=60).read()
    except Exception as e:
        log("sendVoice err: %s"%e); tg_send_message(token, chat_id, text)
```

## Receive loop wiring
```python
text = msg.get("text","")
if not text and (msg.get("voice") or msg.get("audio")):
    fid = (msg.get("voice") or msg.get("audio")).get("file_id")
    tr = transcribe(token, fid)
    if tr: text = tr
    else:
        tg_send_message(token, cid, "Не могу расшифровать голос — проверь OPENAI_API_KEY или напиши текстом.")
        continue
# ... answer ...
if msg.get("voice") or msg.get("audio"):
    speak(token, cid, ans, voice="alloy")   # echo the user's modality
else:
    tg_send_message(token, cid, ans)
```

## System-prompt rules to append (fixes "acts differently")
- VOICE RULE (HARD): "You DO reply with voice when the user sends a voice
  message (the bot speaks your reply aloud). Never say 'I am a text-only bot'."
- NO META RULE (HARD): "NEVER discuss your own configuration, triggers, or
  reply policy. Answer the substance only, like a human colleague." (Apply to
  EVERY agent — Stefan explicitly rejected Richard Marlowe narrating his own
  reply rules into the group chat.)

## Gotchas
- `OPENAI_API_KEY` must exist in the bot's `.env.local` or voice silently
  falls back to text (no crash). Verify with `getMe`/key presence before
  claiming "voice works".
- Nickname accuracy matters: Liz's real handle is `@lizharperbot` (NOT
  `lizharpbot`). A wrong MENTION_RE means group @mentions never match.
- If reusing `run_agent.AIAgent`, define `LIZ_SYSTEM`/`SYSTEM` BEFORE
  `get_agent()` is ever called — otherwise first inbound message raises
  NameError and the agent never builds.
