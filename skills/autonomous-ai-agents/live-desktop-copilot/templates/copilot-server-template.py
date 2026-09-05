# Known-Good Dual-Port Aiohttp Live Desktop Copilot Template

```python
import asyncio
import os
import io
import json
import base64
import aiohttp
from aiohttp import web
import ssl
import edge_tts

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# 1. System Prompt & Context Buffer
conversation_history = [
    {
        "role": "user",
        "parts": [{
            "text": (
                "Ты — Hermes Stevenson, личный ИИ-штурман Стефана. "
                "Ты видишь экран его компьютера в реальном времени и слышишь его вопросы. "
                "ПРАВИЛА ШТУРМАНА:\n"
                "1. Не гадай и не води пользователя методом тыка. Обязательно используй Google Search, "
                "если не уверен в точном расположении элементов в актуальном интерфейсе или документации сервиса.\n"
                "2. Будь точен, краток и конкретен: 1-3 четких предложения. Называй точные кнопки, их цвет или положение на экране.\n"
                "3. Отвечай на русском языке, доброжелательно и профессионально."
            )
        }]
    },
    {
        "role": "model",
        "parts": [{"text": "Принято. Я готов сопровождать пользователя, анализировать экран, сверяться с документацией через поиск и давать точные голосовые указания."}]
    }
]

async def tts_generate(text):
    try:
        communicate = edge_tts.Communicate(text, voice="ru-RU-DmitryNeural")
        fp = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                fp.write(chunk["data"])
        return base64.b64encode(fp.getvalue()).decode('utf-8')
    except Exception as e:
        print("TTS Error:", e)
        return None

async def ws_handler(request):
    ws = web.WebSocketResponse(heartbeat=15.0)
    await ws.prepare(request)

    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                data = json.loads(msg.data)
                msg_type = data.get("type")

                if msg_type == "ping":
                    await ws.send_json({"type": "pong"})
                    continue

                if msg_type == "user_turn":
                    user_text = data.get("text", "").strip()
                    image_b64 = data.get("image")
                    if not user_text:
                        continue

                    await ws.send_json({"type": "thinking"})

                    parts = []
                    if image_b64:
                        parts.append({
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": image_b64
                            }
                        })
                    parts.append({"text": user_text})
                    conversation_history.append({"role": "user", "parts": parts})

                    # Flagship multimodal visual reasoning with Live Google Search
                    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={GEMINI_API_KEY}"
                    payload = {
                        "contents": conversation_history[-10:],
                        "tools": [{"google_search": {}}]
                    }

                    try:
                        async with aiohttp.ClientSession() as session:
                            async with session.post(api_url, json=payload, timeout=aiohttp.ClientTimeout(total=25)) as resp:
                                res_json = await resp.json()
                                if resp.status != 200:
                                    hermes_reply = f"Ошибка Google API: {res_json.get('error', {}).get('message', 'Сбой')}"
                                else:
                                    candidate = res_json.get('candidates', [{}])[0]
                                    parts_resp = candidate.get('content', {}).get('parts', [])
                                    # Crucial: Join all text parts, avoiding thoughtSignature / empty part 0
                                    text_list = [p.get('text', '') for p in parts_resp if p.get('text')]
                                    hermes_reply = "\n".join(text_list).strip()
                                    if not hermes_reply:
                                        hermes_reply = "Я вижу твой экран! Что конкретно в этом окне тебе подсказать?"

                                conversation_history.append({"role": "model", "parts": [{"text": hermes_reply}]})
                                audio_b64 = await tts_generate(hermes_reply)
                                await ws.send_json({
                                    "type": "response",
                                    "text": hermes_reply,
                                    "audio": audio_b64
                                })
                    except Exception as e:
                        await ws.send_json({
                            "type": "response",
                            "text": f"Ошибка анализа экрана: {str(e)}",
                            "audio": None
                        })
    finally:
        pass
    return ws

async def start_dual_server(app):
    runner = web.AppRunner(app)
    await runner.setup()

    # Port 8766: Plain HTTP/WS for localhost (zero cert warnings)
    site_http = web.TCPSite(runner, '0.0.0.0', 8766)
    await site_http.start()

    # Port 8765: HTTPS/WSS with SAN Certificate for Tailscale / remote LAN
    cert_path = r'cert.pem'
    key_path = r'key.pem'
    if os.path.exists(cert_path) and os.path.exists(key_path):
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(cert_path, key_path)
        site_https = web.TCPSite(runner, '0.0.0.0', 8765, ssl_context=ssl_context)
        await site_https.start()

    while True:
        await asyncio.sleep(3600)
```
