# Case: MS To-Do Personal MSA Device Code Block & PC PowerShell Sync

**Date:** 2026-08-30  
**Domain:** `ops_infrastructure` / `life_domains`  
**Tags:** `ms_todo`, `ms_graph`, `powershell`, `tailscale`, `personal_msa`

---

## 1. Симптом
Попытка провести прямую OAuth-авторизацию MS To-Do (MS Graph API) на сервере Servarica через Device Code Flow (`ms_todo_device_auth.py` / `login.microsoft.com/device`) завершилась ошибкой:
> `Selected user account does not exist in tenant 'Microsoft Services' and cannot access the application '6204c1d1-4712-4c46-a7d9-3ed63d992682'`

## 2. Корень проблемы (Root Cause)
Личные аккаунты Microsoft (`supremo@i.ua`, `@outlook.com`, `@hotmail.com`) блокируются авторизационным шлюзом Microsoft при попытке использовать Device Code Flow для консольных/облачных CLI приложений, если идентификатор приложения не зарегистрирован под правильный тип тенанта. Прямой вход с VPS без браузной интерактивной сессии для персональных MSA не поддерживается.

## 3. Решение (Fix)
1. Авторизация Microsoft Graph перенесена на ПК Стефана (`desktop-mst5pt7`) через интерактивный PowerShell:
   `Connect-MgGraph -Scopes "Tasks.ReadWrite"` / `Invoke-MgGraphRequest`.
2. Создан фоновый поллер `ms_todo_sync_poller.py` на ПК / VPS, который запрашивает задачи через живую Graph-сессию Windows и сохраняет нормализованный JSON-слепок (`ms_todo_snapshot.json`).
3. Слепок передается на VPS по Tailscale для использования агентами и кронами.

## 4. Урок и правило
- **Никогда** не предлагать Device Code Flow для личных аккаунтов Microsoft (MSA) на Linux VPS.
- Всегда использовать локальный фоновый скрипт/модуль PowerShell на Windows ПК с синхронизацией снимка состояния по Tailscale.
