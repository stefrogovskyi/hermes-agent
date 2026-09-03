import json, re

with open('/opt/hermes/profiles/archie/cache/terminal-output/out-1788160440-3216452-28a0.log', 'r') as f:
    text = f.read()

pos = text.find("Rule 1")
if pos != -1:
    print(text[pos:pos+4000])
else:
    print("Rule 1 not found in log")
