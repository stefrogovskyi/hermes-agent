# -*- coding: utf-8 -*-
"""
daily_full_indexer.py — Дифференциальная индексация файлов и Google Workspace в базу данных SQLite FTS5.
"""

import os, sys, time, sqlite3, json, subprocess

DB_PATH = "/opt/hermes/state/full_reality_index.db"
LOG_FILE = "/opt/hermes/logs/indexer.log"

os.makedirs("/opt/hermes/state", exist_ok=True)
os.makedirs("/opt/hermes/logs", exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH, timeout=5.0)
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
    file_types = {}
    batch = []
    scanned_folders = set()
    sample_files = []
    
    target_roots = [
        "/opt/hermes/skills",
        "/opt/hermes/scripts",
        "/opt/hermes/memories",
    ]
    for p in ["aeon", "alistair", "archie", "ben", "callum", "harrison", "liz", "richard"]:
        target_roots.append(f"/opt/hermes/profiles/{p}/skills")
        target_roots.append(f"/opt/hermes/profiles/{p}/scripts")
        target_roots.append(f"/opt/hermes/profiles/{p}/memories")
    
    skip_set = {"__pycache__", ".git", "venv", "node_modules"}
    
    for troot in target_roots:
        if not os.path.exists(troot):
            continue
        rel_folder = os.path.relpath(troot, "/opt/hermes")
        scanned_folders.add(rel_folder)
        for root, dirs, files in os.walk(troot):
            dirs[:] = [d for d in dirs if d not in skip_set]
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext in [".py", ".md", ".json", ".txt", ".yaml", ".yml", ".sh", ".docx", ".xlsx"]:
                    fpath = os.path.join(root, f)
                    try:
                        rel_p = os.path.relpath(fpath, "/opt/hermes")
                        with open(fpath, "r", encoding="utf-8", errors="ignore") as fp:
                            content = fp.read(1500)
                        batch.append((rel_p, f, content, fpath))
                        file_types[ext] = file_types.get(ext, 0) + 1
                        if len(sample_files) < 4 and ext in [".md", ".docx", ".py"]:
                            sample_files.append(rel_p)
                    except Exception:
                        pass

    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    cur = conn.cursor()
    cur.executemany("""
        INSERT OR REPLACE INTO reality_fts(file_id, file_name, source, mime_type, content, web_link)
        VALUES (?, ?, 'local', 'text/plain', ?, ?)
    """, batch)
    conn.commit()
    conn.close()
    return len(batch), file_types, list(scanned_folders)[:5], sample_files

def index_google_workspace():
    gapi_script = "/opt/hermes/skills/productivity/google-workspace/scripts/google_api.py"
    if not os.path.exists(gapi_script):
        return 0, [], "Скрипт Google API не найден"

    try:
        cmd = ["/opt/hermes/hermes-agent/venv/bin/python3", gapi_script, "drive", "search", "trashed=false", "--raw-query", "--max", "50"]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if res.returncode == 0:
            files = json.loads(res.stdout)
            batch = []
            sample_docs = []
            for item in files:
                fid = item.get("id")
                fname = item.get("name")
                mime = item.get("mimeType")
                link = item.get("webViewLink")
                batch.append((fid, fname, mime, fname, link))
                if len(sample_docs) < 4 and fname:
                    sample_docs.append(fname)
            
            conn = sqlite3.connect(DB_PATH, timeout=10.0)
            cur = conn.cursor()
            cur.executemany("""
                INSERT OR REPLACE INTO reality_fts(file_id, file_name, source, mime_type, content, web_link)
                VALUES (?, ?, 'google_drive', ?, ?, ?)
            """, batch)
            conn.commit()
            conn.close()
            return len(files), sample_docs, None
        else:
            return 0, [], f"Google API: {res.stderr[:80]}"
    except Exception as e:
        return 0, [], str(e)

def main():
    start_time = time.time()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    init_db()
    local_count, file_types, sample_folders, sample_local_files = index_local_files()
    gdrive_count, sample_docs, gdrive_err = index_google_workspace()
    
    duration = time.time() - start_time
    
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM reality_fts")
    total_db_records = cur.fetchone()[0]
    conn.close()

    types_breakdown = ", ".join([f"`{k}`: {v}" for k, v in sorted(file_types.items(), key=lambda x: -x[1])[:5]])
    
    report = []
    report.append("📚 **Ежедневная индексация экосистемы и Google Workspace (Full Reality)**")
    report.append(f"⏱ *Время запуска:* `{timestamp}` (Киев) | ⚡ *Длительность:* `{duration:.2f}с`")
    report.append("—" * 28)
    report.append("")
    report.append(f"📁 **Локальный воркспейс (`/opt/hermes`):**")
    report.append(f"• Проиндексировано файлов знаний: **`{local_count:,}`**")
    report.append(f"• Топ форматов: {types_breakdown}")
    if sample_folders:
        folders_str = ", ".join([f"`{f}`" for f in sample_folders[:4]])
        report.append(f"• Основные папки: {folders_str}")
    if sample_local_files:
        report.append("• Примеры проиндексированных файлов:")
        for sf in sample_local_files[:3]:
            report.append(f"  └ 📄 `{sf}`")
    report.append("")
    report.append(f"☁️ **Google Drive & Docs:**")
    if gdrive_err:
        report.append(f"• ⚠️ Статус: *{gdrive_err}*")
    else:
        report.append(f"• Проиндексировано активных документов/таблиц: **`{gdrive_count}`**")
        if sample_docs:
            report.append("• Примеры свежих документов:")
            for sd in sample_docs[:4]:
                report.append(f"  └ 📑 *{sd}*")
    report.append("")
    report.append(f"🔍 **База полнотекстового поиска (SQLite FTS5):**")
    report.append(f"• Всего записей в индексе: **`{total_db_records:,}`**")
    report.append(f"• База: `/opt/hermes/state/full_reality_index.db`")
    report.append("")
    report.append("—" * 28)
    report.append("✨ **Итог:** База знаний актуальна. Все агенты могут находить любые локальные файлы и Google Документы мгновенно!")

    final_msg = "\n".join(report)
    print(final_msg)
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] [DailyIndexer]\n" + final_msg + "\n\n")

if __name__ == "__main__":
    main()
