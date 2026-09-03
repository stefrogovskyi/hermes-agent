import re

with open("audit.py", "r") as f:
    content = f.read()

orig_match = re.search(r'orig = """(.*?)"""', content, re.DOTALL)
rewrite_match = re.search(r'rewrite = """(.*?)"""', content, re.DOTALL)

if orig_match and rewrite_match:
    orig = orig_match.group(1)
    rewrite = rewrite_match.group(1)

    orig_words = re.findall(r'\b\w+\b', orig)
    rewrite_words = re.findall(r'\b\w+\b', rewrite)

    print(f"Original word count: {len(orig_words)}")
    print(f"Rewrite word count: {len(rewrite_words)}")
