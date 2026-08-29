#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ms_todo_sync.py — Прямая двухсторонняя синхронизация Microsoft To-Do через подключённый PowerShell MS Graph
"""

import subprocess
import json
import sys

def run_ps(script):
    full_cmd = f"""ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no Stefan@100.79.157.46 powershell -NoProfile -Command "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; Connect-MgGraph -Scopes 'Tasks.ReadWrite' -ContextScope CurrentUser -NoWelcome -ErrorAction SilentlyContinue; {script}" """
    res = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
    return res.stdout.strip()

def get_lists():
    ps = "(Invoke-MgGraphRequest -Method GET -Uri 'https://graph.microsoft.com/v1.0/me/todo/lists').value | ConvertTo-Json -Depth 3"
    out = run_ps(ps)
    try:
        return json.loads(out)
    except Exception as e:
        print("Parse error:", e, out)
        return []

def get_tasks_by_list_name(list_name):
    ps = f"""
    $l = (Invoke-MgGraphRequest -Method GET -Uri 'https://graph.microsoft.com/v1.0/me/todo/lists').value | Where-Object {{ $_.displayName -eq '{list_name}' }};
    if ($l) {{
        (Invoke-MgGraphRequest -Method GET -Uri \"https://graph.microsoft.com/v1.0/me/todo/lists/$($l.id)/tasks\").value | ConvertTo-Json -Depth 3
    }} else {{
        '[]'
    }}
    """
    out = run_ps(ps)
    try:
        return json.loads(out)
    except Exception as e:
        return []

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "tasks":
        name = sys.argv[2] if len(sys.argv) > 2 else "Tasks"
        print(f"Tasks for '{name}':")
        tasks = get_tasks_by_list_name(name)
        if isinstance(tasks, dict):
            tasks = [tasks]
        for t in tasks:
            print(f"- [{t.get('status')}] {t.get('title')} (Importance: {t.get('importance')})")
    else:
        lists = get_lists()
        print(f"Total lists: {len(lists)}")
        for l in lists:
            print(f"📁 {l.get('displayName')} (ID: {l.get('id')})")
