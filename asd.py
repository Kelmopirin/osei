import requests
import json
def post_booking(config, rendelo_id, sportolo_id):
    url = config["url"]
    headers = config["headers"]
    payload = f"------WebKitFormBoundaryEq1G4XkGCDfxqw8z\r\nContent-Disposition: form-data; name=\"rendelo\"\r\n\r\n{rendelo_id}\r\n------WebKitFormBoundaryEq1G4XkGCDfxqw8z\r\nContent-Disposition: form-data; name=\"sportolo[]\"\r\n\r\n{sportolo_id}\r\n------WebKitFormBoundaryEq1G4XkGCDfxqw8z--\r\n"
    resp = requests.post(url, headers=headers, data=payload)
    return resp

# load config from JSON
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)


rendelo_id = 13
sportolo_id = 306048

# perform the POST with the explicit body
resp = post_booking(config, rendelo_id, sportolo_id)

print("status", resp.status_code)
print(resp.text)

