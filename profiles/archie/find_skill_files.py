import glob, json, os

def search_text():
    for root, dirs, files in os.walk('/opt/hermes'):
        for f in files:
            if f.endswith('.py') or f.endswith('.json') or f.endswith('.md') or f.endswith('.log'):
                path = os.path.join(root, f)
                try:
                    text = open(path, encoding='utf-8', errors='ignore').read()
                    if '1. Запрет em-dash' in text or 'Rule 1: No em-dash' in text or '8-ШАГОВОМУ' in text or '8-step process' in text:
                        print("MATCH:", path)
                except Exception:
                    pass

search_text()
