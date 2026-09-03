#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
voice_server.py — Richard Marlowe (Navo24)
Bi-directional Audio WebSocket Server for Twilio Media Streams.
Connects Twilio Call -> Speech Recognition -> Gemini/LLM -> Polly/Neural Voice.
"""

import os
import json
import asyncio
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import Response
import uvicorn

app = FastAPI(title="Richard Marlowe Voice Gateway")

TWIML_RESPONSE = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Brian-Neural" language="en-GB">Hello. This is Richard Marlowe from Navo twenty four in London. Connecting to our live sales desk.</Say>
    <Connect>
        <Stream url="wss://{host}/media-stream" />
    </Connect>
</Response>
"""

@app.api_route("/incoming-call", methods=["GET", "POST"])
async def incoming_call(request: Request):
    host = request.headers.get("host", "localhost:8000")
    xml_content = TWIML_RESPONSE.format(host=host)
    return Response(content=xml_content, media_type="application/xml")

@app.websocket("/media-stream")
async def media_stream(websocket: WebSocket):
    await websocket.accept()
    print(" Twilio WebSocket Media Stream connected!")
    
    try:
        async for message in websocket.iter_text():
            data = json.loads(message)
            event = data.get("event")
            
            if event == "start":
                print(f"Call Stream Started: SID={data.get('start', {}).get('streamSid')}")
            elif event == "media":
                # Process 8kHz mulaw audio packet from caller
                payload = data.get("media", {}).get("payload")
                # Route to STT & LLM Pipeline
                pass
            elif event == "stop":
                print("Call Stream Stopped.")
                break
    except Exception as e:
        print(f"WebSocket Error: {e}")
    finally:
        await websocket.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
