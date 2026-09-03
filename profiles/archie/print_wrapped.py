import textwrap

with open("/opt/hermes/profiles/archie/cache/delegation/live/deleg_28d5b3bd/task-0.log") as f:
    text = f.read()

idx = text.find("STRICT RULES TO FOLLOW:")
rules_text = text[idx:idx+2500]
first_line = rules_text.splitlines()[0]

wrapped = textwrap.wrap(first_line, width=70)
for w in wrapped:
    print(w)
