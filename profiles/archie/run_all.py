import json

with open("/opt/hermes/profiles/archie/make_json.py") as f:
    code = f.read()

exec(code)

with open("/opt/hermes/profiles/archie/check.py") as f:
    check_code = f.read()

exec(check_code)
