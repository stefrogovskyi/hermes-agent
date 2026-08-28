#!/usr/bin/env python3
"""
Fallback Chain Health-Check & Free Model Discovery Daemon.
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
            api_key = keys.get("ANTHROPIC_API_KEY")
            if not api_key:
                return model, provider, "SKIPPED", "No ANTHROPIC_API_KEY", 0
            headers = {"x-api-key": api_key, "anthropic-version": "2023-06-01", "Content-Type": "application/json"}
            payload = {"model": model, "messages": [{"role": "user", "content": "ping"}], "max_tokens": 5}
            r = requests.post("https://api.anthropic.com/v1/messages", json=payload, headers=headers, timeout=10)
            latency = round(time.time() - t0, 2)
            if r.status_code == 200:
                return model, provider, "LIVE", f"{latency}s", latency
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

        status_emoji = "✅" if status == "LIVE" else ("⏳" if "429" in status or "BUSY" in status else "⚠️")
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
                        if res[2] in ["LIVE", "BUSY (429)"]:
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
                        if res[2] in ["LIVE", "BUSY (429)"]:
                            entry = {"model": mid, "provider": "nous"}
                            active_fallback.append(entry)
                            existing_model_names.add(mid)
                            new_discovered.append((mid, "nous"))
    except Exception as e:
        pass

    # 4. Save updated configs if changes occurred
    if pruned_models or new_discovered:
        profiles = ["default", "ben", "callum", "liz", "harrison", "aeon", "richard", "alistair", "archie"]
        for p in profiles:
            p_path = f"{HERMES_HOME}/config.yaml" if p == "default" else f"{HERMES_HOME}/profiles/{p}/config.yaml"
            if os.path.exists(p_path):
                with open(p_path) as pf:
                    pcfg = yaml.safe_load(pf)
                pcfg["fallback"] = active_fallback
                pcfg["fallback_providers"] = active_fallback
                with open(p_path, "w") as pf:
                    yaml.dump(pcfg, pf, allow_unicode=True, sort_keys=False)

    # 5. Build user digest
    report = []
    report.append(f"📊 **Ежедневный отчет Fallback-цепочки и пула моделей**")
    report.append(f"🕒 Время проверки: `{kyiv_time}`")
    report.append(f"🔢 Всего активных моделей в цепочке: **{len(active_fallback)}**\n")

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

    report.append("📋 **Текущий статус цепочки резервирования:**")
    report.extend(table_rows)

    print("\n".join(report))

if __name__ == "__main__":
    main()
