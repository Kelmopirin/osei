import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://online.osei.hu/uj-idopont-foglalasa")
email, password = open("credentials.txt").readlines()
driver.find_element(By.NAME, "email").send_keys(email)
driver.find_element(By.NAME, "password").send_keys(password)
driver.find_element(By.ID, "btn-sesion").click()
time.sleep(2)

# extract the session ID after successful login
phpsessid = None
for cookie in driver.get_cookies():
    if cookie["name"] == "PHPSESSID":
        phpsessid = cookie["value"]
        break

if phpsessid:
    print(f"Session ID found: {phpsessid}")
    # update config.json with the new session ID
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    config["headers"]["Cookie"] = f"PHPSESSID={phpsessid}"
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print("config.json updated with new session ID")
else:
    print("Warning: PHPSESSID not found")

try:
    driver.find_elements(By.CLASS_NAME, "btn-secondary")[1].click()
except:
    print("No secondary button found.")
driver.get("https://online.osei.hu/uj-idopont-foglalasa")
driver.find_element(By.ID, "rendelo116476").click()
driver.find_element(By.ID, "306048").click()
time.sleep(2)
driver.quit()