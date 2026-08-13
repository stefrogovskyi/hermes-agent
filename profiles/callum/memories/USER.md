# CALLUM VANCE INFRASTRUCTURE & CREDENTIALS
- GitHub Token: ACTIVE (stefrogovskyi)
- Hostinger SSH/SFTP: ACTIVE (u473746908 @ 82.29.199.155:65002)
- Callum Kanban: LIVE at https://callum-kanban.vercel.app/
- Tailscale IP: 100.99.146.42
- Vercel CLI: ACTIVE & DEPLOYED
§
KPI design preference: Prefers a 2-phase model for AI developers (Phase 1 = 1-month baseline observation of velocity with Claude Code/Dev servers, Phase 2 = setting measured SLAs).
§
Navo Agents group (-5305384342) behavior: Respond ONLY when explicitly tagged via @. Include explicit @ mention when addressing another bot (@qubicpmbot, @richnavobot) ONLY if an answer/action is needed; do NOT tag them otherwise.
§
ФАЙЛЫ (Google Drive & ПК): При запросе любых файлов с Google Диска — выкачивать их напрямую через Google Drive API. При запросе файлов с ПК (Anetta12/DESKTOP) — выкачивать по Tailscale, если ПК включен, и отправлять файлом в Telegram.
§
ALL modal windows in apps/dashboards MUST support closing via Escape key (e.key === 'Escape' keydown listener).
§
ИЗОЛЯЦИЯ ПРОФИЛЕЙ (Cross-Profile Isolation Directive):
Тебе СТРОГО ЗАПРЕЩЕНО вносить изменения, редактировать файлы, память, скиллы или Канбан-доски ДРУГИХ агентов. Каждый агент (Alistair, Richard, Callum, Liz, Ben) имеет право менять файлы и Канбан ИСКЛЮЧИТЕЛЬНО своего собственного профиля. Только главный Гермес (Orchestrator) обладает правом межпрофильного управления.

§
ПРАВИЛА ГРУППОВЫХ ЧАТОВ (Group Chat Triggers):
Все агенты (Hermes, Richard, Callum, Alistair, Liz, Ben) отвечают ЛЮБОМУ участнику группы (не только Стефану или Алексею) в трех случаях:
1. Прямой @тег бота (@richnavobot, @callumvancebot и т.д.).
2. Обращение по имени текстом ("Ричард", "Каллум", "Алистер" и т.д.).
3. Прямой Reply (ответ) на сообщение бота от ЛЮБОГО участника группы.
Защита от зацикливания бот-боту (is_bot: true) сохраняется.
