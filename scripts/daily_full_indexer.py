# -*- coding: utf-8 -*-
"""
daily_full_indexer.py — Дифференциальная индексация файлов (VPS + Windows Desktop + Google Workspace) в базу данных SQLite FTS5.
"""

import os, sys, time, sqlite3, json, subprocess, base64

DB_PATH = "/opt/hermes/state/full_reality_index.db"
LOG_FILE = "/opt/hermes/logs/indexer.log"
DESKTOP_SSH = "Stefan@100.79.157.46"

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

def index_local_vps_files():
    file_types = {}
    batch = []
    scanned_folders = set()
    sample_files = []
    
    target_roots = [
        "/opt/hermes/skills",
        "/opt/hermes/scripts",
        "/opt/hermes/memories",
    ]
    for p in ["aeon", "alistair", "archie", "ben", "callum", "charile", "harrison", "liz", "richard"]:
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
                        batch.append((rel_p, f, "local_vps", "text/plain", content, fpath))
                        file_types[ext] = file_types.get(ext, 0) + 1
                        if len(sample_files) < 4 and ext in [".md", ".docx", ".py"]:
                            sample_files.append(rel_p)
                    except Exception:
                        pass

    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    cur = conn.cursor()
    cur.executemany("""
        INSERT OR REPLACE INTO reality_fts(file_id, file_name, source, mime_type, content, web_link)
        VALUES (?, ?, ?, ?, ?, ?)
    """, batch)
    conn.commit()
    conn.close()
    return len(batch), file_types, list(scanned_folders)[:5], sample_files

def index_desktop_files():
    ps_code = """
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    $dirs = @(
        "$env:USERPROFILE\\Desktop",
        "$env:USERPROFILE\\Documents",
        "$env:USERPROFILE\\Downloads",
        "$env:LOCALAPPDATA\\hermes\\skills",
        "$env:LOCALAPPDATA\\hermes\\memories"
    )
    $filesList = @()
    foreach ($d in $dirs) {
        if (Test-Path $d) {
            $items = Get-ChildItem -Path $d -Recurse -File -Include *.docx,*.xlsx,*.pdf,*.txt,*.md,*.py,*.json,*.csv -ErrorAction SilentlyContinue | Select-Object -First 400
            foreach ($i in $items) {
                $filesList += [PSCustomObject]@{
                    FullName = $i.FullName
                    Name = $i.Name
                    Extension = $i.Extension
                    Length = $i.Length
                    LastWriteTime = $i.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss")
                }
            }
        }
    }
    $filesList | ConvertTo-Json -Depth 3
    """
    try:
        encoded = base64.b64encode(ps_code.encode('utf-16le')).decode('ascii')
        cmd = ["ssh", "-o", "ConnectTimeout=8", DESKTOP_SSH, "powershell", "-NoProfile", "-EncodedCommand", encoded]
        res = subprocess.run(cmd, capture_output=True, text=True, errors="replace", timeout=15)
        
        if res.returncode == 0 and len(res.stdout.strip()) > 10:
            data = json.loads(res.stdout)
            batch = []
            sample_pc_files = []
            for item in data:
                fpath = item.get("FullName")
                fname = item.get("Name")
                ext = item.get("Extension", "").lower()
                content = f"Desktop File: {fname} | Path: {fpath} | LastModified: {item.get('LastWriteTime')}"
                batch.append((fpath, fname, "desktop_pc", ext, content, f"tailscale://desktop-mst5pt7/{fpath}"))
                if len(sample_pc_files) < 4 and ext in [".pdf", ".docx", ".xlsx", ".txt"]:
                    sample_pc_files.append(fname)
                    
            conn = sqlite3.connect(DB_PATH, timeout=10.0)
            cur = conn.cursor()
            cur.executemany("""
                INSERT OR REPLACE INTO reality_fts(file_id, file_name, source, mime_type, content, web_link)
                VALUES (?, ?, ?, ?, ?, ?)
            """, batch)
            conn.commit()
            conn.close()
            return len(data), sample_pc_files, None
        else:
            return 0, [], "Десктоп оффлайн или не ответил по SSH"
    except Exception as e:
        return 0, [], f"Ошибка связи с ПК: {str(e)[:60]}"

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
                batch.append((fid, fname, "google_drive", mime, fname, link))
                if len(sample_docs) < 4 and fname:
                    sample_docs.append(fname)
            
            conn = sqlite3.connect(DB_PATH, timeout=10.0)
            cur = conn.cursor()
            cur.executemany("""
                INSERT OR REPLACE INTO reality_fts(file_id, file_name, source, mime_type, content, web_link)
                VALUES (?, ?, ?, ?, ?, ?)
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
    local_count, file_types, sample_folders, sample_local_files = index_local_vps_files()
    desktop_count, sample_pc_files, desktop_err = index_desktop_files()
    gdrive_count, sample_docs, gdrive_err = index_google_workspace()
    
    duration = time.time() - start_time
    
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM reality_fts")
    total_db_records = cur.fetchone()[0]
    conn.close()

    types_breakdown = ", ".join([f"`{k}`: {v}" for k, v in sorted(file_types.items(), key=lambda x: -x[1])[:5]])
    
    report = []
    report.append("📚 **Ежедневная индексация экосистемы (VPS + Desktop PC + Google Workspace)**")
    report.append(f"⏱ *Время запуска:* `{timestamp}` (Киев) | ⚡ *Длительность:* `{duration:.2f}с`")
    report.append("—" * 28)
    report.append("")
    report.append(f"📁 **Сервер VPS (`/opt/hermes`):**")
    report.append(f"• Проиндексировано файлов знаний: **`{local_count:,}`**")
    report.append(f"• Топ форматов: {types_breakdown}")
    if sample_local_files:
        report.append("• Примеры файлов:")
        for sf in sample_local_files[:3]:
            report.append(f"  └ 📄 `{sf}`")
    report.append("")
    report.append(f"💻 **Десктоп Стефана (ПК Windows `100.79.157.46`):**")
    if desktop_err:
        report.append(f"• ⚠️ Статус: *{desktop_err}* (использован сохраненный индекс)")
    else:
        report.append(f"• Проиндексировано файлов (Рабочий стол, Документы, Загрузки): **`{desktop_count:,}`**")
        if sample_pc_files:
            report.append("• Примеры локальных файлов ПК:")
            for pf in sample_pc_files[:4]:
                report.append(f"  └ 💻 *{pf}*")
    report.append("")
    report.append(f"☁️ **Google Drive & Workspace:**")
    if gdrive_err:
        report.append(f"• ⚠️ Статус: *{gdrive_err}*")
    else:
        report.append(f"• Проиндексировано документов и таблиц: **`{gdrive_count}`**")
        if sample_docs:
            report.append("• Примеры документов:")
            for sd in sample_docs[:3]:
                report.append(f"  └ 📑 *{sd}*")
    report.append("")
    report.append(f"🔍 **Общая база полнотекстового поиска (SQLite FTS5):**")
    report.append(f"• Всего записей в индексе: **`{total_db_records:,}`**")
    report.append(f"• База: `/opt/hermes/state/full_reality_index.db`")
    report.append("")
    report.append("—" * 28)
    report.append("✨ **Итог:** Единый поисковый индекс экосистемы объединяет файлы на VPS, документы твоего ПК и облако Google Drive!")

    final_msg = "\n".join(report)
    print(final_msg)
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] [DailyIndexer]\n" + final_msg + "\n\n")

if __name__ == "__main__":
    main()
