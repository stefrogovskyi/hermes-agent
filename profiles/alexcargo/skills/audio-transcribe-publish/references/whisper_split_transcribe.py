import os, sys, time, json, urllib.request

OUTDIR = r"C:\Users\Stefan\AppData\Local\hermes\scripts\transcribe_tmp"
SRC = r"C:\Users\Stefan\Desktop\Standard recording 1.mp3"   # <-- set per run
OUT = os.path.join(OUTDIR, "full_transcript.txt")
os.makedirs(OUTDIR, exist_ok=True)

# OpenAI key from Hermes .env (NOT os.environ)
key = None
for line in open(r"C:\Users\Stefan\AppData\Local\hermes\.env", encoding="utf-8"):
    if line.strip().startswith("VOICE_TOOLS_OPENAI_KEY="):
        key = line.strip().split("=", 1)[1].strip().strip('"')
assert key, "no key"

# 1) split into ~9-min parts (<25MB)
import subprocess
dur = float(json.loads(subprocess.run(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", SRC],
    capture_output=True, text=True).stdout)["format"]["duration"])
SEG = 540
n = max(1, int(dur // SEG) + (1 if dur % SEG else 0))
for i in range(n):
    out = os.path.join(OUTDIR, "part_%02d.mp3" % i)
    if os.path.exists(out) and os.path.getsize(out) > 1000:
        continue
    subprocess.run(["ffmpeg", "-y", "-ss", str(i*SEG), "-i", SRC, "-t", str(SEG), "-c", "copy", out],
                   capture_output=True, text=True, timeout=300)

# 2) transcribe each part
parts = sorted(f for f in os.listdir(OUTDIR) if f.startswith("part_") and f.endswith(".mp3"))
full = []
for p in parts:
    path = os.path.join(OUTDIR, p)
    data = open(path, "rb").read()
    for attempt in range(3):
        try:
            boundary = "----hermeswhisper"
            body = (b"--%s\r\n" % boundary.encode() +
                    b'Content-Disposition: form-data; name="model"\r\n\r\nwhisper-1\r\n' +
                    b"--%s\r\n" % boundary.encode() +
                    b'Content-Disposition: form-data; name="file"; filename="a.mp3"\r\n' +
                    b"Content-Type: audio/mpeg\r\n\r\n" + data +
                    b"\r\n--%s--\r\n" % boundary.encode())
            req = urllib.request.Request("https://api.openai.com/v1/audio/transcriptions",
                                         data=body, method="POST")
            req.add_header("Authorization", "Bearer %s" % key)
            req.add_header("Content-Type", "multipart/form-data; boundary=%s" % boundary)
            with urllib.request.urlopen(req, timeout=120) as r:
                full.append(json.loads(r.read().decode("utf-8")).get("text", ""))
            break
        except Exception as e:
            print("err", p, e); time.sleep(5)

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n\n".join(full))
print("SAVED", OUT, sum(len(x) for x in full), "chars")
