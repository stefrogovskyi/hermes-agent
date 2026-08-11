# -*- coding: utf-8 -*-
"""
daily_full_indexer.py — Дифференциальная индексация файлов и Google Workspace в базу данных SQLite FTS5.
"""

import os, sys, time, sqlite3, json, subprocess

DB_PATH = "/opt/hermes/state/full_reality_index.db"
LOG_FILE = "/opt/hermes/logs/indexer.log"

os.makedirs("/opt/hermes/state", exist_ok=True)
os.makedirs("/opt/hermes/logs", exist_ok=True)

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] [DailyIndexer] {msg}"
    print(formatted, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(formatted + "\n")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS reality_fts USING fts5(
            file_id,
            file_name,
            source,
            mime_type,
            content,
            web_link
        )
    """)
    conn.commit()
    conn.close()

def index_local_files():
    log("Indexing local workspace files...")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    indexed_count = 0
    for root, dirs, files in os.walk("/opt/hermes"):
        if "venv" in root or ".git" in root or "logs" in root or "cache" in root:
            continue
        for f in files:
            if f.endswith((".py", ".md", ".json", ".txt", ".yaml", ".sh", ".html")):
                fpath = os.path.join(root, f)
                try:
                    rel_p = os.path.relpath(fpath, "/opt/hermes")
                    content = open(fpath, encoding="utf-8", errors="ignore").read(5000)
                    cur.execute("""
                        INSERT OR REPLACE INTO reality_fts(file_id, file_name, source, mime_type, content, web_link)
                        VALUES (?, ?, 'local', 'text/plain', ?, ?)
                    """, (rel_p, f, content, fpath))
                    indexed_count += 1
                except Exception:
                    pass
                    
    conn.commit()
    conn.close()
    log(f"Indexed {indexed_count} local workspace files into FTS5.")

def index_google_workspace():
    log("Indexing Google Drive & Workspace docs...")
    gapi_script = "/opt/hermes/skills/productivity/google-workspace/scripts/google_api.py"
    if not os.path.exists(gapi_script):
        log("Google API script not found, skipping Google Drive index.")
        return

    try:
        cmd = ["/opt/hermes/hermes-agent/venv/bin/python3", gapi_script, "drive", "search", "trashed=false", "--raw-query", "--max", "100"]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if res.returncode == 0:
            files = json.loads(res.stdout)
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            for item in files:
                fid = item.get("id")
                fname = item.get("name")
                mime = item.get("mimeType")
                link = item.get("webViewLink")
                cur.execute("""
                    INSERT OR REPLACE INTO reality_fts(file_id, file_name, source, mime_type, content, web_link)
                    VALUES (?, ?, 'google_drive', ?, ?, ?)
                """, (fid, fname, mime, fname, link))
            conn.commit()
            conn.close()
            log(f"Indexed {len(files)} Google Drive items into FTS5.")
        else:
            log(f"Google Drive search status code non-zero: {res.stderr[:200]}")
    except Exception as e:
        log(f"Google Workspace index exception: {e}")

def main():
    log("=== STARTING DAILY FULL REALITY & GOOGLE WORKSPACE INDEXER ===")
    init_db()
    index_local_files()
    index_google_workspace()
    log("=== DAILY INDEXING COMPLETED SUCCESSFULLY ===")

if __name__ == "__main__":
    main()
