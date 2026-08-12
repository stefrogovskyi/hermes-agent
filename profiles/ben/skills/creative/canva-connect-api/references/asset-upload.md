# Canva Asset Uploads API Reference & Python Code

## Endpoint: Create Asset Upload Job
`POST https://api.canva.com/rest/v1/asset-uploads`

### Headers:
- `Authorization: Bearer <access_token>`
- `Content-Type: application/octet-stream`
- `Asset-Upload-Metadata: {"name_base64": "<base64_encoded_asset_title>"}`

### Body:
Binary file stream (`open(path, 'rb')`).

### Polling Status Endpoint:
`GET https://api.canva.com/rest/v1/asset-uploads/{job_id}`
Headers: `Authorization: Bearer <access_token>`

When `job.status` is `"success"`, `job.asset.id` contains the Canva Asset ID.

### Python Code Example:
```python
import base64
import json
import time
import requests

def upload_image_asset(access_token, file_path, title):
    name_b64 = base64.b64encode(title.encode('utf-8')).decode('utf-8')
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/octet-stream",
        "Asset-Upload-Metadata": json.dumps({"name_base64": name_b64})
    }
    
    with open(file_path, "rb") as f:
        res = requests.post("https://api.canva.com/rest/v1/asset-uploads", headers=headers, data=f)
    res.raise_for_status()
    
    job_id = res.json()["job"]["id"]
    status_url = f"https://api.canva.com/rest/v1/asset-uploads/{job_id}"
    
    for _ in range(10):
        time.sleep(1)
        st_res = requests.get(status_url, headers={"Authorization": f"Bearer {access_token}"})
        if st_res.status_code == 200:
            st_json = st_res.json()
            if st_json["job"]["status"] == "success":
                return st_json["job"]["asset"]
            elif st_json["job"]["status"] == "failed":
                raise Exception(f"Asset upload job failed: {st_json}")
    raise TimeoutError("Asset upload job timed out")
```
