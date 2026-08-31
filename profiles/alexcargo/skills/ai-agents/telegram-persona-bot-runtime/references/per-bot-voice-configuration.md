# Per-Bot Individual Voice Configuration & Native Telegram Voice Memos (`sendVoice`)

Each Telegram persona bot should have its own distinct voice character to reflect its role, gender, and personality:

| Agent Bot | Role | OpenAI STT Model | OpenAI TTS Model | Voice | Character Tone |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Hermes Stevenson** | Chief Orchestrator | `gpt-4o-transcribe` | `gpt-4o-mini-tts` | `onyx` | Deep, calm, authoritative male voice |
| **Alistair Sterling** | Project Manager (Navo) | `gpt-4o-transcribe` | `gpt-4o-mini-tts` | `fable` | Structured, composed British male voice |
| **Richard Marlowe** | Senior Sales (Navo) | `gpt-4o-transcribe` | `gpt-4o-mini-tts` | `echo` | Warm, confident, persuasive male voice |
| **Callum Vance** | Full-Stack Engineer | `gpt-4o-transcribe` | `gpt-4o-mini-tts` | `ash` | Natural, clear, modern male engineer voice |
| **Elizabeth 'Liz' Harper** | CPO (Enlight Group) | `gpt-4o-transcribe` | `gpt-4o-mini-tts` | `nova` | Warm, articulate, inspiring female voice |

## Environment Variables in `.env.local`:
```env
STT_PROVIDER=openai
TTS_PROVIDER=openai
STT_OPENAI_MODEL=gpt-4o-transcribe
TTS_OPENAI_MODEL=gpt-4o-mini-tts
TTS_OPENAI_VOICE=fable   # (fable for Alistair, echo for Richard, ash for Callum, nova for Liz)
```

## Sending Native Telegram Voice Bubbles (`sendVoice`):
To send audio as a native Telegram voice bubble (`.ogg` Opus format), use `multipart/form-data` with `sendVoice` directly from the **agent's OWN bot token** so the message appears from that specific agent in Telegram:

```python
import uuid, json, urllib.request, os

def tg_send_voice(token, chat_id, ogg_path, caption=None):
    boundary = uuid.uuid4().hex
    headers = {'Content-Type': f'multipart/form-data; boundary={boundary}', 'User-Agent': 'Mozilla/5.0/HermesAgent'}
    filename = os.path.basename(ogg_path)
    file_bytes = open(ogg_path, 'rb').read()
    
    body = []
    body.append(f'--{boundary}\r\nContent-Disposition: form-data; name="chat_id"\r\n\r\n{chat_id}\r\n'.encode('utf-8'))
    if caption:
        body.append(f'--{boundary}\r\nContent-Disposition: form-data; name="caption"\r\n\r\n{caption}\r\n'.encode('utf-8'))
    body.append(f'--{boundary}\r\nContent-Disposition: form-data; name="voice"; filename="{filename}"\r\nContent-Type: audio/ogg\r\n\r\n'.encode('utf-8'))
    body.append(file_bytes)
    body.append(f'\r\n--{boundary}--\r\n'.encode('utf-8'))
    
    payload = b''.join(body)
    url = f'https://api.telegram.org/bot{token}/sendVoice'
    req = urllib.request.Request(url, data=payload, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode('utf-8'))
```
