import re

with open('searates_final_v3.md', encoding='utf-8') as f:
    content = f.read()

title = re.search(r'# TITLE\n(.+)', content).group(1).strip()
meta_title = re.search(r'# META-TITLE\n(.+)', content).group(1).strip()
meta_desc = re.search(r'# META-DESCRIPTION\n(.+)', content).group(1).strip()
body = content.split('# BODY')[1].strip()

print("TITLE:", title, "| len:", len(title))
print("META-TITLE:", meta_title, "| len:", len(meta_title))
print("META-DESC:", meta_desc, "| len:", len(meta_desc))
print()

full_text = title + " " + meta_title + " " + meta_desc + " " + body
print("Em-dash count:", full_text.count('—'))
print("Double-hyphen count:", full_text.count('--'))
print("rather than count:", len(re.findall(r'\brather than\b', full_text, re.I)))
print("instead of count:", len(re.findall(r'\binstead of\b', full_text, re.I)))

# AI clichés
cliches = ["it's important to note", "delve into", "seamless", "unlock", "robust",
           "leverage", "landscape", "in conclusion", "plays a vital role", "underscor",
           "ever-evolving", "unprecedented", "cutting-edge", "harness the power", "ecosystem",
           "synergy", "paradigm", "utilize", "facilitate", "streamline", "holistic",
           "in today's world", "vital role", "pivotal role", "thereby ensuring"]
for c in cliches:
    if c.lower() in full_text.lower():
        print("CLICHE FOUND:", c)

print("Word count body:", len(body.split()))
