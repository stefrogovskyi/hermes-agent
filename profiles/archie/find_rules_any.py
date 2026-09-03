from pathlib import Path

for p in Path("/opt/hermes/profiles/archie").glob("**/*"):
    if p.is_file() and p.suffix in ['.md', '.py', '.txt', '.log']:
        try:
            txt = p.read_text(errors='ignore')
            if "Rule 1" in txt and "Rule 2" in txt and "Rule 3" in txt:
                print("FOUND RULES IN:", p)
                idx = txt.find("Rule 1")
                print(txt[idx:idx+2000])
                print("="*50)
        except Exception:
            pass
