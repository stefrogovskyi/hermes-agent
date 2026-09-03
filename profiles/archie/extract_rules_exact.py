with open("/opt/hermes/profiles/archie/cache/delegation/live/deleg_28d5b3bd/task-0.log") as f:
    lines = f.readlines()
    for l in lines:
        if "STRICT RULES TO FOLLOW:" in l:
            idx = l.find("STRICT RULES TO FOLLOW:")
            print(l[idx:])
            break
