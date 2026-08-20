# Git Autosync & GitHub Push Protection Fix

**Дата:** 2026-08-19  
**Участники:** Hermes Stevenson, Стефан  
**Категория:** ai_infra / ops_infrastructure  

## Описание
Диагностика и устранение сбоев авто-пуша в GitHub репозиторий `stefrogovskyi/hermes-agent`.

## Причина сбоя
1. GitHub Push Protection блокировал авто-пуш из-за секретов (Vercel Personal Access Tokens / API keys), сохраненных в старых коммитах рабочей директории.
2. Новые PAT-токены GitHub работали штатно, но Push Protection вешал блокировку на стороне remote.

## Решение
1. Очистка непубличных секретов и использование unblock/secret URL от GitHub для подтверждения безопасности.
2. Обновление расписания cron-задачи `Git Workspace Auto-Sync Daily` (`0302075fc0ce`) на `0 0 * * *` (ежедневно в 03:00 по Киеву / 00:00 UTC).
