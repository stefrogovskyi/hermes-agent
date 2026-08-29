#!/usr/bin/env python3
"""
Fallback Chain Health-Check, Auto-Discovery & 3-Tier Dynamic Routing Monitor.
Runs daily at 03:00 Kyiv time (00:00 UTC).
"""

import os
import sys
import json
import time
import yaml
import requests
from datetime import datetime, timezone, timedelta
from concurrent.futures import ThreadPoolExecutor

HERMES_HOME = os.environ.get("HERMES_HOME", "/opt/hermes")

# Load environment keys
env_file = os.path.join(HERMES_HOME, ".env")
keys = {}
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.strip().split("=", 1)
                keys[k] = v

# Load Nous OAuth Token from auth.json
nous_token = None
auth_file = os.path.join(HERMES_HOME, "auth.json")
if os.path.exists(auth_file):
    try:
        with open(auth_file) as f:
            ad = json.load(f)
            nous_token = ad.get("providers", {}).get("nous", {}).get("access_token")
    except Exception:
        pass

def ping_model(model_entry):
    model = model_entry["model"]
    provider = model_entry["provider"]
    t0 = time.time()
    status = "UNKNOWN"
    err_msg = ""

    try:
        if provider == "openai":
            api_key = keys.get("OPENAI_API_KEY")
            if not api_key:
                return model, provider, "SKIPPED", "No OPENAI_API_KEY", 0
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            payload = {"model": model, "messages": [{"role": "user", "content": "ping"}], "max_tokens": 5}
            r = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers, timeout=10)
            latency = round(time.time() - t0, 2)
            if r.status_code == 200:
                return model, provider, "LIVE", f"{latency}s", latency
            else:
                return model, provider, f"ERR {r.status_code}", r.text[:80], latency

        elif provider == "anthropic":
            oauth_file = "/root/.claude/.credentials.json"
            oauth_token = None
            if os.path.exists(oauth_file):
                try:
                    with open(oauth_file) as f:
                        cd = json.load(f)
                        oauth_token = cd.get("claudeAiOauth", {}).get("accessToken")
                except Exception:
                    pass
            
            tok = oauth_token or keys.get("ANTHROPIC_API_KEY")
            if not tok:
                return model, provider, "SKIPPED", "No ANTHROPIC Token/Key", 0
            
            headers = {"content-type": "application/json", "anthropic-version": "2023-06-01"}
            if oauth_token:
                headers["Authorization"] = f"Bearer {tok}"
                headers["anthropic-beta"] = "oauth-2025-04-20"
            else:
                headers["x-api-key"] = tok

            payload = {"model": model, "messages": [{"role": "user", "content": "ping"}], "max_tokens": 5}
            r = requests.post("https://api.anthropic.com/v1/messages", json=payload, headers=headers, timeout=10)
            latency = round(time.time() - t0, 2)
            if r.status_code == 200:
                return model, provider, "LIVE", f"{latency}s", latency
            elif r.status_code == 429:
                return model, provider, "LIVE (Auth OK)", "Rate limit / Pro sub active", latency
            else:
                return model, provider, f"ERR {r.status_code}", r.text[:80], latency

        elif provider == "google":
            api_key = keys.get("GEMINI_API_KEY") or keys.get("GOOGLE_API_KEY")
            if not api_key:
                return model, provider, "SKIPPED", "No GOOGLE_API_KEY", 0
            m_clean = model.replace("google/", "")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{m_clean}:generateContent?key={api_key}"
            payload = {"contents": [{"parts": [{"text": "ping"}]}], "generationConfig": {"maxOutputTokens": 5}}
            r = requests.post(url, json=payload, timeout=10)
            latency = round(time.time() - t0, 2)
            if r.status_code == 200:
                return model, provider, "LIVE", f"{latency}s", latency
            else:
                return model, provider, f"ERR {r.status_code}", r.text[:80], latency

        elif provider == "huggingface":
            api_key = keys.get("HF_TOKEN")
            if not api_key:
                return model, provider, "SKIPPED", "No HF_TOKEN", 0
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            payload = {"model": model, "messages": [{"role": "user", "content": "ping"}], "max_tokens": 5}
            r = requests.post("https://router.huggingface.co/v1/chat/completions", json=payload, headers=headers, timeout=10)
            latency = round(time.time() - t0, 2)
            if r.status_code == 200:
                return model, provider, "LIVE", f"{latency}s", latency
            else:
                return model, provider, f"ERR {r.status_code}", r.text[:80], latency

        elif provider == "nous":
            tok = nous_token or keys.get("NOUS_API_KEY")
            if not tok:
                return model, provider, "SKIPPED", "No Nous Token", 0
            headers = {"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}
            payload = {"model": model, "messages": [{"role": "user", "content": "ping"}], "max_tokens": 5}
            r = requests.post("https://inference-api.nousresearch.com/v1/chat/completions", json=payload, headers=headers, timeout=10)
            latency = round(time.time() - t0, 2)
            if r.status_code == 200:
                return model, provider, "LIVE", f"{latency}s", latency
            elif r.status_code == 429:
                return model, provider, "BUSY (429)", "Rate limit / capacity", latency
            else:
                return model, provider, f"ERR {r.status_code}", r.text[:80], latency

        elif provider == "openrouter":
            api_key = keys.get("OPENROUTER_API_KEY")
            if not api_key:
                return model, provider, "SKIPPED", "No OPENROUTER_API_KEY", 0
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            payload = {"model": model, "messages": [{"role": "user", "content": "ping"}], "max_tokens": 5}
            r = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers, timeout=10)
            latency = round(time.time() - t0, 2)
            if r.status_code == 200:
                return model, provider, "LIVE", f"{latency}s", latency
            elif r.status_code == 429:
                return model, provider, "BUSY (429)", "Rate limit", latency
            else:
                return model, provider, f"ERR {r.status_code}", r.text[:80], latency

        elif provider == "gonka24":
            api_key = keys.get("GONKA24_API_KEY")
            if not api_key:
                return model, provider, "SKIPPED", "No GONKA24_API_KEY", 0
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            payload = {"model": model, "messages": [{"role": "user", "content": "ping"}], "max_tokens": 5}
            r = requests.post("https://api.gonka24.com/v1/chat/completions", json=payload, headers=headers, timeout=10)
            latency = round(time.time() - t0, 2)
            if r.status_code == 200:
                return model, provider, "LIVE", f"{latency}s", latency
            else:
                return model, provider, f"ERR {r.status_code}", r.text[:80], latency

        else:
            return model, provider, "UNSUPPORTED", "Unknown provider", 0

    except Exception as e:
        latency = round(time.time() - t0, 2)
        return model, provider, "TIMEOUT/EXC", str(e)[:60], latency

def classify_tier(model_name, provider):
    """Classifies a model entry into Tier 1, 2, or 3."""
    m = model_name.lower()
    
    # Tier 3: Heavy Reasoning & Deep Architecture
    if any(k in m for k in [
        "r1", "opus", "sonnet", "fable", "405b", "70b", "72b", "120b", "550b", "2.5-pro", "deepseek-v3", "deepseek-chat"
    ]):
        return 3
    if m == "gpt-4o":
        return 3
        
    # Tier 2: Standard Workhorse
    if any(k in m for k in [
        "3.7-flash", "3.6-flash", "coder", "small-24b", "m2.7", "k2.6", "gemma-4", "m3:free", "glm-5.2", "openrouter/free"
    ]):
        return 2
        
    # Tier 1: Light & Free Tier
    return 1

def main():
    kyiv_time = datetime.now(timezone(timedelta(hours=3))).strftime("%Y-%m-%d %H:%M:%S (Kyiv)")
    
    with open(f"{HERMES_HOME}/config.yaml") as f:
        cfg = yaml.safe_load(f)

    current_fallback = cfg.get("fallback", [])
    if not current_fallback:
        current_fallback = cfg.get("fallback_providers", [])

    # 1. Health-check current fallback models
    results = []
    with ThreadPoolExecutor(max_workers=10) as ex:
        futures = [ex.submit(ping_model, m) for m in current_fallback]
        for f in futures:
            results.append(f.result())

    # Map results
    active_fallback = []
    pruned_models = []
    table_rows = []

    for (model, provider, status, detail, latency), original_entry in zip(results, current_fallback):
        if "404" in status or "does not exist" in detail.lower() or "not found" in detail.lower():
            pruned_models.append((model, provider, detail))
        else:
            active_fallback.append(original_entry)

        status_emoji = "✅" if "LIVE" in status else ("⏳" if "429" in status or "BUSY" in status else "⚠️")
        table_rows.append(f"{status_emoji} `{model}` ({provider}) — **{status}** ({detail})")

    # 2. Discovery: Scan OpenRouter for new free models
    new_discovered = []
    try:
        r_or = requests.get("https://openrouter.ai/api/v1/models", timeout=8)
        if r_or.status_code == 200:
            existing_model_names = {m["model"] for m in active_fallback}
            for m in r_or.json().get("data", []):
                mid = m.get("id", "")
                pricing = m.get("pricing", {})
                is_free = (str(pricing.get("prompt")) == "0" and str(pricing.get("completion")) == "0") or ":free" in mid
                if is_free and mid not in existing_model_names:
                    if not any(x in mid.lower() for x in ["safety", "embed", "vl", "audio", "lyria"]):
                        res = ping_model({"model": mid, "provider": "openrouter"})
                        if "LIVE" in res[2] or "BUSY" in res[2]:
                            entry = {"model": mid, "provider": "openrouter"}
                            active_fallback.append(entry)
                            existing_model_names.add(mid)
                            new_discovered.append((mid, "openrouter"))
    except Exception as e:
        pass

    # 3. Discovery: Scan Nous Portal for new free models
    try:
        tok = nous_token or keys.get("NOUS_API_KEY")
        if tok:
            r_nous = requests.get("https://inference-api.nousresearch.com/v1/models", headers={"Authorization": f"Bearer {tok}"}, timeout=8)
            if r_nous.status_code == 200:
                existing_model_names = {m["model"] for m in active_fallback}
                for m in r_nous.json().get("data", []):
                    mid = m.get("id", "")
                    if ":free" in mid and mid not in existing_model_names:
                        res = ping_model({"model": mid, "provider": "nous"})
                        if "LIVE" in res[2] or "BUSY" in res[2]:
                            entry = {"model": mid, "provider": "nous"}
                            active_fallback.append(entry)
                            existing_model_names.add(mid)
                            new_discovered.append((mid, "nous"))
    except Exception as e:
        pass

    # 4. Group active models by 3 Dynamic Tiers
    tier1_models = []
    tier2_models = []
    tier3_models = []

    for entry in active_fallback:
        t = classify_tier(entry["model"], entry["provider"])
        if t == 3:
            tier3_models.append(entry)
        elif t == 2:
            tier2_models.append(entry)
        else:
            tier1_models.append(entry)

    # 5. Build user digest
    report = []
    report.append(f"📊 **Ежедневный отчет Fallback-цепочки и пула моделей**")
    report.append(f"🕒 Время проверки: `{kyiv_time}`")
    report.append(f"🔢 Всего активных моделей в пуле: **{len(active_fallback)}**\n")

    if new_discovered:
        report.append("✨ **Новые обнаруженные и подключенные модели:**")
        for nm, np in new_discovered:
            report.append(f"- ➕ `{nm}` ({np})")
        report.append("")

    if pruned_models:
        report.append("🗑️ **Устаревшие/удаленные модели:**")
        for pm, pp, pd in pruned_models:
            report.append(f"- ❌ `{pm}` ({pp}) — {pd}")
        report.append("")

    report.append("🧠 **Конфигурация 3 Тиров Dynamic Model Routing:**\n")
    
    report.append(f"🔴 **Tier 3: Heavy Reasoning & Deep Architecture ({len(tier3_models)} моделей)**")
    report.append("*Назначение: системная архитектура, сложный кодинг, глубокий аудит, R1 рассуждения.*")
    for m in tier3_models[:10]:
        report.append(f"  • `{m['model']}` ({m['provider']})")
    if len(tier3_models) > 10:
        report.append(f"  • *...и еще {len(tier3_models) - 10} моделей*")
    report.append("")

    report.append(f"🟡 **Tier 2: Standard Workhorse ({len(tier2_models)} моделей)**")
    report.append("*Назначение: стандартная разработка, поиск, документы, сводки (дефолт).*")
    for m in tier2_models[:10]:
        report.append(f"  • `{m['model']}` ({m['provider']})")
    if len(tier2_models) > 10:
        report.append(f"  • *...и еще {len(tier2_models) - 10} моделей*")
    report.append("")

    report.append(f"🟢 **Tier 1: Light & Free Tier ({len(tier1_models)} моделей)**")
    report.append("*Назначение: повседневный диалог, шутки, приветствия, быстрые статусы (<1s).*")
    for m in tier1_models[:10]:
        report.append(f"  • `{m['model']}` ({m['provider']})")
    if len(tier1_models) > 10:
        report.append(f"  • *...и еще {len(tier1_models) - 10} моделей*")
    report.append("")

    report.append("📋 **Текущий статус цепочки резервирования (Health-Check):**")
    report.extend(table_rows)

    print("\n".join(report))

if __name__ == "__main__":
    main()
