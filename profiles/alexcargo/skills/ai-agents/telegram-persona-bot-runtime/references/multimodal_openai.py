# -*- coding: utf-8 -*-
"""Verified stdlib-only multimodal helpers for the Richard Marlowe / persona bot.
No pip deps. Uses OPENAI_API_KEY from .env.local. Nous inference 404s on vision/audio,
so media MUST go through OpenAI directly.

Verified live 2026-07-23:
  - whisper-1 transcription: HTTP 200, returns {"text": "..."}
  - gpt-4o-mini vision on a 32x32 PIL PNG: HTTP 200, returns color description
  (1x1 PNG -> 400 Bad Request; use >=32px for tests)
"""

import os
import json
import base64
import subprocess
import urllib.request
import urllib.error

OPENAI_BASE = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")


def openai_key():
    k = os.environ.get("OPENAI_API_KEY", "")
    return k if (k and not k.startswith("stub-")) else ""


def _dl_telegram_file(token, file_id):
    """GET https://api.telegram.org/bot<token>/getFile -> file_path -> download bytes."""
    info = json.loads(urllib.request.urlopen(
        "https://api.telegram.org/bot%s/getFile?file_id=%s" % (token, file_id),
        timeout=60).read().decode())
    path = info.get("result", {}).get("file_path")
    if not path:
        return None
    return urllib.request.urlopen(
        "https://api.telegram.org/file/bot%s/%s" % (token, path), timeout=60).read()


def transcribe_audio(token, file_id):
    """Voice/audio -> text via OpenAI Whisper. Returns transcript str or None."""
    key = openai_key()
    if not key:
        return None
    data = _dl_telegram_file(token, file_id)
    if not data:
        return None
    boundary = "----richardboundary"
    body = b"".join([
        ("--%s\r\n" % boundary).encode(),
        b'Content-Disposition: form-data; name="model"\r\n\r\n', b"whisper-1\r\n",
        ("--%s\r\n" % boundary).encode(),
        b'Content-Disposition: form-data; name="file"; filename="audio.ogg"\r\n',
        b"Content-Type: audio/ogg\r\n\r\n", data,
        ("\r\n--%s--\r\n" % boundary).encode(),
    ])
    req = urllib.request.Request(OPENAI_BASE + "/audio/transcriptions", data=body, method="POST")
    req.add_header("Authorization", "Bearer %s" % key)
    req.add_header("Content-Type", "multipart/form-data; boundary=%s" % boundary)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode("utf-8")).get("text", "")
    except Exception as e:
        print("[bot] whisper err: %s" % e)
        return None


def describe_image(token, file_id, kind="photo", frame=False):
    """Photo/video -> text via OpenAI gpt-4o-mini vision. kind='video' pulls 1 frame w/ ffmpeg."""
    key = openai_key()
    if not key:
        return None
    if kind == "video" and frame:
        import tempfile
        data = _dl_telegram_file(token, file_id)
        if not data:
            return None
        tmp = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
        tmp.write(data); tmp.close()
        jpg = tmp.name + ".jpg"
        subprocess.run(["ffmpeg", "-y", "-i", tmp.name, "-frames:v", "1", "-ss", "00:00:01", jpg],
                       capture_output=True, timeout=60)
        with open(jpg, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        os.remove(tmp.name)
    else:
        data = _dl_telegram_file(token, file_id)
        if not data:
            return None
        b64 = base64.b64encode(data).decode()
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": "Describe this image concisely. Reply in the user's language."},
            {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,%s" % b64}},
        ]}],
        "max_tokens": 300,
    }
    req = urllib.request.Request(OPENAI_BASE + "/chat/completions",
                                 data=json.dumps(payload).encode(), method="POST")
    req.add_header("Authorization", "Bearer %s" % key)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode("utf-8"))["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("[bot] vision err: %s" % e)
        return None
