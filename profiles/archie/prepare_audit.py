import json

with open("/opt/hermes/profiles/archie/writer_output.json", "r", encoding="utf-8") as f:
    writer_data = json.load(f)

with open("/opt/hermes/profiles/archie/source_clean.txt", "r", encoding="utf-8") as f:
    orig_text = f.read()

audit_input = {
    "original_source": orig_text,
    "rewrite": writer_data
}

with open("/opt/hermes/profiles/archie/audit_input.json", "w", encoding="utf-8") as f:
    json.dump(audit_input, f, ensure_ascii=False, indent=2)

print("Prepared audit_input.json")
