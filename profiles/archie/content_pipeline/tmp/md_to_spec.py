import json, re, sys

src = sys.argv[1]
out = sys.argv[2]

with open(src, encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')

def parse_inline(line):
    """Convert a line with **bold** and [text](url) into a list of runs."""
    runs = []
    # tokenize by combined regex for bold and links
    pattern = re.compile(r'(\*\*(.+?)\*\*)|(\[([^\]]+)\]\(([^)]+)\))')
    pos = 0
    for m in pattern.finditer(line):
        if m.start() > pos:
            runs.append({"text": line[pos:m.start()]})
        if m.group(1):  # bold
            runs.append({"text": m.group(2), "bold": True})
        elif m.group(3):  # link
            anchor = m.group(4)
            url = m.group(5)
            runs.append({"text": anchor, "bold": True})
            runs.append({"text": f" ({url})"})
        pos = m.end()
    if pos < len(line):
        runs.append({"text": line[pos:]})
    if not runs:
        runs = [{"text": line}]
    return runs

blocks = []
i = 0
n = len(lines)
while i < n:
    line = lines[i].rstrip()
    if not line.strip():
        i += 1
        continue
    if line.startswith('### '):
        blocks.append({"type": "heading", "text": line[4:].strip(), "level": 3})
    elif line.startswith('## '):
        blocks.append({"type": "heading", "text": line[3:].strip(), "level": 2})
    elif line.startswith('# '):
        blocks.append({"type": "heading", "text": line[2:].strip(), "level": 1})
    else:
        runs = parse_inline(line)
        blocks.append({"type": "paragraph", "runs": runs})
    i += 1

spec = {
    "page": {"width_mm": 210, "height_mm": 297, "margins_mm": {"top": 25, "bottom": 25, "left": 20, "right": 20}},
    "styles": [
        {"name": "H1Style", "base": "Heading 1", "font": "Calibri", "size_pt": 20, "bold": True, "color": "1F4E79"},
        {"name": "H2Style", "base": "Heading 2", "font": "Calibri", "size_pt": 15, "bold": True, "color": "1F4E79"}
    ],
    "blocks": blocks
}

with open(out, 'w', encoding='utf-8') as f:
    json.dump(spec, f, ensure_ascii=False, indent=2)

print(json.dumps({"ok": True, "blocks": len(blocks)}))
