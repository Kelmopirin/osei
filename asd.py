import requests

# load credentials
email = open("credentials.txt").read().splitlines()[0].strip()

# target endpoint copied from your HTTP headers list
url = "https://online.osei.hu/pages/idopontfoglalas/szabad_idopontok_keresese.php"

# headers that the browser sends; requests will populate some automatically (Content-Type, Content-Length)
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "hu-HU,hu;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6",
    "Connection": "keep-alive",
    # "Content-Type" is set by requests when using files or data
    # "Content-Length" also handled automatically
    "Origin": "https://online.osei.hu",
    "Referer": "https://online.osei.hu/uj-idopont-foglalasa",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    # if you need to send a session cookie replace the value below
    "Cookie": "PHPSESSID=c5aqp41bj70mlkkpq4qe3tma4a",
}

# if you already have the raw body (including boundaries), assign it here
# below is the payload corresponding to the form-data you sent:
#
# rendelo=17
# sportolo[]=306048
#
# make sure the boundary value matches the one in Content-Type header
payload = (
    "------WebKitFormBoundaryEq1G4XkGCDfxqw8z\r\n"
    "Content-Disposition: form-data; name=\"rendelo\"\r\n\r\n"
    "13\r\n"
    "------WebKitFormBoundaryEq1G4XkGCDfxqw8z\r\n"
    "Content-Disposition: form-data; name=\"sportolo[]\"\r\n\r\n"
    "306048\r\n"
    "------WebKitFormBoundaryEq1G4XkGCDfxqw8z--\r\n"
)


# if you need to override content-type to include the exact boundary do it now
# (requests will omit this if you're sending a raw bytes payload)
headers["Content-Type"] = "multipart/form-data; boundary=----WebKitFormBoundaryEq1G4XkGCDfxqw8z"

# perform the POST with the explicit body
resp = requests.post(url, headers=headers, data=payload)

print("status", resp.status_code)
print(resp.text)
