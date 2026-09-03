import re
from pathlib import Path

for p in Path("/opt/hermes/profiles/archie").rglob("*"):
    if p.is_file() and p.suffix in ['.txt', '.md', '.json', '.log']:
        try:
            content = p.read_text(encoding="utf-8", errors="ignore")
            if "11. " in content or "11) " in content:
                for line in content.splitlines():
                    if "11." in line or "11)" in line:
                        print(f"File {p}: {line}")
        except Exception:
            pass
