#!/usr/bin/env python3
"""
add_case.py — добавить новый кейс в долгосрочную память (memory_v2).
Создаёт файл в cases/ с шаблоном, обновляет index.md (таблицу).

Использование:
  python add_case.py "2026-07-28_my_case" "Краткое описание" "Ключевой урок"
"""
import sys, os, datetime, glob

MEMORY_V2 = os.path.dirname(os.path.abspath(__file__))
CASES = os.path.join(MEMORY_V2, "cases")
INDEX = os.path.join(MEMORY_V2, "index.md")

TEMPLATE = """# Case: {slug}

## Симптом
<!-- что наблюдали -->

## Гипотеза / что пошло не так
<!-- если был ложный путь — опиши -->

## Корень (ФАКТ, проверенный)
<!-- доказательство: вызов/лог/ответ -->

## Фикс (применён и проверен)
<!-- что сделано -->

## Рефлексия (зарегистрированный опыт)
<!-- жёсткие правила/выводы -->

## Где искать при повторе
<!-- пути к файлам, функциям -->
"""

def update_index(slug, desc, lesson):
    date = datetime.date.today().isoformat()
    row = f"| {date} | {desc} | cases/{slug}.md | {lesson} |"
    lines = open(INDEX, encoding="utf-8").read().splitlines()
    # найти таблицу cases (после "## Cases")
    out = []
    inserted = False
    for ln in lines:
        out.append(ln)
        if ln.strip().startswith("| Дата") and not inserted:
            out.append(row)
            inserted = True
    open(INDEX, "w", encoding="utf-8").write("\n".join(out) + "\n")

def main():
    if len(sys.argv) < 4:
        print('Usage: python add_case.py <slug> "<desc>" "<lesson>"')
        return
    slug, desc, lesson = sys.argv[1], sys.argv[2], sys.argv[3]
    path = os.path.join(CASES, slug + ".md")
    if os.path.exists(path):
        print(f"[add_case] уже существует: {path}")
        return
    open(path, "w", encoding="utf-8").write(TEMPLATE.format(slug=slug))
    update_index(slug, desc, lesson)
    print(f"[add_case] создан {path}, index обновлён")

if __name__ == "__main__":
    main()
