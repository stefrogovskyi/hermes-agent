import subprocess
import json

SCRIPT_PATH = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"
FILE_PATH = "/opt/hermes/profiles/archie/German_Truck_Towing_Guide.docx"
FOLDER_ID = "14SwSwwYvop7GLM6R0eDTG5ZLlUTLZr-Z"
MIME_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

cmd = [
    "python3", SCRIPT_PATH, "drive", "upload",
    "--parent", FOLDER_ID,
    "--mime-type", MIME_TYPE,
    FILE_PATH
]

res = subprocess.run(cmd, capture_output=True, text=True)
print("Upload stdout:", res.stdout)
if res.stderr:
    print("Upload stderr:", res.stderr)

try:
    upload_data = json.loads(res.stdout)
    with open("/opt/hermes/profiles/archie/upload_result.json", "w", encoding="utf-8") as f:
        json.dump(upload_data, f, ensure_ascii=False, indent=2)
    print("Saved upload_result.json")
except Exception as e:
    print("JSON decode error:", e)
