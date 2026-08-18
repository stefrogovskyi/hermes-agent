#!/usr/bin/env python3
import http.server
import socketserver
import os, json, sqlite3, glob, time, urllib.request
from urllib.parse import urlparse, parse_qs

PORT = 8888
DIRECTORY = "/opt/hermes/mission-control"

PROFILES = {
    "hermes": {"name": "Hermes Stevenson", "db": "/opt/hermes/state.db", "role": "Master Orchestrator", "category": "Master Orchestrator", "badge": "gemini-3.7-flash"},
    "openclaw": {"name": "OpenClaw Gateway", "db": "", "role": "AI Coding Agent Gateway :18789", "category": "AI Coding Agent", "badge": "OpenClaw 2026.8.1"},
    "richard": {"name": "Richard Marlowe", "db": "/opt/hermes/profiles/richard/state.db", "role": "B2B Sales CRM (@richnavobot)", "category": "Autonomous Agent", "badge": "Sales Lead"},
    "callum": {"name": "Callum Vance", "db": "/opt/hermes/profiles/callum/state.db", "role": "Full-Stack Engineer (@callumvancebot)", "category": "Autonomous Agent", "badge": "Engineer"},
    "alistair": {"name": "Alistair", "db": "/opt/hermes/profiles/alistair/state.db", "role": "Benchmark Lead (@alistairkanbanbot)", "category": "Autonomous Agent", "badge": "SeaRates vs Navo"},
    "archie": {"name": "Archie Wright", "db": "/opt/hermes/profiles/archie/state.db", "role": "Content Strategist (@archiewrightbot)", "category": "Autonomous Agent", "badge": "Copywriter"},
    "liz": {"name": "Liz Harper", "db": "/opt/hermes/profiles/liz/state.db", "role": "Executive Assistant", "category": "Autonomous Agent", "badge": "Operations"},
    "ben": {"name": "Ben", "db": "/opt/hermes/profiles/ben/state.db", "role": "Operations Specialist", "category": "Autonomous Agent", "badge": "Logistics"},
    "career_scanner": {"name": "Career Scanner v2", "db": "", "role": "11 Verified APIs + Workday + Oracle", "category": "Automated Feeds", "badge": "Daily 09:00 MSK"},
    "odessa_router": {"name": "Odessa Safe Router", "db": "", "role": "Telethon Closed TG Group Ingress", "category": "Safety Feeds", "badge": "Session Active"}
}

class MissionControlHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/send_message":
            content_len = int(self.headers.get('Content-Length', 0))
            post_body = self.rfile.read(content_len)
            try:
                payload = json.loads(post_body.decode('utf-8'))
                profile = payload.get('profile', 'hermes')
                text = payload.get('message', '').strip()
                if not text:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Empty message"}).encode('utf-8'))
                    return

                # If openclaw -> post to telegram / openclaw gateway
                if profile == 'openclaw':
                    import urllib.request
                    # Direct to Telegram bot API
                    tg_token = "8899116964:AAF8te9U2FSa-cnJg6tT1Dx7ljwPaINk4RM"
                    tg_url = f"https://api.telegram.org/bot{tg_token}/sendMessage"
                    req = urllib.request.Request(tg_url, data=json.dumps({"chat_id": 330656040, "text": f"[AgentOS Web]: {text}"}).encode('utf-8'), headers={'Content-Type': 'application/json'})
                    try:
                        urllib.request.urlopen(req, timeout=5)
                    except Exception:
                        pass
                    
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "sent", "profile": profile}).encode('utf-8'))
                    return

                # Record message into Hermes profile DB
                cfg = PROFILES.get(profile, PROFILES['hermes'])
                db_path = cfg["db"]
                if os.path.exists(db_path):
                    conn = sqlite3.connect(db_path)
                    cur = conn.cursor()
                    cur.execute("SELECT session_id FROM messages ORDER BY id DESC LIMIT 1")
                    row = cur.fetchone()
                    sess_id = row[0] if row else "agentos_web_session"
                    cur.execute("INSERT INTO messages (session_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
                                (sess_id, "user", f"[AgentOS Web] {text}", time.strftime('%Y-%m-%d %H:%M:%S')))
                    conn.commit()
                    conn.close()

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok", "profile": profile}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()

    def do_HEAD(self):
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/"):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            return
        super().do_HEAD()

    def do_GET(self):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)

        if parsed.path.startswith("/api/"):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()

            endpoint = parsed.path[5:]
            profile = query.get('profile', ['hermes'])[0]

            # 1. MESSAGES
            if endpoint == "messages":
                limit = int(query.get('limit', ['50'])[0])
                cfg = PROFILES.get(profile, PROFILES['hermes'])
                db_path = cfg["db"]

                messages = []
                if db_path and os.path.exists(db_path):
                    try:
                        conn = sqlite3.connect(db_path)
                        cur = conn.cursor()
                        cur.execute("SELECT id, session_id, role, content, timestamp FROM messages ORDER BY id DESC LIMIT ?", (limit,))
                        rows = cur.fetchall()
                        conn.close()
                        for r in reversed(rows):
                            messages.append({
                                "id": r[0],
                                "session_id": r[1],
                                "role": r[2],
                                "content": r[3],
                                "time": r[4]
                            })
                    except Exception as e:
                        messages = [{"id": 0, "role": "system", "content": f"Database read error: {e}", "time": ""}]

                self.wfile.write(json.dumps({"profile": profile, "messages": messages}, ensure_ascii=False).encode('utf-8'))
                return

            # 2. KANBAN STORE
            elif endpoint == "kanban":
                try:
                    url = f"https://dev.aavalanche.com/kanban_api.php?agent={profile}"
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=5) as resp:
                        data = json.loads(resp.read().decode('utf-8'))
                        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
                except Exception as e:
                    self.wfile.write(json.dumps({"cards": [], "activity": [], "error": str(e)}).encode('utf-8'))
                return

            # 3. CRONS
            elif endpoint == "crons":
                crons = []
                for fn in glob.glob('/opt/hermes/cron/jobs/*.json'):
                    try:
                        with open(fn) as f:
                            d = json.load(f)
                            crons.append({
                                "id": d.get("job_id", os.path.basename(fn).replace(".json", "")),
                                "name": d.get("name", "Unnamed Cron"),
                                "schedule": d.get("schedule", ""),
                                "prompt": d.get("prompt", "")[:120] + "...",
                                "state": d.get("state", "active")
                            })
                    except Exception:
                        pass
                self.wfile.write(json.dumps({"crons": crons}, ensure_ascii=False).encode('utf-8'))
                return

            # 4. CAPABILITIES (Skills, Tools, MCP, Browse Hub)
            elif endpoint == "capabilities":
                skills = []
                for s_path in glob.glob('/opt/hermes/skills/**/SKILL.md', recursive=True):
                    try:
                        rel = os.path.relpath(s_path, '/opt/hermes/skills')
                        parts = rel.split(os.sep)
                        cat = parts[0] if len(parts) > 1 else 'general'
                        name = parts[-2] if len(parts) > 1 else os.path.basename(os.path.dirname(s_path))
                        # Read frontmatter description
                        desc = ""
                        with open(s_path, 'r', encoding='utf-8', errors='ignore') as sf:
                            for line in sf:
                                if line.startswith('description:'):
                                    desc = line.split('description:', 1)[1].strip().strip('"').strip("'")
                                    break
                        skills.append({"name": name, "category": cat, "description": desc or "No description", "type": "skill"})
                    except Exception:
                        pass
                
                # Built-in Tools
                tools = [
                    {"name": "terminal", "category": "execution", "description": "Execute shell commands, run tests, deploys, and builds in Linux.", "type": "tool"},
                    {"name": "read_file", "category": "filesystem", "description": "Read text files, notebooks, docs, and structured data.", "type": "tool"},
                    {"name": "write_file", "category": "filesystem", "description": "Write and create files with syntax verification.", "type": "tool"},
                    {"name": "patch", "category": "filesystem", "description": "Targeted fuzzy find-and-replace edits in files.", "type": "tool"},
                    {"name": "search_files", "category": "filesystem", "description": "Ripgrep-powered regex content and file search.", "type": "tool"},
                    {"name": "web_search", "category": "web", "description": "Search web engine results for real-time data.", "type": "tool"},
                    {"name": "web_extract", "category": "web", "description": "Extract clean markdown content from URLs and PDFs.", "type": "tool"},
                    {"name": "browser_exec", "category": "browser", "description": "Full headless Chromium browser automation (Playwright/CDP).", "type": "tool"},
                    {"name": "delegate_task", "category": "agentic", "description": "Spawn and orchestrate isolated background subagents.", "type": "tool"},
                    {"name": "cronjob", "category": "scheduler", "description": "Autonomous cron job creation, updating, and execution.", "type": "tool"},
                    {"name": "memory", "category": "memory", "description": "Persistent memory storage across sessions.", "type": "tool"},
                    {"name": "vision_analyze", "category": "multimodal", "description": "Inspect and reason over images, diagrams, and screenshots.", "type": "tool"}
                ]

                # MCP Servers
                mcp = [
                    {"name": "TrackingMCP", "category": "Logistics", "description": "Navo unified container tracking API across ocean lines.", "type": "mcp"},
                    {"name": "SchedulesMCP", "category": "Logistics", "description": "Point-to-point vessel schedules and ocean routing.", "type": "mcp"},
                    {"name": "FreightRatesMCP", "category": "Logistics", "description": "Real-time spot freight rates benchmark and quote calculator.", "type": "mcp"},
                    {"name": "TouchDesigner MCP", "category": "Media", "description": "Real-time generative visuals & AV bridge over MCP.", "type": "mcp"}
                ]

                # Browse Hub
                browse_hub = [
                    {"name": "Nous Research Hub", "category": "Community", "description": "Official community skills registry and model fine-tunes.", "type": "hub"},
                    {"name": "NVIDIA NIM Catalog", "category": "Compute", "description": "102 microservice models with enterprise governance.", "type": "hub"},
                    {"name": "Hugging Face Spaces", "category": "Models", "description": "Open models, datasets, and serverless inference.", "type": "hub"}
                ]

                self.wfile.write(json.dumps({
                    "skills": skills,
                    "tools": tools,
                    "mcp": mcp,
                    "browse_hub": browse_hub
                }, ensure_ascii=False).encode('utf-8'))
                return

            # 5. ARTIFACTS (Images, Files, Links)
            elif endpoint == "artifacts":
                # Scan /opt/hermes for generated artifacts
                images = []
                for ext in ('*.png', '*.jpg', '*.jpeg', '*.webp'):
                    for img in glob.glob(f'/opt/hermes/cache/images/{ext}') + glob.glob(f'/opt/hermes/artifacts/{ext}'):
                        images.append({
                            "name": os.path.basename(img),
                            "path": img,
                            "size": f"{os.path.getsize(img) // 1024} KB",
                            "time": time.strftime('%Y-%m-%d %H:%M', time.localtime(os.path.getmtime(img))),
                            "type": "image"
                        })

                files = []
                for f_path in glob.glob('/opt/hermes/scripts/*.py') + glob.glob('/opt/hermes/mission-control/*.html') + glob.glob('/opt/hermes/mission-control/*.php'):
                    files.append({
                        "name": os.path.basename(f_path),
                        "path": f_path,
                        "size": f"{os.path.getsize(f_path) // 1024} KB",
                        "time": time.strftime('%Y-%m-%d %H:%M', time.localtime(os.path.getmtime(f_path))),
                        "type": "file"
                    })

                links = [
                    {"name": "AgentOS Mission Control", "url": "https://aavalanche.com/agentos/", "category": "Dashboard", "type": "link"},
                    {"name": "OpenClaw Gateway UI", "url": "http://100.99.146.42:18789", "category": "Gateway", "type": "link"},
                    {"name": "Richard Kanban", "url": "https://richard-kanban.vercel.app", "category": "Kanban", "type": "link"},
                    {"name": "Callum Kanban", "url": "https://callum-kanban.vercel.app", "category": "Kanban", "type": "link"},
                    {"name": "Alistair Kanban", "url": "https://alistair-kanban.vercel.app", "category": "Kanban", "type": "link"},
                    {"name": "Archie Kanban", "url": "https://dev.aavalanche.com/kanban_api.php?agent=archie", "category": "Kanban", "type": "link"},
                    {"name": "Liz Kanban", "url": "https://liz-kanban.vercel.app", "category": "Kanban", "type": "link"},
                    {"name": "Ben Kanban", "url": "https://ben-kanban.vercel.app", "category": "Kanban", "type": "link"},
                    {"name": "NVIDIA Build API", "url": "https://build.nvidia.com", "category": "API", "type": "link"}
                ]

                self.wfile.write(json.dumps({
                    "images": images,
                    "files": files,
                    "links": links
                }, ensure_ascii=False).encode('utf-8'))
                return

            # 6. SETTINGS & GEAR (Hermes Desktop-like options & Models)
            elif endpoint == "settings":
                # Read config.yaml & fallback providers
                import yaml
                cfg = {}
                with open('/opt/hermes/config.yaml', 'r') as f:
                    cfg = yaml.safe_load(f) or {}

                models_all = [
                    {"id": "google/gemini-3.7-flash", "provider": "google", "tier": "Primary", "desc": "Master Orchestrator Global Default"},
                    {"id": "google/gemini-2.5-flash", "provider": "google", "tier": "Fallback 1", "desc": "High Speed Google Native"},
                    {"id": "gpt-4o", "provider": "openai", "tier": "Fallback 2", "desc": "OpenAI Flagship Tier"},
                    {"id": "gpt-4o-mini", "provider": "openai", "tier": "Fallback 3", "desc": "OpenAI Fast Tier"},
                    {"id": "nvidia/nemotron-3.5-lightning-30b-a3b", "provider": "nvidia", "tier": "Direct NIM", "desc": "0.29s Latency NVIDIA NIM Cloud"},
                    {"id": "nvidia/llama-3.3-nemotron-super-49b-v1.5", "provider": "nvidia", "tier": "Direct NIM", "desc": "NVIDIA High Precision Reasoning"},
                    {"id": "nvidia/nemotron-mini-4b-instruct", "provider": "nvidia", "tier": "Direct NIM", "desc": "Ultra Fast 0.22s Edge NIM"},
                    {"id": "meta-llama/Llama-3.3-70B-Instruct", "provider": "huggingface", "tier": "Direct HF", "desc": "Hugging Face Inference Router"},
                    {"id": "Qwen/Qwen2.5-72B-Instruct", "provider": "huggingface", "tier": "Direct HF", "desc": "Hugging Face Qwen High-Compute"},
                    {"id": "minimax-m2.7", "provider": "gonka24", "tier": "Gonka24", "desc": "Gonka24 High Context Engine"},
                    {"id": "kimi-k2.6", "provider": "gonka24", "tier": "Gonka24", "desc": "Gonka24 Fast Math & Reasoning"},
                    {"id": "openrouter/nvidia/nemotron-3.5-lightning:free", "provider": "openrouter", "tier": "Free Tier", "desc": "OpenRouter Zero-Cost Fast Lane"}
                ]

                self.wfile.write(json.dumps({
                    "config": {
                        "primary_model": cfg.get("model", {}).get("default", "google/gemini-3.7-flash"),
                        "primary_provider": cfg.get("model", {}).get("provider", "google"),
                        "timeout_seconds": cfg.get("model", {}).get("request_timeout_seconds", 30),
                        "max_retries": cfg.get("model", {}).get("max_retries", 2),
                        "temperature": 0.7,
                        "fallback_providers_count": len(cfg.get("fallback_providers", [])),
                        "auto_tts": False,
                        "voice": "onyx"
                    },
                    "models": models_all
                }, ensure_ascii=False).encode('utf-8'))
                return

            self.wfile.write(json.dumps({"status": "unknown endpoint"}).encode('utf-8'))
            return

        super().do_GET()

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    os.chdir(DIRECTORY)
    with ReusableTCPServer(("", PORT), MissionControlHandler) as httpd:
        print(f"AgentOS Master API Gateway serving on port {PORT}")
        httpd.serve_forever()
