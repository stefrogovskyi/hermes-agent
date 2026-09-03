import os
import json
import asyncio
import websockets
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(title="Voice AI Telephony Bridge")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def load_session_instructions() -> tuple[str, str]:
    """Loads memory, caller context, and builds grounded persona."""
    call_ctx_path = "active_call_context.json"
    call_ctx = {}
    if os.path.exists(call_ctx_path):
        try:
            with open(call_ctx_path, "r", encoding="utf-8") as f:
                call_ctx = json.load(f)
        except Exception:
            pass

    caller_name = call_ctx.get("name", "Colleague")
    caller_role = call_ctx.get("role", "Partner")
    greeting = call_ctx.get("greeting", "Hello! This is Richard Marlowe from Navo24. How are you today?")

    prompt = f"""You are Richard Marlowe, Senior B2B Sales Manager at Navo24.
You are on a live phone call with {caller_name} ({caller_role}).

UNIVERSAL LANGUAGE POLICY:
1. Detect and speak the EXACT SAME language that the caller is speaking.
2. Once a language is active, REMAIN in that language 100% across all turns.
3. NEVER switch languages autonomously. Only switch when the caller switches.

CONVERSATIONAL TONE (HUMANIZE):
- Speak like a real human: warm, relaxed, concise (1-2 sentences).
- FORBIDDEN: robotic corporate clichés ("ready for a productive talk", "let's set priorities", "act strictly on business").
- If interrupted, yield immediately and answer the caller's new thought.
- Do NOT invent unverified features. Ground all answers in real product facts.
"""
    return prompt, greeting

@app.websocket("/media-stream")
async def media_stream(websocket: WebSocket):
    await websocket.accept()
    openai_ws_url = "wss://api.openai.com/v1/realtime?model=gpt-realtime"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    stream_sid = None

    try:
        async with websockets.connect(openai_ws_url, additional_headers=headers) as openai_ws:
            await openai_ws.recv() # session.created
            
            system_prompt, dynamic_greeting = load_session_instructions()
            
            # Configure session for G.711 PCMU & tuned server VAD (anti-false-cutoff)
            session_config = {
                "type": "session.update",
                "session": {
                    "type": "realtime",
                    "instructions": system_prompt,
                    "audio": {
                        "input": {
                            "format": {"type": "audio/pcmu"},
                            "transcription": {"model": "whisper-1"},
                            "turn_detection": {
                                "type": "server_vad",
                                "threshold": 0.65,
                                "prefix_padding_ms": 300,
                                "silence_duration_ms": 350,
                                "create_response": True,
                                "interrupt_response": True
                            }
                        },
                        "output": {
                            "format": {"type": "audio/pcmu"},
                            "voice": "ash"
                        }
                    }
                }
            }
            await openai_ws.send(json.dumps(session_config))
            await openai_ws.recv() # session.updated

            async def openai_to_twilio():
                nonlocal stream_sid
                try:
                    async for raw in openai_ws:
                        evt = json.loads(raw)
                        t = evt.get("type")
                        if t == "response.output_audio.delta" and stream_sid:
                            await websocket.send_text(json.dumps({
                                "event": "media",
                                "streamSid": stream_sid,
                                "media": {"payload": evt["delta"]}
                            }))
                        elif t == "input_audio_buffer.speech_started" and stream_sid:
                            # Clear Twilio playback buffer immediately (barge-in)
                            await websocket.send_text(json.dumps({
                                "event": "clear",
                                "streamSid": stream_sid
                            }))
                        elif t == "conversation.item.input_audio_transcription.completed":
                            user_text = evt.get("transcript", "").strip()
                            if user_text:
                                print(f"🗣️ [Caller]: {user_text}")
                        elif t == "response.output_audio_transcript.done":
                            bot_text = evt.get("transcript", "").strip()
                            if bot_text:
                                print(f"🤖 [Assistant]: {bot_text}")
                except Exception:
                    pass

            async def twilio_to_openai():
                nonlocal stream_sid
                greeting_sent = False
                try:
                    while True:
                        msg = await websocket.receive_text()
                        data = json.loads(msg)
                        e = data.get("event")
                        if e == "start":
                            stream_sid = data.get("start", {}).get("streamSid")
                            if not greeting_sent:
                                greeting_sent = True
                                await openai_ws.send(json.dumps({
                                    "type": "response.create",
                                    "response": {
                                        "instructions": f"Say naturally: '{dynamic_greeting}'"
                                    }
                                }))
                        elif e == "media":
                            payload = data.get("media", {}).get("payload")
                            if payload:
                                await openai_ws.send(json.dumps({
                                    "type": "input_audio_buffer.append",
                                    "audio": payload
                                }))
                        elif e == "stop":
                            break
                except Exception:
                    pass

            t1 = asyncio.create_task(openai_to_twilio())
            t2 = asyncio.create_task(twilio_to_openai())
            await asyncio.wait([t1, t2], return_when=asyncio.FIRST_COMPLETED)
    except Exception:
        pass
