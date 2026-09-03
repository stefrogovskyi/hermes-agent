with open('/opt/hermes/profiles/archie/cache/terminal-output/out-1788160440-3216452-28a0.log') as f:
    text = f.read()

pos = text.find("MANDATORY RULES:")
while pos != -1:
    block = text[pos:pos+1800]
    if "11." in block or "10." in block or "RULE 11" in block:
        print("FOUND FULL BLOCK:\n", block)
        break
    pos = text.find("MANDATORY RULES:", pos+1)
