#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_ecosystem_sheet_registry.py — Обновляет реестр кронов и скиллов в Google Таблице с 6 колонками:
A: Агент
B: Тип (Крон/Скилл)
C: Название
D: ID / Имя файла
E: Когда работает (понятный русский язык)
F: Описание
"""

import json, os, urllib.request, urllib.parse

def human_schedule(sched):
    if isinstance(sched, dict):
        kind = sched.get('kind')
        if kind == 'interval':
            mins = sched.get('minutes', 0)
            if mins == 1:
                return "Каждую минуту"
            elif mins < 60:
                return f"Каждые {mins} мин"
            elif mins % 60 == 0:
                hours = mins // 60
                return f"Каждые {hours} ч"
            else:
                return f"Интервал: {mins} мин"
        elif kind == 'cron':
            expr = sched.get('expr') or sched.get('display') or ''
            return parse_cron_expr(expr)
        return sched.get('display') or str(sched)
    elif isinstance(sched, str):
        s = sched.strip()
        if s.startswith('every '):
            val = s.replace('every ', '')
            if val.endswith('m'):
                return f"Каждые {val[:-1]} мин"
            elif val.endswith('h'):
                return f"Каждые {val[:-1]} ч"
            elif val.endswith('d'):
                return f"Каждые {val[:-1]} дн"
            return f"Каждые {val}"
        return parse_cron_expr(s)
    return "По вызову / триггеру"

def parse_cron_expr(expr):
    parts = expr.split()
    if len(parts) == 5:
        m, h, dom, mon, dow = parts
        # Server is in UTC. Kyiv is UTC+3.
        # Let's convert hour to Kyiv time if it's a fixed hour
        try:
            if h.isdigit() and m.isdigit():
                utc_h = int(h)
                kyiv_h = (utc_h + 3) % 24
                time_str = f"{kyiv_h:02d}:{int(m):02d} Киев ({utc_h:02d}:{int(m):02d} UTC)"
                
                if dom == '*' and mon == '*' and dow == '*':
                    return f"Ежедневно в {time_str}"
                elif dow == '0' or dow == '7':
                    return f"По воскресеньям в {time_str}"
                elif dow == '1-5':
                    return f"По будням (Пн-Пт) в {time_str}"
                elif dow == '1':
                    return f"По понедельникам в {time_str}"
                elif dow == '6':
                    return f"По субботам в {time_str}"
                else:
                    return f"По расписанию `{expr}` (в {time_str})"
            elif h.startswith('*/'):
                step = h.replace('*/', '')
                return f"Каждые {step} ч (в :{m.zfill(2)})"
        except Exception:
            pass
    return f"Cron: `{expr}`"

def sync_registry():
    token_path = '/opt/hermes/profiles/archie/google_token.json'
    client_secret_path = '/opt/hermes/profiles/archie/google_client_secret.json'
    registry_file = '/opt/hermes/ecosystem_registry_sheet.json'
    
    if not os.path.exists(token_path) or not os.path.exists(registry_file):
        print("Missing config or tokens")
        return

    with open(token_path) as f:
        token_data = json.load(f)
    with open(registry_file) as f:
        sheet_info = json.load(f)
        
    spreadsheet_id = sheet_info['spreadsheet_id']
    access_token = token_data.get('access_token')

    refresh_token = token_data.get('refresh_token')
    if refresh_token and os.path.exists(client_secret_path):
        with open(client_secret_path) as f:
            cs = json.load(f)
            client_info = cs.get('installed') or cs.get('web') or {}
            client_id = client_info.get('client_id')
            client_secret = client_info.get('client_secret')
        if client_id and client_secret:
            try:
                url = "https://oauth2.googleapis.com/token"
                data = urllib.parse.urlencode({
                    'client_id': client_id,
                    'client_secret': client_secret,
                    'refresh_token': refresh_token,
                    'grant_type': 'refresh_token'
                }).encode()
                req = urllib.request.Request(url, data=data)
                with urllib.request.urlopen(req) as resp:
                    new_token_data = json.loads(resp.read().decode())
                    access_token = new_token_data['access_token']
                    token_data['access_token'] = access_token
                    with open(token_path, 'w') as f_out:
                        json.dump(token_data, f_out)
            except Exception as e:
                print("Refresh error:", e)

    agents = ['default', 'alistair', 'archie', 'ben', 'callum', 'harrison', 'liz', 'richard', 'aeon']
    headers_row = ["Агент", "Тип", "Название", "ID", "Когда работает", "Описание"]
    rows = [headers_row]

    # 1. Crons
    for a in agents:
        agent_name = "Hermes Stevenson" if a == 'default' else a.capitalize()
        cron_path = '/opt/hermes/cron/jobs.json' if a == 'default' else f'/opt/hermes/profiles/{a}/cron/jobs.json'
        if os.path.exists(cron_path):
            try:
                with open(cron_path) as f:
                    data = json.load(f)
                    jobs = []
                    if isinstance(data, dict):
                        jobs = data.get('jobs', [])
                        if not jobs:
                            jobs = list(data.values()) if all(isinstance(v, dict) for v in data.values()) else []
                    elif isinstance(data, list):
                        jobs = data
                    for j in jobs:
                        if isinstance(j, dict):
                            job_id = j.get('id') or j.get('job_id') or "-"
                            name = j.get('name') or j.get('job_id') or "Cron Job"
                            sched = j.get('schedule', '')
                            human_sched = human_schedule(sched)
                            prompt = (j.get('prompt') or '').strip().replace('\n', ' ')
                            if len(prompt) > 400:
                                prompt = prompt[:397] + "..."
                            desc = prompt if prompt else f"Скрипт: {j.get('script') or '-'}"
                            rows.append([agent_name, "Крон", name, job_id, human_sched, desc])
            except Exception as e:
                print(f"Cron err {a}: {e}")

    # 2. Skills
    for a in agents:
        agent_name = "Hermes Stevenson" if a == 'default' else a.capitalize()
        skill_dir = '/opt/hermes/skills' if a == 'default' else f'/opt/hermes/profiles/{a}/skills'
        if os.path.exists(skill_dir):
            for root, dirs, files in sorted(os.walk(skill_dir)):
                if 'SKILL.md' in files:
                    skill_path = os.path.join(root, 'SKILL.md')
                    rel = os.path.relpath(root, skill_dir)
                    skill_name = os.path.basename(root)
                    desc = ""
                    with open(skill_path, 'r', errors='ignore') as f:
                        for l in f:
                            if l.startswith('description:'):
                                desc = l.split('description:', 1)[1].strip().strip('"\'')
                                break
                            elif l.startswith('name:'):
                                raw_n = l.split('name:', 1)[1].strip().strip('"\'')
                                if raw_n:
                                    skill_name = raw_n
                    
                    rows.append([agent_name, "Скилл", skill_name, rel, "По вызову / триггеру", desc])

    # Clear old and write new
    range_clear = urllib.parse.quote("A1:F2000")
    clear_url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{range_clear}:clear"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    try:
        req_clear = urllib.request.Request(clear_url, data=b"{}", headers=headers, method="POST")
        urllib.request.urlopen(req_clear)
    except Exception as e:
        print("Clear err:", e)

    range_name = f"A1:F{len(rows)}"
    encoded_range = urllib.parse.quote(range_name)
    update_url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{encoded_range}?valueInputOption=RAW"
    body = {"range": range_name, "majorDimension": "ROWS", "values": rows}
    
    req = urllib.request.Request(update_url, data=json.dumps(body).encode(), headers=headers, method="PUT")
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode())
        print(f"Successfully synced {len(rows)} entries (6 columns) to Google Sheet!")

if __name__ == '__main__':
    sync_registry()
