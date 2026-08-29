#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fallback_monitor.py — Ежедневный аудит fallback-цепочки, пинг моделей, классификация по 3 тирам и авто-синхронизация во вкладку 'Models' в Google Таблицу.
"""

import os, sys, json, time, requests, yaml, urllib.request, urllib.parse
from datetime import datetime, timezone, timedelta
from concurrent.futures import ThreadPoolExecutor

CONFIG_PATH = "/opt/hermes/config.yaml"
AUTH_PATH = "/opt/hermes/auth.json"
SHEET_CONFIG = "/opt/hermes/ecosystem_registry_sheet.json"
GOOGLE_TOKEN_PATH = "/opt/hermes/profiles/archie/google_token.json"
GOOGLE_SECRET_PATH = "/opt/hermes/profiles/archie/google_client_secret.json"

MODELS_CATALOG = [
    # Primary & Flagship
    {"model": "gemini-3.7-flash", "provider": "google", "tier": 2},
    {"model": "gemini-2.5-pro", "provider": "google", "tier": 3},
    {"model": "gemini-2.5-flash", "provider": "google", "tier": 2},
    
    # Anthropic Claude Pro OAuth
    {"model": "claude-sonnet-4-5", "provider": "anthropic", "tier": 3},
    {"model": "claude-haiku-4-5", "provider": "anthropic", "tier": 2},
    {"model": "claude-opus-4-5", "provider": "anthropic", "tier": 3},

    # Nous Free
    {"model": "meituan/longcat-2.0:free", "provider": "nous", "tier": 1},
    {"model": "stepfun/step-3.7-flash:free", "provider": "nous", "tier": 3},
    {"model": "tencent/hy3:free", "provider": "nous", "tier": 2},
    {"model": "poolside/laguna-s-2.1:free", "provider": "nous", "tier": 2},
    {"model": "poolside/laguna-xs-2.1:free", "provider": "nous", "tier": 1},
    {"model": "upstage/solar-pro4:free", "provider": "nous", "tier": 2},

    # OpenRouter
    {"model": "deepseek/deepseek-r1:free", "provider": "openrouter", "tier": 3},
    {"model": "deepseek/deepseek-chat:free", "provider": "openrouter", "tier": 2},
    {"model": "meta-llama/llama-3.3-70b-instruct:free", "provider": "openrouter", "tier": 2},
    {"model": "qwen/qwen-2.5-72b-instruct:free", "provider": "openrouter", "tier": 2},
    {"model": "google/gemini-2.0-flash-exp:free", "provider": "openrouter", "tier": 1},

    # NVIDIA NIM
    {"model": "meta/llama-3.3-70b-instruct", "provider": "nvidia", "tier": 2},
    {"model": "deepseek-ai/deepseek-r1", "provider": "nvidia", "tier": 3},
    {"model": "nvidia/llama-3.1-nemotron-70b-instruct", "provider": "nvidia", "tier": 2},
    
    # Gonka24
    {"model": "minimax-m2.7", "provider": "gonka24", "tier": 2},
    {"model": "kimi-k2.6", "provider": "gonka24", "tier": 3}
]

def get_keys():
    keys = {}
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            cfg = yaml.safe_load(f) or {}
            keys = cfg.get("keys", {})
    return keys

def get_nous_token():
    if os.path.exists(AUTH_PATH):
        try:
            with open(AUTH_PATH, "r") as f:
                data = json.load(f)
                return data.get("providers", {}).get("nous", {}).get("access_token")
        except Exception:
            pass
    return None

def get_claude_pro_cookie():
    path = "/root/.claude/.credentials.json"
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                data = json.load(f)
                oauth = data.get("claudeAiOauth", {})
                return oauth.get("accessToken")
        except Exception:
            pass
    return None

def ping_model(entry):
    model = str(entry.get("model", ""))
    provider = str(entry.get("provider", ""))
    tier = entry.get("tier", 1)
    keys = get_keys()
    nous_tok = get_nous_token()
    claude_tok = get_claude_pro_cookie()

    t0 = time.time()
    headers = {}
    url = ""
    payload = {"model": model, "messages": [{"role": "user", "content": "ping"}], "max_tokens": 5}

    if provider == "google":
        url = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
        headers = {"Authorization": f"Bearer {keys.get('GEMINI_API_KEY')}"}
    elif provider == "openrouter":
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {"Authorization": f"Bearer {keys.get('OPENROUTER_API_KEY')}"}
    elif provider == "nous":
        url = "https://inference-api.nousresearch.com/v1/chat/completions"
        tok = nous_tok or keys.get("NOUS_API_KEY")
        headers = {"Authorization": f"Bearer {tok}"}
    elif provider == "nvidia":
        url = "https://integrate.api.nvidia.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {keys.get('NVIDIA_API_KEY')}"}
    elif provider == "anthropic":
        url = "https://api.anthropic.com/v1/messages"
        tok = keys.get("ANTHROPIC_API_KEY") or claude_tok
        headers = {
            "x-api-key": tok,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        payload = {"model": model, "messages": [{"role": "user", "content": "ping"}], "max_tokens": 5}
    elif provider == "gonka24":
        url = "https://api.gonka24.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {keys.get('GONKA24_API_KEY')}"}
    else:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {"Authorization": f"Bearer {keys.get('OPENROUTER_API_KEY')}"}

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=12)
        latency = round(time.time() - t0, 2)
        if r.status_code == 200:
            return (model, provider, tier, "LIVE (200 OK)", "Работает", latency)
        elif r.status_code == 429:
            return (model, provider, tier, "BUSY (429)", "Лимит запросов / Очередь", latency)
        elif r.status_code == 404:
            return (model, provider, tier, "DEAD (404)", "Модель не найдена / Устарела", latency)
        elif r.status_code == 401:
            return (model, provider, tier, "AUTH_ERR (401)", "Неверный токен / ключ", latency)
        else:
            return (model, provider, tier, f"ERR ({r.status_code})", r.text[:60].replace("\n", " "), latency)
    except requests.exceptions.Timeout:
        return (model, provider, tier, "TIMEOUT (>12s)", "Таймаут ответа", 12.0)
    except Exception as e:
        return (model, provider, tier, "FAIL", str(e)[:60], 0.0)

def sync_to_google_sheet(results, kyiv_timestamp):
    if not os.path.exists(GOOGLE_TOKEN_PATH) or not os.path.exists(SHEET_CONFIG):
        return False

    with open(GOOGLE_TOKEN_PATH) as f:
        token_data = json.load(f)
    with open(SHEET_CONFIG) as f:
        sheet_info = json.load(f)

    spreadsheet_id = sheet_info.get("spreadsheet_id")
    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")

    if refresh_token and os.path.exists(GOOGLE_SECRET_PATH):
        try:
            with open(GOOGLE_SECRET_PATH) as f:
                cs = json.load(f)
                client_info = cs.get("installed") or cs.get("web") or {}
                client_id = client_info.get("client_id")
                client_secret = client_info.get("client_secret")
            if client_id and client_secret:
                url = "https://oauth2.googleapis.com/token"
                data = urllib.parse.urlencode({
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "refresh_token": refresh_token,
                    "grant_type": "refresh_token"
                }).encode()
                req = urllib.request.Request(url, data=data)
                with urllib.request.urlopen(req) as resp:
                    new_token_data = json.loads(resp.read().decode())
                    access_token = new_token_data["access_token"]
                    token_data["access_token"] = access_token
                    with open(GOOGLE_TOKEN_PATH, "w") as f_out:
                        json.dump(token_data, f_out)
        except Exception:
            pass

    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

    rows = [
        [f"🕒 Последнее обновление: {kyiv_timestamp}", "", "", "", "", ""],
        ["Провайдер", "Модель", "Тир (Назначение)", "Статус", "Пинг (сек)", "Детали / Примечание"]
    ]

    tier_names = {
        3: "Tier 3 (Reasoning & Deep Arch)",
        2: "Tier 2 (Standard Workhorse)",
        1: "Tier 1 (Fast & Free / Light)"
    }

    # Sort results by Tier desc, then Status
    sorted_results = sorted(results, key=lambda x: (x[2], "LIVE" in x[3]), reverse=True)

    for model, provider, tier, status, detail, latency in sorted_results:
        t_label = tier_names.get(tier, f"Tier {tier}")
        status_clean = "✅ LIVE" if "LIVE" in status else ("⏳ BUSY (429)" if "BUSY" in status else f"⚠️ {status}")
        rows.append([
            provider.upper(),
            model,
            t_label,
            status_clean,
            f"{latency}s" if latency > 0 else "-",
            detail
        ])

    range_clear = urllib.parse.quote("Models!A1:F150")
    clear_url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{range_clear}:clear"
    try:
        req_clear = urllib.request.Request(clear_url, data=b"{}", headers=headers, method="POST")
        urllib.request.urlopen(req_clear)
    except Exception:
        pass

    range_name = f"Models!A1:F{len(rows)}"
    encoded_range = urllib.parse.quote(range_name)
    update_url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{encoded_range}?valueInputOption=RAW"
    body = {"range": range_name, "majorDimension": "ROWS", "values": rows}

    try:
        req_up = urllib.request.Request(update_url, data=json.dumps(body).encode(), headers=headers, method="PUT")
        with urllib.request.urlopen(req_up) as resp:
            return True
    except Exception as e:
        print(f"Sheet update error: {e}")
        return False

def main():
    kyiv_tz = timezone(timedelta(hours=3))
    kyiv_time = datetime.now(kyiv_tz).strftime("%Y-%m-%d %H:%M:%S Киев")

    print(f"Running Fallback Models Health-Check ({len(MODELS_CATALOG)} models)...")
    results = []
    with ThreadPoolExecutor(max_workers=10) as ex:
        futures = [ex.submit(ping_model, m) for m in MODELS_CATALOG]
        for f in futures:
            results.append(f.result())

    synced = sync_to_google_sheet(results, kyiv_time)

    report = []
    report.append(f"📊 **Ежедневный отчет Fallback-цепочки и пула моделей**")
    report.append(f"🕒 Время проверки: `{kyiv_time}`")
    report.append(f"🔢 Проверено моделей: **{len(results)}**")
    if synced:
        report.append(f"✅ Результаты синхронизированы в Google Sheet во вкладку **Models**!\n")
    else:
        report.append(f"⚠️ Синхронизация с Google Sheet пропущена/ошибка.\n")

    report.append("📋 **Текущий статус цепочки резервирования (Health-Check):**")
    for model, provider, tier, status, detail, latency in sorted(results, key=lambda x: x[2], reverse=True):
        status_emoji = "✅" if "LIVE" in status else ("⏳" if "BUSY" in status or "429" in status else "⚠️")
        report.append(f"{status_emoji} `{model}` ({provider}) — **{status}** ({latency}s) | {detail}")

    print("\n".join(report))

if __name__ == "__main__":
    main()
