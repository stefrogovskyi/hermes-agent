import os, sys
sys.path.insert(0, r"C:\Users\Stefan\AppData\Local\hermes\hermes-agent")
os.environ.setdefault("HERMES_HOME", r"C:\Users\Stefan\AppData\Local\hermes")

from run_agent import AIAgent
from hermes_cli.runtime_provider import resolve_runtime_provider

transcript = open(r"C:\Users\Stefan\AppData\Local\hermes\scripts\transcribe_tmp\full_transcript.txt",
                  encoding="utf-8").read()

PROMPT = (
    "Вот стенография проповеди (транскрипция):\n\n" + transcript[:60000] + "\n\n"
    "Напиши размышления по проповеди от первого лица (я, мы), в свободном человеческом "
    "разговорном стиле, на 500 слов, используй оригинальные места Писания и приведи ссылки "
    "на Библейские стихи. Не используй длинное тире. Умышленно допускай некоторые "
    "пунктуационные и фразеологические ошибки неточности"
)

rt = resolve_runtime_provider(requested="nous")
agent = AIAgent(
    model="tencent/hy3:free",
    api_key=rt.get("api_key"), base_url=rt.get("base_url"),
    provider="nous", requested_provider="nous",
    enabled_toolsets=["file", "memory"], quiet_mode=True, platform="telegram",
    session_id="reflection_task",
    ephemeral_system_prompt=(
        "Ты пишешь искренние размышления от первого лица по христианской проповеди. "
        "Стиль живой, разговорный. Допускай лёгкие пунктуационные и речевые шероховатости. "
        "Обязательно давай ссылки на стихи Библии."),
    skip_memory=True,
)
res = agent.run_conversation(PROMPT)
text = (res.get("final_response") or "").strip()
out = r"C:\Users\Stefan\AppData\Local\hermes\scripts\transcribe_tmp\reflection.txt"
with open(out, "w", encoding="utf-8") as f:
    f.write(text)
print("REFLECTION", len(text), "chars ->", out)
