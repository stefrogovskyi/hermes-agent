with open("/opt/hermes/profiles/archie/cache/delegation/live/deleg_28d5b3bd/task-0.log") as f:
    text = f.read()

idx = text.find("STRICT RULES TO FOLLOW:")
rules_text = text[idx:idx+2500]
for sentence in rules_text.split("Rule "):
    print("Rule " + sentence)
