with open('cache/delegation/live/deleg_d3ba7327/task-0.log') as f:
    text = f.read()

pos = text.find("def detailed_audit")
if pos != -1:
    print(text[pos:pos+3500])
